from random import randint
from time import sleep

class Player:
    def __init__(self,number,name,money):
        self.number = number
        self.name = name
        self.money = money
        self.position = 0
        self.injail = False
        self.jailfree = False
        self.chance = 0
        self.chancesaved = False

    def move(self):
        if self.injail == True:                                                  # in jail?
            self.injail = False
            if self.jailfree == True:                                            # have a get out of jail free card?
                self.jailfree = False                                            # use card
                print(self.name,"uses get out of jail free card.")
            else:
                self.money -= 1                                                  # no free card, pay $1
                print(self.name,"pays $1 to get out of jail.")
        if self.chancesaved == True:                                             # next turn chance card
            self.chancesaved = False
            chance_next_turn(self)
            return
        die = randint(1,6)
        print(self.name,"Rolled",die)
        self.position = self.position + die                                      # move to new position
        if self.position>23:                                                     # passed go?
            self.position = self.position - 24                                   # reset position
            self.money = self.money + 2                                          # collect $2
            print(self.name,"collects $2 from GO")
        print(self.name,"landed on", board[self.position].name)
        if board[self.position].kind == "property":                              # landed on property?
            buy_or_rent(self,False)
        if board[self.position].kind == "parking":                               # landed on free parking?
            pass
        if board[self.position].kind == "jail":                                  # landed on jail?
            self.position = 6                                                    # move player to jail
            self.injail = True                                                   # set jail flag
            print(self.name,"landed in Jail")

        if board[self.position].kind == "chance":                                # landed on chance?
            chance_card(self)
                
        print(self.name,"has $",self.money)                                                                          
        
class Place:
    #kind = ["property","go","chance","jail"]
    def __init__(self,name,cost,kind,other):
        self.name = name
        self.cost = cost
        self.owner = -1
        self.kind = kind
        self.other = other
        
class Chance:
    # action: 0=advance free/pay, 1=collect bank, 2=pay bank, 3=advance GO, 4=players pay you, 5=move forward or take card, 6=move up to 5, 7=jail free, 8=next turn
    def __init__(self,text,action,advancepos1,advancepos2,advancepos3,advancepos4,giveto): 
        self.text = text
        self.action = action
        self.advancepos1 = advancepos1
        self.advancepos2 = advancepos2
        self.advancepos3 = advancepos3
        self.advancepos4 = advancepos4
        self.giveto = giveto


numplayers = 2
chancepos = 0
players = []
board = []
chance = []

def chance_card(self):
    global chancepos
    print(chance[chancepos].text)
    if chance[chancepos].action == 0:                                    # advance to multiple
        multi_choice(self)
    if chance[chancepos].action == 1:                                    # collect $2 from bank
        self.money += 2
    if chance[chancepos].action == 2:                                    # pay $2 to bank
        self.money -= 2
    if chance[chancepos].action == 3:                                    # chance - advance to go? 
        advance_go(self)
    if chance[chancepos].action == 4:                                    # players pay you
        players_pay_you(self)
    if chance[chancepos].action == 5:                                    # move forward 1 or take another card
        if board[self.position+1].kind == "property" and board[self.position+1].owner == -1 and self.money > board[self.position+1].cost :   # is a property and not owned and can pay
            self.position += 1
            buy_or_rent(self,False)                                      # buy property
        else:
            chance_discard()                                              
            chance_card(self)                                            # take another card
    if chance[chancepos].action == 6:                                    # move up to 5 spaces
        move_5(self)
    if chance[chancepos].action == 7:                                    # get out of jail free
        self.jailfree = True
    if chance[chancepos].action == 8:                                    # save card for next turn
        self.chancesaved = True
        self.chance = chance[chancepos]
    if chance[chancepos].action == 9:                                    # advance to new single position
        check_pass_go(self,chance[chancepos].advancepos1)                # check if advance-to passes GO
        self.position = chance[chancepos].advancepos1                    # move to new position
        buy_or_rent(self,True)                                           # True=free
    chance_discard()

def chance_discard():
    global chancepos
    chancepos += 1                                                       # discard current card
    if chancepos > len(chance):
        chancepos = 0                                                    # used all cards? reset deck


def buy_or_rent(self,free):
    monopoly = 1 
    if board[self.position].owner == -1:                                 # nobody owns property?
        if self.money < board[self.position].cost and not free:          # enough money to buy property?
            print(self.name,"does not have enough to buy, bankrupt!")
            self.money = 0                                               # not enough money, bankrupt!
            return
        board[self.position].owner = self.number                         # player buy property
        if not free:
            self.money = self.money - board[self.position].cost          # subtract money from player
            print(self.name,"bought",board[self.position].name,"for $",board[self.position].cost)               
    elif board[self.position].owner != self.number:                      # does player not own it?
        if board[self.position].owner == board[board[self.position].other].owner: # is a monopoly?
            monopoly = 2                                                 # pay x2 if monopoly
            print("Property is monopoly")                
        if self.money >= board[self.position].cost*monopoly:             # enough money to pay rent?
            self.money = self.money - board[self.position].cost*monopoly # subtract rent from player
            players[board[self.position].owner].money = players[board[self.position].owner].money + board[self.position].cost*monopoly  # pay full rent to owner                    
            print(self.name,"payed $", board[self.position].cost*monopoly,"to", players[board[self.position].owner].name) 
        else:
            players[board[self.position].owner].money = players[board[self.position].owner].money + self.money  # pay remaining money as rent
            print(self.name,"payed $", self.money,"to", players[board[self.position].owner].name)
            self.money = 0                                               # zero out account
    else:
        print(self.name,"owns it")

def move_5(player):
    for i in range(player.position+1,player.position+6):
        print (board[i].name)
        if board[i].kind == "property" and board[i].owner == -1 and player.money > board[i].cost :   # is a property and not owned and can pay
            check_pass_go(player,i) 
            player.position = i
            buy_or_rent(player,False)                                            # buy property
            return
    for i in range(player.position+1,player.position+6):
        if board[i].kind == "go":
            advance_go(player)
            return
    for i in range(player.position+1,player.position+6):
        if board[i].kind == "visiting":
            player.position = i
            print(player.name,"moves to Just Visiting")
            return


def advance_go(player):
    player.position = 0
    player.money = player.money + 2
    print(player.name,"collects $2")
    
def check_pass_go(player,card_position): 
    if player.position > card_position:
        player.money += 2
        print(player.name,"passes GO and collects $2")
        
def multi_choice(player):
    global chancepos
    if board[chance[chancepos].advancepos1].owner == -1:                           # check first property for owner
        print(player.name,"gets",board[chance[chancepos].advancepos1].name,"for free!")
        check_pass_go(player,chance[chancepos].advancepos1) 
        player.position = chance[chancepos].advancepos1
        buy_or_rent(player,True)
    elif board[chance[chancepos].advancepos2].owner == -1:                         # check second property for owner
        print(player.name,"gets",board[chance[chancepos].advancepos2].name,"for free!")
        check_pass_go(player,chance[chancepos].advancepos2) 
        player.position = chance[chancepos].advancepos2
        buy_or_rent(player,True)
    elif board[chance[chancepos].advancepos3].owner == -1:                         # check third property for owner
        print(player.name,"gets",board[chance[chancepos].advancepos3].name,"for free!")
        check_pass_go(player,chance[chancepos].advancepos3) 
        player.position = chance[chancepos].advancepos3
        buy_or_rent(player,True)
    elif board[chance[chancepos].advancepos4].owner == -1:                         # check forth property for owner
        print(player.name,"gets",board[chance[chancepos].advancepos4].name,"for free!")
        check_pass_go(player,chance[chancepos].advancepos4) 
        player.position = chance[chancepos].advancepos4
        buy_or_rent(player,True)
    else:
        check_pass_go(player,chance[chancepos].advancepos4) 
        player.position = chance[chancepos].advancepos4                            # all props owned
        buy_or_rent(player,False)
  

def players_pay_you(player):
    for i in players:
        if i.name != player.name:
            i.money -= 1
            player.money += 1
            print (i.name,"pays",player.name,"$1")

def chance_next_turn(player):
    print(player.name,"is using this card:")
    print(player.chance.text)
    # more ....

def init_chance(): # name,action,pos1,pos2,pos3,pos4,giveto
# action: 0=mult advance buy/rent, 1=collect bank, 2=pay bank, 3=advance GO, 4=players pay you, 5=move forward or take card, 6=move up to 5,
#         7=jail free, 8=next turn, 9=single advance buy/rent 

    chance.append(Chance("Free space : Advance to a brown or yellow space. If one is available get it for free, otherwise pay rent to the owner.",0,1,2,16,17,-1))
    chance.append(Chance("Free space : Advance to a light blue or red space. If one is available get it for free, otherwise pay rent to the owner.",0,4,5,13,14,-1))
    chance.append(Chance("Free space : Advance to a pink or dark blue space. If one is available get it for free, otherwise pay rent to the owner.",0,7,8,22,23,-1))
    chance.append(Chance("Free space : Advance to an orange or green space. If one is available get it for free, otherwise pay rent to the owner.",0,10,11,19,20,-1))
    chance.append(Chance("Free space : Advance to an orange space. If one is available get it for free, otherwise pay rent to the owner.",0,10,11,0,0,-1))
    chance.append(Chance("Free space : Advance to a light blue space. If one is available get it for free, otherwise pay rent to the owner.",0,4,5,0,0,-1))
    chance.append(Chance("Free space : Advance to a red space space. If one is available get it for free, otherwise pay rent to the owner.",0,13,14,0,0,-1))
    chance.append(Chance("Advance to the Skatepark. If no one owns it, get it for free, otherwise pay rent to the owner.",9,10,0,0,0,-1))
    chance.append(Chance("Advance to Boardwalk. If no one owns it, get it for free, otherwise pay rent to the owner.",9,23,0,0,0,-1))    
    chance.append(Chance("Collect $2 from the bank",1,0,0,0,0,-1))
    chance.append(Chance("Everyone gives you $1. Happy Birthday",4,0,0,0,0,-1))
    chance.append(Chance("Pay $2 to the bank",2,0,0,0,0,-1))
    chance.append(Chance("Advance to Go, collect $2",3,0,0,0,0,-1))
    chance.append(Chance("Move forward one space or take another chance card.",5,0,0,0,0,-1))
    chance.append(Chance("Move forward *up to* 5 spaces.",6,0,0,0,0,-1))
    chance.append(Chance("Get out of jail free.",7,0,0,0,0,-1))
    chance.append(Chance("Give this card to little Hazel. On your next turn, go forward to any free space and buy it. If all are owned, by one space from any player.",8,0,0,0,0,0))
    chance.append(Chance("Give this card to little Scotty. On your next turn, go forward to any free space and buy it. If all are owned, by one space from any player.",8,0,0,0,0,1))
    chance.append(Chance("Give this card to the toy car. On your next turn, go forward to any free space and buy it. If all are owned, by one space from any player.",8,0,0,0,0,2))
    chance.append(Chance("Give this card to the Toy boat. On your next turn, go forward to any free space and buy it. If all are owned, by one space from any player.",8,0,0,0,0,3))

    for i in range(0,len(chance)):            # shuffle deck
        randpos = randint(0,len(chance)-1)
        temppos = chance[i]
        chance[i] = chance[randpos]
        chance[randpos] = temppos
        
#     for i in range(0,len(chance)):
#         print(chance[i].text)
#     exit()

def init_money(numplayers):  # set the starting money
    if numplayers == 2:      # based on number of players
        return 20
    if numplayers == 3:
        return 18
    else:
        return 16

def init_players():
    global numplayers
    player_names = ["Little Hazel","little Scotty","Toy car","Toy boat"]
    numplayers = int(input("Number of players? 1-4 "))
    start_money = init_money(numplayers)
    quick_start(start_money)
    return
    for i in range(1,numplayers+1):
        print("Player",i)
        answer = "n"
        while answer != "y":
            j=0
            for i in player_names:
                print(player_names)
                print (i,"y or n")
                answer = input()
                if answer == "y":
                    players.append(Player(j,i,start_money)) #                    number, name, money
                    player_names.pop(j)
                    break
                j+=1
                

def quick_start(start_money):
    players.append(Player(0,"Little Hazel",start_money))
    players.append(Player(1,"little Scotty",start_money))
    players.append(Player(2,"Toy car",start_money))
    players.append(Player(3,"Toy boat",start_money))



def init_board():
    #                   Name, cost, type, Monopoly other
    board.append(Place("Go",0,"go",0))
    board.append(Place("Burger Joint",1,"property",2))
    board.append(Place("Pizza House",1,"property",1))
    board.append(Place("Chance",0,"chance",0))
    board.append(Place("Candy Store",1,"property",5))
    board.append(Place("Ice Cream Parlor",1,"property",4))
    board.append(Place("Just Visiting",0,"visiting",0))
    board.append(Place("Museum",2,"property",8))
    board.append(Place("Library",2,"property",7))
    board.append(Place("Chance",0,"chance",0))
    board.append(Place("Skate Park",2,"property",11))
    board.append(Place("Swimming Pool",2,"property",10))
    board.append(Place("Free Parking",0,"parking",0))
    board.append(Place("Video Game Arcade",3,"property",14))
    board.append(Place("Movie Theater",3,"property",13))
    board.append(Place("Chance",0,"chance",0))
    board.append(Place("Toy Store",3,"property",17))
    board.append(Place("Pet Store",3,"property",16))
    board.append(Place("Go to Jail",0,"jail",0))
    board.append(Place("Bowling Alley",4,"property",20))
    board.append(Place("The Zoo",4,"property",19))
    board.append(Place("Chance",0,"chance",0))
    board.append(Place("Park Place",4,"property",23))
    board.append(Place("Boardwalk",4,"property",22))

def board_results():
    print()
    for i in board:
        owned = 0
        for j in players:
            if i.owner == j.number:
                print(j.name,i.name)
                owned = 1
        if owned == 0:        
            print("             ",i.name)


init_board()
init_players()
init_chance()
gameover = False

while gameover == False:
    #z=input()
    for i in range(0,numplayers):
        z=input()
        players[i].move()
        if players[i].money < 1:
            gameover = True
            #print(players[i].name,"Bankrupt!")
            print()
            break
        print()
#        sleep(1)

for i in range(0,numplayers):
    print(players[i].name,"has $",players[i].money)

#board_results()
exit()

