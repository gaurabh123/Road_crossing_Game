import pygame as p
import time

# Define the Car class
class Car(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        # Initialize car properties based on the number parameter
        if number == 1:
            self.x = 250
            self.image = p.image.load('../images/Slow Car.png')
            self.vel = -4
        elif number == 2:
            self.x = 500
            self.image = p.image.load('../images/Fast Car.png')
            self.vel = 5
        else:
            self.x = 850
            self.image = p.image.load('../images/racing_car.png')
            self.vel = 5
            
        # Set initial y position to half the screen height
        self.y = HEIGHT / 2
        # Set width and height for collision detection
        self.width = 100
        self.height = 150
        # Scale the image to desired size
        self.image = p.transform.scale(self.image, (self.width, self.height))
        # Get the rectangle for collision detection
        self.rect = self.image.get_rect()
        # Create a mask for pixel-perfect collision detection
        self.mask = p.mask.from_surface(self.image)

    # Update method to move the car and update its position
    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    # Method to handle car movement
    def movement(self):
        self.y += self.vel
        # If car hits top or bottom of the screen, reverse direction
        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vel *= -1
        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2
            self.vel *= -1

# Define the Cat class
class Cat(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Initialize cat properties
        self.x = 70
        self.y = HEIGHT / 2
        self.vel = 8
        self.width = 90
        self.height = 70

        # Load cat images and scale them
        self.cat1 = p.image.load('../images/cat1.png')
        self.cat2 = p.image.load('../images/cat2.png')
        self.cat1 = p.transform.scale(self.cat1, (self.width, self.height))
        self.cat2 = p.transform.scale(self.cat2, (self.width, self.height))

        # Set initial image to cat1
        self.image = self.cat1
        # Get the rectangle for collision detection
        self.rect = self.image.get_rect()
        # Create a mask for pixel-perfect collision detection
        self.mask = p.mask.from_surface(self.image)

    # Update method to move the cat, correct its position, and check for collision
    def update(self):
        self.movement()
        self.correction()
        self.checkCollision()
        self.rect.center = (self.x, self.y)

    # Method to handle cat movement
    def movement(self):
        keys = p.key.get_pressed()

        if keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.cat2
        elif keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.cat1
        if keys[p.K_UP]:
            self.y -= self.vel
        elif keys[p.K_DOWN]:
            self.y += self.vel

    # Method to correct cat's position if it goes out of screen boundaries
    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2
        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2
        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.width / 2

    # Method to check collision between cat and cars
    def checkCollision(self):
        car_check = p.sprite.spritecollide(self, car_group, False, p.sprite.collide_mask)
        if car_check:
            explosion.explode(self.x, self.y)
           
# Define the Screen class
class Screen(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load screen images
        self.img1 = p.image.load('../images/imgg.png')
        self.img2 = p.image.load('../images/You Win.png')
        self.img3 = p.image.load('../images/You Lose.png')

        # Scale screen images to match screen dimensions
        self.img1 = p.transform.scale(self.img1, (WIDTH, HEIGHT))
        self.img2 = p.transform.scale(self.img2, (WIDTH, HEIGHT))
        self.img3 = p.transform.scale(self.img3, (WIDTH, HEIGHT))

        # Set initial image to img1
        self.image = self.img1
        self.x = 0
        self.y = 0
        # Get the rectangle for screen positioning
        self.rect = self.image.get_rect()
        
    # Update method to update screen position
    def update(self):
        self.rect.topleft = (self.x, self.y)

# Define the Flag class
class Flag(p.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number

        # Load flag images based on number parameter
        if self.number == 1:
            self.image = p.image.load('../images/green flag.png')
            self.visible = False
            self.x = 50
        else:
            self.image = p.image.load('../images/white flag.png')
            self.visible = True
            self.x = 1150

        # Set initial y position to half the screen height
        self.y = HEIGHT / 2
        # Scale flag images
        self.image = p.transform.scale2x(self.image)
        # Get the rectangle for collision detection
        self.rect = self.image.get_rect()
        # Create a mask for pixel-perfect collision detection
        self.mask = p.mask.from_surface(self.image)

    # Update method to update flag position and check for collision
    def update(self):
        if self.visible:
            self.collison()
            self.rect.center = (self.x, self.y)

    # Method to check collision between flag and cat
    def collison(self):
        global SCORE, cat
        flag_hit = p.sprite.spritecollide(self, cat_group, False, p.sprite.collide_mask)
        if flag_hit:
            self.visible = False
            # If green flag is hit
            if self.number == 1:
                white_flag.visible = True
                # If score is less than 5, switch level, else end game with win screen
                if SCORE < 5:
                    SwitchLevel()
                else:
                    cat_group.empty()
                    DeleteOtherItems()
                    EndScreen(1)
            # If white flag is hit
            else:
                green_flag.visible = True

# Define the Explosion class
class Explosion(object):
    def __init__(self):
        self.costume = 1
        self.width = 140
        self.height = 140
        # Load initial explosion image
        self.image = p.image.load('../images/explosion' + str(self.costume) + '.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))

    # Method to create explosion effect
    def explode(self, x, y):
        x = x - self.width / 2
        y = y - self.height / 2
        DeleteCat()

        # Loop through explosion images
        while self.costume  < 9:
            self.image = p.image.load('../images/explosion' + str(self.costume) + '.png')
            self.image = p.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            p.display.update()

            self.costume += 1
            time.sleep(0.1)

        DeleteOtherItems()
        EndScreen(0)

# Function to display score
def scoreDisplay():
    global gameOn
    if gameOn:  
        score_text = score_font.render(str(SCORE) + ' /5', True, (0,0,0))
        win.blit(score_text,(500,10))

# Function to check flags visibility and update flag group
def checkFlags():
    for flag in flags:
        if not flag.visible:
            flag.kill()
        else:
            if not flag.alive():
                flag_group.add(flag)

# Function to switch level
def SwitchLevel():
    global SCORE

    if slow_car.vel < 0:
        slow_car.vel -= 1
    else:
        slow_car.vel += 1
    
    if fast_car.vel < 0:
        fast_car.vel -= 1
    else:
        fast_car.vel += 1
    SCORE += 1

# Function to delete cat sprite
def DeleteCat():
    global cat
    cat.kill()
    screen_group.draw(win)
    car_group.draw(win)
    flag_group.draw(win)

    screen_group.update()
    car_group.update()
    flag_group.update()

# Function to delete other sprites and clear flags list
def DeleteOtherItems():
    car_group.empty()
    flag_group.empty()
    flags.clear()

# Function to display end screen
def EndScreen(n):
    global gameOn
    gameOn = False
    
    if n == 0:
        bg.image = bg.img3
    elif n == 1:
        bg.image = bg.img2

# Set screen dimensions
WIDTH = 1200
HEIGHT = 700
# Initialize pygame
p.init()
# Create game window
win = p.display.set_mode((WIDTH, HEIGHT))
# Set window caption
p.display.set_caption('Road Crossing Game')

# Initialize clock
clock = p.time.Clock()

# Initialize score and font
SCORE = 0
score_font = p.font.SysFont('comicsans', 80, True)

# Initialize screen background
bg = Screen()
screen_group = p.sprite.Group()
screen_group.add(bg)

# Initialize cat sprite
cat = Cat()
cat_group = p.sprite.Group()
cat_group.add(cat)

# Initialize car sprites
slow_car = Car(1)
fast_car = Car(2)
car3 = Car(1)
car4 = Car(2)

# Set initial positions and velocities for additional cars
car3.x = 800
car4.x = 1000
car3.vel = -4
car4.vel = 6

# Create car group and add car sprites
car_group = p.sprite.Group()
car_group.add(slow_car, fast_car, car3, car4)

# Initialize flag sprites
green_flag = Flag(1)
white_flag = Flag(2)

# Create flag group and add flag sprites
flag_group = p.sprite.Group()
flag_group.add(green_flag, white_flag)
# Store flags in a list
flags = [green_flag, white_flag]

# Initialize explosion effect
explosion = Explosion()

# Set game state to on
gameOn = True
# Main game loop
run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

    # Draw screen background
    screen_group.draw(win)
    # Display score
    scoreDisplay()
    # Check flags visibility
    checkFlags()
 
    # Draw car, cat, and flag sprites
    car_group.draw(win)
    cat_group.draw(win)
    flag_group.draw(win)
    
    # Update car, cat, and flag sprites
    car_group.update()
    cat_group.update()
    flag_group.update()
    screen_group.update()

    # Update display
    p.display.update()

# Quit pygame
p.quit()
