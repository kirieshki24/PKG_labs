# Документация разработчика

## Наименование программы

**3D Letter Visualizer** — приложение на Python для визуализации и трансформации 3D модели буквы с поддержкой масштабирования, перемещения и вращения в реальном времени.

---

## Назначение программы

Приложение позволяет:
- Отобразить **3D модель буквы** в виде каркасного представления.
- Применять трансформации в реальном времени:
  - **Масштабирование**
  - **Перемещение** по осям X, Y и Z
  - **Вращение** вокруг осей X, Y и Z
- Отображать матрицу преобразований, которая применяется к модели.

---

## Функциональные возможности

### Основные функции
1. **3D Визуализация**:
   - Отображение 3D модели буквы.
   - Представление модели в виде нескольких проекций:
     - **3D проекция**
     - **Проекция на плоскость XY**
     - **Проекция на плоскость XZ**
     - **Проекция на плоскость YZ**

2. **Трансформации**:
   - **Масштабирование**: Изменение размера модели.
   - **Перемещение**: Сдвиг модели вдоль осей X, Y и Z.
   - **Вращение**: Поворот модели вокруг осей X, Y и Z (в градусах).

3. **Матрица преобразований**:
   - Отображение текущей матрицы 4x4 после применения всех преобразований.

---

## Обзор программы

### Управление и интерфейс
Графический интерфейс включает:
- **Слайдеры**:
  - **Масштабирование**: Диапазон от 0.1 до 2.0.
  - **Перемещение**: Слайдеры для каждой оси (X, Y, Z) с диапазоном от -5 до 5.
  - **Вращение**: Слайдеры для каждой оси (X, Y, Z) с диапазоном от 0° до 360°.
- **Матрица преобразований**:
  - Динамическое отображение текущей матрицы после изменений.
- **Окно визуализации**:
  - Включает 3D проекцию и 2D проекции модели.

---

## Структура кода

### Используемые библиотеки
- `customtkinter`: Создание современного графического интерфейса.
- `numpy`: Математические вычисления и преобразования.
- `matplotlib`: Отображение 3D и 2D графиков.

### Основные компоненты

1. **Класс `Letter3DApp`**:
   - Создаёт интерфейс и инициализирует 3D модель.
   - Содержит вершины и рёбра, описывающие букву.

2. **Трансформации**:
   - **Масштабирование**: Изменяет размеры модели пропорционально.
   - **Перемещение**: Сдвигает модель по трём осям.
   - **Вращение**: Применяет матрицы поворота вокруг осей X, Y и Z.

3. **Визуализация**:
   - Использует библиотеку `matplotlib` для отображения:
     - 3D представления модели.
     - 2D проекций на плоскости XY, XZ и YZ.

4. **Обработка событий**:
   - При изменении значений слайдеров обновляются матрица преобразований и визуализация.

---

## Установка и запуск

### Системные требования
- **Python** версии 3.11
- **Необходимые библиотеки**:
  - `customtkinter`
  - `numpy`
  - `matplotlib`

---

### Инструкция по запуску

1. **Скачайте исходный код**:
   - Извлеките ZIP-архив с файлами.

2. **Установите Python**:
   - Убедитесь, что Python 3.11 установлен на вашем компьютере.
   - Скачайте Python с официального сайта: [python.org](https://www.python.org).

3. **Настройте окружение и запустите программу**:
   Откройте командную строку (Windows) и выполните следующие команды:

   ```bash
   chdir ...\letter3Dprojection  # Укажите путь к директории с файлом main.py
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python main.py
   ```

4. **Запуск программы**:
   - После выполнения команд приложение откроет графический интерфейс.

---

## Детали модели

### Вершины и рёбра
- **Вершины**:
   - Модель состоит из точек в 3D пространстве, определённых в массиве NumPy.
- **Рёбра**:
   - Линии, соединяющие вершины, для создания каркасного представления.

### Преобразования
- Преобразования выполняются последовательно:
  1. Масштабирование
  2. Вращение вокруг осей X, Y и Z
  3. Перемещение по осям X, Y и Z
- Итоговая матрица преобразований объединяет все операции и применяется к вершинам модели.

---

## Возможные улучшения
- Добавить возможность загружать пользовательские 3D модели.
- Реализовать перспективные преобразования для более реалистичного отображения.
- Внедрить поддержку дополнительных типов преобразований (сдвиги, искажения).
