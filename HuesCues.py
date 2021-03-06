import sys
import random
import pickle
from pyface.qt import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from matplotlib import ticker
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib as mpl
import math

class LoadWindow(QWidget):
    

    def __init__(self, parent=None):
        super(LoadWindow, self).__init__(parent)

        self.colorcanvas = QLabel()
        self.color_dim = 500
        colorwheel = QPixmap(r"colorwheel.png")
        colorwheel = colorwheel.scaled(self.color_dim, self.color_dim, QtCore.Qt.KeepAspectRatio)
        self.colorcanvas.setAlignment(QtCore.Qt.AlignHCenter)
        self.colorcanvas.setPixmap(colorwheel)

        self.scorecanvas = QLabel()
        score = QPixmap(r"PlaceHolder.png")
        self.score_dim = 425
        score = score.scaled(self.score_dim, self.score_dim, QtCore.Qt.KeepAspectRatio)
        self.scorecanvas.setAlignment(QtCore.Qt.AlignVCenter)
        self.scorecanvas.setPixmap(score)
        
        cwidg = QHBoxLayout()
        cwidg.addWidget(self.colorcanvas)
        cwidg.addWidget(self.scorecanvas)

        self.button1 = QPushButton('Player 1')
        self.button1.setFont(QFont('Times', 14))
        self.p1text = QLineEdit('Enter Name')
        self.p1text.setFont(QFont('Times', 14))
        self.button1.setCheckable(True)
        self.button1.clicked.connect(self.switch_player)

        self.button2 = QPushButton('Player 2')        
        self.button2.setFont(QFont('Times', 14))
        self.button2.clicked.connect(self.switch_player)
        self.p2text = QLineEdit('Enter Name')
        self.p2text.setFont(QFont('Times', 14))
        self.button2.setCheckable(True)

        self.button3 = QPushButton('Player 3')
        self.button3.setFont(QFont('Times', 14))
        self.button3.clicked.connect(self.switch_player)
        self.p3text = QLineEdit('Enter Name')
        self.p3text.setFont(QFont('Times', 14))
        self.button3.setCheckable(True)
        
        self.button4 = QPushButton('Player 4')
        self.button4.setFont(QFont('Times', 14))
        self.button4.clicked.connect(self.switch_player)
        self.p4text = QLineEdit('Enter Name')
        self.p4text.setFont(QFont('Times', 14))
        self.button4.setCheckable(True)
        self.last_selected = None

        players = QGridLayout()
        players.addWidget(self.button1, 0, 0)
        players.addWidget(self.p1text, 1, 0)
        players.addWidget(self.button2, 0, 1)
        players.addWidget(self.p2text, 1, 1)
        players.addWidget(self.button3, 0, 2)
        players.addWidget(self.p3text, 1, 2)
        players.addWidget(self.button4, 0, 3)
        players.addWidget(self.p4text, 1, 3)
        self.scores = {}
        self.turn_log = {}
        self.turn_color = None
        self.colorcanvas.mousePressEvent = self.btnPass

        self.comm = QLabel()
        self.comm.setText('It works')
        self.comm.setFont(QFont('Arial', 20))
        self.comm.setAlignment(QtCore.Qt.AlignHCenter)
        communicate = QHBoxLayout()
        communicate.addWidget(self.comm)

        self.answer_btn = QPushButton('Show Answer')
        self.answer_btn.setFont(QFont('Times', 14))
        self.answer_btn.clicked.connect(self.show_answer)
        self.start_btn = QPushButton('Next Round')
        self.start_btn.setFont(QFont('Times', 14))
        self.start_btn.clicked.connect(self.next_round)
        self.start_btn.setDisabled(True)
        self.restart_btn = QPushButton('Play Again')
        self.restart_btn.setFont(QFont('Times', 14))
        self.restart_btn.clicked.connect(self.restart)
        example = QHBoxLayout()
        example.addWidget(self.start_btn)
        example.addWidget(self.answer_btn)
        example.addWidget(self.restart_btn)

        vbox = QVBoxLayout(self)
        vbox.addLayout(players)
        vbox.addLayout(cwidg)
        vbox.addLayout(communicate)

        vbox.addLayout(example)

        self.setLayout(vbox)


    def switch_player(self):
        color = { 1:QtCore.Qt.darkGreen, 2:QtCore.Qt.darkRed,
                  3:QtCore.Qt.gray, 4:QtCore.Qt.black}
        if self.last_selected != None:
            print('Last selected is ', self.last_selected.text())
            print('Toggling')
            self.last_selected.toggle()
        if self.button1.isChecked():
            print(f'{self.p1text.text()} now taking turn!')
            self.log_key = self.p1text.text()
            self.painter = QtGui.QPainter(self.colorcanvas.pixmap())
            self.painter.setPen(QtGui.QPen(color[1], 20))
            # self.last_selected.setChecked(False)
            self.last_selected = self.button1
        elif self.button2.isChecked():
            print(f'{self.p2text.text()} now taking turn!')
            self.log_key = self.p2text.text()
            self.painter = QtGui.QPainter(self.colorcanvas.pixmap())
            self.painter.setPen(QtGui.QPen(color[2], 20))
            # self.last_selected.setChecked(False)
            self.last_selected = self.button2            
        elif self.button3.isChecked():
            print(f'{self.p3text.text()} now taking turn!')
            self.log_key = self.p3text.text()
            self.painter = QtGui.QPainter(self.colorcanvas.pixmap())
            self.painter.setPen(QtGui.QPen(color[3], 20))
            # self.last_selected.setChecked(False)
            self.last_selected = self.button3
        elif self.button4.isChecked():
            print(f'{self.p4text.text()} now taking turn!')
            self.log_key = self.p4text.text()
            self.painter = QtGui.QPainter(self.colorcanvas.pixmap())
            self.painter.setPen(QtGui.QPen(color[4], 20))
            # self.last_selected.setChecked(False)
            self.last_selected = self.button4
        self.colorcanvas.mousePressEvent = self.paint
        return 

    def btnPass(self, event):
        event.ignore()

    def paint(self, event):
        painter = QPainter()
        painter.begin(self)
        x = event.pos().x()
        y = event.pos().y()
        self.turn_log[self.log_key] = (x,y)
        self.painter.drawEllipse(x,y,5,5)
        print(x,y)
        self.update()
        painter.end()
        # self.get_score()
        print(self.turn_log)
        self.last_selected.toggle()
        self.last_selected.setDisabled(True)
        self.last_selected = None
        self.painter = None
        self.colorcanvas.mousePressEvent = self.btnPass

    def pull_color(self):
        z = [(col, code) for col, code in zip(self.colors, self.codes)]
        random.shuffle(z)
        chosen = z.pop(0)
        color = chosen[0]
        code = chosen[1]
        self.comm.setText(f'Color: {color}')
        self.turn_color = code
        print(color, code)
        return

    def next_round(self):
        self.player_reset()
        self.turn_log = {}
        colorwheel = QPixmap(r"colorwheel.png")
        colorwheel = colorwheel.scaled(self.color_dim, self.color_dim, QtCore.Qt.KeepAspectRatio)
        self.colorcanvas.setAlignment(QtCore.Qt.AlignHCenter)
        self.colorcanvas.setPixmap(colorwheel)
        self.pull_color()
        self.start_btn.setDisabled(True)
        self.answer_btn.setDisabled(False)

    def player_reset(self):
        self.button1.setDisabled(False)
        self.button2.setDisabled(False)
        self.button3.setDisabled(False)
        self.button4.setDisabled(False)
        return

    def hex_coords(self, h):
        vals = {
            'A':10, 'B':11, 'C':12,
            'D':13, 'E':14, 'F':15
        }
        r, g, b = h[:2], h[2:4], h[4:]
        scale = []
        for c in [r,g,b]:
            tot = 0
            if c[0].isalpha():
                tot += vals[c[0].upper()] * 16
            else:
                tot += int(c[0]) * 16
            if c[1].isalpha():
                tot += vals[c[1].upper()] * 1
            else:
                tot += int(c[1])
            scale.append(tot)
        angs = [2*np.pi, 2/3*np.pi, 4/3*np.pi]
        res  =[]
        for val, ang in zip(scale, angs):
            res.append(val / 255 )
        return res

    def vectorize(self, l):
        s = np.array([0.,0.])
        vecs = np.array([
                        [1,0],
                        [-1/2, np.sqrt(3)/2],
                        [-1/2, np.sqrt(3)/-2],
                        ])
        for i, v in enumerate(vecs):
            s += v * l[i]
        
        return math.atan2(s[1],s[0])/math.pi*180, 2*np.pi * np.sqrt(s[0]**2 + s[1]**2), s
    
    def coords(self, degrees):
        s = ((360 + degrees) % 360) / 360 * 2*np.pi
        return s

    def det_winner(self):
        closest = None
        dist = 1e6
        for player, point in self.turn_log.items():
            _x = self.turn_answer[0]
            _y = self.turn_answer[1]
            euc = np.sqrt(abs(_x - point[0])**2 + abs(_y - point[1])**2)
            print(f'Player {player} is {euc} units away')
            if euc < dist:
                closest = player
            dist = euc
        print(f'Winner is {closest}!')
        for player in self.turn_log.keys():
            if player != closest:
                self.scores[player] = self.scores.get(player, 0)
            else:
                self.scores[player] = self.scores.get(player, 0) + 1
        self.scores = dict(sorted(self.scores.items(), key=lambda x: x[1], reverse=True))
        self.get_score()

    def restart(self):
        self.scores = {}
        self.turn_log = {}
        colorwheel = QPixmap(r"colorwheel.png")
        colorwheel = colorwheel.scaled(self.color_dim, self.color_dim, QtCore.Qt.KeepAspectRatio)
        self.colorcanvas.setAlignment(QtCore.Qt.AlignHCenter)
        self.colorcanvas.setPixmap(colorwheel)
        self.player_reset()

        score = QPixmap(r"PlaceHolder.png")
        score = score.scaled(self.score_dim, self.score_dim, QtCore.Qt.KeepAspectRatio)
        self.scorecanvas.setAlignment(QtCore.Qt.AlignVCenter)
        self.scorecanvas.setPixmap(score)
        self.pull_color()
        self.answer_btn.setDisabled(False)
        self.start_btn.setDisabled(True)

    def get_score(self):
        print('Scores', self.scores)
        print('Turn', self.turn_log)
        players = list(self.scores.keys())
        vals = list(self.scores.values())
        print(players, vals)
        colors = ['#4680c7' if s <= 9 else '#d12c2c' for s in vals]
        fig, ax = plt.subplots(1,1)
        ax.barh(players, vals, color=colors)
        ax.set_facecolor('#FFFFFF')
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        # ax.set_yticks(fontsize=20)
        # ax.set_xticks(fontsize=20)
        ax.tick_params(labelsize=20)
        ax.vlines(10, -1, 5, linestyle='--', color='k')
        ax.set_ylim(-0.5, len(players)-0.5)
        print('AM DRAWING')
        plt.savefig('Scores.png', bbox_inches='tight', dpi=125)
        score = QPixmap('Scores.png')
        score = score.scaled(self.score_dim, self.score_dim, QtCore.Qt.KeepAspectRatio)
        self.scorecanvas.setAlignment(QtCore.Qt.AlignVCenter)
        self.scorecanvas.setPixmap(score)

    def show_answer(self):
        l = self.hex_coords(self.turn_color)
        _, _, coord = self.vectorize(l)

        x, y = coord[0], coord[1]
        x = self.color_dim/2 + (self.color_dim/2 * x)
        y = self.color_dim/2 + (self.color_dim/2 * -y)

        x, y = x//1, y//1
        self.turn_answer = (x,y)
        self.painter = QtGui.QPainter(self.colorcanvas.pixmap())
        self.painter.setPen(QtGui.QPen(QtCore.Qt.black, 40))
        painter = QPainter()
        painter.begin(self)
        self.painter.drawEllipse(int(x),int(y),5,5)
        self.update()
        painter.end()
        self.painter = None
        self.det_winner()
        self.start_btn.setDisabled(False)
        self.answer_btn.setDisabled(True)
        self.colorcanvas.mousePressEvent = self.btnPass

    


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.window = LoadWindow()
        self.setWindowTitle("Hues & Cues Dupe")
        self.setCentralWidget(self.window)
        self.setGeometry(50, 100, 300, 150)
        self.show()
        d = pickle.load(open('ColorCodes.p', 'rb'))
        self.window.colors = [c for c in d.keys()]
        self.window.codes = [c for c in d.values()]
        self.window.pull_color()



if __name__ == '__main__':
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
        screen = app.primaryScreen()
        size = screen.size()
    w = MainWindow()
    sys.exit(app.exec_())