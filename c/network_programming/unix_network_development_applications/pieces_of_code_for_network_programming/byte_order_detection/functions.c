//
// Created by Shrekulka on 25.10.2023.
//
#include "functions.h"

// Функция для получения информации о операционной системе и процессоре.
const char* get_os_and_cpu_info()
{
	// Выделение памяти для хранения информации о системе и процессоре.
	char* info = (char*)malloc(INFO_SIZE);
	if (info == NULL)
	{
		perror("Error allocating memory for info");
		exit(EXIT_FAILURE);
	}
	// Установка всех байтов в буфере info в ноль.
	memset(info, 0, INFO_SIZE);

#ifdef __linux__
	// Определяем структуру utsname с именем buf, которая используется для получения информации о системе, такой как имя
	// ядра, версия и другие атрибуты.
	struct utsname buf;
	// Вызывается функция uname(&buf), которая заполняет структуру buf данными об операционной системе. Если функция
	// завершится с ошибкой, макрос CHECK_ERR будет использоваться для обработки ошибки.
	CHECK_ERR(uname(&buf), "Error getting OS info");
	// Форматируем и сохраняем информацию в буфер.
	snprintf(info, INFO_SIZE, "OS: %s, Vendor: %s", buf.sysname, get_cpu_vendor_id());
#endif

#ifdef _WIN32
	// Создаем структуру OSVERSIONINFOEX для получения информации о версии Windows.
	OSVERSIONINFOEX osvi;

	// Определяем размер структуры в байтах.
	osvi.dwOSVersionInfoSize = sizeof(OSVERSIONINFOEX);

	// Пытаемся получить информацию о версии Windows с использованием функции GetVersionEx.
	if (GetVersionEx((OSVERSIONINFO*)&osvi))

		// Определяем указатель на строку, в которой будет храниться название операционной системы.
		const char* os_name;

		// Проверяем тип платформы Windows.
		if (osvi.dwPlatformId == VER_PLATFORM_WIN32_NT)
		{
			// Если платформа - Windows NT, определяем версию.
			if (osvi.dwMajorVersion == 10)
			{
				os_name = "Windows 10";
			}
			else if (osvi.dwMajorVersion == 11)
			{
				os_name = "Windows 11";
			}
			else if (osvi.dwMajorVersion == 6 && osvi.dwMinorVersion == 1)
			{
				os_name = "Windows 7";
			}
			else
			{
				os_name = "Unknown";
			}
		}
		else if (osvi.dwPlatformId == VER_PLATFORM_WIN32_WINDOWS)
		{
			// Если платформа - Windows 9x/ME.
			os_name = "Windows 9x/ME";
		}
		else
		{
			os_name = "Unknown";
		}

		// Форматируем и сохраняем информацию о системе и производителе процессора в буфер.
		snprintf(info, INFO_SIZE, "OS: %s, Vendor: %s", os_name, get_cpu_vendor_id());
	}
	else
	{
		fprintf(stderr, "Error getting Windows version");
	}
#endif


#ifdef __APPLE__
	// Объявляется переменная len типа size_t, которая устанавливается в размер буфера INFO_SIZE. Эта переменная будет
	// использоваться для определения размера данных, которые могут быть прочитаны или записаны.
	size_t len = INFO_SIZE;
	// sysctlbyname - это функция для получения информации о системе. Если функция выполняется успешно (возвращает 0),
	// то выполнится код внутри этого блока.
	if (sysctlbyname("kern.ostype", info, &len, NULL, 0) == 0)
	{
		// Выделяется память размером INFO_SIZE. Эта память будет использоваться для хранения информации о модели
		// процессора.
		char* model = (char*)malloc(INFO_SIZE);
		// Эта строка кода использует функцию perror для вывода сообщения об ошибке, связанной с выделением памяти для model.
		if (model == NULL)
		{
			perror("Error allocating memory for model");
			exit(EXIT_FAILURE);
		}
		// Создание переменной model_len типа size_t и установка ее значения в INFO_SIZE. Эта переменная будет
		// использоваться для указания размера данных, которые могут быть прочитаны или записаны в буфер model.
		size_t model_len = INFO_SIZE;
		// Эта функция используется для получения информации о модели процессора на macOS. Если функция выполняется
		// успешно (возвращает 0), код внутри этого блока будет выполнен.
		if (sysctlbyname("machdep.cpu.brand_string", model, &model_len, NULL, 0) == 0)
		{
			strcat(info, ", Vendor: "); // информация будет о производителе процессора.
			strcat(info, model);        // информация о системе и производителе процессора
		}
		else
		{
			fprintf(stderr, "Error getting CPU model info");
		}
		free(model);
	}
	else
	{
		fprintf(stderr, "Error getting OS info");
	}
#endif

	// info - Этот буфер используется для хранения информации о системе и процессоре. Он выделяется в функции
	// get_os_and_cpu_info с использованием malloc и размером INFO_SIZE. Далее, этот буфер заполняется информацией о
	// операционной системе и производителе процессора, и результат будет возвращен из функции.
	return info;
}

// Функция для получения идентификатора производителя процессора.
const char* get_cpu_vendor_id()
{
	// Выделение памяти для хранения идентификатора производителя процессора.
	char* vendor = (char*)malloc(VENDOR_ID_SIZE);
	if (vendor == NULL)
	{
		perror("Error allocating memory for CPU vendor");
		exit(EXIT_FAILURE);
	}

#ifdef __linux__
	// Если код выполняется на Linux, получаем идентификатор производителя с использованием функции __get_cpuid.
	unsigned int eax, ebx, ecx, edx;

	// __get_cpuid - это функция, которая обычно используется для получения информации о процессоре. Она принимает
	// несколько аргументов, включая 4 регистра (eax, ebx, ecx и edx), которые будут заполнены данными о процессоре. В
	// данном случае, мы вызываем функцию с параметром 0, что означает запрос информации о производителе процессора.
	// __get_cpuid(0, &eax, &ebx, &ecx, &edx) - Эта инструкция вызывает функцию __get_cpuid, передавая в нее 0 в качестве
	// параметра запроса информации о производителе процессора. Регистры eax, ebx, ecx и edx передаются по ссылке, так
	// что функция будет заполнять их данными.
	// != 0 - Это сравнение проверяет, вернула ли функция __get_cpuid значение, отличное от нуля. Если функция успешно
	// выполняется и возвращает информацию о производителе процессора, она обычно возвращает ненулевое значение.
	if (__get_cpuid(0, &eax, &ebx, &ecx, &edx) != 0)
	{
		// Копируем данные в буфер.
		memcpy(vendor, &ebx, 4);
		memcpy(vendor + 4, &edx, 4);
		memcpy(vendor + 8, &ecx, 4);
		vendor[12] = '\0';
	}
	else
	{
		fprintf(stderr, "Error getting CPU vendor info on Linux");
	}
#endif

#ifdef _WIN32
	// Если код выполняется на Windows, получаем идентификатор производителя с использованием функции __cpuid.
	// Этот массив будет использоваться для хранения информации о процессоре, которую получит функция __cpuid.
	int cpuInfo[4] = { 0 };

	// Эта строка вызывает функцию __cpuid, передавая ей массив cpuInfo и параметр 0. Функция __cpuid предназначена для
	// выполнения CPUID-инструкции, которая используется для получения информации о процессоре на платформе x86 (и
	// совместимых). Параметр 0 указывает, что мы хотим получить информацию о процессоре для основного уровня (например,
	// базовая информация о процессоре).
	__cpuid(cpuInfo, 0);
	// Копируем данные в буфер.
	memcpy(vendor, &cpuInfo[1], 4);
	memcpy(vendor + 4, &cpuInfo[3], 4);
	memcpy(vendor + 8, &cpuInfo[2], 4);
	vendor[12] = '\0';
#endif

	// vendor - Этот буфер используется для хранения идентификатора производителя процессора. Он выделяется в функции
	// get_cpu_vendor_id с использованием malloc и размером VENDOR_ID_SIZE. Этот буфер заполняется идентификатором
	// производителя процессора, который затем будет использован для определения производителя процессора в общей
	// информации о системе и процессоре.
	return vendor;
}