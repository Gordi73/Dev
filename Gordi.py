def start():
    print(" Добро пожаловать в игру крестики нолики!!! ")
start()
pole = [[" "] * 3 for i in range(3)]
def show():
    print(f" 0  1  2 ")
    for i in range(3):
        korrect = " ".join(pole[i])
        print(f"{i} {korrect}")

def vvod():
    while True:
        x, y =map(int, input("     Ваш ход ").split())

        if 0 > x or x > 2 or 0 > y or y > 2 :
            print(" Координаты вне диапозона ")
            continue

        if pole[x][y] != " ":
             print(" Клетка занята ")
             continue

        return x, y


def win_comb():
        win_num = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                   ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
                   ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)))
        for win in win_num:
            symbols = []
            for c in win:
                symbols.append(pole[c[0]][c[1]])
            if symbols == ["x", "x", "x"]:
                print(" Выиграл x ")
                return True
            if symbols == ["0", "0", "0"]:
                print(" Выиграл 0 ")
                return True

        return False
num = 0
while True:
    num += 1

    show()

    if num % 2 == 1:
        print(" Ходит крестик ")
    else:
        print(" Ходит нолик ")

    x, y = vvod()

    if num % 2 == 1:
        pole[x][y] = "x"
    else:
        pole[x][y] = "0"

    if win_comb():
        break
    if num == 9:
        print(" Ничья ")
        break