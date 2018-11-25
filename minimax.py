from tictactoe import TicTacToe, winner


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
