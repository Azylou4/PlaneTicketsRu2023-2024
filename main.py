import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

# Чтение данных из файла
with open('biddata', 'r', encoding='utf-8') as file:
    data = file.read()

# Обновленное регулярное выражение для парсинга данных
pattern = r'([\w\s]+ - [\w\s]+) за (\d+₽) в (\w+ \w+), вылеты (\d{2} \w+), рейсы (\w+), с (\w+)'
matches = re.findall(pattern, data)

# Создание DataFrame
df = pd.DataFrame(matches, columns=['Маршрут', 'Цена', 'Тип билета', 'Дата вылета', 'Тип рейса', 'Багаж'])

# Удаление символов \n и лишних пробелов из столбца "Маршрут"
df['Маршрут'] = df['Маршрут'].str.strip()

# Преобразуем колонку с ценами в числовой формат
df['Цена (рубли)'] = df['Цена'].str.replace('₽', '').astype(int)

# Разбиваем маршруты на "Город отправления" и "Город назначения"
df[['Город отправления', 'Город назначения']] = df['Маршрут'].str.split(' - ', expand=True)

# Функция для очистки названий городов от лишних символов
def clean_city_name(city):
    return re.sub(r'[^а-яА-Яa-zA-Z\s]', '', city).strip()

# Применяем очистку к городам отправления и назначения
df['Город отправления'] = df['Город отправления'].apply(clean_city_name)
df['Город назначения'] = df['Город назначения'].apply(clean_city_name)

# Группируем по городу отправления и вычисляем среднюю цену
average_price_by_departure = df.groupby('Город отправления')['Цена (рубли)'].mean().reset_index()

# Сортируем города по средней цене
average_price_by_departure_sorted = average_price_by_departure.sort_values(by='Цена (рубли)', ascending=True)

# Выводим результат
print(average_price_by_departure_sorted)

# Визуализируем средние цены по городам отправления
plt.figure(figsize=(10,6))
plt.barh(average_price_by_departure_sorted['Город отправления'], average_price_by_departure_sorted['Цена (рубли)'], color='lightgreen')
plt.xlabel('Средняя цена (рубли)')
plt.ylabel('Город отправления')
plt.title('Средние цены на билеты по городам отправления')
plt.show()
