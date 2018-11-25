import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, \
    QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel
from random import randint, choice
from datetime import datetime


winner_lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                [0, 3, 6], [1, 4, 7], [2, 5, 8],
                [0, 4, 8], [2, 4, 6]]


class Random:
    def __init__(self, state):
        self.state = state

    @property
    def best_action(self):
        return choice([i for i, x in enumerate(self.state) if x is None])


class QPushButton(QPushButton):

    def setText(self, string):
        super().setText(string)
        self.repaint()


class QLabel(QLabel):

    def setText(self, string):
        super().setText(string.ljust(27))
        self.repaint()


class App(QDialog):

    def __init__(self, npc_policy=Random):
        super().__init__()
        self.board = [None] * 9
        self.turn = randint(0, 1)
        self.npc_policy = npc_policy
        self.buttons = [None] * 9
        self.title = 'Gato'
        self.initUI()
        self.run()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.label = QLabel('')
        self.box = self.createGridLayout()
        restart = QPushButton('Reiniciar')
        restart.clicked.connect(self.restart)

        windowLayout = QVBoxLayout()

        windowLayout.addWidget(self.label)
        windowLayout.addWidget(self.box)
        windowLayout.addWidget(restart)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        box = QGroupBox()
        layout = QGridLayout()
        for i in range(3):
            for j in range(3):
                button = QPushButton('')
                button.setFixedSize(50, 50)
                button.coords = i, j
                button.played = False
                layout.addWidget(button, i, j)
                button.clicked.connect(self.buttonClicked)
                self.buttons[i * 3 + j] = button
        box.setLayout(layout)
        return box

    def buttonClicked(self):
        button = self.sender()
        if not button.played and not self.finished[0]:
            self.play_user(button)

    def restart(self):
        self.board = [None] * 9
        self.turn = randint(0, 1)
        for button in self.buttons:
            button.setText('')
            button.played = False
        self.label.setText('')
        self.run()

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
        if self.turn == 1:
            self.play_npc()

    def play_user(self, button):
        button.played = True
        button.setText('X')
        x, y = button.coords
        self.board[x * 3 + y] = 0

        finished, outcome = self.finished
        if finished:
            self.label.setText(outcome)
        else:
            self.play_npc()
        self.turn = 1 - self.turn

    def play_npc(self):
        i = datetime.now()
        policy = self.npc_policy(self.board)
        index = policy.best_action
        self.label.setText(f'Tiempo decisión: {str(datetime.now() - i)[:10]}')

        button = self.buttons[index]
        button.played = True
        button.setText('O')
        self.board[index] = 1

        finished, outcome = self.finished
        if finished:
            self.label.setText(outcome)
        self.turn = 1 - self.turn


def winner(state, player):
    indices = [i for i, x in enumerate(state) if x == player]
    winners = filter(
        lambda x: len(x) == 3,
        (set(indices).intersection(set(i)) for i in winner_lines)
    )
    return any(winners)


class TicTacToeGui():
    def __init__(self, policy=Random):
        self.policy = policy

    def run(self):
        app = QApplication(sys.argv)
        ex = App(self.policy)
        sys.exit(app.exec_())


if __name__ == '__main__':
    g = TicTacToeGui()
    g.run()
