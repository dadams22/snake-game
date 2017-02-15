"""An attempt to recreate the classic snake arcade game.  Created by David Adams"""
from random import randint

# Each square in the grid is 15x15
grid_size = 15

# Dimensions of grid in squares
w = 30
h = 30

# Links keycodes with their corresponding directions
directions = {
    '38': (0, -1),
    '40': (0, 1),
    '37': (-1, 0),
    '39': (1, 0),
}


class Segment():
    """Represents one single block of a snake"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
        

class Snake():
    """Represents the snake that moves on the screen"""
    def __init__(self):
        self.segments = [Segment(w / 2, h / 2)]
        self.y_direction = 0
        self.x_direction = 0
        self.previous = []
    
    def show_snake(self):
        """Prints segments of snake to the canvas"""
        stroke(0)
        fill(0, 200, 0)
        for segment in self.segments:
            rect(segment.x * grid_size, segment.y * grid_size, grid_size, grid_size)
    
    def move_snake(self):
        """Changes the direction of the snake when a key is pressed
        and translates the segments of the snake in that direction"""
        if self.x_direction != 0 or self.y_direction != 0:
            head = self.segments[0]
            previous = self.segments.pop()
            snake.previous.insert(0, previous)
            if len(snake.previous) > 3:
                snake.previous.pop()
            new_segment = Segment(head.x + self.x_direction, head.y + self.y_direction)
            self.segments.insert(0, new_segment)
            
    def in_boundary(self):
        """Returns False if snake exits the boundaries"""
        for segment in self.segments:
            if segment.x > w or segment.x < 0:
                return False
            elif segment.y > h or segment.y < 0:
                return False
        else:
            return True
    
    def is_tangled(self):
        """Returns True if any segment of the snake is intersecting
        with another segment"""
        snake_segments = self.segments[:]
        while snake_segments:
            checking_segment = snake_segments.pop()
            for segment in snake_segments:
                if checking_segment.x == segment.x and checking_segment.y == segment.y:
                    return True
        else:
            return False
            
        
    def eat_food(self):
        """Grows the snake when it eats food"""
        for segment in snake.previous:
            snake.segments.append(segment)



class Food():
    """Represents one piece of food on the screen"""
    def __init__(self):
        self.x = randint(0, w)
        self.y = randint(0, h)
    
    def show_food(self):
        stroke(255, 0, 0)
        fill(255, 0, 0)
        rect(self.x * grid_size, self.y * grid_size, grid_size, grid_size)



class Button():
    """Represents a button for the user to press on the start screen"""
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.text_size = 22
        self.x_size = (len(self.label) * (self.text_size / 2)) + 30
        self.y_size = self.text_size + 10
        self.x_corner = self.x - (self.x_size / 2)
        self.y_corner = self.y - (self.y_size / 2)
    
    def show_button(self):
        """Displays the button on the canvas"""
        stroke(0)
        fill(180)
        rect(self.x_corner, self.y_corner, self.x_size, self.y_size, 5)
        textSize(self.text_size)
        textAlign(CENTER, CENTER)
        fill(0)
        text(self.label, self.x, self.y)
        


def generate_food(snake):
    """Generates a food block that does not intersect with the snake"""
    food = Food()
    for segment in snake.segments:
        if food.x == segment.x and food.y == segment.y:
            generate_food(snake)
    else:
        return food


"""Beginning of main code"""
snake = Snake()
food = generate_food(snake)
start_screen = True
active = False
game_over = False

# Relates each difficulty button with a corresponding frame rate
# for the game to run at
buttons = {
    '6': Button(225, 230, "EASY"),
    '11': Button(225, 280, "MEDIUM"),
    '15': Button(225, 330, "HARD"),
    '22': Button(225, 380, "EXTREME")
}

def mousePressed():
    """When the mouse is pressed, the program checks which button was clicked,
    if any, on the start screen and sets the frame rate to the corresponding 
    difficulty level"""
    global buttons, active, start_screen
    between_x = False
    between_y = False
    
    for frame_rate, button in buttons.items():
        if mouseX > button.x_corner and mouseX < button.x_corner + button.x_size:
            between_x = True
        if mouseY > button.y_corner and mouseY < button.y_corner + button.y_size:
            between_y = True
        if between_x and between_y:
            frameRate(int(frame_rate))
            active = True
            start_screen = False
            break
        else:
            between_x = False
            between_y = False

def keyPressed():
    """Changes the direction of the snake based on the key that was pressed"""
    global directions, snake
    if str(keyCode) in directions.keys():
        requested_direction = directions[str(keyCode)]
        disallowed_direction = (0,0)
        if len(snake.segments) > 1:
            disallowed_direction = (-snake.x_direction, -snake.y_direction)
            
        if requested_direction != disallowed_direction:
            snake.x_direction = requested_direction[0]
            snake.y_direction = requested_direction[1]


def setup():
    size((w * grid_size) + grid_size, (h * grid_size) + grid_size)


def draw():
    global snake, food, active, game_over
    
    if start_screen:
        background(0)
        textAlign(CENTER, CENTER)
        fill(0, 255, 0)
        textSize(65)
        text("Snake Game", 225, 110)
        fill(255)
        textSize(25)
        text("Choose a Difficulty to Begin", 225, 170)
        for button in buttons.values():
            button.show_button()
    
    snake.move_snake()
    
    if not snake.in_boundary() or snake.is_tangled():
        active = False
        game_over = True
            
    if active:
        background(0)
    
        if snake.segments[0].x == food.x and snake.segments[0].y == food.y:
            snake.eat_food()
            food = generate_food(snake)
    
        food.show_food()
        snake.show_snake()
        
    if game_over:
        background(0)
        textSize(50)
        textAlign(CENTER, CENTER)
        fill(255)
        stroke(255)
        text("Game Over", (w / 2) * grid_size, (h / 2) * grid_size - 50)
        textSize(30)
        final_length = "Final Length: " + str(len(snake.segments))
        text(final_length, (w / 2) * grid_size, (h / 2) * grid_size)

    