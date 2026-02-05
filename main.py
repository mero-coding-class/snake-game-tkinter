import tkinter as tk
import random

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# ---------------- CANVAS ----------------
WIDTH = 400
HEIGHT = 400
canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# ---------------- SNAKE ----------------
snake = [[200, 200], [190, 200], [180, 200]]
direction = "RIGHT"

# ---------------- FOOD ----------------
food_x = random.randint(0, 39) * 10
food_y = random.randint(0, 39) * 10

# ---------------- GAME DATA ----------------
score = 0
game_over = False

# ---------------- TEXT ----------------
score_text = canvas.create_text(50, 10, fill="white", text="Score: 0", anchor="nw")

# ---------------- FUNCTIONS ----------------
def change_direction(event):
    global direction
    if event.keysym == "Up":
        direction = "UP"
    elif event.keysym == "Down":
        direction = "DOWN"
    elif event.keysym == "Left":
        direction = "LEFT"
    elif event.keysym == "Right":
        direction = "RIGHT"

def move_snake():
    global food_x, food_y, score, game_over

    if game_over:
        canvas.create_text(200, 200, fill="white", text="GAME OVER", font=("Arial", 20))
        return

    head_x, head_y = snake[0]

    if direction == "UP":
        new_head = [head_x, head_y - 10]
    elif direction == "DOWN":
        new_head = [head_x, head_y + 10]
    elif direction == "LEFT":
        new_head = [head_x - 10, head_y]
    else:
        new_head = [head_x + 10, head_y]

    # Game over conditions
    if (new_head in snake or
        new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT):
        game_over = True
        move_snake()
        return

    snake.insert(0, new_head)

    # Eat food
    if new_head[0] == food_x and new_head[1] == food_y:
        score += 1
        canvas.itemconfig(score_text, text="Score: " + str(score))
        food_x = random.randint(0, 39) * 10
        food_y = random.randint(0, 39) * 10
    else:
        snake.pop()

    draw_game()
    window.after(100, move_snake)

def draw_game():
    canvas.delete("all")

    # Draw score
    canvas.create_text(50, 10, fill="white",
                       text="Score: " + str(score), anchor="nw")

    # Draw food
    canvas.create_rectangle(food_x, food_y,
                            food_x + 10, food_y + 10,
                            fill="red")

    # Draw snake
    for part in snake:
        canvas.create_rectangle(part[0], part[1],
                                part[0] + 10, part[1] + 10,
                                fill="green")

# ---------------- KEY BINDINGS ----------------
window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)

# ---------------- START GAME ----------------
move_snake()
window.mainloop()
