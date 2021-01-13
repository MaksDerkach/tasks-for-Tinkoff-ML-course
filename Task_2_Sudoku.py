import random
import pickle
import copy


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

    difficulty = int(input('Введите количество полей, которые необходимо убрать, что опредлит сложность игры: '))
    ready = str(input('По умолчанию в данной игре используется поле 9×9. Если Вы готовы продолжить, введите "+": '))

    if ready == '+':
        session = Sudoku(difficulty)
        session.show()
        session.swap_vertic_area()
        session.show()


class Sudoku:
    def __init__(self, difficulty=17, n=9):
        self.difficulty = difficulty
        self.n = n
        self.session = [[((j * n // 3 + i + j // (n // 3)) % n + 1) for i in range(n)] for j in range(n)]
        self.answer = []

    def generate(self):
        pass

    # вывод поля судоку
    def show(self):
        print(*self.session, sep='\n')
        print()

    #  сохранение сессии в файл
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

    def swap_horiz_area(self):
        swap_list = [0, 1, 2]
        one = random.choice(swap_list)
        # оформим таким образом, чтобы быть уверенными, что большая строка не поменяется сама с собой
        two = random.choice(list(set(swap_list) - {one}))
        for i in range(self.n // 3):
            p = self.n // 3 * one
            q = self.n // 3 * two
            self.session[i + q], self.session[i + p] = self.session[i + p], self.session[i + q]

    def swap_vertic_area(self):
        self.rotation()
        self.swap_horiz_area()
        self.rotation()


start_game()

input()
