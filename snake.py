import tkinter as tk
import random

# Game Constants
WIDTH = 500
HEIGHT = 500
SNAKE_SIZE = 20
SPEED = 100  # Adjust speed (lower is faster)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Snake Game")

        # Create canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Game variables
        self.snake = [[100, 100], [80, 100], [60, 100]]  # Initial snake position
        self.food = self.create_food()
        self.direction = "Right"
        self.running = True
        self.score = 0

        # Display score
        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 14), fg="white", bg="black")
        self.score_label.pack()

        # Key bindings
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))

        # Start game loop
        self.update_game()

    def create_food(self):
        """Generate a random food position."""
        x = random.randint(0, (WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
        return [x, y]

    def change_direction(self, new_direction):
        """Change the snake's direction."""
        opposite_directions = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_direction != opposite_directions.get(self.direction, ""):
            self.direction = new_direction

    def update_game(self):
        """Update game state and animate movement."""
        if not self.running:
            return

        # Move the snake
        head_x, head_y = self.snake[0]
        if self.direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.direction == "Right":
            head_x += SNAKE_SIZE
        elif self.direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.direction == "Down":
            head_y += SNAKE_SIZE

        new_head = [head_x, head_y]

        # Check for collisions
        if new_head in self.snake or head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.game_over()
            return

        # Add new head
        self.snake.insert(0, new_head)

        # Check if snake eats food
        if new_head == self.food:
            self.food = self.create_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.snake.pop()  # Remove last segment to maintain length

        # Animate the movement
        self.draw_elements()

        # Schedule next update
        self.root.after(SPEED, self.update_game)

    def draw_elements(self):
        """Draw the snake and food with smooth animation."""
        self.canvas.delete("all")  # Clear canvas

        # Draw food with animation effect
        self.canvas.create_oval(
            self.food[0] + 3, self.food[1] + 3, self.food[0] + SNAKE_SIZE - 3, self.food[1] + SNAKE_SIZE - 3,
            fill="red", outline="yellow", width=2
        )

        # Draw snake with rounded animated effect
        for i, segment in enumerate(self.snake):
            color = "lime green" if i == 0 else "green"
            self.canvas.create_oval(
                segment[0] + 3, segment[1] + 3, segment[0] + SNAKE_SIZE - 3, segment[1] + SNAKE_SIZE - 3,
                fill=color, outline="dark green", width=2
            )

    def game_over(self):
        """Display game over animation."""
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="GAME OVER", fill="white", font=("Arial", 24, "bold"))
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 + 40, text="Press R to Restart", fill="white", font=("Arial", 14))
        self.root.bind("<r>", self.restart_game)  # Bind 'R' key to restart

    def restart_game(self, event):
        """Restart the game."""
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.food = self.create_food()
        self.direction = "Right"
        self.running = True
        self.score = 0
        self.score_label.config(text="Score: 0")
        self.update_game()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()