# Документация разработчика

## Название программы

**AlgorithmClippingVisualizer** — приложение для визуализации алгоритмов отсечения отрезков на плоскости с использованием алгоритмов **Коэна-Сазерленда** и **Сайруса-Бека**. Графический интерфейс построен с использованием библиотеки **CustomTkinter**.

---

## Назначение программы

Приложение позволяет:
- Читать входные данные из текстового файла, содержащего описание отрезков и параметров отсечения.
- Выполнять отсечение отрезков с использованием:
  - **Алгоритма Коэна-Сазерленда** (отсекание в прямоугольном окне).
  - **Алгоритма Сайруса-Бека** (отсекание в многоугольнике произвольной формы).
- Визуализировать исходные отрезки, отсечённые отрезки и область отсечения.

---

## Основные возможности

1. **Поддержка двух алгоритмов отсечения**:
   - **Коэна-Сазерленда** — отсечение отрезков в прямоугольном окне.
   - **Сайруса-Бека** — отсечение отрезков в многоугольнике.

2. **Визуализация**:
   - Исходные отрезки отображаются **синими пунктирными линиями**.
   - Отсечённые отрезки отображаются **зелёными сплошными линиями**.
   - Область отсечения (прямоугольник или многоугольник) выделяется **красным контуром**.

3. **Удобный интерфейс**:
   - Возможность выбора входного файла через диалоговое окно.
   - Обработка ошибок при неверном формате данных.

---

## Формат входного файла

### Для алгоритма Коэна-Сазерленда
```plaintext
1                   # Тип алгоритма (1 - Коэна-Сазерленда)
N                   # Количество отрезков
x1 y1 x2 y2         # Координаты отрезков (N строк)
xmin ymin xmax ymax  # Координаты прямоугольного окна
```

### Для алгоритма Сайруса-Бека
```plaintext
2                   # Тип алгоритма (2 - Сайруса-Бека)
1               
x1 y1 x2 y2         # Координаты одного отрезка
M                   # Количество вершин многоугольника
x1 y1               # Координаты каждой вершины многоугольника (M строк)
```

---

## Структура кода

### Основные модули и функции

1. **Чтение данных из файла**:
   - `read_file(file_path)`:
     - Читает файл, разбирает данные и возвращает их для дальнейшей обработки.

2. **Алгоритмы отсечения**:
   - `cohen_sutherland_clip(line, window)`:
     - Реализует алгоритм Коэна-Сазерленда для отсечения отрезков прямоугольным окном.
   - `cyrus_beck_clip(line, clip_polygon)`:
     - Реализует алгоритм Сайруса-Бека для отсечения отрезков многоугольником.

3. **Визуализация**:
   - `visualize(algorithm_type, segments, clipping_window, clipping_polygon, clipped_segments, canvas_frame)`:
     - Отображает исходные отрезки, отсечённые отрезки и область отсечения на графике.

4. **Логика интерфейса**:
   - `main_application()`:
     - Основной цикл программы. Реализует графический интерфейс и обработку файлов.

---

## Графический интерфейс

1. **Главное окно**:
   - Заголовок: "Визуализация Алгоритмов Отсечения".
   - Размер: 800x600 пикселей.

2. **Элементы управления**:
   - **Кнопка "Выбрать Входной Файл"**:
     - Открывает диалоговое окно для выбора файла.
   - **Метка состояния**:
     - Отображает путь к выбранному файлу.

3. **Область визуализации**:
   - Отображает график с исходными отрезками, отсечёнными отрезками и областью отсечения.

---

## Требования к системе

### Версия Python
- Python **3.11** или выше.

### Необходимые библиотеки
Установите зависимости через файл `requirements.txt`:
```plaintext
customtkinter
matplotlib
numpy
```

---

## Инструкция по запуску

### Шаги для запуска программы

1. **Скачайте и распакуйте код**:
   - Скачайте архив с исходным кодом и извлеките его содержимое.

2. **Установите Python**:
   - Убедитесь, что установлен Python версии **3.11**. Скачать можно с официального сайта [python.org](https://www.python.org).

3. **Настройте окружение и запустите программу**:
   В командной строке выполните следующие команды:

   ```bash
   chdir ...\dev_documentation   # Замените троеточие на путь к папке с файлом main.py
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

4. **Выберите входной файл**:
   - В открывшемся приложении нажмите на кнопку **"Выбрать Входной Файл"** и укажите файл с входными данными.

---

## Основные файлы

- **main.py**:
   - Основной файл программы, содержащий логику GUI, алгоритмы и визуализацию.

---

## Потенциальные улучшения

1. Добавление поддержки других алгоритмов отсечения (например, **Ляна-Барски**).
2. Реализация сохранения результатов отсечения в новый файл.
3. Улучшение пользовательского интерфейса с возможностью интерактивного выбора алгоритма.