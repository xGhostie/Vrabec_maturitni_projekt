import os
import random
import turtle
import time
import tkinter as tk
from tkinter import simpledialog

Hra = False
speed_boost_active = False

SCORE_FILE = "text.txt"
MAX_SCORES = 5  # Maximální počet záznamů ve scoreboardu

def load_scoreboard():
    """Načte žebříček skóre ze souboru"""
    if not os.path.exists(SCORE_FILE):
        return []

    with open(SCORE_FILE, "r") as file:
        lines = file.readlines()

    scoreboard = []
    for line in lines:
        parts = line.strip().split(":")
        if len(parts) == 2:
            try:
                name, score = parts[0], int(parts[1])
                scoreboard.append((name, score))
            except ValueError:
                continue  # Ignorujeme neplatné řádky

    return sorted(scoreboard, key=lambda x: x[1], reverse=True)[:MAX_SCORES]

def save_scoreboard(scoreboard):
    """Uloží žebříček skóre do souboru"""
    with open(SCORE_FILE, "w") as file:
        for name, score in scoreboard:
            file.write(f"{name}:{score}\n")

def get_player_name():
    """Získá jméno hráče pomocí dialogového okna."""
    root = tk.Tk()
    root.withdraw()  # Skryje hlavní okno Tkinteru
    name = simpledialog.askstring("Zadejte jméno", "Jaké je vaše jméno?")
    root.destroy() #zavreme okno po zadani jmena
    return name if name else "Anonym"

def save_new_score(score):
    """Uloží nové skóre do scoreboardu"""
    name = get_player_name()
    scoreboard = load_scoreboard()
    scoreboard.append((name, score))
    save_scoreboard(sorted(scoreboard, key=lambda x: x[1], reverse=True)[:MAX_SCORES])

def show_menu():
    """Zobrazí hlavní menu hry"""
    print("Menu is showing...")
    root = tk.Tk()
    root.title("Menu Hry")
    root.geometry("400x400")

    tk.Label(root, text="Hra na hada", font=("Arial", 20)).pack(pady=10)
    tk.Button(root, text="Spustit hru", font=("Arial", 14), command=lambda: start_game(root)).pack(pady=10)
    tk.Button(root, text="Scoreboard", font=("Arial", 14), command=lambda: show_scoreboard(root)).pack(pady=10)
    tk.Button(root, text="Ukončit", font=("Arial", 14), command=root.quit).pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", root.destroy) # Zmeneno na destroy #zavreme okno po kliknuti na X
    root.mainloop()

def show_scoreboard(root):
    """Zobrazí žebříček skóre"""
    root.destroy()
    new_root = tk.Tk()
    new_root.title("Scoreboard")
    new_root.geometry("400x400")
    
    scoreboard = load_scoreboard()
    tk.Label(new_root, text="Hra na hada", font=("Arial", 20)).pack(pady=10)
    tk.Label(new_root, text="Scoreboard:", font=("Arial", 14, "bold")).pack(pady=5)
    
    for i, (name, score) in enumerate(scoreboard, 1):
        tk.Label(new_root, text=f"{i}. {name}: {score}", font=("Arial", 12)).pack()

    tk.Button(new_root, text="Zpět do menu", font=("Arial", 14), command=lambda: close_and_show_menu(new_root)).pack(pady=10)
    new_root.protocol("WM_DELETE_WINDOW", new_root.destroy) # Přidáno pro správné zavření okna #zavreme okno po kliknuti na X
    new_root.mainloop()

def close_and_show_menu(root):
    """Zavře okno a zobrazí hlavní menu"""
    root.destroy()
    show_menu()

def start_game(root):
    """Spustí hru"""
    global Hra
    root.destroy()
    Hra = True
    play()

def play():
    """Spustí samotnou hru hada"""
    global Hra
    global delay
    global screen

    delay = 0.15
    min_delay = 0.05  # Minimalni hodnota delay
    score = 0
    segments = []
    
    screen = turtle.Screen()
    screen.title("Hra na hada")
    screen.bgcolor("green")
    screen.setup(width=600, height=600)
    screen.tracer(0)  # Vypne automatické vykreslování

    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "stop"

    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)

    blue_food = turtle.Turtle()
    blue_food.speed(0)
    blue_food.shape("circle")
    blue_food.color("blue")
    blue_food.penup()
    blue_food.goto(random.randint(-280, 280), random.randint(-280, 280))

    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

    def go_up():
        """Pohyb hada nahoru"""
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        """Pohyb hada dolů"""
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        """Pohyb hada doleva"""
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        """Pohyb hada doprava"""
        if head.direction != "left":
            head.direction = "right"

    def move():
        """Posune hada podle jeho směru"""
        if head.direction == "up":
            head.sety(head.ycor() + 20)
        elif head.direction == "down":
            head.sety(head.ycor() - 20)
        elif head.direction == "left":
            head.setx(head.xcor() - 20)
        elif head.direction == "right":
            head.setx(head.xcor() + 20)

    screen.listen()  # Začne poslouchat stisk kláves
    screen.onkeypress(go_up, "w")
    screen.onkeypress(go_down, "s")
    screen.onkeypress(go_left, "a")
    screen.onkeypress(go_right, "d")

    while Hra:
        screen.update()  # Ruční aktualizace obrazovky

        # Kontrola kolize s okrajem
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
            time.sleep(1)
            save_new_score(score)
            Hra = False
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)  # Schová segmenty mimo obrazovku
            segments.clear()
            screen.bye() #zavreme turtle okno
            show_menu()
            return

        # Kontrola kolize s jídlem
        if head.distance(food) < 20:
            x, y = random.randint(-280, 280), random.randint(-280, 280)
            food.goto(x, y)
            
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            delay = max(min_delay, delay - 0.001)  # Zajistí, že delay neklesne pod min_delay
            score += 10
            pen.clear()
            pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

        # Kontrola kolize s modrým jídlem (speed boost)
        if head.distance(blue_food) < 20:
            x, y = random.randint(-280, 280), random.randint(-280, 280)
            blue_food.goto(x, y)
            speed_boost()

        # Pohyb segmentů hada
        for index in range(len(segments) - 1, 0, -1):
            segments[index].goto(segments[index - 1].pos())
        if segments:
            segments[0].goto(head.pos())

        move()  # Pohyb hlavy hada

        # Kontrola kolize hada sama se sebou
        if any(segment.distance(head) < 20 for segment in segments):
            time.sleep(1)
            save_new_score(score)
            Hra = False
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            screen.bye() #zavreme turtle okno
            show_menu()
            return

        time.sleep(delay)  # Řízení rychlosti hry

def reset_game():
    """Resetuje herní stav po smrti."""
    global Hra
    Hra = False

def speed_boost():
    """Aktivuje dočasný speed boost"""
    global delay, speed_boost_active, screen
    if not speed_boost_active:
        speed_boost_active = True
        temp_delay = delay  # Uloží původní delay
        delay = 0.05  # Nastaví nový delay pro speed boost
        screen.ontimer(lambda: reset_speed(temp_delay), 5000)  # Po 5 sekundách resetuje rychlost

def reset_speed(original_delay):
    """Resetuje rychlost hry po uplynutí speed boostu"""
    global delay, speed_boost_active
    delay = original_delay  # Obnoví původní delay
    speed_boost_active = False

if __name__ == "__main__":
    show_menu()  # Spustí hlavní menu hry

    #ondra husak  je nigga
    
