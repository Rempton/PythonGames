import turtle

# Fenster einrichten
s = turtle.Screen()
s.title("Das verlangsamte Schildkröten-Rennen")
s.bgcolor("#111")
s.setup(width=800, height=400)

# Ziellinie zeichnen
ziel = turtle.Turtle()
ziel.speed(0)
ziel.color("white")
ziel.penup()
ziel.goto(300, 150)
ziel.pendown()
ziel.goto(300, -150)
ziel.hideturtle()

# Spieler 1 (Blau)
p1 = turtle.Turtle()
p1.color("cyan")
p1.shape("turtle")
p1.shapesize(2)
p1.penup()
p1.goto(-350, 50)

# Spieler 2 (Rot)
p2 = turtle.Turtle()
p2.color("tomato")
p2.shape("turtle")
p2.shapesize(2)
p2.penup()
p2.goto(-350, -50)

# Text für den Gewinner
text = turtle.Turtle()
text.color("yellow")
text.penup()
text.hideturtle()

gewonnen = False

# --- LANGSAME GESCHWINDIGKEIT ---
# Hier ist der Wert jetzt auf 4 gesetzt, damit es sich langsamer bewegt.
schritt = 4

def p1_vor():
    global gewonnen
    if not gewonnen:
        p1.forward(schritt)
        if p1.xcor() >= 300:
            gewonnen = True
            text.write("SPIELER 1 (BLAU) GEWINNT! 🎉", align="center", font=("Arial", 24, "bold"))

def p2_vor():
    global gewonnen
    if not gewonnen:
        p2.forward(schritt)
        if p2.xcor() >= 300:
            gewonnen = True
            text.write("SPIELER 2 (ROT) GEWINNT! 🎉", align="center", font=("Arial", 24, "bold"))

# Tasten anbinden (Sofortige Reaktion ohne Enter!)
s.listen()
s.onkey(p1_vor, "w")
s.onkey(p2_vor, "Up")

# Das Fenster offen halten
turtle.done()
