class DiskNotFoundError(Exception):
    """
    Исключение, возникающее, если файл диска не найден.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Disk file not found. Creating a new disk."
    """

    def __init__(self, message: str = "Disk file not found. Creating a new disk.") -> None:
        """
        Инициализирует объект исключения DiskNotFoundError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Disk file not found. Creating a new disk."
        """
        self.message = message
        super().__init__(self.message)


class UnknownDiskFormatError(Exception):
    """
    Исключение, возникающее, если формат диска не распознан.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Unknown disk format."
    """

    def __init__(self, message: str = "Unknown disk format") -> None:
        """
        Инициализирует объект исключения UnknownDiskFormatError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Unknown disk format."
        """
        self.message = message
        super().__init__(self.message)


class DirectoryNotFoundError(Exception):
    """
    Исключение, возникающее, если директория не найдена.

    Args:
        directory_path (str): Путь к директории, которая не существует.
    """

    def __init__(self, directory_path: str) -> None:
        """
        Инициализирует объект исключения DirectoryNotFoundError.

        Args:
            directory_path (str): Путь к директории, которая не существует.
        """
        self.message = f"Directory '{directory_path}' does not exist."
        super().__init__(self.message)


class InvalidNameError(Exception):
    """
    Исключение, возникающее, если имя файла или директории недопустимо.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Invalid characters in name."
    """

    def __init__(self, message: str = "Invalid characters in name.") -> None:
        """
        Инициализирует объект исключения InvalidNameError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Invalid characters in name."
        """
        self.message = message
        super().__init__(self.message)


class RootDirectoryFullError(Exception):
    """
    Исключение, возникающее, если корневая директория переполнена.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Root directory is full."
    """

    def __init__(self, message: str = "Root directory is full.") -> None:
        """
        Инициализирует объект исключения RootDirectoryFullError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Root directory is full."
        """
        self.message = message
        super().__init__(self.message)


class FatLoadError(Exception):
    """
    Исключение, возникающее при ошибке загрузки данных FAT.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Failed to load FAT data."
    """

    def __init__(self, message: str = "Failed to load FAT data.") -> None:
        """
        Инициализирует объект исключения FatLoadError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Failed to load FAT data."
        """
        self.message = message
        super().__init__(self.message)


class FileAllocationError(Exception):
    """
    Исключение, возникающее при ошибке выделения сектора для файла.

    Args:
        message (str, optional): Сообщение об ошибке. По умолчанию "Failed to allocate sector for file."
    """

    def __init__(self, message: str = "Failed to allocate sector for file.") -> None:
        """
        Инициализирует объект исключения FileAllocationError.

        Args:
            message (str, optional): Сообщение об ошибке. По умолчанию "Failed to allocate sector for file."
        """
        self.message = message
        super().__init__(self.message)
