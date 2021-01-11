import csv


# функция поиска даты покупки-продажи акции с максимлаьной прибылью
def maximum_profit(low_prices, high_prices):
    min_price, max_price = 0, 0
    min_ind, max_ind = 0, 0
    profit = max_price - min_price

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
    return min_ind, max_ind


# получение дня продажи-покупки акции
def get_day(ind, date):
    return date[ind + 1][:4] + '.' + date[ind + 1][4:6] + '.' + date[ind + 1][6:]


# получение времени продажи-покупки акции
def get_time(ind, time):
    return time[ind + 1][:2] + ':' + time[ind + 1][2:4] + ':' + time[ind + 1][4:]


filename = "YNDX_160101_161231.csv"
date = []
time = []
high_prices = []
low_prices = []

with open(filename, 'r') as file:
    data = csv.reader(file)
    for row in data:
        date.append(row[0])
        time.append(row[1])
        high_prices.append(row[3])
        low_prices.append(row[4])

low_prices = list(map(float, low_prices[1:]))
high_prices = list(map(float, high_prices[1:]))

request = int(input("Введите количество транзакций покупки-продажи: "))

if request == 1:
    print('ОПИСАНИЕ АЛГОРИТМА:')
    print("Алгоритм находит пару - минимальное значение 'низкой' цены (LOW), которая для нас является ценой \
покупки акции, \nи максимальное значение 'высокой' цены (HIGH),которая для нас является ценой продажи акции, - \
 \nу которой разница, т.е. доходность после купли/продажи будет наибольшая.\n")

    min_ind, max_ind = maximum_profit(low_prices, high_prices)
    profit = high_prices[max_ind] - low_prices[min_ind]

    d_buy = get_day(min_ind, date)
    d_sell = get_day(max_ind, date)
    t_buy = get_time(min_ind, time)
    t_sell = get_time(max_ind, time)

    print('Дата покупки:', d_buy, 'в', t_buy, '\nДата продажи:', d_sell, 'в', t_sell)
    print('Сумма "чистого" дохода составляет:', profit)

    print('Далее будет представлено изменние цены акции с', d_buy, 'по', d_sell)
    for j in range(min_ind + 1, max_ind + 2):
        d_curr = date[j + 1][:4] + '.' + date[j + 1][4:6] + '.' + date[j + 1][6:]
        t_curr = time[j + 1][:2] + ':' + time[j + 1][2:4] + ':' + time[j + 1][4:]
        # print('Минимальная цена на', d_curr, 'в', t_curr, 'составляет', low_prices[j])
        # print('Максимлаьная цена на', d_curr, 'в', t_curr, 'составляет', high_prices[j])

    print(min_ind + 1, max_ind + 1)

elif request == 2:
    print('ОПИСАНИЕ АЛГОРИТМА:')
    print("Аналогично алгоритму для единственной транзакции сначала он находит пару - минимальное значение \
'низкой' цены (LOW),\nкоторая для нас является ценой покупки акции, и максимальное значение 'высокой' цены (HIGH), \
которая для нас\nявляется ценой продажи акции, - у которой разница, т.е. доходность \
после купли/продажи будет наибольшая.\nДалее в оставшихся периодах времени до и после транзакции снова происходит \
поиск такой же пары и выбирается \nта пара, у которой 'чистая' прибыль больше.")

    min_price, max_price = 0, 0
    min_ind, max_ind = 0, 0
    profit = max_price - min_price

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
