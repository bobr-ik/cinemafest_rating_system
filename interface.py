import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os


os.makedirs('графики', exist_ok=True)

# Вариант 1: Столбчатая диаграмма средних оценок по категориям для каждого фильма
def plot_average_scores(data):
    fig, ax = plt.subplots(figsize=(12, 8))
    
    categories = list(list(data.values())[0].keys())
    films = list(data.keys())
    
    # Вычисляем средние оценки для каждого фильма по категориям
    averages = {}
    for film in films:
        averages[film] = []
        for category in categories:
            scores = [rate['value'] for rate in data[film][category]]
            avg_score = sum(scores) / len(scores)
            averages[film].append(avg_score)
    
    # Настройки для группированных столбцов
    x = np.arange(len(categories))
    width =  1/ (1 +len(data))
    
   # Создаем столбцы для каждого фильма
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#96CEB4', '#FFEAA7']  # Добавляем больше цветов на случай большего количества фильмов
    bars = []

    for i, (film_name, film_avg) in enumerate(averages.items()):
        offset = width * (i - (len(averages) - 1) / 2)  # Центрируем столбцы
        bar = ax.bar(x + offset, film_avg, width, label=film_name, alpha=0.8, color=colors[i % len(colors)])
        bars.append(bar)

    # Настройка внешнего вида
    ax.set_xlabel('Категории оценки')
    ax.set_ylabel('Средняя оценка')
    ax.set_title('Сравнение средних оценок фильмов по категориям')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Добавляем значения на столбцы
    for bar_group in bars:
        for bar in bar_group:
            height = bar.get_height()
            ax.annotate(f'{height:.1f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('графики/столбчатая_диаграмма_средних_оценок.png')

# Вариант 2: Радарная диаграмма для сравнения фильмов
def plot_radar_chart(data):
    categories = list(list(data.values())[0].keys())
    N = len(categories)
    films = list(data.keys())
    
    # Цвета для разных фильмов
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#96CEB4', '#FFEAA7']
    
    # Углы для радарной диаграммы
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Замыкаем круг
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Рисуем графики для каждого фильма
    for i, film in enumerate(films):
        # Вычисляем средние оценки для текущего фильма
        avg_scores = []
        for category in categories:
            scores = [rate['value'] for rate in data[film][category]]
            avg_score = sum(scores) / len(scores)
            avg_scores.append(avg_score)
        
        # Замыкаем круг для радарной диаграммы
        avg_scores += avg_scores[:1]
        
        # Рисуем график
        ax.plot(angles, avg_scores, 'o-', linewidth=2, label=film, color=colors[i % len(colors)])
        ax.fill(angles, avg_scores, alpha=0.25, color=colors[i % len(colors)])
    
    # Настройка внешнего вида
    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 10)
    ax.set_title('Сравнение фильмов по категориям оценок', size=15, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    plt.tight_layout()
    plt.savefig('графики/радарная_диаграмма.png', dpi=300, bbox_inches='tight')
    plt.close()
# Функция для расчета общей средней оценки фильма
def calculate_overall_average(film_data):
    all_scores = []
    for category in film_data:
        for rate in film_data[category]:
            all_scores.append(rate['value'])
    return sum(all_scores) / len(all_scores) if all_scores else 0

# Вариант 4: График средней оценки по всему фильму
def plot_overall_average_scores(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    films = list(data.keys())
    overall_averages = [calculate_overall_average(data[film]) for film in films]
    
    # Цвета для столбцов
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#F9A602', '#96CEB4', '#FFEAA7']
    
    # Создаем столбцы
    bars = ax.bar(films, overall_averages, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    
    # Настройка внешнего вида
    ax.set_xlabel('Фильмы')
    ax.set_ylabel('Средняя оценка')
    ax.set_title('Общая средняя оценка фильмов', fontsize=16, pad=20)
    ax.set_ylim(0, 10)
    
    # Добавляем сетку
    ax.grid(True, alpha=0.3, axis='y')
    
    # Добавляем значения на столбцы
    for bar, value in zip(bars, overall_averages):
        height = bar.get_height()
        ax.annotate(f'{value:.2f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom',
                   fontsize=12, fontweight='bold')
    
    # Добавляем горизонтальную линию для среднего значения
    avg_all = sum(overall_averages) / len(overall_averages)
    ax.axhline(y=avg_all, color='red', linestyle='--', alpha=0.7, 
               label=f'Среднее по всем фильмам: {avg_all:.2f}')
    
    ax.legend()
    plt.tight_layout()
    plt.savefig('графики/общая_средняя_оценка.png')
    
    # Выводим числовые значения
    print("Общие средние оценки:")
    for film, avg in zip(films, overall_averages):
        print(f"{film}: {avg:.2f}")

# Вариант 5: Круговые диаграммы для каждого фильма
def plot_pie_charts_comparison(data):
    films = list(data.keys())
    categories = list(list(data.values())[0].keys())
    colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FF99CC', '#C9A0DC']
    
    # Определяем количество строк и столбцов (максимум 2 в строке)
    n_films = len(films)
    n_cols = min(2, n_films)  # Максимум 2 столбца
    n_rows = (n_films + n_cols - 1) // n_cols  # Округление вверх
    
    # Создаем сетку подграфиков
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 5 * n_rows))
    
    # Преобразуем axes в плоский массив для удобства
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    
    # Для каждого фильма
    for i, film in enumerate(films):
        ax = axes[i]
        
        # Вычисляем средние оценки для текущего фильма
        film_avgs = []
        for category in categories:
            scores = [rate['value'] for rate in data[film][category]]
            film_avgs.append(sum(scores) / len(scores))
        
        # Создаем круговую диаграмму
        wedges, texts, autotexts = ax.pie(film_avgs, labels=categories, colors=colors,
                                         autopct='%1.1f%%', startangle=90)
        ax.set_title(f'{film}', fontsize=14, pad=20)
        
        # Делаем центр круга пустым для лучшего вида
        centre_circle = plt.Circle((0,0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Настраиваем внешний вид текста
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
    
    # Скрываем пустые subplots, если они есть
    for i in range(len(films), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('графики/круговые_диаграммы.png', dpi=300, bbox_inches='tight')
    plt.close()



def generate_md_report_with_graphs():
    """
    Генерирует MD-файл со всеми созданными графиками
    """
    md_content = """# 📊 Визуализация оценок фильмов

## 📈 Графики анализа оценок

Ниже представлены все созданные графики для визуального анализа оценок фильмов.

### 1. Средние оценки по категориям
![Средние оценки по категориям](графики/столбчатая_диаграмма_средних_оценок.png)

*Сравнение средних оценок двух фильмов по различным категориям*

---

### 2. Радарная диаграмма сравнения
![Радарная диаграмма](графики/радарная_диаграмма.png)

*Визуальное сравнение сильных и слабых сторон фильмов*

---

### 3. Общая средняя оценка фильмов
![Общая средняя оценка](графики/общая_средняя_оценка.png)

*Сравнение итоговых средних оценок по всем фильмам*

---

### 4. Распределение оценок по категориям
![Круговые диаграммы](графики/круговые_диаграммы.png)

*Процентное распределение средних оценок по категориям для каждого фильма*

---

## 📋 Информация о графиках

Все графики созданы с помощью:
- **Python** с библиотеками matplotlib и numpy
- **Разрешение:** 300 DPI (высокое качество)
- **Формат:** PNG
- **Размеры:** адаптированы для лучшей читаемости

Графики сохранены в папке `графики/` в текущей директории.
"""

    # Сохраняем MD-файл
    with open('отчет_с_графиками.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("MD-файл с графиками создан: 'отчет_с_графиками.md'")
