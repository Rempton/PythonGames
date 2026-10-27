import tkinter as tk
import random
import time

class MeteorShowdownStark:
    def __init__(self, root):
        self.root = root
        self.root.title("Meteoriten-Showdown: ULTRA STABIL")
        self.root.resizable(False, False)
        
        self.b, self.h = 800, 600
        self.canvas = tk.Canvas(root, width=self.b, height=self.h, bg="#050518")
        self.canvas.pack()
        
        # Spieler-Variablen
        self.p1_x, self.p1_speed, self.p1_shield, self.p1_boost = 250, 7, 0, 0
        self.p2_x, self.p2_speed, self.p2_shield, self.p2_boost = 550, 7, 0, 0
        self.y = 540
        self.r = 16 
        
        # Die Spieler-UFOs (Schöne, runde Kreise mit farbiger Kuppel)
        self.o1 = self.canvas.create_oval(self.p1_x-self.r, self.y-self.r, self.p1_x+self.r, self.y+self.r, fill="deep sky blue", outline="white", width=2)
        self.o1_top = self.canvas.create_oval(self.p1_x-8, self.y-14, self.p1_x+8, self.y-2, fill="cyan", outline="")
        
        self.o2 = self.canvas.create_oval(self.p2_x-self.r, self.y-self.r, self.p2_x+self.r, self.y+self.r, fill="gold", outline="white", width=2)
        self.o2_top = self.canvas.create_oval(self.p2_x-8, self.y-14, self.p2_x+8, self.y-2, fill="magenta", outline="")
        
        # Schutzschild-Ringe um die UFOs
        self.shield1_ui = self.canvas.create_oval(0,0,0,0, outline="spring green", width=4, state="hidden")
        self.shield2_ui = self.canvas.create_oval(0,0,0,0, outline="spring green", width=4, state="hidden")
        
        # Text-Anzeigen direkt über den Spielern für die verbleibende Schild-Zeit
        self.p1_timer_text = self.canvas.create_text(0, 0, text="", fill="spring green", font=("Arial", 10, "bold"), state="hidden")
        self.p2_timer_text = self.canvas.create_text(0, 0, text="", fill="spring green", font=("Arial", 10, "bold"), state="hidden")
        
        self.meteors = []
        self.powerups = [] # [x, y, box_id, text_id, typ]
        
        self.game_speed = 4.5
        self.spawn_rate = 0.08
        
        self.tasten = {}
        self.root.bind("<KeyPress>", lambda e: self.tasten.__setitem__(e.keysym.lower(), True))
        self.root.bind("<KeyRelease>", lambda e: self.tasten.__setitem__(e.keysym.lower(), False))
        
        self.running = True
        self.loop()

    def loop(self):
        if not self.running: return
        jetzt = time.time()
        
        # --- SPIELER 1 EFFEKTE & SHIELD TIMER ---
        p1_akt_speed = self.p1_speed * 1.8 if jetzt < self.p1_boost else self.p1_speed
        if jetzt < self.p1_boost:
            self.canvas.itemconfig(self.o1, fill="orange") # Leuchtet orange bei Speed
        else:
            self.canvas.itemconfig(self.o1, fill="deep sky blue")
            
        if jetzt < self.p1_shield:
            restzeit = self.p1_shield - jetzt
            self.canvas.itemconfig(self.shield1_ui, state="normal")
            self.canvas.coords(self.shield1_ui, self.p1_x-self.r-6, self.y-self.r-6, self.p1_x+self.r+6, self.y+self.r+6)
            
            # Text-Timer über Spieler 1 aktualisieren
            self.canvas.itemconfig(self.p1_timer_text, state="normal", text=f"IMMORTAL: {restzeit:.1f}s")
            self.canvas.coords(self.p1_timer_text, self.p1_x, self.y - 30)
        else:
            self.canvas.itemconfig(self.shield1_ui, state="hidden")
            self.canvas.itemconfig(self.p1_timer_text, state="hidden")
            
        # --- SPIELER 2 EFFEKTE & SHIELD TIMER ---
        p2_akt_speed = self.p2_speed * 1.8 if jetzt < self.p2_boost else self.p2_speed
        if jetzt < self.p2_boost:
            self.canvas.itemconfig(self.o2, fill="orange")
        else:
            self.canvas.itemconfig(self.o2, fill="gold")
            
        if jetzt < self.p2_shield:
            restzeit = self.p2_shield - jetzt
            self.canvas.itemconfig(self.shield2_ui, state="normal")
            self.canvas.coords(self.shield2_ui, self.p2_x-self.r-6, self.y-self.r-6, self.p2_x+self.r+6, self.y+self.r+6)
            
            # Text-Timer über Spieler 2 aktualisieren
            self.canvas.itemconfig(self.p2_timer_text, state="normal", text=f"IMMORTAL: {restzeit:.1f}s")
            self.canvas.coords(self.p2_timer_text, self.p2_x, self.y - 30)
        else:
            self.canvas.itemconfig(self.shield2_ui, state="hidden")
            self.canvas.itemconfig(self.p2_timer_text, state="hidden")

        # --- BEWEGUNG ---
        if self.tasten.get("a") and self.p1_x > self.r: self.p1_x -= p1_akt_speed
        if self.tasten.get("d") and self.p1_x < self.b - self.r: self.p1_x += p1_akt_speed
        if self.tasten.get("left") and self.p2_x > self.r: self.p2_x -= p2_akt_speed
        if self.tasten.get("right") and self.p2_x < self.b - self.r: self.p2_x += p2_akt_speed
        
        # UFO-Grafiken mitbewegen
        self.canvas.coords(self.o1, self.p1_x-self.r, self.y-self.r, self.p1_x+self.r, self.y+self.r)
        self.canvas.coords(self.o1_top, self.p1_x-8, self.y-14, self.p1_x+8, self.y-2)
        
        self.canvas.coords(self.o2, self.p2_x-self.r, self.y-self.r, self.p2_x+self.r, self.y+self.r)
        self.canvas.coords(self.o2_top, self.p2_x-8, self.y-14, self.p2_x+8, self.y-2)
        
        # --- SPAWN METEORE & POWERUPS ---
        if random.random() < self.spawn_rate:
            mx = random.randint(15, self.b-15)
            m_id = self.canvas.create_oval(mx-12, -20, mx+12, 4, fill="tomato", outline="dark orange", width=2)
            self.meteors.append([mx, -10, m_id])
            
        if random.random() < 0.012:
            px = random.randint(25, self.b-25)
            typ = random.choice(["shield", "speed"])
            
            if typ == "shield":
                p_id = self.canvas.create_rectangle(px-15, -24, px+15, -2, fill="blue", outline="cyan", width=2)
                t_id = self.canvas.create_text(px, -13, text="[I]", fill="white", font=("Arial", 10, "bold"))
            else:
                p_id = self.canvas.create_rectangle(px-15, -24, px+15, -2, fill="purple", outline="magenta", width=2)
                t_id = self.canvas.create_text(px, -13, text="[S]", fill="white", font=("Arial", 10, "bold"))
                
            self.powerups.append([px, -10, p_id, t_id, typ])
            
        # --- POWER-UPS BEWEGEN ---
        for pu in self.powerups[:]:
            pu += 3
            self.canvas.move(pu, 0, 3)
            self.canvas.move(pu, 0, 3)
            typ = pu
            
            if self.y - self.r <= pu <= self.y + self.r:
                dauer = 5.0
                if abs(pu - self.p1_x) < self.r + 15:
                    if typ == "shield": self.p1_shield = time.time() + dauer
                    else: self.p1_boost = time.time() + dauer
                    self.canvas.delete(pu); self.canvas.delete(pu)
                    self.powerups.remove(pu)
                    continue
                if abs(pu - self.p2_x) < self.r + 15:
                    if typ == "shield": self.p2_shield = time.time() + dauer
                    else: self.p2_boost = time.time() + dauer
                    self.canvas.delete(pu); self.canvas.delete(pu)
                    self.powerups.remove(pu)
                    continue
                    
            if pu > self.h:
                self.canvas.delete(pu); self.canvas.delete(pu)
                self.powerups.remove(pu)

        # --- METEORE BEWEGEN & LINEAR-HITBOX-CHECK ---
        hit1, hit2 = False, False
        for m in self.meteors[:]:
            altes_y = m
            m += self.game_speed
            self.canvas.move(m, 0, self.game_speed)
            
            if altes_y <= self.y + self.r and m >= self.y - self.r:
                if abs(m - self.p1_x) < self.r + 12:
                    if jetzt < self.p1_shield:
                        self.canvas.delete(m)
                        self.meteors.remove(m)
                        continue
                    else: hit1 = True
                    
                if abs(m - self.p2_x) < self.r + 12:
                    if jetzt < self.p2_shield:
                        self.canvas.delete(m)
                        self.meteors.remove(m)
                        continue
                    else: hit2 = True
                
            if m > self.h:
                self.canvas.delete(m)
                self.meteors.remove(m)
                
        self.game_speed += 0.0025
        self.spawn_rate = min(0.35, self.spawn_rate + 0.00004)
        
        # --- GAME OVER ---
        if hit1 or hit2:
            self.running = False
            self.canvas.delete(self.shield1_ui); self.canvas.delete(self.shield2_ui)
            self.canvas.delete(self.p1_timer_text); self.canvas.delete(self.p2_timer_text)
            msg = "SPACE COLLISION!\nUnentschieden." if hit1 and hit2 else ("GELBES UFO GEWINNT! 🛸" if hit1 else "BLAUES UFO GEWINNT! 🛸")
            self.canvas.create_text(400, 300, text=msg, fill="yellow", font=("Arial", 32, "bold"), justify="center")
            return
            
        self.root.after(16, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    spiel = MeteorShowdownStark(root)
    root.mainloop()

