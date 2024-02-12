# simple_echo_bot/utils/client_utils.py

from aiogram.types import Message


async def get_invoice_data(message: Message) -> dict:
    """
        Get invoice data from the message.

        Args:
            message (Message): Incoming message object.

        Returns:
            dict: Invoice data.
    """
    # Получаем объект счета
    invoice = message.invoice
    # Извлекаем заголовок счета
    invoice_title = invoice.title
    # Извлекаем общую сумму счета
    total_amount = invoice.total_amount
    return {"title": invoice_title, "total_amount": total_amount}


async def get_passport_data(message: Message) -> dict:
    """
        Get passport data from the message.

        Args:
            message (Message): Incoming message object.

        Returns:
            dict: Passport data.
    """
    # Получаем объект данных паспорта
    passport_data = message.passport_data
    # Извлекаем номер паспорта
    passport_number = passport_data.passport_number
    # Извлекаем дату истечения срока действия паспорта
    expiry_date = passport_data.expiry_date
    return {"passport_number": passport_number, "expiry_date": expiry_date}


async def get_successful_payment_data(message: Message) -> dict:
    """
        Get successful payment data from the message.

        Args:
            message (Message): Incoming message object.

        Returns:
            dict: Successful payment data.
    """
    # Получаем объект данных об успешной оплате
    successful_payment = message.successful_payment
    # Извлекаем валюту оплаты
    currency = successful_payment.currency
    # Извлекаем общую сумму оплаты
    total_amount = successful_payment.total_amount
    return {"currency": currency, "total_amount": total_amount}
