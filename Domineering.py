import turtle

s = turtle.Screen()
s.title("Domineering: Der Blockade-Krieg")
s.bgcolor("#111")
s.setup(width=900, height=600)  # Fenster etwas breiter für die Erklärung
s.tracer(0)

# 6x6 Grid erzeugen
grid = {}
for x in range(-50, 201, 50):  # Spielfeld nach rechts verschoben, um Platz für Text zu machen
    for y in range(-125, 126, 50):
        grid[(x, y)] = "free"

# Spieler-Cursor
p1 = turtle.Turtle(); p1.color("cyan"); p1.shape("square"); p1.shapesize(1, 2.2); p1.penup(); p1.goto(-50, 125)
p2 = turtle.Turtle(); p2.color("tomato"); p2.shape("square"); p2.shapesize(2.2, 1); p2.penup(); p2.goto(200, -125)

dw = turtle.Turtle(); dw.hideturtle(); dw.speed(0)

# Statische Erklärung auf der linken Seite zeichnen
anleitung = turtle.Turtle()
anleitung.color("white")
anleitung.penup()
anleitung.hideturtle()
anleitung.goto(-420, 150)
anleitung.write(
    "📜 ANLEITUNG & REGELN:\n"
    "-------------------------\n"
    "Ziel ist es, den Gegner so zu\n"
    "blockieren, dass er keinen Stein\n"
    "mehr platzieren kann.\n\n"
    "🔵 SPIELER 1 (Cyan):\n"
    "• Setzt HORIZONTALE Steine (1x2)\n"
    "• Steuerung: W, A, S, D\n"
    "• Platzieren: LEERTASTE\n\n"
    "🔴 SPIELER 2 (Rot):\n"
    "• Setzt VERTIKALE Steine (2x1)\n"
    "• Steuerung: Pfeiltasten\n"
    "• Platzieren: ENTER\n\n"
    "Achtung: Steine dürfen niemals\n"
    "übereinander gelegt werden!",
    align="left", font=("Arial", 11, "normal")
)

def draw_board():
    dw.clear()
    for (gx, gy), status in grid.items():
        dw.penup(); dw.goto(gx-22, gy-22); dw.pendown()
        if status == "free": dw.color("gray")
        else: dw.color(status)
        dw.begin_fill()
        for _ in range(4): dw.forward(44); dw.left(90)
        if status == "cyan": dw.fillcolor("#003366")
        elif status == "tomato": dw.fillcolor("#661111")
        else: dw.fillcolor("#222")
        dw.end_fill()

turn = 1
ui = turtle.Turtle(); ui.color("white"); ui.penup(); ui.hideturtle(); ui.goto(75, 220)

def update_ui():
    ui.clear()
    wer = "BLAU (Horizontal)" if turn == 1 else "ROT (Vertikal)"
    ui.write(f"Am Zug: {wer}", align="center", font=("Arial", 14, "bold"))

update_ui()

def move_p(spieler, dx, dy):
    if spieler != turn: return
    p = p1 if spieler == 1 else p2
    nx, ny = p.transform_x() if hasattr(p, "transform_x") else p.xcor() + dx, p.transform_y() if hasattr(p, "transform_y") else p.ycor() + dy
    if -50 <= nx <= 200 and -125 <= ny <= 125:
        p.goto(nx, ny)
        s.update()

def place(spieler):
    global turn
    if spieler != turn: return
    p = p1 if spieler == 1 else p2
    x, y = round(p.xcor()), round(p.ycor())
    
    if spieler == 1: # Horizontal: Teste Feld und rechtes Nachbarfeld
        f1, f2 = (x, y), (x + 50, y)
        if x < 200 and grid.get(f1) == "free" and grid.get(f2) == "free":
            grid[f1] = grid[f2] = "cyan"
            turn = 2
    else: # Vertikal: Teste Feld und unteres Nachbarfeld
        f1, f2 = (x, y), (x, y - 50)
        if y > -125 and grid.get(f1) == "free" and grid.get(f2) == "free":
            grid[f1] = grid[f2] = "tomato"
            turn = 1
            
    draw_board()
    update_ui()
    s.update()
    win_check()

def win_check():
    has_move = False
    for (gx, gy), status in grid.items():
        if turn == 1:
            if gx < 200 and grid[(gx, gy)] == "free" and grid[(gx+50, gy)] == "free": has_move = True
        else:
            if gy > -125 and grid[(gx, gy)] == "free" and grid[(gx, gy-50)] == "free": has_move = True
            
    if not has_move:
        ui.goto(75, 0)
        winner = "ROT (Vertikal)" if turn == 1 else "BLAU (Horizontal)"
        ui.write(f"KEINE ZÜGE MEHR MÖGLICH!\n🏆 {winner} GEWINNT! 🏆", align="center", font=("Arial", 20, "bold"))

s.listen()
s.onkey(lambda: move_p(1, 0, 50), "w"); s.onkey(lambda: move_p(1, 0, -50), "s")
s.onkey(lambda: move_p(1, -50, 0), "a"); s.onkey(lambda: move_p(1, 50, 0), "d")
s.onkey(lambda: place(1), "space")

s.onkey(lambda: move_p(2, 0, 50), "Up"); s.onkey(lambda: move_p(2, 0, -50), "Down")
s.onkey(lambda: move_p(2, -50, 0), "Left"); s.onkey(lambda: move_p(2, 50, 0), "Right")
s.onkey(lambda: place(2), "Return")

draw_board()
s.update()
turtle.done()
