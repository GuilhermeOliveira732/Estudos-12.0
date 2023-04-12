# Game Ping-Pong
import tkinter
from tkinter import *
import random
import time

# Printa a mensagem de escolha de nível e pega o input do jogador
level = int(input("Qual nível você gostaria de jogar? 1/2/3/4/5 \n"))

# Para cada nível (1 a 5), é dividido o tamanho da barra pelo nível (ex.: nível 5, divide 500/5)
length = 500 / level

# Tem haver com o tkinter, que faz a parte "visual" da janela do jogo
# root = Tk()
root = tkinter.Tk()


# Define o título a ser exibido no topo da janela, o nome do jogo "Ping Pong"
root.title("Ping Pong")
# Define se a janela será "resizible", se poderá ser "maximizada" ou não, sendo "0" o valor para "false"
root.resizable(0, 0)

""" Decide atributos da janela, exemplo, se ela será transparente, se ficará no topo das outras a ser aberta,
no caso do código, é colocado que ela estará no topo de todas (topmost e retorna o boolean como True, 1 ou -1 """
#root.wm_attributes("-topmost", -1)
#root.wm_attributes("-topmost", True)
root.wm_attributes("-topmost", 1)


# Define o tamanho da tela
canvas = Canvas(root, width=800, height=600, bd=0, highlightthickness=0)
canvas.pack()

root.update()

# Variável
count = 0
lost = False


class Bola:
    def __init__(self, canvas, Barra, color):
        self.canvas = canvas
        self.Barra = Barra
        # define, entre outras coisas, as medidas da bola e sua cor, que pode ser alterada, por exemplo, com "red"
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color)
        self.canvas.move(self.id, 245, 200)

        starts_x = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts_x)

        self.x = starts_x[0]
        self.y = -3

        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)

        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.y = -3

        if pos[0] <= 0:
            self.x = 3

        if pos[2] >= self.canvas_width:
            self.x = -3

        self.Barra_pos = self.canvas.coords(self.Barra.id)

        if pos[2] >= self.Barra_pos[0] and pos[0] <= self.Barra_pos[2]:
            if pos[3] >= self.Barra_pos[1] and pos[3] <= self.Barra_pos[3]:
                self.y = -3
                global count
                count += 1
                score()

        if pos[3] <= self.canvas_height:
            self.canvas.after(10, self.draw)
        else:
            game_over()
            global lost
            lost = True


class Barra:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, length, 10, fill=color)
        self.canvas.move(self.id, 200, 400)

        self.x = 0

        self.canvas_width = self.canvas.winfo_width()

        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)

        self.pos = self.canvas.coords(self.id)

        if self.pos[0] <= 0:
            self.x = 0

        if self.pos[2] >= self.canvas_width:
            self.x = 0

        global lost

        if lost == False:
            self.canvas.after(10, self.draw)

    def move_left(self, event):
        if self.pos[0] >= 0:
            self.x = -3

    def move_right(self, event):
        if self.pos[2] <= self.canvas_width:
            self.x = 3


def start_game(event):
    global lost, count
    lost = False
    count = 0
    score()
    canvas.itemconfig(game, text=" ")

    time.sleep(1)
    Barra.draw()
    Bola.draw()


def score():
    canvas.itemconfig(score_now, text="Pontos: " + str(count))


def game_over():
    canvas.itemconfig(game, text="Game over!")


Barra = Barra(canvas, "orange")
Bola = Bola(canvas, Barra, "purple")

score_now = canvas.create_text(430, 20, text="Pontos: " + str(count), fill="green", font=("Arial", 16))
game = canvas.create_text(400, 300, text=" ", fill="red", font=("Arial", 40))

canvas.bind_all("<Button-1>", start_game)

root.mainloop()


