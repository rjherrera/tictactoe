from random import randint

winner_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]


class TicTacToe:
    def __init__(self):
        self.board = [None] * 9
        self.turn = randint(0, 1)

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
        minimax = MiniMaxTree(self.board)
        index = minimax.best_action
        self.board[index] = 1

    def __str__(self):
        _ = ['X', 'O', '_']
        board = self.board if self.board.count(None) != 9 else [2] * 9
        string = ''
        for i in range(2, 9, 3):
            row = [_[i] if i is not None else ' ' for i in board[i - 2:i + 1]]
            string += '|'.join(row) + f'   -   {i-1}|{i}|{i+1}\n'
        return string[:-1]


class Node:
    def __init__(self, value,  parent=None):
        self.value = value
        self.parent = parent
        self.leaf = False
        self.score = None
        self.children = []

    def add_child(self, node):
        self.children.append(node)


class MiniMaxTree:
    def __init__(self, root):
        self.root = root if isinstance(root, Node) else Node(root)
        self.leaves = []
        self.build(self.root, 1)
        self.score_leaves()
        self.calculate_score(self.root, 0)

    def build(self, node, turn):
        states = next_states(node.value, turn)
        if not states:
            self.add_leaf(node)
        for state in states:
            child = Node(state, parent=node)
            node.add_child(child)
            self.build(child, 1 - turn)

    def add_leaf(self, node):
        node.leaf = True
        self.leaves.append(node)

    def score_leaves(self):
        for leaf in self.leaves:
            if winner(leaf.value, 1):
                leaf.score = 1
            elif winner(leaf.value, 0):
                leaf.score = -1
            else:
                leaf.score = 0

    def calculate_score(self, node, turn):
        if node.leaf:
            return node.score
        scores = [self.calculate_score(i, 1 - turn) for i in node.children]
        node.score = max(scores) if turn == 0 else min(scores)
        node.best_choice = node.children[scores.index(node.score)]
        return node.score

    @property
    def best_action(self):
        state = self.root.value
        next_state = self.root.best_choice.value
        for i in range(9):
            if state[i] != next_state[i]:
                return i
        raise Exception('States are equal or different in size')


def winner(state, player):
    indices = [i for i, x in enumerate(state) if x == player]
    winners = filter(
        lambda x: len(x) == 3,
        (set(indices).intersection(set(i)) for i in winner_lines)
    )
    return any(winners)


def terminal(state):
    return winner(state, 1) or winner(state, 0) or state.count(None) == 0


def next_states(state, turn):
    indices = [i for i, x in enumerate(state) if x is None]
    if not terminal(state):
        return [state[:i] + [turn] + state[i + 1:] for i in indices]
    return []


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
