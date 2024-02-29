import os
import random

RESOLUTION = 600
ROWS = 20
COLS = 20
WIDTH = RESOLUTION / COLS
HEIGHT = RESOLUTION / ROWS
fruits=['apple', 'banana']
colours=[[173,48,32],[251,226,76],[80,153,32]]
score=0
game_over=False
curr_direction='right'

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    # Displays the game board divided into tiles (if required)
    def display(self):
            noFill()
            stroke(0)
            strokeWeight(2)
            #rect(self.col * WIDTH, self.row * HEIGHT, WIDTH, HEIGHT)
            
            
class Snake(list):
    def __init__(self, row, col, count):
        self.direction = 'right'
        self.img=loadImage(os.getcwd() + "\\head_left.png")
        head = SnakeElement(row, col, self.img, True, self.direction)
        self.append(head)
        for i in range(1,count):
            self.append(SnakeElement(row, col - i))
            
    def update(self):
        head = self[0]
 
        #updating the head position based on the direction
        if self.direction == 'right':
            new_head = SnakeElement(head.position.row, head.position.col + 1, self.img, True, direction=self.direction)
            self.img=loadImage(os.getcwd() + "\\head_left.png")
        elif self.direction == 'left':
            new_head = SnakeElement(head.position.row, head.position.col - 1, self.img, True, direction=self.direction)
            self.img=loadImage(os.getcwd() + "\\head_left.png")
        elif self.direction == 'down':
            new_head = SnakeElement(head.position.row + 1, head.position.col, self.img, True, direction=self.direction)
            self.img=loadImage(os.getcwd() + "\\head_up.png")
        elif self.direction == 'up':
            new_head = SnakeElement(head.position.row - 1, head.position.col, self.img, True, direction=self.direction)
            self.img=loadImage(os.getcwd() + "\\head_up.png")
        else:
            pass

        #updating the body positions
        for i in range(len(self)-1,0,-1):
            current_body_part = self[i]
            previous_body_part = self[i - 1]
            new_body_part = SnakeElement(previous_body_part.position.row, previous_body_part.position.col, None,fruit_type=current_body_part.fruit_type)
            self[i] = new_body_part

        #inserting the updated head at the front of the snake
        self[0] = new_head
       
    def get_position(self):
       return self[0].position.row,self[0].position.col     

    def display(self):
        for element in self:
            element.display()
            
    #adding an element to the snake when a fruit is eaten        
    def add_element(self, fruit_type):
        last_element = self[-1]
        if self.direction == 'right':
            self.append(SnakeElement(last_element.position.row, last_element.position.col + 1, None, fruit_type=fruit_type, direction=self.direction))
        elif self.direction == 'left':
            self.append(SnakeElement(last_element.position.row, last_element.position.col - 1, None, fruit_type=fruit_type, direction=self.direction))
        elif self.direction == 'down':
            self.append(SnakeElement(last_element.position.row + 1, last_element.position.col, None, fruit_type=fruit_type, direction=self.direction))
        elif self.direction == 'up':
            self.append(SnakeElement(last_element.position.row - 1, last_element.position.col, None, fruit_type=fruit_type, direction=self.direction))
        else:
            pass
            
    def check_collision(self):
        body=self[1]
        #checking for collision with boundaries of the board
        if self.direction == 'right' and body.position.col==COLS:
            return True
        elif self.direction == 'left' and body.position.col==0:
            return True
        elif self.direction == 'down' and body.position.row==ROWS:
            return True
        elif self.direction == 'up' and body.position.row==0:
            return True
        #checking for collision with the tail of the snake
        else:
            for element in snake[1::]:
                if snake[0].position.row==element.position.row and snake[0].position.col==element.position.col:
                    return True
        #if no collision is found        
        return False        
    
        #checks if the snake has filled the boundaries of the board    
    def check_win(self):
        if len(self)==ROWS*COLS:
            return True
        else:
            return False

class SnakeElement:
    def __init__(self, row, col, img=None,is_head=False, fruit_type=None, direction=None):
        self.position = Tile(row, col)
        self.img=img
        self.is_head=is_head
        self.fruit_type=fruit_type
        self.direction = direction
        #print(self.fruit_type)
        if self.fruit_type=='apple':
            self.colour=colours[0]
        elif self.fruit_type=='banana':
            self.colour=colours[1]
        else:
            self.colour=colours[2]
    
    #displays each element of the snake
    def display(self):
        if self.is_head==True:
            if self.direction == 'right':
                image(self.img, self.position.col * WIDTH, self.position.row * HEIGHT, WIDTH, HEIGHT, 30, 0, 0, 30)
            elif self.direction == 'left':
                image(self.img, self.position.col * WIDTH, self.position.row * HEIGHT, WIDTH, HEIGHT)
            elif self.direction == 'down':
                image(self.img, self.position.col * WIDTH, self.position.row * HEIGHT, WIDTH, HEIGHT, 30, 30, 0, 0)
            elif self.direction == 'up':
                image(self.img, self.position.col * WIDTH, self.position.row * HEIGHT, WIDTH, HEIGHT)
            
        else:
            stroke(self.colour[0],self.colour[1],self.colour[2])
            fill(self.colour[0],self.colour[1],self.colour[2])
            ellipse(self.position.col * WIDTH + WIDTH / 2, self.position.row * HEIGHT + HEIGHT / 2, WIDTH, HEIGHT)


class Game(list):
    def __init__(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.append(Tile(row, col))

    def display(self):
        for tile in self:
            tile.display()

class Fruit:
    def __init__(self):
        overlap=False
        while True:
            #Generating a random type of druit and position on the board for it to be placed
            self.position = Tile(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            self.rand_index= random.randint(0,1)
            self.type=fruits[self.rand_index]
            self.img = loadImage(os.getcwd() + "\\" + str(self.type) + ".png")
            global snake
            for element in snake:
                if element.position.row==self.position.row and element.position.col==self.position.col: #makes sure the generated position does not overlap with the body of the snake
                    overlap=True 
            if overlap==True:
                continue
            else:
                break
            
    def display(self):
        x = self.position.col * WIDTH
        y = self.position.row * HEIGHT
        image(self.img, x, y, WIDTH, HEIGHT)
        
    def get_position(self):
        return self.position.row,self.position.col

    def eatfruit(self):
        overlap=False
        while True:
            self.position = Tile(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
            self.rand_index= random.randint(0,1)
            self.type=fruits[self.rand_index]
            self.img = loadImage(os.getcwd() + "\\" + str(self.type) + ".png")
            global snake
            for element in snake:
                if element.position.row==self.position.row and element.position.col==self.position.col: #makes sure the generated position does not overlap with the body of the snake
                    overlap=True
            if overlap==True:
                continue
            else:
                break
            
        
# Initialize the game elements
snake = Snake(ROWS//2, COLS//2, 3) 
game = Game()
fruit = Fruit()    

def keyPressed():
    global snake
    global curr_direction
    if keyCode == RIGHT and curr_direction!='left':
        snake.direction = 'right'
        curr_direction='right'
    elif keyCode == LEFT and curr_direction!='right':
        snake.direction = 'left'
        curr_direction='left'
    elif keyCode == DOWN and curr_direction!='up':
        snake.direction = 'down'
        curr_direction='down'
    elif keyCode == UP and curr_direction!='down':
        snake.direction = 'up'
        curr_direction='up'
        
                    
def setup():
    size(RESOLUTION, RESOLUTION)

def draw():
    if frameCount%12== 0:
        background(205)
        
        # Core logic of the game
        snake.update()
        
        # Displays elements
        game.display()
        fruit.display()
        snake.display()
    
        # Display the score
        global score
        fill(0)
        textAlign(RIGHT, TOP)  # Align the text to the top right
        textSize(15)
        text('Score: ' + str(score), width - 10, 10)
        
        # Checks if fruit can be eaten by the snake
        if snake.get_position()==fruit.get_position():
            snake.add_element(fruit.type)
            fruit.eatfruit()
            score+=1
            
        # Checks for win i.e the snake has filled the entire board
        global game_over
        if snake.check_win()==True:
            background(205)
            textAlign(CENTER, CENTER) 
            textSize(40)
            text('Congratulations!', width/2, height/2-20)
            textSize(20)
            text('You have filled the board. The game is now over.', width/2, height/2+20)
            game_over=True 
            
        # Checks if snake has collided with boundaries/itself    
        elif snake.check_collision():
            background(205)
            fill(0)
            textAlign(CENTER, CENTER) 
            textSize(35)
            text('Game Over', width/2, height/2 - 20)  
            textSize(22)
            text('Score: ' + str(score), width/2, height/2 + 20)
            game_over=True 
            noLoop() #exits the draw() loop
        else:
            game_over=False
            
#                    
def mouseClicked():
    global game_over
    if game_over==True:
        global snake
        global score
        global curr_direction
        # Resets snake, game, and score
        snake = Snake(ROWS//2, COLS//2, 3)
        game = Game()
        fruit = Fruit()
        score = 0
        game_over=False
        curr_direction='right'
        loop() #restarts the draw() loop
