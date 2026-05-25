# inter_exchange_arbitrage_bot/src/services/enhanced_ai_processor_service.py
import asyncio
import json
import re
import time
import unicodedata
from typing import List, Dict, Any, Union

import httpx
import src.core.state as app_state
from src.constants.api_constants import (
    AI_SINGLE_REQUEST_TIMEOUT, GROQ_API_URL, GEMINI_API_URL_TEMPLATE, OPENROUTER_API_URL,
    GROQ_BASE_PRIORITY, GEMINI_BASE_PRIORITY, OPENROUTER_BASE_PRIORITY,
    AI_CONSERVATIVE_TOKEN_LIMIT, AI_PROVIDER_SAFETY_MARGIN, AI_SYSTEM_PROMPT_TOKENS_ESTIMATE, AI_MAX_CONCURRENT_REQUESTS
)
from src.constants.prompts import NEWS_ANALYSIS_PROMPT_JSON, COMPREHENSIVE_NEWS_ANALYSIS_PROMPT_JSON
from src.core.config import AIConfig, config
from src.core.enhanced_ai_resilience import ProviderConfig, enhanced_ai_manager
from src.utils.logger import logger


class EnhancedAIProcessorService:
    def __init__(self, ai_config: AIConfig, http_session: httpx.AsyncClient):
        self.config = ai_config
        self.session = http_session
        self._initialize_providers()

    def _initialize_providers(self):
        """
        УНИВЕРСАЛЬНАЯ инициализация всех AI-провайдеров.
        Корректно создает отдельную запись для КАЖДОЙ комбинации "ключ + модель".
        """
        providers_to_register = []

        def register_provider_variants(provider_name: str, provider_config, base_priority: int, tokens_per_min: int,
                                       max_tokens: int, delay: float):
            if not provider_config.keys:
                logger.warning(f"{provider_name.upper()}_API_KEYS не заданы.")
                return 0
            if not provider_config.models:
                logger.warning(f"{provider_name.upper()}_MODELS не заданы.")
                return 0

            priority_counter = 0
            for i, key in enumerate(provider_config.keys):
                for j, model in enumerate(provider_config.models):
                    providers_to_register.append(ProviderConfig(
                        name=f"{provider_name.capitalize()}-{i + 1}-{model.replace('/', '_')}",
                        api_key=key,
                        model=model,
                        tokens_per_minute=tokens_per_min,
                        max_tokens_per_request=max_tokens,
                        base_delay=delay,
                        priority=base_priority + priority_counter
                    ))
                    priority_counter += 1
            return priority_counter

        register_provider_variants("Groq", self.config.groq, GROQ_BASE_PRIORITY, 6000, 1000, 0.5)
        register_provider_variants("Gemini", self.config.gemini, GEMINI_BASE_PRIORITY, 15000, 2000, 0.3)
        register_provider_variants("OpenRouter", self.config.openrouter, OPENROUTER_BASE_PRIORITY, 10000, 1500, 0.4)

        if not providers_to_register:
            logger.warning("Ни один AI-провайдер не был зарегистрирован. Проверьте .env файл.")
            return

        for provider in providers_to_register:
            enhanced_ai_manager.register_provider(provider)

        logger.info(f"Успешно зарегистрировано {len(providers_to_register)} AI-провайдеров с поддержкой failover.")

    async def _worker(self, worker_id: str, queue: asyncio.Queue, results: list, comprehensive_mode: bool):
        while True:
            try:
                # Безопасно ждем новую задачу из очереди
                batch_index, batch = await queue.get()

                logger.debug(f"Рабочий {worker_id}: Взял в обработку пакет #{batch_index + 1}")

                prompt = self._create_prompt_from_list(batch,
                                                       comprehensive_mode=comprehensive_mode)  # <-- ИЗМЕНЕНИЕ: Используем переменную
                if not prompt or not prompt.strip():
                    logger.error(f"Рабочий {worker_id}: Пустой промпт для пакета #{batch_index + 1}")
                    queue.task_done()
                    continue

                result = await enhanced_ai_manager.execute_with_failover(
                    self._execute_ai_request,
                    prompt=prompt,
                    comprehensive_mode=True
                )

                if result:
                    # Сохраняем результат вместе с его исходным индексом
                    results.append((batch_index, result))
                    logger.debug(f"Рабочий {worker_id}: Успешно обработал пакет #{batch_index + 1}")

            except asyncio.CancelledError:
                # Если диспетчер отменяет задачу, выходим из цикла
                logger.info(f"Рабочий {worker_id}: Получен сигнал отмены.")
                break
            except Exception as e:
                logger.critical(f"КРИТИЧНО: Рабочий {worker_id} столкнулся с неперехватываемой ошибкой: {e}",
                                exc_info=True)
            finally:
                # ВАЖНО: В любом случае (успех, ошибка, пустой результат) сообщаем очереди, что задача обработана
                queue.task_done()

    async def process_news_batch(self, news_list: List[Dict], comprehensive_mode: bool = True) -> Dict[str, Any]:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Параллельная обработка с надежным управлением задачами.
        Этот метод выступает в роли "диспетчера".
        """
        start_time = time.time()
        if not news_list:
            return {"news": [], "market_summary": ""}

        try:
            valid_news = [item for item in news_list if
                          isinstance(item, dict) and (item.get('title') or item.get('body'))]
            if not valid_news:
                logger.error("После валидации не осталось обрабатываемых новостей")
                return {"news": [], "market_summary": "Нет валидных новостей для анализа"}
            news_list = valid_news
        except Exception as e:
            logger.error(f"Ошибка при валидации новостей: {e}")
            return {"news": [], "market_summary": "Ошибка валидации данных"}

        optimized_batches = self._create_token_optimized_batches(news_list)

        queue = asyncio.Queue()
        for i, batch in enumerate(optimized_batches):
            queue.put_nowait((i, batch))

        results_with_indices = []

        num_workers = min(AI_MAX_CONCURRENT_REQUESTS, len(optimized_batches))
        workers = [
            asyncio.create_task(self._worker(
                f"Worker-{i + 1}",
                queue,
                results_with_indices,
                comprehensive_mode=comprehensive_mode
            ))
            for i in range(num_workers)
        ]

        # АРГУМЕНТАЦИЯ: `queue.join()` будет ждать, пока для КАЖДОГО элемента,
        # положенного в очередь, не будет вызван `task_done()`. Это самый надежный
        # способ дождаться завершения всей работы.
        await queue.join()

        # АРГУМЕНТАЦИЯ: После завершения всей работы в очереди, мы можем безопасно
        # остановить наших "рабочих", отправив им сигнал отмены.
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)  # Ждем завершения отмены

        # АРГУМЕНТАЦИЯ: Сортируем результаты по их исходному индексу, чтобы
        # сохранить логический порядок market_summary.
        results_with_indices.sort(key=lambda x: x[0])

        all_news_results = []
        all_summaries = []

        for batch_index, result in results_with_indices:
            if isinstance(result, dict):
                if result.get("news"): all_news_results.extend(result["news"])
                if result.get("market_summary"): all_summaries.append(result["market_summary"])

        final_summary = "\n\n".join(all_summaries) if all_summaries else "Аналитика не была сгенерирована."

        processing_time = time.time() - start_time
        logger.info(
            f"Параллельная обработка {len(optimized_batches)} батчей ({len(workers)} рабочих) завершена за {processing_time:.2f}с.")

        return {"news": all_news_results, "market_summary": final_summary}

    def _create_token_optimized_batches(self, news_list: List[Dict]) -> List[List[Dict]]:
        """Формирует батчи, которые безопасны для любого провайдера."""
        if not news_list:
            return []

        max_tokens_for_news = int(
            AI_CONSERVATIVE_TOKEN_LIMIT * AI_PROVIDER_SAFETY_MARGIN - AI_SYSTEM_PROMPT_TOKENS_ESTIMATE)
        logger.debug(f"Формирую батчи. Безопасный лимит для новостей: {max_tokens_for_news} токенов.")

        batches = []
        current_batch = []
        current_tokens = 0

        for news_item in news_list:
            item_tokens = self._estimate_news_tokens(news_item)

            if item_tokens > max_tokens_for_news:
                logger.warning(f"Новость слишком длинная ({item_tokens} токенов) и будет обработана в отдельном батче.")
                if current_batch:
                    batches.append(current_batch)
                batches.append([news_item])
                current_batch = []
                current_tokens = 0
                continue

            if current_tokens + item_tokens > max_tokens_for_news and current_batch:
                batches.append(current_batch)
                current_batch = [news_item]
                current_tokens = item_tokens
            else:
                current_batch.append(news_item)
                current_tokens += item_tokens

        if current_batch:
            batches.append(current_batch)

        avg_size = len(news_list) / len(batches) if batches else 0
        logger.info(f"Создано {len(batches)} батчей. Средний размер: {avg_size:.1f} новостей.")
        return batches

    async def _execute_ai_request(
            self,
            provider_name_override: str,
            prompt: str,
            comprehensive_mode: bool
    ) -> Union[List[Dict], Dict[str, Any]]:
        """
        ФИНАЛЬНАЯ ВЕРСИЯ: Использует отказоустойчивый каскадный механизм смены IP
        с возможностью полного отключения и корректной поддержкой Tor.
        """
        provider_config = enhanced_ai_manager.providers[provider_name_override]
        api_key = provider_config.api_key
        model = provider_config.model
        provider_name_lower = provider_name_override.lower()

        try:
            key_index = int(provider_name_override.split('-')[1]) - 1
        except (IndexError, ValueError):
            key_index = 0

        async def make_request_with_client(client: httpx.AsyncClient):
            if provider_name_lower.startswith("groq"):
                return await self._process_with_groq(prompt, api_key, model, comprehensive_mode, client=client)
            elif provider_name_lower.startswith("gemini"):
                return await self._process_with_gemini(prompt, api_key, model, comprehensive_mode, client=client)
            elif provider_name_lower.startswith("openrouter"):
                return await self._process_with_openrouter(prompt, api_key, model, comprehensive_mode, client=client)
            raise ValueError(f"Неизвестный тип AI провайдера: {provider_name_override}")

        # --- Стратегия #0: Проверка глобального флага отключения ---
        if not config.network.ip_rotation_enabled:
            logger.debug(f"AI запрос [{provider_name_override}]: ➡️ Прямое соединение (ротация IP отключена).")
            return await make_request_with_client(self.session)

        # --- Стратегия #1: Прямое соединение для первого ключа ---
        if key_index == 0:
            logger.info(f"AI запрос [{provider_name_override}]: ➡️ Прямое соединение (первый ключ).")
            return await make_request_with_client(self.session)

        # --- Стратегия #2: Перебор всех прокси ---
        if 'proxy_fallback' in config.network.ip_rotation_strategy:
            healthy_proxies = app_state.proxy_manager.get_healthy_proxies() if app_state.proxy_manager else []
            if healthy_proxies:
                logger.debug(f"AI запрос [{provider_name_override}]: Запускаю перебор {len(healthy_proxies)} прокси...")
                for i, proxy_str in enumerate(healthy_proxies):
                    try:
                        transport = httpx.AsyncHTTPTransport(proxy=f"http://{proxy_str}")
                        async with httpx.AsyncClient(transport=transport,
                                                     timeout=config.network.proxy_check_timeout) as client:
                            result = await make_request_with_client(client)
                            logger.info(
                                f"AI запрос [{provider_name_override}] ✅ Успешно через прокси #{i + 1} ({proxy_str})")
                            return result
                    except Exception as e:
                        logger.debug(
                            f"AI запрос [{provider_name_override}] ❌ Прокси #{i + 1} ({proxy_str}) не сработал: {type(e).__name__}")
                        continue
            else:
                logger.warning(f"AI запрос [{provider_name_override}] Список 'здоровых' прокси пуст.")

        # --- Стратегия #3: Tor (если все прокси провалились) ---
        if 'tor_fallback' in config.network.ip_rotation_strategy:
            if app_state.proxy_manager and app_state.proxy_manager.is_tor_available:
                logger.debug(f"AI запрос [{provider_name_override}]: Пробую через Tor...")
                try:
                    import httpx_socks
                    transport = httpx_socks.AsyncProxyTransport.from_url(config.network.tor_proxy_url)
                    async with httpx.AsyncClient(transport=transport,
                                                 timeout=config.network.proxy_check_timeout) as client:
                        result = await make_request_with_client(client)
                        logger.info(f"AI запрос [{provider_name_override}] ✅ Успешно через Tor.")
                        return result
                except ImportError:
                    logger.warning(
                        f"AI запрос [{provider_name_override}] ❌ Попытка через Tor не удалась: httpx_socks не найден.")
                except Exception as e:
                    logger.warning(
                        f"AI запрос [{provider_name_override}] ❌ Попытка через Tor не удалась: {type(e).__name__}")
            else:
                logger.warning(f"AI запрос [{provider_name_override}] Tor недоступен или отключен.")

        # --- Стратегия #4: Прямое соединение (последняя надежда) ---
        logger.warning(f"AI запрос [{provider_name_override}] ⚠️ Все стратегии ротации IP не сработали. Прямой запрос.")
        return await make_request_with_client(self.session)

    def _parse_ai_response(self, response_text: str, comprehensive_mode: bool = False) -> Union[
        List[Dict], Dict[str, Any]]:
        """
        УЛУЧШЕННАЯ ВЕРСИЯ парсера с дополнительными проверками и логгированием.
        """
        if not response_text or not response_text.strip():
            logger.error("AI вернул пустой или состоящий из пробелов ответ.")
            raise json.JSONDecodeError("Пустой ответ от AI", "", 0)

        start_index = response_text.find('{')
        end_index = response_text.rfind('}')

        if start_index == -1 or end_index == -1 or end_index < start_index:
            logger.error("Не удалось найти валидные границы JSON в ответе AI.")
            debug_text = response_text[:200] + "..." if len(response_text) > 200 else response_text
            logger.debug(f"Начало ответа: {debug_text}")
            raise json.JSONDecodeError("Не найдены границы JSON в ответе.", response_text, 0)

        json_body = response_text[start_index: end_index + 1]

        try:
            # Первая попытка
            data = json.loads(json_body)
            return self._process_parsed_data(data, comprehensive_mode)
        except json.JSONDecodeError as e:
            logger.warning(f"Стандартный парсер JSON не справился: {e}. Применяю универсальный метод очистки...")

            try:
                # Вторая попытка с использованием улучшенного "чистильщика"
                corrected_json = self._sanitize_and_fix_json_string(json_body)
                data = json.loads(corrected_json)
                logger.info("JSON успешно исправлен и распарсен после полной очистки.")
                return self._process_parsed_data(data, comprehensive_mode)
            except json.JSONDecodeError as final_e:
                logger.error(f"Не удалось распарсить JSON даже после полной очистки: {final_e}")
                # Логируем для отладки, но ограничиваем размер
                debug_json = corrected_json[:500] + "..." if len(corrected_json) > 500 else corrected_json
                logger.debug(f"Проблемный JSON после очистки: {debug_json}")
                raise final_e

    def _sanitize_and_fix_json_string(self, json_text: str) -> str:
        """
        Единый и ИСЧЕРПЫВАЮЩИЙ метод для очистки и исправления JSON-строки от AI.
        ИСПРАВЛЕННАЯ ВЕРСИЯ с корректным отслеживанием экранирования.
        """
        # Шаг 1: Начальная нормализация и удаление невидимых символов
        corrected = unicodedata.normalize('NFC', json_text)
        corrected = corrected.replace('\ufeff', '')  # BOM
        corrected = corrected.replace('\u200b', '')  # Zero-width space
        corrected = corrected.replace('\u00a0', ' ')  # Non-breaking space

        # Шаг 2: Экранирование недопустимых управляющих символов (коды < 32)
        def replace_control_chars(match):
            char = match.group(0)
            code = ord(char)
            if code in {9, 10, 13}:  # Разрешаем \t, \n, \r
                return char
            return f'\\u{code:04x}'  # Экранируем остальные

        corrected = re.sub(r'[\x00-\x1f]', replace_control_chars, corrected)

        # Шаг 3: Исправление неэкранированных переносов строк внутри строковых значений JSON
        in_string = False
        escaped = False
        result_chars = []

        for char in corrected:
            if char == '"' and not escaped:
                in_string = not in_string

            if in_string and not escaped:
                if char == '\n':
                    result_chars.append('\\n')
                elif char == '\r':
                    result_chars.append('\\r')
                elif char == '\t':
                    result_chars.append('\\t')
                else:
                    result_chars.append(char)
            else:
                result_chars.append(char)

            # ИСПРАВЛЕННАЯ логика отслеживания экранирования
            escaped = (char == '\\' and not escaped)

        corrected = "".join(result_chars)

        # Шаг 4: Удаление висячих запятых (очень частая ошибка LLM)
        corrected = re.sub(r',\s*([}\]])', r'\1', corrected)

        return corrected.strip()

    def _process_parsed_data(self, data: dict, comprehensive_mode: bool) -> Union[List[Dict], Dict[str, Any]]:
        """
        Выносит логику обработки успешно распарсенных данных для избежания дублирования кода.
        """
        if comprehensive_mode:
            news_list = data.get("news", [])
            summary = data.get("market_summary", "")
            if not isinstance(news_list, list):
                logger.warning(f"AI вернул 'news' не в виде списка, а как {type(news_list)}. Возвращаю пустой список.")
                news_list = []
            if not isinstance(summary, str):
                logger.warning(
                    f"AI_FORMAT_VIOLATION: AI вернул 'market_summary' в виде {type(summary)}, а не строки. Конвертирую в JSON.")
                summary = json.dumps(summary, indent=2, ensure_ascii=False) if summary else ""

            return {"news": news_list, "market_summary": summary}
        else:
            news_list = data.get('news', [])
            if not isinstance(news_list, list):
                logger.warning(f"AI вернул 'news' не в виде списка, а как {type(news_list)}. Возвращаю пустой список.")
                news_list = []
            return news_list

    async def _process_with_groq(self, prompt: str, api_key: str, model: str, comprehensive_mode: bool,
                                 client: httpx.AsyncClient) -> Union[List[Dict], Dict[str, Any]]:
        """Обработка запроса через Groq с динамической моделью."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }

        response = await client.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=AI_SINGLE_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        return self._parse_ai_response(content, comprehensive_mode)

    async def _process_with_gemini(self, prompt: str, api_key: str, model: str, comprehensive_mode: bool,
                                   client: httpx.AsyncClient) -> Union[List[Dict], Dict[str, Any]]:
        """ИСПРАВЛЕННАЯ обработка запроса через Gemini с динамической моделью."""
        try:
            base_url = GEMINI_API_URL_TEMPLATE.format(model_name=model)
            url = f"{base_url}?key={api_key}"
        except Exception as e:
            raise ValueError(f"Ошибка в шаблоне URL Gemini или имени модели {model}: {e}")

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        }

        response = await client.post(url, json=payload, timeout=AI_SINGLE_REQUEST_TIMEOUT)
        response.raise_for_status()

        response_text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return self._parse_ai_response(response_text, comprehensive_mode=comprehensive_mode)

    async def _process_with_openrouter(self, prompt: str, api_key: str, model: str, comprehensive_mode: bool,
                                       client: httpx.AsyncClient) -> Union[List[Dict], Dict[str, Any]]:
        """Обработка запроса через OpenRouter с динамической моделью."""
        response = await client.post(
            OPENROUTER_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": 0.1
            },
            timeout=AI_SINGLE_REQUEST_TIMEOUT
        )
        response.raise_for_status()

        response_text = response.json()['choices'][0]['message']['content']
        return self._parse_ai_response(response_text, comprehensive_mode=comprehensive_mode)

    async def get_service_status(self) -> Dict[str, Any]:
        """Возвращает расширенный статус сервиса"""
        return {
            "service": "EnhancedAIProcessorService",
            "providers": enhanced_ai_manager.get_status_report(),
            "total_providers": len(enhanced_ai_manager.providers),
            "available_providers": len([
                p for p in enhanced_ai_manager.provider_states.values()
                if p['rate_limit_until'] <= time.time()
            ])
        }

    async def generate_text_insight(self, prompt: str) -> str:
        """Выполняет запрос к AI для получения текстового ответа (не JSON)."""
        try:
            result_text = await enhanced_ai_manager.execute_with_failover(self._execute_text_request, prompt)
            return result_text if isinstance(result_text, str) else "Не удалось получить ответ от AI."
        except Exception as e:
            logger.error(f"Критическая ошибка при генерации текстовой аналитики: {e}")
            return "Аналитика временно недоступна из-за ошибки AI провайдеров."

    async def _execute_text_request(self, prompt: str, provider_name_override: str) -> str:
        """Метод для текстовых запросов с динамическими моделями."""
        provider_config = enhanced_ai_manager.providers[provider_name_override]
        api_key = provider_config.api_key
        model = provider_config.model

        if provider_name_override.startswith("Groq"):
            return await self._process_with_groq_text(prompt, api_key, model)
        elif provider_name_override.startswith("Gemini"):
            return await self._process_with_gemini_text(prompt, api_key, model)
        elif provider_name_override.startswith("OpenRouter"):
            return await self._process_with_openrouter_text(prompt, api_key, model)
        else:
            raise ValueError(f"Неизвестный тип провайдера для текстового запроса: {provider_name_override}")

    async def _process_with_groq_text(self, prompt: str, api_key: str, model: str) -> str:
        """ИСПРАВЛЕННАЯ версия для текстовых запросов к Groq с динамической моделью."""
        response = await self.session.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "max_tokens": 1024
            },
            timeout=AI_SINGLE_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    async def _process_with_gemini_text(self, prompt: str, api_key: str, model: str) -> str:
        """Обработка через Gemini для текста с динамической моделью."""
        base_url = GEMINI_API_URL_TEMPLATE.format(model_name=model)
        url = f"{base_url}?key={api_key}"

        payload = {"contents": [{"parts": [{"text": prompt}]}],
                   "generationConfig": {"temperature": 0.2}}
        response = await self.session.post(url, json=payload, timeout=AI_SINGLE_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()['candidates'][0]['content']['parts'][0]['text']

    async def _process_with_openrouter_text(self, prompt: str, api_key: str, model: str) -> str:
        """Обработка через OpenRouter для текста с динамической моделью."""
        response = await self.session.post(
            OPENROUTER_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            },
            timeout=AI_SINGLE_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']

    def _sanitize_text(self, text: str) -> str:
        """Очистка текста для AI API с сохранением читаемости."""
        if not isinstance(text, str) or not text.strip():
            return ""

        try:
            text = unicodedata.normalize('NFC', text)
            cleaned_chars = []
            for char in text:
                try:
                    if unicodedata.category(char)[0] != 'C':
                        cleaned_chars.append(char)
                except (TypeError, ValueError):
                    continue

            text = ''.join(cleaned_chars)
            text = re.sub(r'\s+', ' ', text).strip()
            text = text.replace('\\', '\\\\').replace('"', '\\"')
            return text

        except Exception as e:
            logger.error(f"Ошибка очистки текста: {e}")
            try:
                return ' '.join(str(text).split()) if text else ""
            except Exception:
                return ""

    def _estimate_news_tokens(self, news_item: Dict) -> int:
        """Оценивает токены для ОДНОЙ новости, включая 'обертку' из промпта."""
        title = self._sanitize_text(news_item.get('title', ''))
        body = self._sanitize_text(news_item.get('body', ''))
        formatted_text = f"ID: 99\nTITLE: {title}\nBODY: {body}\n---\n"
        return enhanced_ai_manager.estimate_tokens(formatted_text)

    def _create_prompt_from_list(self, news_list: List[Dict], comprehensive_mode: bool = False) -> str:
        """Создает промпт с дополнительной защитой от проблемных данных."""
        if not news_list:
            return ""

        news_string = ""
        for i, news in enumerate(news_list):
            try:
                if not isinstance(news, dict):
                    logger.warning(f"Элемент новостей #{i} не является словарем: {type(news)}")
                    continue

                title = news.get('title', '')
                body = news.get('body', '')

                if not isinstance(title, str):
                    title = str(title) if title is not None else ''
                if not isinstance(body, str):
                    body = str(body) if body is not None else ''

                title = self._sanitize_text(title)
                body = self._sanitize_text(body)

                news_string += f"ID: {i}\nTITLE: {title}\nBODY: {body}\n---\n"

            except Exception as e:
                logger.error(f"Ошибка при обработке новости #{i}: {e}")
                news_string += f"ID: {i}\nTITLE: [Ошибка обработки]\nBODY: [Новость не может быть обработана]\n---\n"

        if not news_string.strip():
            logger.warning("После обработки не осталось валидных новостей для промпта")
            return ""

        prompt_template = COMPREHENSIVE_NEWS_ANALYSIS_PROMPT_JSON if comprehensive_mode else NEWS_ANALYSIS_PROMPT_JSON

        try:
            return prompt_template.format(news_text=news_string)
        except Exception as e:
            logger.error(f"Ошибка при форматировании промпта: {e}")
            return ""
