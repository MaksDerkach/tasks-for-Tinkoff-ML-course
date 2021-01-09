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
    min_price, max_price = 0, 0
    min_ind, max_ind = 0, 0
    profit = max_price - min_price
    # для начала находим первый минимум для покупки акции,
    # а уже после находим максимум для продажи

    for i in range(len(low_prices)):
        if max_ind < i:
            leave_part = high_prices[i:]
            max_price = max(leave_part)
            max_ind_temp = leave_part.index(max_price) + i
        if max_price - low_prices[i] >= profit:
            profit = max_price - low_prices[i]
            min_price = low_prices[i]
            min_ind = i
            max_ind = max_ind_temp

    d_buy = date[min_ind + 1][:4] + '.' + date[min_ind + 1][4:6] + '.' + date[min_ind + 1][6:]
    d_sell = date[max_ind + 1][:4] + '.' + date[max_ind + 1][4:6] + '.' + date[max_ind + 1][6:]

    print('День покупки:', d_buy, min_ind + 1)
    print('День продажи:', d_sell, max_ind + 1)
