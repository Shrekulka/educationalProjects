# auto_ria_tracker/utils/proxy_manager.py

from typing import List


class ProxyManager:
    """
    A utility class for managing and rotating proxy servers.

    This class provides a simple round-robin mechanism for cycling through
    a list of proxy servers, ensuring distributed load and potential
    IP address rotation.

    Attributes:
        proxies (List[str]): A list of proxy server URLs or IP addresses
        current_index (int): Current position in the proxy list for rotation
    """
    def __init__(self, proxies: List[str]) -> None:
        """
        Initialize the ProxyManager with a list of proxy servers.

        Args:
           proxies (List[str]): List of proxy server URLs or IP addresses

        Raises:
           ValueError: If the provided proxies list is empty
        """
        # Проверяем, что список прокси не пустой
        if not proxies:
            raise ValueError("Proxy list cannot be empty")

        # Сохраняем список прокси-серверов
        self.proxies = proxies

        # Инициализируем начальный индекс для круговой выборки  =
        self.current_index = 0

    def get_next_proxy(self) -> str:
        """
        Retrieve the next proxy from the list using round-robin selection.

        Returns:
           str: The next proxy server URL/IP

        Notes:
           - Automatically cycles through the entire list of proxies
           - Ensures even distribution of proxy usage
        """
        # Получаем текущий прокси из списка
        proxy = self.proxies[self.current_index]

        # Обновляем индекс с круговым переходом (модуль длины списка)
        self.current_index = (self.current_index + 1) % len(self.proxies)

        return proxy
