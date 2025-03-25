import pygame
import random
import time
import tkinter
from tkinter import simpledialog
import sqlite3

# Inicializace Pygame
pygame.init()
pygame.font.init()

# Nastavení okna
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Vytvoří herní okno
pygame.display.set_caption("Hra na hada")  # Nastaví titulek okna

# Barvy
GREEN = (0, 125, 0)  
BLACK = (0, 0, 0)  
RED = (255, 0, 0)  
BLUE = (0, 0, 255)  
WHITE = (255, 255, 255)  
GREY = (128, 128, 128)  

# Velikost hada a jídla
SNAKE_SIZE = 20  # Velikost jednoho segmentu hada
FOOD_SIZE = 20  # Velikost jídla

# Proměnné hry
Hra = True  # Řídí běh hry
speed_boost_active = False  # Stav speed boostu
MAX_SCORES = 5    # Maximální počet záznamů ve scoreboardu

# Inicializace databáze
def init_database():
    """Inicializuje databázovou tabulku pro scoreboard"""
    conn = sqlite3.connect('snake_scoreboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scoreboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            game_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Funkce pro načtení scoreboardu
def load_scoreboard():
    """Načte žebříček skóre z databáze"""
    conn = sqlite3.connect('snake_scoreboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT player_name, score FROM scoreboard 
        ORDER BY score DESC 
        LIMIT ?
    ''', (MAX_SCORES,))
    scoreboard = cursor.fetchall()
    conn.close()
    return scoreboard

# Funkce pro uložení scoreboardu
def save_scoreboard(name, score):
    """Uloží nové skóre do databáze"""
    conn = sqlite3.connect('snake_scoreboard.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scoreboard (player_name, score) 
        VALUES (?, ?)
    ''', (name, score))
    conn.commit()
    conn.close()

# Funkce pro získání jména hráče
def get_player_name():
    """Získá jméno hráče pomocí dialogového okna."""
    # Použije simpledialog z tkinter
    root = tkinter.Tk()  # Vytvoří dočasné okno tkinter
    root.withdraw()    # Skryje hlavní okno tkinter
    name = simpledialog.askstring("Zadejte jméno", "Jaké je vaše jméno?")  # Zobrazí dialogové okno pro zadání jména
    root.destroy()  # Zavře dočasné okno tkinter
    return name if name else "Anonym"  # Vrátí jméno nebo "Anonym"

# Funkce pro uložení nového skóre
def save_new_score(score):
    """Uloží nové skóre do scoreboardu"""
    name = get_player_name()  # Získá jméno hráče
    save_scoreboard(name, score)  # Uloží skóre

# Funkce pro zobrazení menu
def show_menu():
    """Zobrazí hlavní menu hry"""
    screen.fill(GREEN)    # Nastaví pozadí na zelené
    font_title = pygame.font.SysFont("Arial", 30)  # Nastaví font pro titul
    font_button = pygame.font.SysFont("Arial", 20)  # Nastaví font pro tlačítka

    title_text = font_title.render("Hra na hada", True, BLACK)  # Vykreslí text titulu
    title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 4))  # Získá obdélník titulu a vycentruje ho

    start_button_text = font_button.render("Spustit hru", True, BLACK)  # Vykreslí text tlačítka "Spustit hru"
    start_button_rect = start_button_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Získá obdélník tlačítka a vycentruje ho
    start_button = pygame.Rect(start_button_rect.left - 10, start_button_rect.top - 5, start_button_rect.width + 20, start_button_rect.height + 10)  # Vytvoří obdélník pro tlačítko

    scoreboard_button_text = font_button.render("Scoreboard", True, BLACK)  # Vykreslí text tlačítka "Scoreboard"
    scoreboard_button_rect = scoreboard_button_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
    scoreboard_button = pygame.Rect(scoreboard_button_rect.left - 10, scoreboard_button_rect.top - 5, scoreboard_button_rect.width + 20, scoreboard_button_rect.height + 10)

    quit_button_text = font_button.render("Ukončit", True, BLACK)  # Vykreslí text tlačítka "Ukončit"
    quit_button_rect = quit_button_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 100))
    quit_button = pygame.Rect(quit_button_rect.left - 10, quit_button_rect.top - 5, quit_button_rect.width + 20, quit_button_rect.height + 10)

    screen.blit(title_text, title_rect)  # Vykreslí titul
    pygame.draw.rect(screen, WHITE, start_button)  # Vykreslí tlačítko "Spustit hru"
    screen.blit(start_button_text, start_button_rect)  # Vykreslí text na tlačítku
    pygame.draw.rect(screen, WHITE, scoreboard_button)  # Vykreslí tlačítko "Scoreboard"
    screen.blit(scoreboard_button_text, scoreboard_button_rect)
    pygame.draw.rect(screen, WHITE, quit_button)  # Vykreslí tlačítko "Ukončit"
    screen.blit(quit_button_text, quit_button_rect)

    pygame.display.update()  # Aktualizuje obrazovku

    while True:
        for event in pygame.event.get():  # Prochází všechny události
            if event.type == pygame.QUIT:  # Pokud je událost typu QUIT (zavření okna)
                pygame.quit()  # Ukončí Pygame
                return  # Ukončí funkci show_menu
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Pokud je událost kliknutí myši
                if start_button.collidepoint(event.pos):  # Pokud bylo kliknuto na tlačítko "Spustit hru"
                    start_game()  # Zavolá funkci pro spuštění hry
                    return
                elif scoreboard_button.collidepoint(event.pos):  # Pokud bylo kliknuto na tlačítko "Scoreboard"
                    show_scoreboard()
                    return
                elif quit_button.collidepoint(event.pos):  # Pokud bylo kliknuto na tlačítko "Ukončit"
                    pygame.quit()
                    return

# Funkce pro zobrazení scoreboardu
def show_scoreboard():
    """Zobrazí žebříček skóre"""
    screen.fill(GREEN)    # Nastaví pozadí
    font_title = pygame.font.SysFont("Arial", 30)
    font_header = pygame.font.SysFont("Arial", 20, bold=True)  # Tučný font pro hlavičku
    font_score = pygame.font.SysFont("Arial", 16)
    back_button_font = pygame.font.SysFont("Arial", 14)

    title_text = font_title.render("Hra na hada", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH / 2, HEIGHT / 8))

    header_text = font_header.render("Scoreboard:", True, BLACK)
    header_rect = header_text.get_rect(center=(WIDTH / 2, HEIGHT / 8 + 40))

    screen.blit(title_text, title_rect)
    screen.blit(header_text, header_rect)

    scoreboard = load_scoreboard()  # Načte skóre
    y_offset = HEIGHT / 8 + 70  # Počáteční pozice pro vykreslování skóre
    for i, (name, score) in enumerate(scoreboard, 1):  # Prochází skóre a indexuje od 1
        score_text = font_score.render(f"{i}. {name}: {score}", True, BLACK)  # Vytvoří text s pořadím, jménem a skóre
        score_rect = score_text.get_rect(center=(WIDTH / 2, y_offset))  # Vycentruje text
        screen.blit(score_text, score_rect)  # Vykreslí text
        y_offset += 20  # Posune pozici pro další skóre

    back_button_text = back_button_font.render("Zpět do menu", True, BLACK)
    back_button_rect = back_button_text.get_rect(center=(WIDTH / 2, HEIGHT * 7/8))
    back_button = pygame.Rect(back_button_rect.left - 10, back_button_rect.top - 5, back_button_rect.width + 20, back_button_rect.height + 10)
    pygame.draw.rect(screen, WHITE, back_button)
    screen.blit(back_button_text, back_button_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    show_menu()
                    return

# Funkce pro spuštění hry
def start_game():
    """Spustí hru"""
    global Hra
    Hra = True
    play()

# Funkce pro hru
def play():
    """Spustí samotnou hru hada"""
    global Hra, delay, screen
    Hra = True
    delay = 0.15  # Počáteční rychlost hry
    min_delay = 0.05  # Minimální rychlost hry
    score = 0  # Počáteční skóre
    snake_body = [(WIDTH / 2, HEIGHT / 2)]  # Počáteční pozice hada (uprostřed obrazovky)
    snake_direction = "stop"  # Počáteční směr hada

    # Pozice jídla
    food_pos = (random.randint(0, (WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
                random.randint(0, (HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)

    # Pozice speciálního jídla
    blue_food_pos = (random.randint(0, (WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
                    random.randint(0, (HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)

    font = pygame.font.SysFont("Courier", 24)  # Font pro zobrazení skóre

    def draw_snake(snake_body):
        """Vykreslí hada na obrazovku"""
        for i, (x, y) in enumerate(snake_body):
            if i == 0:
                pygame.draw.rect(screen, BLACK, (x, y, SNAKE_SIZE, SNAKE_SIZE))  # Hlava je černá
            else:
                pygame.draw.rect(screen, GREY, (x, y, SNAKE_SIZE, SNAKE_SIZE))  # Tělo je šedé

    def draw_food(pos, color):
        """Vykreslí jídlo na obrazovku"""
        pygame.draw.rect(screen, color, (pos[0], pos[1], FOOD_SIZE, FOOD_SIZE))

    def display_score(score):
        """Zobrazí skóre na obrazovce"""
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (0, 0))

    def move_snake(snake_body, snake_direction):
        """Posune hada v daném směru"""
        x, y = snake_body[0]  # Získá pozici hlavy hada
        if snake_direction == "up":
            y -= SNAKE_SIZE
        elif snake_direction == "down":
            y += SNAKE_SIZE
        elif snake_direction == "left":
            x -= SNAKE_SIZE
        elif snake_direction == "right":
            x += SNAKE_SIZE
        new_head = (x, y)  # Nová pozice hlavy
        return [new_head] + snake_body[:-1]  # Přidá novou hlavu a odstraní poslední segment těla

    def check_collision(snake_body):
        """Zkontroluje, zda had nenarazil do sebe nebo do okraje"""
        x, y = snake_body[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:  # Kontrola okraje
            return True
        for segment in snake_body[1:]:  # Kontrola kolize se sebou samým
            if x == segment[0] and y == segment[1]:
                return True
        return False

    def reset_game():
        """Resetuje herní stav po smrti."""
        global Hra
        Hra = True

    def speed_boost():
        """Aktivuje dočasný speed boost"""
        global delay, speed_boost_active
        if not speed_boost_active:
            speed_boost_active = True
            temp_delay = delay
            delay = 0.05
            pygame.time.set_timer(pygame.USEREVENT, 5000)  # Nastavíme timer na 5 sekund

    def reset_speed(original_delay):
        """Resetuje rychlost hry po uplynutí speed boostu"""
        global delay, speed_boost_active
        delay = original_delay
        speed_boost_active = False
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Vypneme timer

    # Hlavní herní smyčka
    while Hra:
        screen.fill(GREEN)  # Vyplní obrazovku zelenou barvou
        for event in pygame.event.get():  # Prochází všechny události
            if event.type == pygame.QUIT:  # Pokud je událost typu QUIT (zavření okna)
                pygame.quit()  # Ukončí Pygame
                return  # Ukončí hru
            elif event.type == pygame.KEYDOWN:  # Pokud je událost stisknutí klávesy
                if event.key == pygame.K_w and snake_direction != "down":  # Pokud je stisknuto 'w' a had nejede dolů
                    snake_direction = "up"  # Změní směr na nahoru
                elif event.key == pygame.K_s and snake_direction != "up":
                    snake_direction = "down"
                elif event.key == pygame.K_a and snake_direction != "right":
                    snake_direction = "left"
                elif event.key == pygame.K_d and snake_direction != "left":
                    snake_direction = "right"
            elif event.type == pygame.USEREVENT:  # Event pro konec speed boostu
                reset_speed(0.15)

        snake_body = move_snake(snake_body, snake_direction)  # Posune hada

        if check_collision(snake_body):  # Zkontroluje kolize
            time.sleep(1)
            save_new_score(score)
            Hra = False  # Nastavíme Hra na False, ale neukončujeme hru
            reset_game()
            break  # Přerušíme herní smyčku, zobrazí se menu

        if snake_body[0] == food_pos:  # Pokud had sní jídlo
            snake_body.append(snake_body[-1])  # Prodluž hada
            food_pos = (random.randint(0, (WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,  # Vygeneruj nové jídlo
                        random.randint(0, (HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)
            score += 10  # Zvýš skóre
            delay = max(min_delay, delay - 0.001)  # Zrychli hru

        if snake_body[0] == blue_food_pos:  # Pokud had sní modré jídlo
            blue_food_pos = (random.randint(0, (WIDTH - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE,
                            random.randint(0, (HEIGHT - FOOD_SIZE) // FOOD_SIZE) * FOOD_SIZE)
            speed_boost()  # Aktivuj speed boost

        draw_snake(snake_body)  # Vykresli hada
        draw_food(food_pos, RED)  # Vykresli jídlo
        draw_food(blue_food_pos, BLUE)
        display_score(score)  # Zobraz skóre
        pygame.display.update()  # Aktualizuj obrazovku
        time.sleep(delay)  # Zpoždění pro řízení rychlosti hry
    show_menu()  # Po skončení hry (smyčky) zobrazíme menu

if __name__ == "__main__":
    # Inicializace databáze před spuštěním hry
    init_database()
    show_menu()  # Spustí menu při spuštění programu