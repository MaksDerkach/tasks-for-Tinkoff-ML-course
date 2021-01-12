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

    difficulty = int(input('Введите количество полей, которые необходимо убрать, что опредлит сложность игры: '))
    ready = str(input('По умолчанию в данной игре используется поле 9×9. Если Вы готовы продолжить, введите "+": '))

    if ready == '+':
        session = Sudoku(difficulty)
        session.show()
        session.mix()
        session.show()


class Sudoku:
    def __init__(self, difficulty=17, n=9):
        self.difficulty = difficulty
        self.n = n
        self.session = [[((j * n // 3 + i + j // (n // 3)) % n + 1) for i in range(n)] for j in range(n)]

    def generate(self):
        pass

    def show(self):
        print(*self.session, sep='\n')
        print()

    def save(self):
        with open('saved_data.pkl', 'wb') as file:
            pickle.dump(self.session, file)

    def download(self):
        with open('saved_data.pkl', 'rb') as file:
            load = pickle.load(file)
            self.session = load

    def mix(self):
        mix_list = ['self.swap_horiz_lines()', 'self.rotation()', 'self.swap_vertic_lines()']
        for i in range(10):
            chosen_change = random.choice(mix_list)
            eval(chosen_change)
        pass

    def swap_horiz_lines(self):
        swap_list = [0, 1, 2]
        one, two = random.choice(swap_list), random.choice(swap_list)
        group = random.choice(swap_list) * 3
        self.session[one + group], self.session[two + group] = self.session[two + group], self.session[one + group]

    def swap_vertic_lines(self):
        self.rotation()
        self.swap_horiz_lines()
        self.rotation()

    def rotation(self):
        self.session = list(map(list, zip(*self.session)))


start_game()

input()
