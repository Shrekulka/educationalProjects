# ai_checklist_guardian/services/openai_service.py
import traceback

import openai
from openai.error import RateLimitError

from config import OPENAI_API_KEY
from logger import logger


class OpenAIService:
    """
        Class OpenAIService provides methods for interacting with the OpenAI API.

        Methods:

        __init__():
            Initializes the OpenAIService object using the OpenAI API key.

        analyze_report(report: str) -> str:
            Analyzes the provided report using the GPT-3.5-Turbo model. Returns the analysis text or an error string.

        get_ai_response(report: str) -> str:
            Sends the report to OpenAI and returns the text response from the GPT-3.5-Turbo model.
            In case of an error, returns an error message.

        preprocess_report(location: str, checklist: dict) -> str:
            Forms the report text based on location and checklist data.
            Returns the formatted report text.

        send_report(location: str, checklist: dict) -> str:
            Sends the report to OpenAI and returns the text response from the GPT-3.5-Turbo model.
            In case of an error, returns an error message.
    """

    def __init__(self):
        """
            Initializes the OpenAIService object using the OpenAI API key.
        """

        openai.api_key = OPENAI_API_KEY

    @staticmethod
    def analyze_report(report):
        """
            Analyzes the provided report using the GPT-3.5-Turbo model.

            Parameters:
            - report (str): The text of the report to analyze.

            Returns:
            - str: The text of the analysis or an error message.
        """

        try:
            # Формируем запрос для анализа
            prompt = f"Analyze the following report:\n{report}"
            # Выполняем запрос к модели GPT-3.5-Turbo
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["\n"]
            )
            # Получаем результат анализа
            result = response.choices[0].text.strip()
            logger.info("Analysis successful.")
            return result
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            logger.error(f"Error analyzing report: {e}\n{detailed_send_message_error}")
            return "Error analyzing report"

    def get_ai_response(self, report: str) -> str:
        """
            Sends a report to OpenAI and returns the response text from the GPT-3.5-Turbo model.

            Parameters:
            - report (str): The text of the report to be sent to OpenAI.

            Returns:
            - str: The response text from the GPT-3.5-Turbo model or an error message.
        """

        try:
            # Выполняем запрос к модели GPT-3.5-Turbo для получения ответа
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=report,
                max_tokens=100,
                temperature=0.5,
            )
            # Получаем текст ответа
            result = response.choices[0].text.strip()
            logger.info("AI response received successfully.")
            return result
        except RateLimitError as e:
            detailed_send_message_error = traceback.format_exc()
            logger.error(f"Rate limit exceeded. Waiting and retrying. Error: {e}\n{detailed_send_message_error}")
            # time.sleep(5)  # Пауза перед повторной попыткой (может потребоваться другое значение)
            # return self.get_ai_response(report)  # Повторяем запрос
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            logger.error(f"Error getting AI response: {e}\n{detailed_send_message_error}")
            return "Error getting AI response"

    def preprocess_report(self, location: str, checklist: dict) -> str:
        """
            Generates a report text based on location data and a checklist.

            Parameters:
            - location (str): The location to which the report pertains.
            - checklist (dict): A dictionary containing checklist data.

            Returns:
            - str: Formatted text of the report.
        """

        try:
            # Формируем текст отчета с использованием данных о локации и чек-листе
            report = f"Location: {location}\nChecklist: {checklist}\n"
            logger.info("Report text generated successfully.")
            return report
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            logger.error(f"Error when generating report text: {e}\n{detailed_send_message_error}")
            return "Error when generating report text."

    def send_report(self, location: str, checklist: dict) -> str:
        """
            Sends a report to AI and returns the response.

            Parameters:
            - location (str): The location to which the report pertains.
            - checklist (dict): A dictionary containing checklist data.

            Returns:
            - str: The response text from the GPT-3.5-Turbo model or an error message.
        """

        try:
            # Форматируем отчет
            formatted_report = self.preprocess_report(location, checklist)
            # Получаем ответ от OpenAI
            ai_response = self.get_ai_response(formatted_report)
            logger.info("Report sent to AI successfully.")
            return ai_response
        except Exception as e:
            detailed_send_message_error = traceback.format_exc()
            logger.error(f"Failed to send report to AI. Error: {e}\n{detailed_send_message_error}")
            return "An error occurred while sending the report. Please try again later."
