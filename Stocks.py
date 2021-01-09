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

    print('ОПИСАНИЕ АЛГОРИТМА:')
    print("Алгоритм находит пару - минимальное значение низкой цены (LOW) и \
максимальное значение высокой цены (HIGH), \nу которой разница, т.е. доходность после купли/продажи будет наибольшая.")

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
            # print(profit,  min_ind, max_ind)

    d_buy = date[min_ind + 1][:4] + '.' + date[min_ind + 1][4:6] + '.' + date[min_ind + 1][6:]
    d_sell = date[max_ind + 1][:4] + '.' + date[max_ind + 1][4:6] + '.' + date[max_ind + 1][6:]

    print('День покупки:', d_buy, '\nДень продажи:', d_sell)
    print('Сумма "чистого" дохода составляет:', profit)

    print('Далее будет представлено изменние цены акции с', d_buy, 'по', d_sell)
    for j in range(min_ind + 1, max_ind + 2):
        d_curr = date[j + 1][:4] + '.' + date[j + 1][4:6] + '.' + date[j + 1][6:]
        t_curr = time[j + 1][:2] + ':' + time[j + 1][2:4] + ':' + time[j + 1][4:]
        print('Минимальная цена на', d_curr, 'в', t_curr, 'составляет', low_prices[j])
        print('Максимлаьная цена на', d_curr, 'в', t_curr, 'составляет', high_prices[j])

    print(min_ind + 1, max_ind + 1)
