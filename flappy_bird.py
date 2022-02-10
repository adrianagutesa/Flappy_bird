import turtle

wn = turtle.Screen()
wn.title("Flappy bird by Adriana")
wn.bgcolor("blue")
wn.setup(width=500, height=800)

player = turtle.Turtle()
player.speed(0)
player.penup()
player.color("yellow")
player.shape("turtle")
player.shapesize(stretch_wid=3, stretch_len=3, outline=None)
player.goto(-200, 0)
player.dx=0
player.dy=1

#Main Game Loop
while True:
    #Move player
    y = player.ycor()
    y += player.dy
    player.sety(y)








wn.mainloop()
