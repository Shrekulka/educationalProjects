# callback_data_factory/filters/goods_callback_factory.py

from aiogram.filters.callback_data import CallbackData


# Определение класса GoodsCallbackFactory с указанием наследования от CallbackData, префикса 'goods' и разделителя '|'
class GoodsCallbackFactory(CallbackData, prefix='goods', sep='|'):
    """
        Factory for generating and handling callback_data for buttons.

        Args:
            CallbackData: Base class for working with callback_data.
            prefix (str): The prefix from which button callback_data starts (default is 'goods').
            sep (str): Separator for fields in callback_data (default is '|').

        Attributes:
            category_id (int): Identifier of the product category.
            subcategory_id (int): Identifier of the product subcategory.
            item_id (int): Identifier of the product.

        Usage example:
            Create a button object with specified callback_data using the factory:
            ```
            button_1 = InlineKeyboardButton(
                text='Category 1',
                callback_data=GoodsCallbackFactory(
                    category_id=1,
                    subcategory_id=0,
                    item_id=0
                ).pack()
            )
            ```
    """
    category_id: int     # Определение поля category_id типа int
    subcategory_id: int  # Определение поля subcategory_id типа int
    item_id: int         # Определение поля item_id типа int
