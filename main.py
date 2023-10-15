import time
import random
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_INKY_PACK

# Initialize display and buttons
display = PicoGraphics(display=DISPLAY_INKY_PACK)
display.set_update_speed(3)
button_a = Button(12)
button_b = Button(13)

# Screen dimensions
WIDTH = 296
HEIGHT = 128

# Paddle and ball variables
paddle_x = WIDTH // 2
paddle_y = HEIGHT - 10
paddle_width = 40
paddle_height = 4
ball_x = WIDTH // 2
ball_y = HEIGHT - 20
ball_radius = 4
ball_speed_x = random.choice([-2, 2])
ball_speed_y = -10

# Bricks variables
brick_width = 40
brick_height = 10
bricks = []

# Game variables
score = 0

def create_bricks():
    global bricks
    bricks = []
    for i in range(10):
        for j in range(4):
            brick_x = i * brick_width
            brick_y = j * brick_height + 30
            bricks.append((brick_x, brick_y))

def draw_paddle():
    display.set_pen(3)
    display.rectangle(paddle_x - paddle_width // 2, paddle_y, paddle_width, paddle_height)

def draw_ball():
    display.set_pen(0)
    display.circle(ball_x, ball_y, ball_radius)

def draw_bricks():
    display.set_pen(5)
    for brick in bricks:
        brick_x, brick_y = brick
        display.rectangle(brick_x, brick_y, brick_width, brick_height)

def draw_score():
    display.set_pen(1)
    display.text("Score: " + str(score), 5, 5, 40, 3)

def move_paddle():
    global paddle_x
    if button_a.read() and paddle_x - paddle_width // 2 > 0:
        paddle_x -= 10
    if button_b.read() and paddle_x + paddle_width // 2 < WIDTH:
        paddle_x += 10

def update_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score, bricks

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check collision with the screen boundaries
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x = -ball_speed_x

    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y

    # Check collision with the paddle
    if (
        ball_y + ball_radius >= paddle_y
        and paddle_x - paddle_width // 2 <= ball_x <= paddle_x + paddle_width // 2
    ):
        ball_speed_y = -ball_speed_y

    # Check collision with bricks
    to_remove = None
    for i, brick in enumerate(bricks):
        brick_x, brick_y = brick
        if (
            ball_y - ball_radius <= brick_y + brick_height
            and ball_y + ball_radius >= brick_y
            and ball_x >= brick_x
            and ball_x <= brick_x + brick_width
        ):
            to_remove = i
            score += 1
            ball_speed_y = -ball_speed_y
            break

    if to_remove is not None:
        bricks.pop(to_remove)

    # Game over condition
    if ball_y + ball_radius >= HEIGHT:
        score = 0
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        create_bricks()

def main():
    create_bricks()

    while True:
        display.set_pen(15)
        display.clear()

        move_paddle()
        update_ball()
        draw_paddle()
        draw_ball()
        draw_bricks()
        draw_score()

        display.update()
        time.sleep(0.03)

if __name__ == "__main__":
    main()

