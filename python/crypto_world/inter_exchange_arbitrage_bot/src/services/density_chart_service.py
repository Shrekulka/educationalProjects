# inter_exchange_arbitrage_bot/src/services/density_chart_service.py

import math
import sys
import time
import warnings
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Optional

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from src.bot.logic.report_maps import DENSITY_ACTION_MAP
from src.constants.trading_constants import DENSITY_CHART_CONFIG
from src.models.screener_models import Density
from src.strategies.enums import DensityAction
from src.utils.logger import logger


class DensityChartService:
    """
    ✅ ВЕРСИЯ 10.0: Создание блочной структуры для каждой биржи.
    Каждая биржа получает свой отдельный блок с топ-2 поддержками и сопротивлениями.
    """

    def __init__(self):
        self.config = DENSITY_CHART_CONFIG
        Path(self.config['TEMP_DIR']).mkdir(exist_ok=True)
        plt.switch_backend('Agg')

        # Добавляем поддержку Emoji в зависимости от ОС
        try:
            if sys.platform == "darwin":  # macOS
                font_name = "Apple Color Emoji"
            elif sys.platform == "win32":  # Windows
                font_name = "Segoe UI Emoji"
            else:  # Linux
                font_name = "Noto Color Emoji"

            # Добавляем шрифт в начало списка sans-serif
            # Matplotlib будет сначала искать глифы в этом шрифте
            plt.rcParams['font.sans-serif'].insert(0, font_name)
            logger.info(f"Поддержка эмодзи для Matplotlib включена (шрифт: {font_name}).")
        except Exception as e:
            logger.warning(f"Не удалось настроить шрифт для эмодзи в Matplotlib: {e}")

    def get_stats(self, densities: List[Density]) -> Dict:
        if not densities:
            return {"action": DensityAction.NEUTRAL}

        supports = [d for d in densities if d.density_type == 'support']
        resistances = [d for d in densities if d.density_type == 'resistance']
        support_volume = sum(d.volume_usd for d in supports)
        resistance_volume = sum(d.volume_usd for d in resistances)

        action = DensityAction.WAIT_AND_WATCH  # По умолчанию - баланс
        dominance_factor = self.config.get('DOMINANCE_FACTOR', 1.7)

        if support_volume > resistance_volume * dominance_factor:
            action = DensityAction.CONSIDER_LONG
        elif resistance_volume > support_volume * dominance_factor:
            action = DensityAction.CONSIDER_SHORT

        return {
            "total_volume_k": (support_volume + resistance_volume) / 1000,
            "exchanges_count": len(set(d.exchange for d in densities)),
            "support_k": support_volume / 1000,
            "support_count": len(supports),
            "resistance_k": resistance_volume / 1000,
            "resistance_count": len(resistances),
            "action": action
        }

    def _draw_rounded_box(self, ax: Axes, bbox, facecolor, edgecolor, linewidth=1.5):
        p = patches.FancyBboxPatch(
            (bbox[0], bbox[1]), bbox[2], bbox[3],
            boxstyle="round,pad=0.02,rounding_size=0.03",
            facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth,
            transform=ax.transAxes
        )
        ax.add_patch(p)

    def _format_price(self, price: float) -> str:
        return f"${price:,.4f}" if price < 1.0 else f"${price:,.2f}"

    def _group_densities_by_exchange(self, densities: List[Density]) -> Dict[str, Dict[str, List[Density]]]:
        """Группирует плотности по биржам и типам."""
        grouped = defaultdict(lambda: {'support': [], 'resistance': []})

        for density in densities:
            grouped[density.exchange][density.density_type].append(density)

        # Сортируем по объему (убывание) для каждого типа
        for exchange in grouped:
            grouped[exchange]['support'].sort(key=lambda x: x.volume_usd, reverse=True)
            grouped[exchange]['resistance'].sort(key=lambda x: x.volume_usd, reverse=True)

        return dict(grouped)

    def _calculate_grid_layout(self, exchanges_count: int) -> tuple:
        """Вычисляет оптимальную сетку для размещения блоков бирж."""
        if exchanges_count == 1:
            return 1, 1
        elif exchanges_count == 2:
            return 1, 2
        elif exchanges_count <= 4:
            return 2, 2
        elif exchanges_count <= 6:
            return 2, 3
        elif exchanges_count <= 9:
            return 3, 3
        else:
            # Для большого количества бирж
            cols = math.ceil(math.sqrt(exchanges_count))
            rows = math.ceil(exchanges_count / cols)
            return rows, cols

    def create_multi_block_image(self, symbol: str, densities: List[Density], mid_price: float) -> Optional[str]:
        """
        ✅ НОВЫЙ МЕТОД: Создает изображение с блочной структурой для каждой биржи.
        """
        if not densities:
            return None

        exchanges_data = self._group_densities_by_exchange(densities)
        exchanges_list = list(exchanges_data.keys())
        exchanges_count = len(exchanges_list)

        if exchanges_count == 0:
            return None

        rows, cols = self._calculate_grid_layout(exchanges_count)
        fig_width = max(12, cols * 6)
        fig_height = max(8, rows * 5)

        fig: Figure = plt.figure(figsize=(fig_width, fig_height), dpi=150)
        fig.patch.set_facecolor('#24282f')

        fig.suptitle(f"Анализ плотностей для {symbol}",
                     color='#f0c142', fontsize=20, weight='bold', y=0.95)

        for i, exchange in enumerate(exchanges_list):
            ax: Axes = plt.subplot(rows, cols, i + 1)
            ax.set_facecolor('#1a1a1a')
            ax.axis('off')
            self._draw_exchange_block(ax, exchange, exchanges_data[exchange], mid_price)

        stats = self.get_stats(densities)
        self._add_overall_stats(fig, stats)

        file_path = Path(self.config['TEMP_DIR']) / f"blocks_{symbol.replace('/', '_')}_{int(time.time())}.png"

        try:
            plt.tight_layout()
            plt.subplots_adjust(top=0.9, bottom=0.15)
            # Подавляем только специфичное предупреждение о глифах во время сохранения
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="Glyph .* missing from font",
                    category=UserWarning,
                    module="matplotlib"
                )
                plt.savefig(file_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
            return str(file_path)
        except Exception as e:
            logger.error(f"Не удалось сохранить блочное изображение для {symbol}: {e}")
            return None
        finally:
            plt.close(fig)

    def _draw_exchange_block(self, ax: Axes, exchange: str, exchange_data: Dict[str, List[Density]],
                             mid_price: float):
        """Рисует блок для одной биржи с топ-2 поддержками и сопротивлениями."""
        supports = exchange_data['support'][:2]
        resistances = exchange_data['resistance'][:2]
        total_volume = sum(d.volume_usd for d in supports + resistances)

        ax.text(0.5, 0.92, f"{exchange.upper()}",
                color='#67e484', fontsize=14, ha='center', weight='bold',
                transform=ax.transAxes)
        ax.text(0.5, 0.85, f"Объем: ${total_volume / 1000:,.0f}k",
                color='#B0BEC5', fontsize=10, ha='center',
                transform=ax.transAxes)

        self._draw_rounded_box(ax, [0.05, 0.05, 0.9, 0.9],
                               facecolor='none', edgecolor='#4f4f4f', linewidth=2)

        y_pos = 0.72
        if resistances:
            ax.text(0.5, y_pos, "СОПРОТИВЛЕНИЯ",
                    color='#FF4466', fontsize=11, ha='center', weight='bold',
                    transform=ax.transAxes)
            y_pos -= 0.08
            for resistance in resistances:
                price_text = self._format_price(resistance.price)
                volume_text = f"${resistance.volume_usd / 1000:,.0f}k"
                self._draw_rounded_box(ax, [0.1, y_pos - 0.03, 0.8, 0.06],
                                       facecolor='#e6536d', edgecolor='white', linewidth=1)
                ax.text(0.5, y_pos, f"{price_text} | {volume_text}",
                        color='white', fontsize=10, ha='center', va='center',
                        weight='bold', transform=ax.transAxes)
                y_pos -= 0.1

        ax.text(0.5, y_pos, f"— {self._format_price(mid_price)} —",
                color='#f0c142', fontsize=12, ha='center', va='center',
                weight='bold', transform=ax.transAxes)
        y_pos -= 0.08

        if supports:
            ax.text(0.5, y_pos, "ПОДДЕРЖКИ",
                    color='#00FF88', fontsize=11, ha='center', weight='bold',
                    transform=ax.transAxes)
            y_pos -= 0.08
            for support in supports:
                price_text = self._format_price(support.price)
                volume_text = f"${support.volume_usd / 1000:,.0f}k"
                self._draw_rounded_box(ax, [0.1, y_pos - 0.03, 0.8, 0.06],
                                       facecolor='#2fba77', edgecolor='white', linewidth=1)
                ax.text(0.5, y_pos, f"{price_text} | {volume_text}",
                        color='white', fontsize=10, ha='center', va='center',
                        weight='bold', transform=ax.transAxes)
                y_pos -= 0.1

    def _add_overall_stats(self, fig: Figure, stats: Dict):
        """Добавляет общую статистику внизу изображения."""
        if not stats or 'action' not in stats:
            return

        action_info = DENSITY_ACTION_MAP.get(stats['action'], DENSITY_ACTION_MAP[DensityAction.NEUTRAL])
        recommendation_text = f"{action_info['emoji']} РЕКОМЕНДАЦИЯ: {action_info['text'].upper()}"

        stats_text = (f"Объем: ${stats.get('total_volume_k', 0):,.0f}k | "
                      f"Поддержка: ${stats.get('support_k', 0):,.0f}k ({stats.get('support_count', 0)} ур.) | "
                      f"Сопротивление: ${stats.get('resistance_k', 0):,.0f}k ({stats.get('resistance_count', 0)} ур.)")

        fig.text(0.5, 0.08, stats_text, color='white', fontsize=10, ha='center', va='center')
        fig.text(0.5, 0.04, recommendation_text, color='white', fontsize=12, ha='center', va='center', weight='bold')

    def create_final_image(self, symbol: str, densities: List[Density], mid_price: float) -> Optional[str]:
        """
        ✅ ОБНОВЛЕНО: Теперь использует новый блочный метод и имеет корректный type hint.
        """
        return self.create_multi_block_image(symbol, densities, mid_price)

# # inter_exchange_arbitrage_bot/src/services/density_chart_service.py
#
# import time
# from pathlib import Path
# from typing import List, Dict
# import textwrap
#
# import matplotlib.pyplot as plt
# import pandas as pd
# from src.constants.trading_constants import DENSITY_CHART_CONFIG
# from src.models.screener_models import Density
# from src.utils.logger import logger
# from collections import defaultdict
# import matplotlib.patches as patches
#
#
# class DensityChartService:
#     """
#     ✅ ФИНАЛЬНАЯ ВЕРСИЯ: Генерирует единое изображение-макет,
#     которое включает все блоки (уровни, статистика, разбивка по биржам).
#     """
#
#     def __init__(self):
#         self.config = DENSITY_CHART_CONFIG
#         Path(self.config['TEMP_DIR']).mkdir(exist_ok=True)
#         plt.switch_backend('Agg')
#
#     def _get_stats(self, densities: List[Density]) -> Dict:
#         """Собирает статистику по плотностям."""
#         if not densities: return {}
#         supports = [d for d in densities if d.density_type == 'support']
#         resistances = [d for d in densities if d.density_type == 'resistance']
#         total_volume = sum(d.volume_usd for d in densities)
#         balance = "Умеренная поддержка"
#         if sum(d.volume_usd for d in supports) > sum(
#             d.volume_usd for d in resistances) * 1.7: balance = "Сильная поддержка"
#         if sum(d.volume_usd for d in resistances) > sum(
#             d.volume_usd for d in supports) * 1.7: balance = "Сильное сопротивление"
#         return {
#             "total_volume_k": total_volume / 1000,
#             "exchanges_count": len(set(d.exchange for d in densities)),
#             "support_k": sum(d.volume_usd for d in supports) / 1000,
#             "support_count": len(supports),
#             "resistance_k": sum(d.volume_usd for d in resistances) / 1000,
#             "resistance_count": len(resistances),
#             "balance": balance
#         }
#
#     def _draw_rounded_box(self, ax, bbox, facecolor, edgecolor, alpha=1.0):
#         """Рисует прямоугольник со скругленными углами."""
#         p = patches.FancyBboxPatch((bbox[0], bbox[1]), bbox[2], bbox[3],
#                                    boxstyle=f"round,pad=0.02,rounding_size=0.03",
#                                    facecolor=facecolor, edgecolor=edgecolor, alpha=alpha,
#                                    transform=ax.transAxes)  # Координаты в долях от размера фигуры
#         ax.add_patch(p)
#
#     def create_final_image(self, symbol: str, densities: List[Density], mid_price: float) -> str:
#         """Создает финальное изображение, полностью повторяющее макет."""
#         if not densities: return ""
#
#         # --- 1. Подготовка данных ---
#         stats = self._get_stats(densities)
#         supports = sorted([d for d in densities if d.density_type == 'support'], key=lambda x: x.price, reverse=True)
#         resistances = sorted([d for d in densities if d.density_type == 'resistance'], key=lambda x: x.price,
#                              reverse=True)
#         strongest_support = max(supports, key=lambda x: x.volume_usd, default=None)
#         strongest_resistance = max(resistances, key=lambda x: x.volume_usd, default=None)
#         key_resistances = sorted(resistances, key=lambda x: x.volume_usd, reverse=True)[:2]
#         key_supports = sorted(supports, key=lambda x: x.volume_usd, reverse=True)[:2]
#
#         # --- 2. Холст ---
#         fig, ax = plt.subplots(figsize=(10, 10), dpi=150)
#         fig.patch.set_facecolor('#24282f')
#         ax.axis('off')
#
#         # --- 3. Отрисовка блоков ---
#         # Заголовок
#         ax.text(0.5, 0.95, f"4. Многоуровневый вывод ({symbol})", color='#f0c142', fontsize=20, ha='center',
#                 weight='bold', transform=ax.transAxes)
#         ax.axhline(0.93, 0.2, 0.8, color='#f0c142', linewidth=2)
#
#         # --- Блок Ключевые уровни (слева) ---
#         y_pos = 0.8
#         ax.text(0.25, y_pos, "Ключевые уровни", color='#67e484', fontsize=14, ha='center', weight='bold',
#                 transform=ax.transAxes)
#         y_pos -= 0.08
#         for r in key_resistances:
#             star = " ⭐" if strongest_resistance and r.price == strongest_resistance.price else ""
#             text = f"${r.price:,.2f} | ${r.volume_usd / 1000:,.0f}k{star}"
#             self._draw_rounded_box(ax, [0.05, y_pos - 0.025, 0.4, 0.05], facecolor='#e6536d', edgecolor='white')
#             ax.text(0.25, y_pos, text, color='white', fontsize=12, ha='center', va='center', weight='bold',
#                     transform=ax.transAxes)
#             y_pos -= 0.07
#         ax.text(0.25, y_pos, f"— ${mid_price:,.2f} —", color='#f0c142', fontsize=13, ha='center', va='center',
#                 weight='bold', transform=ax.transAxes)
#         y_pos -= 0.07
#         for s in key_supports:
#             star = " ⭐" if strongest_support and s.price == strongest_support.price else ""
#             text = f"${s.price:,.2f} | ${s.volume_usd / 1000:,.0f}k{star}"
#             self._draw_rounded_box(ax, [0.05, y_pos - 0.025, 0.4, 0.05], facecolor='#2fba77', edgecolor='black')
#             ax.text(0.25, y_pos, text, color='white', fontsize=12, ha='center', va='center', weight='bold',
#                     transform=ax.transAxes)
#             y_pos -= 0.07
#
#         # --- Блок Статистика (справа) ---
#         self._draw_rounded_box(ax, [0.55, y_pos, 0.4, 0.8 - y_pos], facecolor='#1a1a1a', edgecolor='gray')
#         ax.text(0.75, 0.8, "Статистика", color='#67e484', fontsize=14, ha='center', weight='bold',
#                 transform=ax.transAxes)
#         stats_text = (
#             f"Общий объем: ${stats['total_volume_k']:,.0f}k\n"
#             f"Биржи: {stats['exchanges_count']} шт.\n"
#             f"Поддержка: ${stats['support_k']:,.0f}k ({stats['support_count']} ур.)\n"
#             f"Сопротивление: ${stats['resistance_k']:,.0f}k ({stats['resistance_count']} ур.)\n"
#             f"Баланс: {stats['balance']}"
#         )
#         ax.text(0.58, 0.75, stats_text, color='white', fontsize=11, ha='left', va='top', transform=ax.transAxes,
#                 linespacing=1.8)
#
#         # --- Блок Подробная разбивка (снизу) ---
#         y_pos -= 0.05
#         self._draw_rounded_box(ax, [0.05, 0.05, 0.9, y_pos - 0.08], facecolor='#2a4a37', edgecolor='#67e484')
#         ax.text(0.1, y_pos - 0.05, "📊 Подробная разбивка:", color='white', fontsize=14, ha='left', va='top',
#                 weight='bold', transform=ax.transAxes)
#
#         y_pos -= 0.12
#         grouped_by_exchange = defaultdict(list)
#         for d in densities: grouped_by_exchange[d.exchange].append(d)
#         sorted_exchanges = sorted(grouped_by_exchange.items(), key=lambda x: sum(d.volume_usd for d in x[1]),
#                                   reverse=True)
#
#         for exchange, dens in sorted_exchanges[:3]:
#             if y_pos < 0.1: break
#             exchange_total = sum(d.volume_usd for d in dens) / 1000
#             header = f"{exchange.upper()} (${exchange_total:,.0f}k):"
#
#             res_parts = [f"${d.price:,.4f}→${d.volume_usd / 1000:.0f}k" for d in
#                          sorted(filter(lambda x: x.density_type == 'resistance', dens), key=lambda x: x.volume_usd,
#                                 reverse=True)[:2]]
#             sup_parts = [f"${d.price:,.4f}→${d.volume_usd / 1000:.0f}k" for d in
#                          sorted(filter(lambda x: x.density_type == 'support', dens), key=lambda x: x.volume_usd,
#                                 reverse=True)[:2]]
#
#             line = ""
#             if res_parts: line += f"🔴 {', '.join(res_parts)}"
#             if sup_parts: line += (" | " if line else "") + f"🟢 {', '.join(sup_parts)}"
#
#             ax.text(0.1, y_pos, header, color='white', fontsize=12, ha='left', va='top', weight='bold',
#                     transform=ax.transAxes)
#             ax.text(0.12, y_pos - 0.05, line, color='white', fontsize=11, ha='left', va='top', transform=ax.transAxes)
#             y_pos -= 0.1
#
#         # --- Сохранение ---
#         file_path = Path(self.config['TEMP_DIR']) / f"final_{symbol.replace('/', '_')}_{int(time.time())}.png"
#         try:
#             plt.savefig(file_path, facecolor=fig.get_facecolor(), bbox_inches='tight')
#             logger.info(f"Финальное изображение для {symbol} сохранено: {file_path}")
#             return str(file_path)
#         except Exception as e:
#             logger.error(f"Не удалось сохранить изображение для {symbol}: {e}")
#             return ""
#         finally:
#             plt.close(fig)


# # inter_exchange_arbitrage_bot/src/services/density_chart_service.py
#
# import time
# from dataclasses import is_dataclass
# from pathlib import Path
# from typing import List, Tuple, Dict, Optional
#
# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.ticker import FuncFormatter
# from matplotlib.patheffects import withStroke
# import numpy as np
#
# from src.constants.trading_constants import DENSITY_CHART_CONFIG
# from src.models.screener_models import Density
# from src.utils.logger import logger
#
#
# class DensityChartService:
#     """Улучшенный сервис для визуализации плотностей с адаптивным масштабированием и оптимизированной читаемостью."""
#
#     def __init__(self):
#         self.config = DENSITY_CHART_CONFIG
#         Path(self.config['TEMP_DIR']).mkdir(exist_ok=True)
#         plt.switch_backend('Agg')
#
#     def _calculate_adaptive_dimensions(self, level_count: int) -> Tuple[
#         Tuple[int, int], Dict[str, float], Dict[str, int]]:
#         """Рассчитывает адаптивные размеры и настройки в зависимости от количества уровней."""
#         # Базовые размеры
#         width = self.config['BASE_FIGURE_WIDTH']
#         height = min(
#             self.config['BASE_FIGURE_HEIGHT'] + level_count * self.config['HEIGHT_PER_LEVEL'],
#             self.config['MAX_FIGURE_HEIGHT']
#         )
#
#         # Выбор настроек отступов
#         if level_count >= self.config['HIGH_DENSITY_THRESHOLD']:
#             adjustments = self.config['HIGH_DENSITY_ADJUSTMENTS'].copy()
#         else:
#             adjustments = self.config['BASE_SUBPLOT_ADJUSTMENTS'].copy()
#
#         # Адаптивные размеры шрифтов
#         font_factor = self.config['FONT_REDUCTION_FACTOR'] if level_count >= self.config[
#             'COMPACT_MODE_THRESHOLD'] else 1.0
#
#         font_sizes = {
#             'title': int(self.config['BASE_TITLE_FONT_SIZE'] * font_factor),
#             'label': int(self.config['BASE_LABEL_FONT_SIZE'] * font_factor),
#             'annotation': int(self.config['BASE_ANNOTATION_FONT_SIZE'] * font_factor),
#             'legend': int(self.config['BASE_LEGEND_FONT_SIZE'] * font_factor),
#             'tick': int(self.config['BASE_TICK_FONT_SIZE'] * font_factor)
#         }
#
#         return (width, height), adjustments, font_sizes
#
#     def _cluster_densities(self, df: pd.DataFrame) -> pd.DataFrame:
#         """Группирует близкие уровни в один, суммируя их объемы."""
#         if df.empty:
#             return df
#
#         df = df.sort_values('price').reset_index(drop=True)
#         clusters = []
#         current_cluster = None
#
#         for _, row in df.iterrows():
#             if current_cluster is None:
#                 current_cluster = [row]
#             else:
#                 price_diff_percent = (abs(row['price'] - current_cluster[-1]['price']) / row['price']) * 100
#                 if price_diff_percent < self.config['CLUSTERING_THRESHOLD_PERCENT']:
#                     current_cluster.append(row)
#                 else:
#                     clusters.append(current_cluster)
#                     current_cluster = [row]
#
#         if current_cluster:
#             clusters.append(current_cluster)
#
#         # Агрегируем кластеры
#         aggregated_data = []
#         for cluster in clusters:
#             cluster_df = pd.DataFrame(cluster)
#             total_volume = cluster_df['volume_usd'].sum()
#             avg_price = (cluster_df['price'] * cluster_df['volume_usd']).sum() / total_volume
#             exchanges = ', '.join(cluster_df['exchange'].unique())
#
#             aggregated_data.append({
#                 'price': avg_price,
#                 'volume_usd': total_volume,
#                 'density_type': cluster_df.iloc[0]['density_type'],
#                 'exchange': exchanges
#             })
#
#         return pd.DataFrame(aggregated_data)
#
#     def _detect_annotation_collisions(self, annotations: List[Dict]) -> List[Dict]:
#         """Обнаруживает и устраняет коллизии между аннотациями."""
#         if not self.config.get('ANNOTATION_COLLISION_DETECTION', False):
#             return annotations
#
#         # Сортируем по Y-координате
#         sorted_annotations = sorted(annotations, key=lambda a: a['y'])
#         min_distance = self.config['MIN_ANNOTATION_DISTANCE']
#
#         # Устраняем коллизии
#         for i in range(1, len(sorted_annotations)):
#             current = sorted_annotations[i]
#             previous = sorted_annotations[i - 1]
#
#             if abs(current['y'] - previous['y']) < min_distance:
#                 # Смещаем текущую аннотацию
#                 current['y'] = previous['y'] + min_distance
#                 # Помечаем как смещенную
#                 current['shifted'] = True
#
#         return sorted_annotations
#
#     def _get_smart_text_position_and_color(self, volume: float, max_volume: float, bar_height: float,
#                                            price: float, density_type: str, level_count: int) -> tuple:
#         """Умно определяет позицию и цвет текста с учетом плотности данных."""
#         volume_ratio = volume / max_volume
#
#         # Адаптируем порог в зависимости от количества уровней
#         threshold = self.config['VOLUME_THRESHOLD_FOR_OUTSIDE_TEXT']
#         if level_count >= self.config['COMPACT_MODE_THRESHOLD']:
#             threshold *= 0.7  # Чаще размещаем текст снаружи при высокой плотности
#
#         place_outside = volume_ratio < threshold
#
#         if place_outside:
#             # Текст снаружи бара
#             x_pos = volume + (max_volume * self.config['TEXT_PADDING_RATIO'])
#             ha = 'left'
#             text_color = self.config['TEXT_ON_DARK_COLOR']
#         else:
#             # Текст внутри бара - адаптивное позиционирование
#             padding_factor = self.config['TEXT_PADDING_RATIO']
#             if level_count >= self.config['HIGH_DENSITY_THRESHOLD']:
#                 padding_factor *= 0.6  # Уменьшаем отступы при высокой плотности
#
#             x_pos = volume - (max_volume * padding_factor)
#             ha = 'right'
#             text_color = self.config['TEXT_ON_LIGHT_COLOR'] if density_type == 'support' else self.config[
#                 'TEXT_ON_DARK_COLOR']
#
#         return x_pos, ha, text_color, place_outside
#
#     def _add_smart_annotations(self, ax, df_clustered: pd.DataFrame, max_visible_volume: float,
#                                bar_height: float, font_sizes: Dict[str, int]):
#         """Добавляет умные аннотации с обнаружением коллизий и адаптивным размещением."""
#         level_count = len(df_clustered)
#         annotations_data = []
#
#         # Подготавливаем данные для аннотаций
#         for _, row in df_clustered.iterrows():
#             volume_text = f"${row['volume_usd'] / 1000:,.0f}k"
#
#             # Умное сокращение названий бирж
#             exchange_names = row['exchange'].split(', ')
#             if len(exchange_names) == 1:
#                 exchange_text = exchange_names[0].upper()[:6]
#             elif len(exchange_names) <= 3:
#                 exchange_text = '+'.join([e.upper()[:3] for e in exchange_names])
#             else:
#                 exchange_text = f"{exchange_names[0].upper()[:3]}+{len(exchange_names) - 1}"
#
#             x_pos, ha, text_color, is_outside = self._get_smart_text_position_and_color(
#                 row['volume_usd'], max_visible_volume, bar_height, row['price'],
#                 row['density_type'], level_count
#             )
#
#             annotations_data.append({
#                 'x': x_pos,
#                 'y': row['price'],
#                 'volume_text': volume_text,
#                 'exchange_text': exchange_text,
#                 'ha': ha,
#                 'color': text_color,
#                 'density_type': row['density_type'],
#                 'is_outside': is_outside,
#                 'shifted': False
#             })
#
#         # Обнаруживаем и устраняем коллизии
#         if self.config.get('SMART_ANNOTATION_SPACING', False):
#             annotations_data = self._detect_annotation_collisions(annotations_data)
#
#         # Отрисовываем аннотации
#         for annotation in annotations_data:
#             # Основной текст объема
#             outline_width = self.config['ANNOTATION_OUTLINE_WIDTH']
#             if annotation['shifted']:
#                 outline_width += 1  # Усиливаем обводку для смещенных аннотаций
#
#             ax.text(
#                 annotation['x'], annotation['y'], annotation['volume_text'],
#                 va='center', ha=annotation['ha'],
#                 color='white',  # Всегда белый для максимального контраста
#                 fontsize=font_sizes['annotation'],
#                 weight='bold',
#                 path_effects=[
#                     withStroke(linewidth=outline_width, foreground='black')
#                 ]
#             )
#
#             # Текст биржи - адаптивное позиционирование
#             offset_factor = 0.35 if level_count >= self.config['COMPACT_MODE_THRESHOLD'] else 0.4
#             offset_y = bar_height * offset_factor
#             if annotation['density_type'] == 'resistance':
#                 offset_y = -offset_y
#
#             ax.text(
#                 annotation['x'], annotation['y'] + offset_y, annotation['exchange_text'],
#                 va='center', ha=annotation['ha'],
#                 color=self.config['EXCHANGE_TEXT_COLOR'],
#                 fontsize=font_sizes['annotation'] - 1,  # Немного меньше основного текста
#                 weight='normal',
#                 path_effects=[
#                     withStroke(linewidth=1, foreground='black')
#                 ]
#             )
#
#     def _create_adaptive_legend_and_infobox(self, ax, support_count: int, resistance_count: int,
#                                             mid_price: float, font_sizes: Dict[str, int],
#                                             total_volume: float):
#         """Создает адаптивную легенду и информационный блок."""
#         from matplotlib.patches import Patch
#
#         # Легенда в левом верхнем углу
#         legend_elements = [
#             Patch(facecolor=self.config['SUPPORT_COLOR'], label=f'Поддержка ({support_count})'),
#             Patch(facecolor=self.config['RESISTANCE_COLOR'], label=f'Сопротивление ({resistance_count})'),
#             plt.Line2D([0], [0], color=self.config['MID_PRICE_COLOR'], lw=2, linestyle='--',
#                        label=f'Цена: ${mid_price:,.4f}')
#         ]
#
#         legend = ax.legend(
#             handles=legend_elements,
#             facecolor='#2c2c2c',
#             edgecolor='gray',
#             labelcolor='white',
#             fontsize=font_sizes['legend'],
#             loc=self.config['LEGEND_LOCATION'],
#             bbox_to_anchor=self.config['LEGEND_BBOX_ANCHOR'],
#             framealpha=0.9
#         )
#         legend.get_frame().set_linewidth(1)
#
#         # Информационный блок в правом верхнем углу (если включен)
#         if self.config.get('INFO_BOX_ENABLED', False):
#             info_text = f"Общий объем: ${total_volume / 1000:,.0f}k\nУровней: {support_count + resistance_count}"
#
#             ax.text(0.98, 0.98, info_text,
#                     transform=ax.transAxes,
#                     fontsize=font_sizes['legend'] - 1,
#                     color='white',
#                     ha='right', va='top',
#                     bbox=dict(boxstyle='round,pad=0.3',
#                               facecolor='#2c2c2c',
#                               alpha=self.config['INFO_BOX_ALPHA'],
#                               edgecolor='gray'),
#                     path_effects=[withStroke(linewidth=1, foreground='black')])
#
#         return legend
#
#     def create_density_chart(self, symbol: str, densities: List[Density], mid_price: float) -> str:
#         """
#         Создает адаптивный график плотностей с улучшенной читаемостью и информативностью.
#         """
#         if not densities:
#             return ""
#
#         dict_densities = [d.__dict__ for d in densities if is_dataclass(d)]
#         if not dict_densities:
#             return ""
#
#         df = pd.DataFrame(dict_densities)
#
#         # Кластеризуем близкие уровни
#         support_df = self._cluster_densities(df[df['density_type'] == 'support'])
#         resistance_df = self._cluster_densities(df[df['density_type'] == 'resistance'])
#
#         df_clustered = pd.concat([support_df, resistance_df])
#         if df_clustered.empty:
#             logger.debug(f"После кластеризации для {symbol} не осталось плотностей.")
#             return ""
#
#         level_count = len(df_clustered)
#
#         # Рассчитываем адаптивные размеры
#         figure_size, subplot_adjustments, font_sizes = self._calculate_adaptive_dimensions(level_count)
#
#         # Динамический расчет масштаба
#         key_prices = [mid_price]
#         key_prices.extend(df_clustered.nlargest(5, 'volume_usd')['price'].tolist())
#
#         min_key_price = min(key_prices)
#         max_key_price = max(key_prices)
#         price_buffer = (max_key_price - min_key_price) * 0.15 if max_key_price > min_key_price else mid_price * 0.015
#         min_y = min_key_price - price_buffer
#         max_y = max_key_price + price_buffer
#
#         # Адаптивная толщина баров
#         bar_height = (max_y - min_y) * self.config['MIN_BAR_HEIGHT_RATIO']
#
#         # Находим самые крупные уровни
#         strongest_support = support_df.loc[support_df['volume_usd'].idxmax()] if not support_df.empty else None
#         strongest_resistance = resistance_df.loc[
#             resistance_df['volume_usd'].idxmax()] if not resistance_df.empty else None
#
#         # Создание холста с адаптивными настройками
#         fig, ax = plt.subplots(figsize=figure_size, dpi=self.config['DPI'])
#         fig.patch.set_facecolor('#1E1E1E')
#         ax.set_facecolor('#1E1E1E')
#
#         # Отрисовка баров
#         max_visible_volume = df_clustered['volume_usd'].max()
#         total_volume = df_clustered['volume_usd'].sum()
#
#         # Отрисовка баров поддержки
#         for _, row in support_df.iterrows():
#             is_strongest = strongest_support is not None and row['price'] == strongest_support['price']
#             color = self.config['STRONGEST_SUPPORT_COLOR'] if is_strongest else self.config['SUPPORT_COLOR']
#             edge_width = 2.5 if is_strongest else 1.5
#             ax.barh(row['price'], row['volume_usd'], height=bar_height,
#                     color=color, edgecolor='white', linewidth=edge_width, alpha=0.9)
#
#         # Отрисовка баров сопротивления
#         for _, row in resistance_df.iterrows():
#             is_strongest = strongest_resistance is not None and row['price'] == strongest_resistance['price']
#             color = self.config['STRONGEST_RESISTANCE_COLOR'] if is_strongest else self.config['RESISTANCE_COLOR']
#             edge_width = 2.5 if is_strongest else 1.5
#             ax.barh(row['price'], row['volume_usd'], height=bar_height,
#                     color=color, edgecolor='white', linewidth=edge_width, alpha=0.9)
#
#         # Добавляем умные аннотации
#         self._add_smart_annotations(ax, df_clustered, max_visible_volume, bar_height, font_sizes)
#
#         # Средняя линия цены
#         ax.axhline(y=mid_price, color=self.config['MID_PRICE_COLOR'], linestyle='--',
#                    linewidth=3, alpha=0.8, zorder=10,
#                    path_effects=[withStroke(linewidth=4, foreground='black')])
#
#         # Заголовок с адаптивным размером
#         title = f'Плотности в стакане для {symbol}'
#         if level_count >= self.config['COMPACT_MODE_THRESHOLD']:
#             title += f'\n{level_count} уровней • ${total_volume / 1000:,.0f}k'
#         else:
#             title += f'\nВсего уровней: {level_count} • Общий объем: ${total_volume / 1000:,.0f}k'
#
#         ax.set_title(title, fontsize=font_sizes['title'], color='white',
#                      weight='bold', pad=20, linespacing=1.2)
#
#         # Настройка осей
#         ax.set_ylabel('Цена (USDT)', fontsize=font_sizes['label'], color='white', weight='bold')
#         ax.set_xlabel('Объем (USD)', fontsize=font_sizes['label'], color='white', weight='bold')
#
#         # Форматирование осей
#         ax.xaxis.set_major_formatter(
#             FuncFormatter(lambda x, p: f'{x / 1000:.0f}k' if x < 1_000_000 else f'{x / 1_000_000:.1f}M'))
#
#         ax.tick_params(axis='x', colors='white', labelsize=font_sizes['tick'])
#         ax.tick_params(axis='y', colors='white', labelsize=font_sizes['tick'])
#
#         # Стилизация границ
#         for spine in ['top', 'right']:
#             ax.spines[spine].set_visible(False)
#         for spine in ['bottom', 'left']:
#             ax.spines[spine].set_color('gray')
#             ax.spines[spine].set_linewidth(1)
#
#         # Создаем адаптивную легенду и инфобокс
#         self._create_adaptive_legend_and_infobox(ax, len(support_df), len(resistance_df),
#                                                  mid_price, font_sizes, total_volume)
#
#         # Сетка
#         ax.grid(axis='x', linestyle=':', alpha=0.3, color=self.config['GRID_COLOR'], linewidth=0.8)
#
#         # Инвертируем ось Y
#         ax.set_ylim(max_y, min_y)
#
#         # Применяем адаптивные отступы
#         fig.subplots_adjust(**subplot_adjustments)
#
#         # Сохранение с оптимальными настройками для Telegram
#         file_path_obj = Path(self.config['TEMP_DIR']) / f"{symbol.replace('/', '_')}_{int(time.time())}.png"
#         try:
#             plt.savefig(file_path_obj, facecolor=fig.get_facecolor(), bbox_inches='tight',
#                         dpi=self.config['DPI'], format='png',
#                         pil_kwargs={'optimize': True, 'quality': 90})
#             logger.info(f"Адаптивный график плотностей для {symbol} сохранен в: {file_path_obj}")
#             return str(file_path_obj)
#         except Exception as e:
#             logger.error(f"Не удалось сохранить график для {symbol}: {e}")
#             return ""
#         finally:
#             plt.close(fig)
#
