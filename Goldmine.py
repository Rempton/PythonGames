import turtle
import random
import math

s = turtle.Screen()
s.title("Gold-Sammelrennen")
s.bgcolor("#111")
s.setup(width=700, height=500)
s.tracer(0)

# Punkte-Stände
score_p1 = 0
score_p2 = 0

# Spieler 1 (Blau)
p1 = turtle.Turtle()
p1.color("cyan")
p1.shape("arrow")
p1.shapesize(1.5)
p1.penup()
p1.goto(-200, 0)

# Spieler 2 (Rot)
p2 = turtle.Turtle()
p2.color("tomato")
p2.shape("arrow")
p2.shapesize(1.5)
p2.penup()
p2.goto(200, 0)
p2.setheading(180)

# Goldklumpen
gold = turtle.Turtle()
gold.color("gold")
gold.shape("circle")
gold.penup()
gold.goto(random.randint(-250, 250), random.randint(-180, 180))

# Anzeigen für den Punktestand
ui = turtle.Turtle()
ui.color("white")
ui.penup()
ui.hideturtle()
ui.goto(0, 200)

def ui_update():
    ui.clear()
    ui.write(f"Blau: {score_p1}  |  Rot: {score_p2}", align="center", font=("Arial", 16, "bold"))

ui_update()

# Steuerung für Spieler 1
def p1_v(): p1.forward(12)
def p1_l(): p1.left(20)
def p1_r(): p1.right(20)

# Steuerung für Spieler 2
def p2_v(): p2.forward(12)
def p2_l(): p2.left(20)
def p2_r(): p2.right(20)

s.listen()
s.onkey(p1_v, "w")
s.onkey(p1_l, "a")
s.onkey(p1_r, "d")
s.onkey(p2_v, "Up")
s.onkey(p2_l, "Left")
s.onkey(p2_r, "Right")

running = True

def loop():
    global score_p1, score_p2, running
    if not running: 
        return
    
    # Bildschirmränder blockieren (damit niemand aus dem Bild fliegt)
    for p in [p1, p2]:
        if p.xcor() > 330: p.setx(330)
        if p.xcor() < -330: p.setx(-330)
        if p.ycor() > 230: p.sety(230)
        if p.ycor() < -230: p.sety(-230)
    
    # Kollision mit Gold prüfen (Abstand messen)
    d1 = math.sqrt((p1.xcor() - gold.xcor())**2 + (p1.ycor() - gold.ycor())**2)
    d2 = math.sqrt((p2.xcor() - gold.xcor())**2 + (p2.ycor() - gold.ycor())**2)
    
    if d1 < 25:
        score_p1 += 1
        gold.goto(random.randint(-250, 250), random.randint(-180, 180))
        ui_update()
    elif d2 < 25:
        score_p2 += 1
        gold.goto(random.randint(-250, 250), random.randint(-180, 180))
        ui_update()
        
    # Sieg prüfen (Wer zuerst 5 Punkte hat)
    if score_p1 >= 5:
        running = False
        ui.goto(0, 0)
        ui.write("BLAU GEWINNT DAS RENNEN! 👑", align="center", font=("Arial", 24, "bold"))
    elif score_p2 >= 5:
        running = False
        ui.goto(0, 0)
        ui.write("ROT GEWINNT DAS RENNEN! 👑", align="center", font=("Arial", 24, "bold"))
        
    s.update()
    # Hier war der Fehler: ontimer statt after benutzen!
    s.ontimer(loop, 20)

# Spiel starten
loop()
turtle.done()
