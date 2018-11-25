from tictactoe import TicTacToe, winner
inf = float('infinity')


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
        self.build(self.root, 1, -inf, +inf)

    def build(self, node, turn, alpha, beta):
        states = next_states(node.value, turn)
        if not states:
            if winner(node.value, 1):
                node.score = 1
            elif winner(node.value, 0):
                node.score = -1
            else:
                node.score = 0
            return node.score
        if turn == 1:
            for state in states:
                child = Node(state)
                node.add_child(child)
                alpha = max(alpha, self.build(child, 0, alpha, beta))
                if beta <= alpha:
                    break
            score = alpha
        else:
            for state in states:
                child = Node(state)
                node.add_child(child)
                beta = min(beta, self.build(child, 1, alpha, beta))
                if beta <= alpha:
                    break
            score = beta
        node.score = score
        return node.score

    @property
    def best_action(self):
        for child in self.root.children:
            if child.score == self.root.score:
                choice = child
                break
        state = self.root.value
        next_state = choice.value
        for i in range(9):
            if state[i] != next_state[i]:
                return i
        raise Exception('States are equal or different in size')


def terminal(state):
    return winner(state, 1) or winner(state, 0) or state.count(None) == 0


def next_states(state, turn):
    indices = [i for i, x in enumerate(state) if x is None]
    if not terminal(state):
        return [state[:i] + [turn] + state[i + 1:] for i in indices]
    return []


if __name__ == '__main__':
    g = TicTacToe(MiniMaxTree)
    g.run()
