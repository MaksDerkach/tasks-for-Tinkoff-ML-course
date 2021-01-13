import random
import pickle


def print_rules():
    print('   ***  Добро пожаловать в игру Судоку!  ***   ')

    printed_rules = [
        'Игровое поле представляет собой квадрат размером 9×9, разделённый на меньшие' +
        ' квадраты со стороной в 3 клетки.\n',
        'Таким образом, всё игровое поле состоит из 81 клетки.' +
        ' В них уже в начале игры стоят некоторые числа (от 1 до 9),\n',
        'называемые подсказками. От игрока требуется заполнить свободные клетки цифрами от 1 до 9 так,',
        ' чтобы в каждой\nстроке, в каждом столбце и в каждом' +
        ' малом квадрате 3×3 каждая цифра встречалась бы только один раз.']

    printed_note = ['Примечание: \nДля ввода варианта заполнения поля необходимо через пробел ввести следующую ',
                    'комбинацию\n', 'из трёх чисел (Строка, Колонка, Число).\n',
                    'Отсчёт строки и колонки начинается с 1 с левого верхнего края поля.']
    print(*printed_rules, sep='')
    print()
    print(*printed_note, sep='')


def start_game():
    print_rules()

    empties = int(input('Введите количество полей, которые необходимо убрать, что опредлит сложность игры: '))
    ready = str(input('По умолчанию в данной игре используется поле 9×9. Если Вы готовы продолжить, введите "+": '))

    if ready == '+':
        session = Sudoku(empties)
        session.show()
        session.swap_vertic_area()
        print()
        session.show()
        session.generate()
        print(session.answer)
        print()
        session.show()


class Sudoku:
    def __init__(self, empties=17, n=9):
        self.empties = empties
        self.n = n
        self.session = [[((j * n // 3 + i + j // (n // 3)) % n + 1) for i in range(n)] for j in range(n)]
        self.answer = []
        self.end_game = 0

    def generate(self):
        self.copy_answer()
        already_used = []
        for i in range(self.empties):
            one, two = random.randint(0, 8), random.randint(0, 8)
            # необходимо, чтобы индексы убираемых чисел вновь не повторялись
            while (one, two) in already_used:
                one, two = random.randint(0, 8), random.randint(0, 8)
            already_used.append((one, two))
            self.session[one][two] = 0

    # вывод поля судоку
    def show(self):

        # вспомогательная функция
        def check_dots(ind, n):
            if ind == 2 or ind == 5:
                return str(n) + ' |' if n != 0 else '.' + ' |'
            else:
                return str(n) if n != 0 else '.'

        i = 0
        for line in self.session:
            if i == 0 or i == 3 or i == 6:
                print(' +---------+----------+----------+')
            print(' | ' + '  '.join([check_dots(ind, n) for ind, n in enumerate(line)]) + ' |')
            i += 1
        print(' +---------+----------+----------+')

    # сохранение сессии в файл
    def save(self):
        with open('saved_data.pkl', 'wb') as file:
            pickle.dump(self.session, file)

    # загрузка сессии из файла
    def download(self):
        with open('saved_data.pkl', 'rb') as file:
            load = pickle.load(file)
            self.session = load

    # функция перемешивания исходного сгенерированного поля судоку
    def mix(self):
        mix_list = ['self.swap_horiz_lines()', 'self.rotation()', 'self.swap_vertic_lines()',
                    'swap_horiz_area', 'swap_vertic_area']
        for i in range(10):
            chosen_change = random.choice(mix_list)
            eval(chosen_change)

    # измение местами двух строк судоку
    def swap_horiz_lines(self):
        swap_list = [0, 1, 2]
        one = random.choice(swap_list)
        # оформим таким образом, чтобы быть уверенными, что строка не поменяется сама с собой
        two = random.choice(list(set(swap_list) - {one}))
        group = random.choice(swap_list) * self.n // 3
        self.session[one + group], self.session[two + group] = self.session[two + group], self.session[one + group]

    # изменение местами двух столбцов судоку
    def swap_vertic_lines(self):
        self.rotation()
        self.swap_horiz_lines()
        self.rotation()

    # вращение или приментельно к матрицам транспонирование поля судоку
    def rotation(self):
        self.session = list(map(list, zip(*self.session)))

    # изменение местами двух горизонтальных полей (состоят из 3 строк)
    def swap_horiz_area(self):
        swap_list = [0, 1, 2]
        one = random.choice(swap_list)
        # оформим таким образом, чтобы быть уверенными, что большая строка не поменяется сама с собой
        two = random.choice(list(set(swap_list) - {one}))
        for i in range(self.n // 3):
            p = self.n // 3 * one
            q = self.n // 3 * two
            self.session[i + q], self.session[i + p] = self.session[i + p], self.session[i + q]

    # изменение местами двух вертикальных полей (состоят из 3 столбцов)
    def swap_vertic_area(self):
        self.rotation()
        self.swap_horiz_area()
        self.rotation()

    # функция для записи ответа в отдельную переменную
    def copy_answer(self):
        for row in self.session:
            curr = row.copy()
            self.answer.append(curr)

    def get_turn(self):
        pass

    def check_solvability(self):
        pass

    def start(self):
        pass

    def print_rules(self):
        pass


start_game()

input()
