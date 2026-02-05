import tkinter as tk
import random

# ---------------- CONSTANTS ----------------
WIDTH = 400
HEIGHT = 400
CELL = 10
SPEED = 100

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# ---------------- CANVAS ----------------
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ---------------- GAME STATE ----------------
snake = []
direction = "RIGHT"
food_x = food_y = 0
score = 0
game_over = False
paused = False

# ---------------- UI ----------------
score_text = canvas.create_text(10, 10, fill="white",
                                font=("Arial", 12), anchor="nw")

game_over_text = None

# ---------------- FUNCTIONS ----------------
def reset_game():
    global snake, direction, score, game_over, paused
    canvas.delete("all")

    snake = [[200, 200], [190, 200], [180, 200]]
    direction = "RIGHT"
    score = 0
    game_over = False
    paused = False

    place_food()
    update_score()
    move_snake()

def update_score():
    canvas.itemconfig(score_text, text=f"Score: {score}")

def place_food():
    global food_x, food_y
    while True:
        food_x = random.randint(0, 39) * CELL
        food_y = random.randint(0, 39) * CELL
        if [food_x, food_y] not in snake:
            break

def change_direction(event):
    global direction
    opposites = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT": "RIGHT",
        "RIGHT": "LEFT"
    }

    if event.keysym.upper() in opposites:
        new_dir = event.keysym.upper()
        if opposites[new_dir] != direction:
            direction = new_dir

def toggle_pause(event=None):
    global paused
    paused = not paused
    if not paused:
        move_snake()

def move_snake():
    global game_over, score

    if game_over or paused:
        return

    head_x, head_y = snake[0]

    if direction == "UP":
        new_head = [head_x, head_y - CELL]
    elif direction == "DOWN":
        new_head = [head_x, head_y + CELL]
    elif direction == "LEFT":
        new_head = [head_x - CELL, head_y]
    else:
        new_head = [head_x + CELL, head_y]

    # Collision detection
    if (
        new_head in snake or
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT
    ):
        end_game()
        return

    snake.insert(0, new_head)

    if new_head == [food_x, food_y]:
        score += 1
        update_score()
        place_food()
    else:
        snake.pop()

    draw_game()
    window.after(SPEED, move_snake)

def end_game():
    global game_over, game_over_text
    game_over = True
    game_over_text = canvas.create_text(
        WIDTH // 2, HEIGHT // 2 - 20,
        fill="white",
        font=("Arial", 20, "bold"),
        text="GAME OVER"
    )

    canvas.create_text(
        WIDTH // 2, HEIGHT // 2 + 20,
        fill="white",
        font=("Arial", 12),
        text="Press R to Restart"
    )

def draw_game():
    canvas.delete("snake")
    canvas.delete("food")

    # Food
    canvas.create_rectangle(
        food_x, food_y,
        food_x + CELL, food_y + CELL,
        fill="red", tags="food"
    )

    # Snake
    for part in snake:
        canvas.create_rectangle(
            part[0], part[1],
            part[0] + CELL, part[1] + CELL,
            fill="green", tags="snake"
        )

# ---------------- KEY BINDINGS ----------------
window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)
window.bind("p", toggle_pause)
window.bind("r", lambda e: reset_game())

# ---------------- START ----------------
reset_game()
window.mainloop()
