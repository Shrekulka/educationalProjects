# # telegram_bot_book/keyboards/pagination_keyboard_wrapper.py
# from aiogram.types import InlineKeyboardMarkup
#
# from keyboards.pagination_kb import create_pagination_keyboard
# from services.file_handling import book
#
#
# #  Эта функция создает клавиатуру пагинации, адаптируя её в зависимости от текущей страницы книги.
# def pagination_keyboard_wrapper(page_num: int) -> InlineKeyboardMarkup:
#     """
#         Wrapper function for creating pagination keyboard depending on the current page.
#
#         Args:
#         page_num (int): The number of the current page.
#
#         Returns:
#             InlineKeyboardMarkup: Pagination keyboard object.
#
#         This function creates a pagination keyboard, adapting it based on the current page of the book.
#         If the current page is the first, it provides only a button to go forward.
#         If the current page is not the last, it provides buttons for both backward and forward navigation.
#         If the current page is the last, it provides only a button to go backward.
#     """
#     # Создаем строку для средней кнопки, содержащей информацию о текущей странице и общем количестве страниц
#     middle_button = f'{page_num}/{len(book)}'
#
#     # Если текущая страница - первая, возвращаем клавиатуру только с кнопкой "Вперед"
#     if page_num == 1:
#         return create_pagination_keyboard(middle_button, 'forward')
#
#     # Если текущая страница не последняя, возвращаем клавиатуру с кнопками "Назад" и "Вперед"
#     elif page_num < len(book):
#         return create_pagination_keyboard('backward', middle_button, 'forward')
#
#     # Если текущая страница - последняя, возвращаем клавиатуру только с кнопкой "Назад"
#     else:
#         return create_pagination_keyboard('backward', middle_button)
