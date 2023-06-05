Транскрибация текста из аудиофайла

В библиотеке `whisper` доступны различные модели для транскрибации речи. Вот краткое описание каждой модели:

1. Tiny: Модель с небольшим размером, обеспечивает базовую функциональность распознавания речи. Хотя она может иметь 
   ограниченные возможности в точности и покрытии, она является легковесным вариантом для простых задач транскрибации.

2. Base: Базовая модель для распознавания речи. Эта модель обладает хорошей точностью и обширным покрытием языковых 
   данных. Она может быть использована для широкого спектра задач транскрибации и обеспечивает хорошие результаты.

3. Small: Модель среднего размера, которая обеспечивает баланс между точностью и производительностью. Она может быть 
   полезна, когда требуется достаточная точность, но при этом нужно управлять потреблением ресурсов.

4. Medium: Средняя модель для распознавания речи, обладающая улучшенной точностью и покрытием по сравнению с более 
   легкими моделями. Эта модель может быть полезна в более требовательных сценариях транскрибации, где требуется высокая
   точность приемлемой производительности.

5. Large: Крупная модель с высокой точностью и обширным покрытием данных. Она предлагает наилучшие результаты для задач 
   транскрибации, но может потребовать больше ресурсов для работы.

При выборе модели следует учитывать баланс между точностью и производительностью, а также требованиями конкретной 
задачи транскрибации.

Что бы убрать предупреждение 
"transcription_of_text_from_an_audio_file/venv/lib/python3.11/site-packages/whisper/timing.py:57: NumbaDeprecationWarning: 
The 'nopython' keyword argument was not supplied to the 'numba.jit' decorator. The implicit default value for this 
argument is currently False, but it will be changed to True in Numba 0.59.0. See https://numba.readthedocs.io/en/stable/
reference/deprecation.html#deprecation-of-object-mode-fall-back-behaviour-when-using-jit for details.
  @numba.jit"

Вам потребуется изменить файл timing.py в директории .../transcription_of_text_from_an_audio_file/venv/lib/python3.11/
site-packages/whisper/. Найдите строку, содержащую декоратор @numba.jit в файле timing.py, и добавьте аргумент 
nopython=True в декоратор, чтобы выглядело так:

```python
@numba.jit(nopython=True)
def get_timing_map(...)
```
Сохраните изменения в файле timing.py. После этого предупреждение о NumbaDeprecationWarning не должно больше появляться 
при запуске кода.

Что бы убрать предупреждение 
".../transcription_of_text_from_an_audio_file/venv/lib/python3.11/site-packages/whisper/transcribe.py:114: UserWarning: 
FP16 is not supported on CPU; using FP32 instead
warnings.warn("FP16 is not supported on CPU; using FP32 instead")"

строку 
result = speech_model.transcribe("data/Рингтон - Зачем мне солнце Монако.mp3") 
заменить на 
result = speech_model.transcribe("data/Рингтон - Зачем мне солнце Монако.mp3", fp16=False)