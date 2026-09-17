"""Snake - mini-juego 2D hecho con tkinter (solo librería estándar de Python)."""
import tkinter as tk
import random

CELL_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 20
INITIAL_SPEED_MS = 150
MIN_SPEED_MS = 60
SPEED_STEP_MS = 5

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITES = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}


def next_head(head, direction):
    dx, dy = DIRECTIONS[direction]
    x, y = head
    return (x + dx, y + dy)


def hits_wall(pos):
    x, y = pos
    return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT


def hits_self(pos, body):
    return pos in body


def is_reversal(current_direction, new_direction):
    """True si new_direction haría que la serpiente choque contra su propio cuello."""
    return OPPOSITES.get(new_direction) == current_direction


def speed_for_score(score):
    """La velocidad aumenta (menos ms de espera) conforme sube el puntaje."""
    return max(MIN_SPEED_MS, INITIAL_SPEED_MS - score * SPEED_STEP_MS)


def random_food_position(body):
    free_cells = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in body
    ]
    return random.choice(free_cells)


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake - Vibecoding")
        self.canvas = tk.Canvas(
            root,
            width=GRID_WIDTH * CELL_SIZE,
            height=GRID_HEIGHT * CELL_SIZE,
            bg="#1e1e1e",
            highlightthickness=0,
        )
        self.canvas.pack()
        self.root.bind("<Key>", self.on_key)
        self.after_id = None
        self.reset()

    def reset(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
        self.body = [(5, 5), (4, 5), (3, 5)]
        self.direction = "Right"
        self.pending_direction = "Right"
        self.score = 0
        self.food = random_food_position(self.body)
        self.running = True
        self.paused = False
        self.started = False
        self.draw()
        self.after_id = self.root.after(INITIAL_SPEED_MS, self.tick)

    def on_key(self, event):
        key = event.keysym
        if key in DIRECTIONS:
            if self.running and not is_reversal(self.direction, key):
                self.pending_direction = key
                self.started = True
        elif key.lower() == "r" and not self.running:
            self.reset()
        elif key.lower() == "p" and self.running and self.started:
            self.paused = not self.paused
            self.draw()

    def tick(self):
        if not self.running:
            return
        if self.paused or not self.started:
            self.after_id = self.root.after(INITIAL_SPEED_MS, self.tick)
            return
        self.direction = self.pending_direction
        new_head = next_head(self.body[0], self.direction)
        if hits_wall(new_head) or hits_self(new_head, self.body):
            self.game_over()
            return
        self.body.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = random_food_position(self.body)
        else:
            self.body.pop()
        self.draw()
        self.after_id = self.root.after(speed_for_score(self.score), self.tick)

    def game_over(self):
        self.running = False
        self.canvas.create_text(
            GRID_WIDTH * CELL_SIZE // 2,
            GRID_HEIGHT * CELL_SIZE // 2,
            text=f"GAME OVER\nPuntaje: {self.score}\nPresiona R para reiniciar",
            fill="white",
            font=("Consolas", 16),
            justify="center",
        )

    def draw(self):
        self.canvas.delete("all")
        for i, (x, y) in enumerate(self.body):
            color = "#4caf50" if i == 0 else "#8bc34a"
            self.canvas.create_rectangle(
                x * CELL_SIZE, y * CELL_SIZE,
                x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE,
                fill=color, outline="#1e1e1e",
            )
        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL_SIZE, fy * CELL_SIZE,
            fx * CELL_SIZE + CELL_SIZE, fy * CELL_SIZE + CELL_SIZE,
            fill="#f44336", outline="",
        )
        self.canvas.create_text(
            40, 12, text=f"Puntaje: {self.score}", fill="white", font=("Consolas", 10)
        )
        if not self.started:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="Usa las flechas para moverte\n'P' pausa - 'R' reinicia",
                fill="white",
                font=("Consolas", 13),
                justify="center",
            )
        elif self.paused:
            self.canvas.create_text(
                GRID_WIDTH * CELL_SIZE // 2,
                GRID_HEIGHT * CELL_SIZE // 2,
                text="PAUSA\n(P para continuar)",
                fill="white",
                font=("Consolas", 16),
                justify="center",
            )


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
