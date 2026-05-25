**Description:**
This is a small utility for gathering system information and determining endianness.

**Main Objectives:**
1. Retrieve information about the operating system and the CPU.
2. Determine the endianness (byte order) of the system.

**Tasks:**
1. Identify the operating system's name, version, and architecture.
2. Obtain the CPU manufacturer's identifier.
3. Check the byte order of the system (big-endian or little-endian).

**Project Structure:**
1. `common.h` - Common includes and definitions.
2. `config.h` - Constants.
3. `utils.h` - Utility macros.
4. `functions.h` - Function declarations.
5. `os_specific.h` - Platform-specific code.
6. `functions.c` - Function implementations.
7. `main.c` - Core program logic.

**Sample Program Output:**
```
CPU_VENDOR_OS: Darwin, Vendor: Apple M1
little-endian

Process finished with exit code 0
```




**Это небольшая утилита для определения информации о системе и порядка байт.**

**Основное назначение:**
1. Получение информации об операционной системе и процессоре
2. Определение порядка байт (endianess) на данной системе

**Задачи:**
1. Определить имя ОС, версию, архитектуру
2. Получить идентификатор производителя процессора
3. Проверить порядок байт на системе (big endian или little endian)

**Структура проекта:**
1. common.h - общие включения и определения;
2. config.h - константы;
3. utils.h - вспомогательные макросы;
4. functions.h - объявления функций;
5. os_specific.h - платформозависимый код;
6. functions.c - реализация функций;
7. main.c - основная логика программы.

Привер ввывода программы:
```
CPU_VENDOR_OS: Darwin, Vendor: Apple M1
little-endian

Process finished with exit code 0
```