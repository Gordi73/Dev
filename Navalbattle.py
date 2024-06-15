from random import randint
# Исключения
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за поле боя"

class BoardUsedException(BoardException):
    def __str__(self):
        return "По этим данным вы уже стреляли"

class BoarWrongShipException(BoardException):
    pass
# Сравнение двух точек и вывод точек в консоль
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# корабль на игровом поле
class Ship:
    def __init__(self, nose, i, n):
        self.nose = nose
        self.i = i
        self.n = n
        self.lives = i
#возвращает список всех точек корабля
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.i):
            po_x = self.nose.x
            po_y = self.nose.y

            if self.n == 0:
                po_x += i

            elif self.n == 1:
                po_y += i

            ship_dots.append(Dot(po_x, po_y))

        return ship_dots

    def fire(self, shot):
        return shot in self.dots

#Поле боя
class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size

        self.defeated = 0

        self.field = [["O"] * size for _ in range(size)]

        self.occupied = []
        self.ships = []

    def __str__(self):
        resp = ""
        resp += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            resp += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            resp = resp.replace("■", "O")
        return resp

    def out(self, d):
        return  not ((0 <= d.x < self.size) and (0 <= d.y <self.size))
# контур коробля
    def countur(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.occupied:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.occupied.append(cur)
# проверка точек корабля
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.occupied:
                raise BoarWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.occupied.append(d)

        self.ships.append(ship)
        self.countur(ship)
# Все что связанно со стрельбой
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.occupied:
            raise BoardUsedException()

        self.occupied.append(d)

        for ship in self.ships:
            if ship.fire(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "x"
                if ship.lives == 0:
                    self.defeated += 1
                    self.countur(ship, verb=True)
                    print("Корабль потоплен!!!")
                    return False
                else:
                    print("Корабль ранен!!!")
                    return True

        self.field[d.x][d.y] = "."
        print("Промах!")
        return False

    def begin(self):
        self.occupied = []

    def defeat(self):
        return self.defeated == len(self.ships)


class Playar:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()
#Выстрел
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

#Компьютер
class AI(Playar):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Playar):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print("Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    # Генерация доски
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for i in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoarWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print("------------------")
        print(" Приветсввуем вас ")
        print("      в игре      ")
        print("    морской бой   ")
        print("------------------")
        print("формат ввода : x y")
        print(" x - номер строки ")
        print("y -  номер столбца")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.defeat():
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()