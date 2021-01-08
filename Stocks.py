import csv

filename = "YNDX_160101_161231.csv"
date = []
time = []
high_prices = []
low_prices = []

request = int(input("Введите уровень сложности задания,\
 которое хотите проверить: "))

if request == 1:
    with open(filename, 'r') as file:
        data = csv.reader(file)
        for row in data:
            date.append(row[0])
            time.append(row[1])
            high_prices.append(row[3])
            low_prices.append(row[4])

    print("Описание алгоритма:\n")

    low_prices = list(map(float, low_prices[1:]))
    high_prices = list(map(float, high_prices[1:]))

    # для начала находим первый минимум для покупки акции,
    # а уже после находим максимум для продажи
    min_low = low_prices.index(min(low_prices))

    max_high = high_prices[min_low:].index(max(high_prices[min_low:])) + min_low

    d_buy = date[min_low+1][:4] + '.' + date[min_low+1][4:6] + '.' + date[min_low+1][6:]
    d_sell = date[max_high+1][:4] + '.' + date[max_high+1][4:6] + '.' + date[max_high+1][6:]

    print('День покупки:', d_buy, min_low+1)
    print('День продажи:', d_sell, max_high+1)
