import csv

filename = "YNDX_160101_161231.csv"
date = []
time = []
high_price = []
low_price = []

request = int(input("Введите уровень сложности задания,\
 которое хотите проверить: "))

if request == 1:
    with open(filename, 'r') as file:
        data = csv.reader(file)
        for row in data:
            date.append(row[0])
            time.append(row[1])
            high_price.append(row[3])
            low_price.append(row[4])

    high_price = list(map(float, high_price[1:]))
    low_price = list(map(float, low_price[1:]))

    min_low = low_price.index(min(low_price)) + 1
    max_high = high_price.index(max(high_price)) + 1

    d_buy = date[min_low][:4] + '.' + date[min_low][4:6] + '.' + date[min_low][6:]
    d_sell = date[max_high][:4] + '.' + date[max_high][4:6] + '.' + date[max_high][6:]

    print('День покупки:', d_buy)
    print('День продажи:', d_sell)
    print('\n')
