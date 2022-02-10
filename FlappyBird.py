import turtle
import time
from random import randint

# Set the screen
screen = turtle.Screen()
screen.title("Flappy bird")
screen.setup(width=500, height=800)
screen.tracer(0)
screen.bgpic('background.gif')
screen.register_shape('ground.gif')
screen.register_shape('bird.gif')
screen.register_shape('pipe-up.gif')
screen.register_shape('pipe-down.gif')

def Save(highscore):
    f = open('score.txt', 'a+')
    f.write("%d\n" % highscore)
    f.close()

def Load():
    f = open('score.txt', 'r')
    maxf = 0

    for line in f:
        if line.strip():
            arr = [int(x) for x in line.strip()]
            maxa = max(arr)
            if maxa > maxf:
                maxf = maxa
    
    z = open('highscore.txt', 'w+')
    z.write("%d\n" % maxf)
    f.close()
    z.close()

    return maxf

class Player(turtle.Turtle): 
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.shape('bird.gif') 
        self.speed(0)
        self.goto(-200, 0)
        self.dx = 0
        self.dy = 1
        self.score = 0
    
    def move(self):
        y = self.ycor()
        y += self.dy
        self.sety(y)

        # Bottom Border
        if self.ycor() < -240:
            self.dy = 0
            self.sety(-240)

    def jump(self):
        self.dy += 6

        # Border check
        if self.dy > 6:
            self.dy = 6 

class Pipe_Top(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.dx = -6
        self.PIPE_TOP = self.shape('pipe-up.gif')
        self.value = 1

    def move(self):
        x = self.xcor()
        x += self.dx
        self.setx(x) 
    
class Pipe_Bottom(turtle.Turtle):
    GAP = 460

    def __init__(self, other):
        turtle.Turtle.__init__(self)
        self.penup()
        self.speed(0)
        self.dx = -6
        self.PIPE_BOTTOM = self.shape('pipe-down.gif')
        self.set_height(other)

    def set_height(self, other):
        a = 400 
        b = randint(200, 400)
        other.goto(a, b)
        self.goto(a, (b - self.GAP))

    def move(self, other):
        x = self.xcor()
        x += self.dx
        self.setx(x)
  
        # Show another pipe
        if other.xcor() < -300:
            n = randint(200, 400)
            other.goto(400, n)
            self.goto(400, (n - self.GAP))
            other.value = 1

class Pen(turtle.Turtle):
     def __init__(self, other):
        turtle.Turtle.__init__(self)
        self.speed(0)
        self.hideturtle()
        self.penup()
        self.color("white")
        self.goto(0, 0)
        self.write("Press S to start", move=False, align="center", font=("Arial", 32, "bold"))
        self.goto(0, -50)
        self.s = Load()
        self.write("Highscore: %d" % self.s, move=False, align="center", font=("Arial", 25, "normal"))
    
start = False

def start_game():
    global start
    pen.clear()
    start = True

def exit_game():
    screen.bye()

def Collisions():
    if (player.xcor() + 10 > pipe_top.xcor() - 30) and (player.xcor() - 10 < pipe_top.xcor() + 30):
            if (player.ycor() + 10 > pipe_top.ycor() - 180) or (player.ycor() - 10 < pipe_bottom.ycor() + 180):
                Save(player.score)
                pen.clear()
                time.sleep(1)

                pen.penup()
                pen.setposition(0, 100)
                pen.pendown()
                pen.write("Game Over", move=False, align="center", font=("Arial", 50, "bold"))

                pen.penup()
                pen.setposition(-75, 0)
                pen.pendown()
                pen.write("RESTART", move=False, align="center", font=("Arial", 20, "bold"))

                pen.penup()
                pen.setposition(0, 50)
                pen.pendown()
                pen.write("Score: %d" % player.score, move=False, align="center", font=("Arial", 20, "normal"))

                pen.penup()
                pen.setposition(90, 0)
                pen.pendown()
                pen.write("EXIT", move=False, align="center", font=("Arial", 20, "bold"))

                canvas = screen.getcanvas()
                canvas.bind('<Motion>', onTextClick)

                global start
                start = False
                     
def Reset():
    global start
    start = True

    player.score = 0

    # Move Pipes Back
    pipe_top.setx(450)
    pipe_bottom.setx(450)

    # Move Player back
    player.goto(-200, 0)
    player.dy = 0

    # Reset the pen
    pen.penup()
    pen.clear()
    pen.goto(0, 250)
    pen.write("0", move=False, align="center", font=("Arial", 32, "bold"))

def Current_score():
    if pipe_top.xcor() + 30 < player.xcor() - 10:
        player.score += pipe_top.value
        pipe_top.value = 0
        pen.goto(0, 250)
        pen.clear()
        pen.write(player.score, move=False, align="left", font=("Arial", 32, "bold"))

def onTextClick(event):
    x, y = event.x, event.y
    if (x >= 113 and x <= 188) and ( y >= 375 and y <= 395):
        screen.onscreenclick(lambda x, y: Reset())
    if (x >= 300 and x <= 385) and ( y >= 375 and y <= 395):
        screen.onscreenclick(lambda x, y: exit_game())


# Create class instances
player = Player()
pipe_top = Pipe_Top()
pipe_bottom = Pipe_Bottom(pipe_top)
pen = Pen(player)

# Set keyboard bindings
screen.listen() 
screen.onkey(player.jump, "space")
screen.onkeypress(start_game, "s")
screen.onkeypress(start_game, "S")

# Making sure bird is going down
gravity = -0.2

# Ground
ground = turtle.Turtle()
ground.speed(0)
ground.penup()
ground.shape('ground.gif')
ground.goto(0, -350)


# Main game loop
while True:
    if start == False:
        screen.update()
    elif start == True:
        # Pause - moving the bird
        time.sleep(0.01)
    
        # Update the screen
        screen.update()

        # Move player
        player.move()
        player.dy += gravity

        # Move the pipes
        pipe_top.move()
        pipe_bottom.move(pipe_top)
     
        # Check for collisions
        Collisions()

        # Check for score        
        Current_score()  

screen.mainloop()
