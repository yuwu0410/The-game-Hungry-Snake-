import pygame
import random

#initialize pygame
pygame.init()

#initialze the background music
pygame.mixer.init()

# the font of the score shown
font=pygame.font.SysFont(None, 35)

#load the music file and play the music
pygame.mixer.music.load('outside.MP3')
pygame.mixer.music.play(-1) #here -1 means keeping playi ng the music

#set the volume of the music
pygame.mixer.music.set_volume(0.6)

#set the size of the screen
screen_width=500
screen_height=500

#initialize the title and the screen
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("HUNGRY SNAKE!")

#define the size of the block which is a component of food and snake
block= 15

# define the basic colors which are going to be used
black=(0, 0, 0) #the color of the screen
red=(255, 0, 0) #the color of the food(apple)
purple=(128, 0, 128) #the color of the snake
white=(255, 255, 255) # the color of the scoreboard
green=(0, 255, 0) # the color of the head of the snake
blue=(0, 0, 255) # the color which show the highest score

# define the class: Snake
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #which means the function has inherited all the methods and attributes of pygame.sprite.Sprite
        self.body=[] #the body of the snake
        self.create_snake() #create the original appearance of the snake

    def create_snake(self):
        i=0
        while i<=5:
            new_block=pygame.Surface((block, block)) #keep creating the surface of the rectangle
            new_block.fill(purple)
            #now we have to clarify the location of the rectangle and make it a part of the snake
            part=new_block.get_rect(topleft=(50-block, 50)) #append the body of the snake from center ro left
            self.body.append([new_block, part])
            i+=1

    def update(self, dir): #move the snake according to direction given, starting from tail to head
        i=len(self.body)-1
        while i>=1:
            self.body[i][1].topleft=self.body[i-1][1].topleft
            i-=1
        #move the head
        self.body[0][1].x=self.body[0][1].x+dir[0]*block
        self.body[0][1].y=self.body[0][1].y+dir[1]*block
        return 
    
    def growing(self): #execute when a food is eaten
        new_block=pygame.Surface((block, block))
        new_block.fill(purple)
        new_part=new_block.get_rect()
        new_part.topleft=self.body[len(self.body)-1][1].topleft
        self.body.append([new_block, new_part])
        return 

    def draw_snake(self, Screen): #draw the head and body of the snake
        head=pygame.Surface((block, block))
        head.fill(green)
        Screen.blit(head, self.body[0][1])
        for i in self.body[1:]:
            Screen.blit(i[0], i[1])
        return 
    
    def check_collision(self): # check whether the snake eat itself
        for block in self.body[1:]:
            if self.body[0][1].colliderect(block[1]):
                return True
        return False
    
    def check_hit_wall(self): # check if the snake hits the wall
        head_position = self.body[0][1] # to get the position of the snake's head
        if head_position.x<0 or head_position.y<0 or head_position.x>=screen_width or head_position.y>=screen_height:
            return True
        return False


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #inherite pygame.sprite.Sprite
        #create the apple
        self.image=pygame.Surface((block, block))
        self.image.fill(red)
        self.rect=self.image.get_rect(topleft= self.get_position())

    def get_position(self): #get the random position of the apple
        x=random.randint(0, screen_width-block)
        y=random.randint(0, screen_height-block)
        return (x//block)*block, (y//block)*block #the type of the position is a tuple, note that here we can't use "/"


    def update(self): #get a new apple
        self.rect.topleft=self.get_position()
        return 

def show_score(score, highest_score): # show the current score of the snake
    message=font.render("Score:"+str(score), True, white)
    message2=font.render("Highest Score:"+str(highest_score), True, blue)
    screen.blit(message, [0, 0])
    screen.blit(message2, [0, 30])
    return max(score, highest_score)

def restart(score): # show the end message and wait for players to input "s" to start an another try
    screen.fill(black)
    message=font.render("Game Over! Final Score: "+str(score), True, white)
    screen.blit(message, [screen_width//4, screen_height //3])
    again=font.render("Press S to try again!", True, white)
    screen.blit(again, [screen_width//4, screen_height//2])
    pygame.display.flip()
    rest=True
    while rest:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_s:
                rest=False


#initialize the game
#create instances
snake=Snake()
apple=Apple()
score=0 # the original score of the player
direction=(1,0) #the original direction of the snake
highest_score=0 # to show the highest score in several games

#start the game
running=True
while running:
    #responding to events:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #user exit the screen
            running= False
        #responding to user's inputs
        elif event.type==pygame.KEYDOWN: #input is by clicking on the keyboard
            if event.key==pygame.K_DOWN: #down 
                direction=(0, 1)
            elif event.key==pygame.K_UP: #up
                direction=(0, -1)
            elif event.key==pygame.K_LEFT: #left
                direction=(-1, 0)
            elif event.key==pygame.K_RIGHT: #right
                direction=(1, 0)

    #after receiving inputs, respond according to specified inputs
    snake.update(direction) #move 
    #check if apple is eaten by collision detection
    if snake.body[0][1].colliderect(apple.rect):
        snake.growing()
        apple.update()
        score+=1

    # check whether the snake eat itself:
    if snake.check_collision() or snake.check_hit_wall():
        restart(score)
        snake=Snake()
        apple=Apple()
        score=0
        direction=(1, 0)

    screen.fill(black)
    snake.draw_snake(screen)
    screen.blit(apple.image, apple.rect)
    highest_score=show_score(score, highest_score) # keep showing the score and updating the highest score

    #update the screen to keep showing the contents on the screen
    pygame.display.flip()
    # set the speed that the game updates
    pygame.time.Clock().tick(18+len(snake.body)/2) # the snake will gradually move faster as its body becomes longer

pygame.quit()
