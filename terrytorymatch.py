import turtle
import math

s = turtle.Screen()
s.title("Hex-Invasion: Taktik-Match")
s.bgcolor("#111")
s.setup(width=700, height=600)
s.tracer(0)

# Spielfeld-Zellen generieren
felder = {}
for x in range(-200, 201, 100):
    for y in range(-200, 201, 100):
        felder[(x, y)] = "gray"

# Spieler laden
p1 = turtle.Turtle()
p1.color("cyan")
p1.shape("circle")
p1.shapesize(1.8)
p1.penup()
p1.goto(-200, -200)

p2 = turtle.Turtle()
p2.color("tomato")
p2.shape("circle")
p2.shapesize(1.8)
p2.penup()
p2.goto(200, 200)

felder[(-200, -200)] = "cyan"
felder[(200, 200)] = "tomato"

# Zeichner für das Raster
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.pensize(2)

def raster_zeichnen():
    drawer.clear()
    for (fx, fy), farbe in felder.items():
        drawer.penup()
        drawer.goto(fx - 40, fy - 40)
        drawer.pendown()
        drawer.color(farbe)
        drawer.begin_fill()
        for _ in range(4):
            drawer.forward(80)
            drawer.left(90)
        if farbe != "gray":
            drawer.fillcolor(farbe)
            drawer.end_fill()

# Steuerung (Bewegen im 100er Raster)
def p1_u(): p1.sety(min(200, p1.ycor() + 100)); feld_check(p1, "cyan")
def p1_d(): p1.sety(max(-200, p1.ycor() - 100)); feld_check(p1, "cyan")
def p1_l(): p1.setx(max(-200, p1.xcor() - 100)); feld_check(p1, "cyan")
def p1_d_r(): p1.setx(min(200, p1.xcor() + 100)); feld_check(p1, "cyan")

def p2_u(): p2.sety(min(200, p2.ycor() + 100)); feld_check(p2, "tomato")
def p2_d(): p2.sety(max(-200, p2.ycor() - 100)); feld_check(p2, "tomato")
def p2_l(): p2.setx(max(-200, p2.xcor() - 100)); feld_check(p2, "tomato")
def p2_r(): p2.setx(min(200, p2.xcor() + 100)); feld_check(p2, "tomato")

def feld_check(p, farbe):
    px, py = round(p.xcor()), round(p.ycor())
    if (px, py) in felder:
        felder[(px, py)] = farbe

s.listen()
s.onkey(p1_u, "w"); s.onkey(p1_d, "s"); s.onkey(p1_l, "a"); s.onkey(p1_d_r, "d")
s.onkey(p2_u, "Up"); s.onkey(p2_d, "Down"); s.onkey(p2_l, "Left"); s.onkey(p2_r, "Right")

ui = turtle.Turtle()
ui.color("white")
ui.penup()
ui.hideturtle()
ui.goto(0, 260)

start_time = turtle.time.time()
running = True

def loop():
    global running
    if not running: return
    
    verbleibend = max(0, int(15 - (turtle.time.time() - start_time)))
    
    # Punkte zählen
    c1 = list(felder.values()).count("cyan")
    c2 = list(felder.values()).count("tomato")
    
    ui.clear()
    ui.write(f"Blau: {c1} | Rot: {c2}  ---  Zeit: {verbleibend}s", align="center", font=("Arial", 14, "bold"))
    
    raster_zeichnen()
    
    if verbleibend <= 0:
        running = False
        ui.goto(0, 0)
        win = "BLAU GEWINNT DIE INVASION! 👑" if c1 > c2 else ("ROT GEWINNT DIE INVASION! 👑" if c2 > c1 else "UNENTSCHIEDEN! 🤝")
        ui.write(f"ZEIT ABGELAUFEN!\n{win}", align="center", font=("Arial", 20, "bold"))
        s.update()
        return

    s.update()
    s.ontimer(loop, 50)

loop()
turtle.done()
