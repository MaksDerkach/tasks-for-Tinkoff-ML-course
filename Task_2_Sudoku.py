import random
import pickle
import copy


def print_rules():
    print('         ***  ДОБРО ПОЖАЛОВАТЬ В ИГРУ СУДОКУ!  ***   ')
    print('           ------------------------------------')

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
    print('           ------------------------------------')
    print(*printed_note, sep='')


def start_game():
    print_rules()
    print('           ------------------------------------')
    print('Выберете режим игры:', '1 - Вы решаете судоку, предложженное компьютером;',
          '2 - Компьютер решает судоку, предложенное Вами;', sep='\n')

    game_mode = 0
    while game_mode == 0:

        # выбор режима игры
        game_mode = int(input('Введите 1 или 2: '))

        if game_mode == 1:
            filling = int(input('Введите количество полей, которые необходимо оставить: '))
            session = Sudoku(filling)
            session.play()
        elif game_mode == 2:
            session = Sudoku(game_mode=2)
            session.play_computer()
        else:
            print('\nВы ввели неверный режим игры. Попробуйте еще раз.')
            print('Выберете режим игры:', '1 - Вы решаете судоку, предложженное компьютером;',
                  '2 - компьютер решает судоку, предложенное Вами;', sep='\n')
            game_mode = 0


class Sudoku:
    # конструктор класса Судоку
    def __init__(self, filling=35, n=9, game_mode=1):
        self.empties = n * n - filling  # количество клеток, которые будут заполнены
        self.n = n
        if game_mode == 1:
            self.session = [[((j * n // 3 + i + j // (n // 3)) % n + 1) for i in range(n)] for j in range(n)]
        elif game_mode == 2:
            self.session = [['.' for i in range(n)] for j in range(n)]
        self.answer = []  # массив для хранения правильного заполения поля судоку
        self.end_game = 0  # маркер для завершения игры
        self.answer_list = []  # массив для хранения ходов игрока

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
        filename = input("Назовите как-нибудь файл сохранений: ")
        with open(filename + '.pkl', 'wb') as file:
            saved = [self.session, self.answer]
            pickle.dump(saved, file)

    # загрузка сессии из файла
    def download(self):
        filename = input('Введите имя файла сохранения:')
        with open(filename + '.pkl', 'rb') as file:
            load = pickle.load(file)
            self.session = load[0]
            self.answer = load[1]

    # функция перемешивания исходного сгенерированного поля судоку
    def mix(self):
        mix_list = ['self.swap_horiz_lines()', 'self.rotation()', 'self.swap_vertic_lines()',
                    'self.swap_horiz_area()', 'self.swap_vertic_area()']
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

    # режим игры для отгадывания судоку человеком
    def play(self):
        self.mix()
        self.generate()
        self.show()
        while self.end_game == 0:
            turn = self.get_turn()
            if len(turn) == 1:
                answer = self.help_menu()
                if answer == '1':
                    self.save()
                    print('Файл успешно сохранён!')
                elif answer == '2':
                    self.download()
                    self.show()
                elif answer == '3':
                    self.print_rules()
                    self.show()
                elif answer == '4':
                    self.end_game = 1
                    print('До свидания!')
                elif answer == '0':
                    continue
            elif len(turn) == 3:
                row, column, num = list(map(int, turn))
                self.make_turn(row, column, num)
                self.show()
                if self.answer == self.session:
                    print('Вы успешно решили судоку! Поздравляем!')
                    self.end_game = 1

    # режим игры для отгадывания судоку компьютером
    def play_computer(self):
        print('Перед Вами пустое поле:')
        self.show()
        print('Имеется три варианта его заполнения:\n', '1 - Ввод через пробел следующей комбинации из',
              'трёх чисел (Строка, Колонка, Число);\n', '2 - Ввод каждой строки судоку, где каждое число отделено от',
              'другого пробелами, а на месте неизвестных стоит "0";\n',
              '3 - Чтение текстового файла с заданным полем, числа разделены пробелами, а на месте неизвестных "0";\n')
        reading_mode = int(input('Выберете режим задания поля: '))
        if reading_mode == 1:
            self.reading_mode_1()
        elif reading_mode == 2:
            self.reading_mode_2()
            self.show()
        elif reading_mode == 3:
            self.reading_mode_3()
            self.show()
        print('Поле успешно заполено!')

    def reading_mode_1(self):
        ans = 0
        while ans != '1':
            ans = input('Введите поле и число (для завершения введите 1): ').split()
            if len(ans) == 3:
                row, column, num = list(map(int, ans))
                self.make_turn(row, column, num)
                self.show()
            else:
                ans = '1'

    def reading_mode_2(self):
        for n in range(self.n):
            curr_row = input('Введите {} строку:'.format(n + 1))
            except_zero = lambda x: int(x) if x != 0 else '.'
            curr_row = list(map(except_zero, curr_row.split(' ')))
            self.session[n] = curr_row

    def reading_mode_3(self):
        filename = input('Введите названия файла с расширением txt: ')
        with open(filename + '.txt', 'r') as file:
            row = 0
            for line in file:
                except_zero = lambda x: int(x) if x != 0 else '.'
                curr_row = list(map(except_zero, line.split(' ')))
                self.session[row] = curr_row
                row += 1

    # рекуррентная функция решения судоку
    def solve(self, grid):
        solution = copy.deepcopy(grid)
        if self.solver(solution):
            return solution
        return None
        pass

    def solver(self, solution):
        pass

    # функция для получения хода игрока
    def get_turn(self):
        ans = input('Введите ваш ход (для справки введите 1): ').split()
        self.answer_list.append('Ход: ' + str(ans))
        return ans

    # функция для выполнения хода, полученного от игрока
    def make_turn(self, row, column, num):
        self.session[row - 1][column - 1] = num

    # вывод меню справки
    def help_menu(self):
        print('Введите 1 для сохранения игры;', 'Введите 2 для загрузки игры;',
              'Ведите 3 для просмотра правил и примечаний;', 'Для выхода из игры введите 4;',
              'Введите 0 для продолжения игры;', sep='\n')
        ans = input('Введите: ')
        return ans

    def check_solvability(self):
        pass

    # определяет в строках значения чисел, которые уже есть
    def get_rows(self, row_ind, curr_state_solution):
        return set(curr_state_solution[row_ind][:]) - set('.')

    # определяет в столбцах значения чисел, которые уже есть
    def get_columns(self, column_ind, curr_state_solution):
        return set(curr_state_solution[:][column_ind]) - set('.')

    # определяет в блоке (3*3 клетки) значения чисел, которые уже есть
    def get_area(self, row, column, curr_state):
        # так как каждая строка и столбец (а точнее элемент на их пересечении) привязаны к своему блоку,
        # то для начала определим к какому блоку принадлежит этот элемент
        row_block_start = (self.n // 3) * (row // 3)
        column_block_start = (self.n // 3) * (column // 3)
        return set(curr_state[row_block_start + i][column_block_start + j] for i in range(self.n // 3)
                   for j in range(self.n // 3)) - set('.')

    # определение возможных значений для конкретной клетки поля
    def possible_values(self, row, column, curr_state_solution):
        set_of_values = set(i for i in range(1, self.n + 1))
        set_of_values -= self.get_rows(row, curr_state_solution)
        set_of_values -= self.get_columns(column, curr_state_solution)
        set_of_values -= self.get_area(row, column, curr_state_solution)
        return set_of_values

    def print_rules(self):
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
        print('           ------------------------------------')
        print(*printed_rules, sep='')
        print('           ------------------------------------')
        print(*printed_note, sep='')


start_game()

input()
