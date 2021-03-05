import argparse

def poliomino(M, Rect_tetramino, L_tetramino, board, N_count):
    if N_count == 0: # Если поместили все фигуры
        return True, board
    else:
        # Поиск номера незаполненного квадрата (elem == 0)
            try:
                index = [item for sublist in board for item in sublist].index(0)
            except ValueError:
                return False, board# Незаполненных квадратов не осталось

            # Выбираем первый незаписанный квадратный тетрамино
            is_Rect_tetramino = False
            for i in range(len(Rect_tetramino)):
                if Rect_tetramino[i][1] > 0:
                    is_Rect_tetramino = True
                    break
            # Если есть ещё незаписанные Rect-тетрамино
            if is_Rect_tetramino:
                S1, S2, N = Rect_tetramino[i][0][0], Rect_tetramino[i][0][1], Rect_tetramino[i][1]
                Rect_tetramino[i][1] = N - 1
                # Ищём возможные расстановки тетрамино на незаполненных квадратах поля
                Cells = Rect_tetramino_mass(Rect_tetramino[i][0], board, (M[0], M[1]))
                if Cells != []:
                    N_count -= 1 # Добавили тетрамино на поле
                while Cells != []: # Перебираем возможные расстановки тетрамино
                    for cell in Cells[0]:
                        board[cell[0]][cell[1]] = N_count+1
                    gues, _ = poliomino((M[0], M[1]), Rect_tetramino, L_tetramino, board, N_count)
                    if gues:
                        return True, board
                    else:
                        for cell in Cells[0]:
                            board[cell[0]][cell[1]] = 0
                        del Cells[0]
                # Если не удалось поместить тетрамино на поле, увеличиваем N-количество незаписанных фигур
                Rect_tetramino[i][1] = N
                return False, board

            # Выбираем первый незаписанный L-тетрамино
            is_L_tetramino = False
            for i in range(len(L_tetramino)):
                if L_tetramino[i][1] > 0:
                    is_L_tetramino = True
                    break
            if is_L_tetramino:
                Q1, Q2, N = L_tetramino[i][0][0], L_tetramino[i][0][1], L_tetramino[i][1]
                L_tetramino[i][1] = N - 1
                # Ищём возможные расстановки тетрамино на незаполненных квадратах поля
                Cells = L_tetramino_mass(L_tetramino[i][0], board, (M[0], M[1]))
                # Добавили тетрамино на поле
                if Cells != []:
                    N_count -= 1
                while Cells != []:# Перебираем возможные расстановки L-тетрамино
                    for cell in Cells[0]:
                        board[cell[0]][cell[1]] = N_count+1
                    gues, _ = poliomino((M[0], M[1]), Rect_tetramino, L_tetramino, board, N_count)
                    if gues:
                        return True, board
                    else:
                        for cell in Cells[0]:
                            board[cell[0]][cell[1]] = 0
                        del Cells[0]
                # Если не удалось поместить тетрамино на поле, увеличиваем N-количество незаписанных фигур
                L_tetramino[i][1] = N
                return False, board
            return True, board


def append_tetramino(tetramino, i, j, M):
    temp_mass = []
    for elem in tetramino:
        try:
            if elem[0] + i < M[1] and elem[1] + j < M[0] and board[elem[0] + i][elem[1] + j] == 0:
                temp_mass.append((elem[0] + i, elem[1] + j))
        except IndexError:
            break
    return temp_mass

def Rect_tetramino_mass(S, board, M):
# Поиск всех возможных размещений Rect-тетрамино
    # 1 1 .
    # 1 1 .
    # . . .
    rect = []
    rect90 = []
    for i in range(S[0]):
        for j in range(S[1]):
            rect.append((i, j))
            rect90.append((j, i))
    mass = []
    for i in range(M[1]):
        for j in range(M[0]):
            if board[i][j] == 0:
                # 0
                temp_mass = append_tetramino(rect, i, j, M)
                if len(temp_mass) == len(rect):
                    mass.append(temp_mass)
                # 90
                temp_mass = append_tetramino(rect90, i, j, M)
                if len(temp_mass) == len(rect90):
                    mass.append(temp_mass)
    return mass


def L_tetramino_mass(Q, board, M):
# Поиск всех возможных размещений L-тетрамино
    # 1 . .
    # 1 . .
    # 1 1 .
    L = []
    L90 = []
    L180 = []
    L270 = []
    for i in range(Q[0]):
        L.append((i, 0))
        L90.append((0, i))
        L180.append((i, 0))
        L270.append((0, i))
    for j in range(1, Q[1]):
        L.append((i, j))
        L90.append((j, i))
        L180.append((0, j))
        L270.append((j, 0))
    mass = []
    for i in range(M[1]):
        for j in range(M[0]):
            if board[i][j] == 0:
                # 0
                temp_mass = append_tetramino(L, i, j, M)
                if len(temp_mass) == len(L):
                    mass.append(temp_mass)
                # 90
                temp_mass = append_tetramino(L90, i, j, M)
                if len(temp_mass) == len(L90):
                    mass.append(temp_mass)
                # 180
                temp_mass = append_tetramino(L180, i, j, M)
                if len(temp_mass) == len(L180):
                    mass.append(temp_mass)
                # 270
                temp_mass = append_tetramino(L270, i, j, M)
                if len(temp_mass) == len(L270):
                    mass.append(temp_mass)
    return mass





if __name__ == '__main__':
    # Парсим данные
    cmd_parser = argparse.ArgumentParser(description=f"Coelus Test VERSION 1.0")
    cmd_parser.add_argument('param', type=str, nargs='*', help='results folder')
    args = cmd_parser.parse_args()
    param = args.param
    if len(param) != 3:
        raise AssertionError("Wrong data!")

    T, Rect_tetramino_str, L_tetramino_str = param[0], param[1], param[2]
    Rect_tetramino, L_tetramino = [], []
    N_count = 0 # Количество фигур
    M1, M2 = int(T[1:-1].split(',')[0]), int(T[1:-1].split(',')[1])
    for elem in Rect_tetramino_str[2:-2].split('),('):
        S1, S2 = int(elem.split('),')[0][1:].split(',')[0]), int(elem.split('),')[0][1:].split(',')[1])
        N = int(elem.split('),')[1])
        N_count += N
        if N == 1:
            Rect_tetramino.append([(S1, S2), N])
        else:
            len_Rect = len(Rect_tetramino)
            for i in range(N):
                Rect_tetramino.insert(len_Rect+i, [(S1, S2), N])
    for elem in L_tetramino_str[2:-2].split('),('):
        Q1, Q2 = int(elem.split('),')[0][1:].split(',')[0]), int(elem.split('),')[0][1:].split(',')[1])
        N = int(elem.split('),')[1])
        N_count += N
        if N == 1:
            L_tetramino.append([(Q1, Q2), N])
        else:
            len_Rect = len(L_tetramino)
            for i in range(N):
                L_tetramino.insert(len_Rect+i, [(Q1, Q2), N])

    # Незаполненое поле
    board = [[0 for j in range(M1)] for i in range(M2)]
    gues, board = poliomino((M1, M2), Rect_tetramino, L_tetramino, board, N_count)
    print(gues)
    if gues:
        for elem in board:
            print(elem)











