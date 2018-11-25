from random import randint, choice

winner_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]


class Random:
    def __init__(self, state):
        self.state = state

    @property
    def best_action(self):
        return choice([i for i, x in enumerate(self.state) if x is None])


class TicTacToe:
    def __init__(self, npc_policy=Random):
        self.board = [None] * 9
        self.turn = randint(0, 1)
        self.npc_policy = npc_policy

    @property
    def finished(self):
        if self.winner_user:
            return True, 'Ganaste!'
        elif self.winner_npc:
            return True, 'Te ganó el computador!'
        elif self.board.count(None) == 0:
            return True, 'Empate'
        return False, ''

    @property
    def winner_user(self):
        return winner(self.board, 0)

    @property
    def winner_npc(self):
        return winner(self.board, 1)

    def run(self):
        print('Tu: X | PC: O')
        print(self, '\n')
        while not self.finished[0]:
            if self.turn == 0:
                print('Tu turno')
                self.play_user()
            else:
                print('Turno del PC')
                self.play_npc()
            self.turn = 1 - self.turn
            print('', self, '', sep='\n')
        print(self.finished[1])

    def play_user(self):
        index = bounded_numeric_input('Indica tu jugada (1-9): ', 1, 9) - 1
        while self.board[index] is not None:
            index = bounded_numeric_input('Indica tu jugada (1-9): ', 1, 9) - 1
        self.board[index] = 0

    def play_npc(self):
        policy = self.npc_policy(self.board)
        index = policy.best_action
        self.board[index] = 1

    def __str__(self):
        _ = ['X', 'O', '_']
        board = self.board if self.board.count(None) != 9 else [2] * 9
        string = ''
        for i in range(2, 9, 3):
            row = [_[i] if i is not None else ' ' for i in board[i - 2:i + 1]]
            string += '|'.join(row) + f'   -   {i-1}|{i}|{i+1}\n'
        return string[:-1]


def winner(state, player):
    indices = [i for i, x in enumerate(state) if x == player]
    winners = filter(
        lambda x: len(x) == 3,
        (set(indices).intersection(set(i)) for i in winner_lines)
    )
    return any(winners)


def bounded_numeric_input(message, start, end):
    def complies(string):
        return string.isdigit() and start <= int(string) <= end
    answer = input(message)
    while not complies(answer):
        answer = input(message)
    return int(answer)


if __name__ == '__main__':
    g = TicTacToe()
    g.run()
