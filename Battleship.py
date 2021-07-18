from random import randint, choice
import pygame
from pygame.locals import *

pygame.init()
width, height = 1800, 800
backgroundColor = 0, 0, 0
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


# C=Carrier 5, B=Battleship 4, R=Cruiser 3, S=Sub 3, D=Destroyer 2
class Board:
    def __init__(self,player,offsetx):
        self.position = []
        self.ships_hit = [5,4,3,3,2]
        self.player = player
        self.offsetx = offsetx
        self.offsety = 20
        self.moves = 0
    def clear(self):
        for y in range(1,12):
            for x in range(1,12):
                self.position.append(' ')
    def place_ships(self,ship_type):
        temp = [0,0,0,0,0]
        length = L[T.index(ship_type)]
        vert = False
        done = False
        if randint(0,1) == 1:
            vert = True
            
        while not done:
            empty = True
            if not vert:
                x = randint(1,11-length)
                y = randint(1,10)
                for i in range(0,length):
                    if self.position[y*10+x+i] == ' ':
                        temp[i] = y*10+(x+i)
                    else:
                        empty = False
                if empty:
                    for i in range(0,length):
                        self.position[temp[i]] = ship_type
                    done = True
            else:
                x = randint(1,10)
                y = randint(1,11-length)
                for i in range(0,length):
                    if self.position[(y+i)*10+x] == ' ':
                        temp[i] = (y+i)*10+x
                    else:
                        empty = False
                if empty:
                    for i in range(0,length):
                        self.position[temp[i]] = ship_type
                    done = True                
    def show(self):
        rows='ABCDEFGHIJ'
        #print(' 1234567890')
        side_letters(self.offsetx)        
        for y in range(1,11):
            #print(rows[y-1:y],end='')
            for x in range(1,11):
                #print(self.position[y*10+x],end='')
                square(x,y,self.position[y*10+x],self.offsetx)
            #print()
        top_numbers(self.offsetx)
        show_ships(self)

def square(x,y,ship_type,p_offsetx): # draw single square with ship
    w = 50
    h = w
    offsetx = 10  + p_offsetx
    offsety = 20
    textsize = 50
    if T.find(ship_type) > -1:
        ship_type = " "
    points = pygame.Rect(x*w+offsetx,y*h+offsety,w,h)
    text_points = pygame.Rect(x*w+offsetx+textsize/4,y*h+offsety+textsize/4,w,h)
    pygame.draw.rect(screen,pygame.Color(128,128,255),points,1)
    font = pygame.font.Font(None, textsize)
    text = font.render(ship_type, 1, (255, 255, 255))
    screen.blit(text, text_points)

def top_numbers(p_offsetx):
    x = 1
    y = 0
    w = 50
    h = w
    offsetx = 10 + p_offsetx
    offsety = 20
    textsize = 50
    for x in range(1,11):
        text_points = pygame.Rect(x*w+offsetx+textsize/4,y*h+offsety+textsize/4,w,h)
        font = pygame.font.Font(None, textsize)
        text = font.render(str(x), 1, (255, 255, 255))
        screen.blit(text, text_points)  

def side_letters(p_offsetx):
    rows='ABCDEFGHIJ'
    x = 0
    y = 0
    w = 50
    h = w
    offsetx = 10 + p_offsetx
    offsety = 20
    textsize = 50
    for y in range(1,11):
        text_points = pygame.Rect(x*w+offsetx+textsize/4,y*h+offsety+textsize/4,w,h)
        font = pygame.font.Font(None, textsize)
        text = font.render(rows[y-1:y], 1, (255, 255, 255)) 
        screen.blit(text, text_points)

def show_ships(player):
    x = 12
    y = 1
    w = 50
    h = w
    offsetx = 10 + player.offsetx
    offsety = 20
    textsize = 50    
    ship = 0
    for i in T:
        for j in range(0,L[ship]):
            text_points = pygame.Rect((j+x)*w+offsetx+textsize/4,(ship+y)*h+offsety+textsize/4,w,h)
            font = pygame.font.Font(None, textsize)
            text = font.render(i, 1, (255, 255, 255))
            screen.blit(text, text_points)
            if j >= player.ships_hit[ship]:
                text = font.render('X', 1, (255, 255, 255))
                screen.blit(text, text_points)
        ship+=1
    text_points = pygame.Rect((12)*w+offsetx+textsize/4,(0)*h+offsety+textsize/4,w,h) # number of moves
    font = pygame.font.Font(None, textsize)
    text = font.render(str(player.moves), 1, (255, 255, 255))
    screen.blit(text, text_points)
    

def fire(board): # random fire
    done = False
    while not done:
        x=randint(1,10)
        y=randint(0,10)
        pos = board.position[y*10+x]
        if T.find(pos) > -1:
            board.position[y*10+x] = str.lower(pos)
            board.ships_hit[T.find(pos)] = board.ships_hit[T.find(pos)] - 1
            done = True
        elif pos == ' ':
            board.position[y*10+x] = 'x'            
            done = True

def player_fire(board,event_pos):
    global numplayers
    board.moves = board.moves + 1
    x,y = event_pos
    #print('player=',board.player,x,y)
    w = 50
    h = w
    offsetx = 10 + board.offsetx
    offsety = 20
    if board.player == 1 and numplayers == 1: #1
        x = int((x - offsetx) / w)
        y = int((y - offsety) / h)
    #print('player=',board.player,x,y)
    pos = board.position[y*10+x]
    if T.find(pos) > -1:                         # Hit!
        board.position[y*10+x] = str.lower(pos)
        board.ships_hit[T.find(pos)] = board.ships_hit[T.find(pos)] - 1
        #print(board.ships_hit)
    elif pos == ' ':
        board.position[y*10+x] = 'x'            

def check_win():
    x = 500
    y = 600
    w = 50
    h = w
    textsize = 100 
    text_points = pygame.Rect(x,y,w,h)
    font = pygame.font.Font(None, textsize)
    if sum(player[1].ships_hit) == 0:
        text = font.render('Player 1 Wins!', 1, (255, 255, 255))         
        screen.blit(text, text_points)
        return True
    elif sum(player[2].ships_hit) == 0:
        text = font.render('Player 2 Wins!', 1, (255, 255, 255))         
        screen.blit(text, text_points)
        return True
    return False


def search_board(player):  # make list of best positions
    score_list = []
    board = player.position
    for ypos in range(1,11):
        for xpos in range(1,11):
            score = 0
            pos = board[xpos+((ypos-0)*10)]
            if pos != 'x' and D.find(pos) == -1 :                      
                if xpos <10: 
                    s = 0
                    for x in range(xpos+1, 11):              # horz right
                        new_s = check_pos(player,x,ypos,s)
                        if new_s == -1:  # stop checking
                            break
                        s += new_s
                    score += s
                    #s = 0
                if xpos >1: 
                    s = 0
                    for x in range(xpos-1, 0, -1):           # horz left
                        new_s = check_pos(player,x,ypos,s)
                        if new_s == -1:  # stop checking
                            break
                        s += new_s
                    score += s
                    #s = 0
                if ypos <10:
                    s = 0
                    for y in range(ypos+1, 11):              # vert down
                        new_s = check_pos(player,xpos,y-0,s)
                        if new_s == -1:  # stop checking
                            break
                        s += new_s
                    score += s
                if ypos >1:
                    s = 0
                    for y in range(ypos, 1, -1):             # vert up
                        new_s = check_pos(player,xpos,y-1,s)
                        if new_s == -1:  # stop checking
                            break
                        s += new_s
                    score += s
            pos = board[xpos+((ypos-0)*10)]
            if pos == 'x' or D.find(pos) > -1 :
                score = 0
            score_list.append(score)
            print(f'{score:4d}',end='')
        print()
    print()
    max_value = max(score_list)
    maxes = [i for i, j in enumerate(score_list) if j == max_value] #random of highs
    max_index = choice(maxes)+1
#    max_index = score_list.index(max_value)+1 # first high 
    x = max_index%10
    y = max_index//10+1
    if x == 0:
        x = 10
        y = max_index/10
    #print (max_index, x,y)
    return (int(x),int(y))



def check_pos(player,x,y,s):
    board = player.position
    pos = board[(y-0)*10+x]
    if D.find(pos) > -1:        # found hit ship
        if player.ships_hit[D.find(pos)] == 0: # is it sunk?
            return -1
        elif s % 100 == 0:      # is it another hit?
            return 100
        else:
            return -1
    if pos == 'x':
        return -1
    if (pos == ' ' and s>99):
        return -1
    if pos == ' ' or T.find(pos) > -1: # empty or unfound ship
        return 1
    return -1

def auto():
    over = False
    x,y = search_board(player[1])
    player_fire(player[1],(x,y))
    x,y = search_board(player[2])
    player_fire(player[2],(x,y))
    screen.fill((0,0,0))
    player[1].show()
    player[2].show()
    over = check_win()
    pygame.display.flip()
    return over




def main():
   while True:
      for event in pygame.event.get():
            if event.type == QUIT:
               pygame.quit()
               return
            elif event.type == MOUSEBUTTONDOWN:
                player_fire(player[1],event.pos)
                x,y = search_board(player[2])
                player_fire(player[2],(x,y))
                screen.fill((0,0,0))
                player[1].show()
                player[2].show()
                check_win()
                pygame.display.flip()
      clock.tick(60)



T = 'CBRSD'     # type of ships
D = 'cbrsd'     # dead ships
L = [5,4,3,3,2] # length of ships
player = []
search = []
player.append(Board(1,0)) # dummy player 0
player.append(Board(1,00))
player.append(Board(2,900))

player[1].clear()
for i in T:
    player[1].place_ships(i)
player[2].clear()
for i in T:
    player[2].place_ships(i)

numplayers = 1
#numplayers = int(input('Number of player 0-1'))
player[1].show()
player[2].show()
pygame.display.flip()  

over = False
if numplayers == 1:
    main()

else:
    while over == False:
        over = auto()



