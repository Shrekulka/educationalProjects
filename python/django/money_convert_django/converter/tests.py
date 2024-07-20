from django.test import TestCase, Client
from django.urls import reverse
from .models import ConversionHistory


class CurrencyConverterTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_currency_converter_page_loads(self):
        response = self.client.get(reverse('money_convert'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'converter/currency_converter.html')

    def test_currency_conversion(self):
        data = {
            'from-amount': '100',
            'from-curr': 'USD',
            'to-curr': 'EUR'
        }
        response = self.client.post(reverse('money_convert'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Подсчитать монетки')

        # Проверка, что запись добавлена в историю
        self.assertEqual(ConversionHistory.objects.count(), 1)