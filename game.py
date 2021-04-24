from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import domino
import os
import random
from math import *
import minimax

set_of_tiles = []
number_tiles = [0,0,0,0,0,0,0]
tiles_on_field = []
player_hand = []
ai_hand = []
game_frame = None
buttons = []
labels = []
field = []

player_score = 0
ai_score = 0
ps = "Pionts: " + str(player_score)
ais = "0" + str(ai_score)

def delete_tiles():
    for i in labels:
        i.destroy

def start_up():
    cover = Label(game_frame, bg="white", width=1800,height=800).place(x=30,y=90)
    player_side = Label(game_frame,bg="black", width=150, height=5).place(x=0, y=600)
    ai_side = Label(game_frame,bg="black", width=150, height=5).place(x=0, y=0)
    random_button = Button(game_frame,text="Take Random Tile",bg="gray", width=15,height=1,command=lambda:get_random_tile(1)).place(x=790,y=580)
    random_button = Button(game_frame,text="Pass",bg="green", width=10,height=1,command=lambda:ai_decision_making()).place(x=700,y=580)
    playerscore = Label(game_frame,bg="white",text=ps,width=20,height=3).place(x=750,y=605)
    aiscore = Label(game_frame,bg="white",text=ais,width=20,height=3).place(x=750,y=30)
    set_of_tiles.clear()
    tiles_on_field.clear()
    player_hand.clear()
    ai_hand.clear()
    create_tiles()
    
    i = 0
    while i < 7:
        ai = random.randint(0,len(set_of_tiles)-1)
        ai_hand.append(set_of_tiles.pop(ai))
        pl = random.randint(0,len(set_of_tiles)-1)
        player_hand.append(set_of_tiles.pop(pl))
        i+=1
    
    
    show_ai_hand()
    show_player_hand()


def clear_frame():
    for widget in game_frame:
        widget.master.destroy()


def add_(hand):
    score = 0
    for i in hand:
        score += i.topval
        score += i.bottomval
    return score


def find_max(tiles):
    maxt = tiles[0]
    for i in tiles:
        num = i.topval + i.bottomval
        m = maxt.topval + maxt.bottomval
        if num > m:
            maxt = i
    return maxt


def ai_decision_making():
    ai_temp_hand = []
    for i in ai_hand: #get playable tiles
        if i.topval == tiles_on_field[0].openval:
            ai_temp_hand.append(i)
        if i.bottomval == tiles_on_field[0].openval:
            ai_temp_hand.append(i)
        if i.topval == tiles_on_field[-1].openval:
            ai_temp_hand.append(i)
        if i.bottomval == tiles_on_field[-1].openval:
            ai_temp_hand.append(i)
    
    if len(ai_temp_hand) == 0: #if none, get random tile
        if len(set_of_tiles) > 0:
            get_random_tile(0)
            ai_decision_making()
        else:
            print("AI cannot get tile")
            return
    
    utility = -inf #utility value
    utile = None #uitility tile
    temp_field = tiles_on_field[:]
    for t in ai_temp_hand: #minimax to make decision
        maxi = minimax.minimax(temp_field,ai_hand,'a',field,set_of_tiles,t)
        if maxi > utility:
            utility = maxi
            utile = t
    
    player_place_tile(utile,ai_hand,0) #place tile
    return




def display():
    print("###")
    for t in tiles_on_field:
        print("openval: " + str(t.openval) + " x: " + str(t.x) + " y: " + str(t.y))


def get_random_tile(x):
    if len(set_of_tiles) == 0:
        print("No more Tiles")
    elif x == 0:
        ai = random.randint(0,len(set_of_tiles)-1)
        ai_hand.append(set_of_tiles.pop(ai))
        show_ai_hand()
    else:
        pl = random.randint(0,len(set_of_tiles)-1)
        player_hand.append(set_of_tiles.pop(pl))
        show_player_hand()
    

def removetile(filename):
    i = 0
    while i < len(ai_hand):
        if ai_hand[i].f == filename:
            ai_hand.pop(i)
            break
        i += 1
    i = 0
    while i < len(player_hand):
        if player_hand[i].f == filename:
            player_hand.pop(i)
            #buttons[i].destroy()
            break
        i += 1


def show_player_hand():
    buttons.clear()
    x1 = 0
    y1 = 600
    
    for d in player_hand:
        d1 = d
        img = d.image
        b = Button(game_frame,image=img,command=lambda d=d1:player_place_tile(d,player_hand,1)).place(x=x1,y=y1)
        buttons.append(b)
        x1+=60


def place_tile(d,val,angle,x1,y1):
    d.align_tile(angle)
    img = d.image
    l = Label(game_frame,image=img, bg="black").place(x=x1,y=y1)
    labels.append(l)
    t = domino.place_t(val,x1,y1)
    field.append(d)
    return t
    
    
    
def player_place_tile(d,hand,g):
    if len(tiles_on_field) == 0:
        number_tiles[d.topval] += 1
        number_tiles[d.bottomval] += 1
        d.align_tile(90)
        img = d.image
        l = Label(game_frame,image=img, bg="black").place(x=450,y=500)
        game_window.update()
        t = domino.place_t(d.topval,450,500)
        t2 = domino.place_t(d.bottomval,451,500)
        tiles_on_field.append(t)
        tiles_on_field.append(t2)
        removetile(d.f)
        field.append(d)
        if g == 0:
            show_ai_hand()
            show_player_hand()
            display()
        else:
            show_player_hand()
            ai_decision_making()
    elif tiles_on_field[0].openval == d.topval:
        number_tiles[d.topval] += 1
        number_tiles[d.bottomval] += 1
        if tiles_on_field[0].x <= 450:
            if tiles_on_field[0].x <= 100:
                if tiles_on_field[0].y <=180:
                    t = place_tile(d,d.bottomval,90,tiles_on_field[0].x+50,tiles_on_field[0].y)
                else:
                    t = place_tile(d,d.bottomval,0,tiles_on_field[0].x,tiles_on_field[0].y-50)
            else:
                t = place_tile(d,d.bottomval,270,tiles_on_field[0].x-50,tiles_on_field[0].y)
        else: 
            if tiles_on_field[0].x >= 800:
                if tiles_on_field[0].y <= 180:
                    t = place_tile(d,d.bottomval,270,tiles_on_field[0].x-50,tiles_on_field[0].y)
                else:
                    t = place_tile(d,d.bottomval,0,tiles_on_field[0].x,tiles_on_field[0].y-50)
            else:
                t = place_tile(d,d.bottomval,90,tiles_on_field[0].x+50,tiles_on_field[0].y)
        tiles_on_field.insert(0,t)
        removetile(d.f)
        if g == 0:
            show_ai_hand()
            show_player_hand()
            display()
        else:
            show_player_hand()
            ai_decision_making()
    elif tiles_on_field[0].openval == d.bottomval:
        number_tiles[d.topval] += 1
        number_tiles[d.bottomval] += 1
        if tiles_on_field[0].x <= 450:
            if tiles_on_field[0].x <= 100:
                if tiles_on_field[0].y <=180:
                    t = place_tile(d,d.topval,270,tiles_on_field[0].x+50,tiles_on_field[0].y)
                else:
                    t = place_tile(d,d.topval,0,tiles_on_field[0].x,tiles_on_field[0].y-50)
            else:
                t = place_tile(d,d.topval,90,tiles_on_field[0].x-50,tiles_on_field[0].y)
        else: 
            if tiles_on_field[0].x >= 800:
                if tiles_on_field[0].y >= 180:
                    t = place_tile(d,d.topval,90,tiles_on_field[0].x-50,tiles_on_field[0].y)
                else:
                    t = place_tile(d,d.topval,0,tiles_on_field[0].x,tiles_on_field[0].y-50)
            else:
                t = place_tile(d,d.topval,270,tiles_on_field[0].x+50,tiles_on_field[0].y)
        tiles_on_field.insert(0,t)
        removetile(d.f)
        if g == 0:
            show_ai_hand()
            show_player_hand()
            display()
        else:
            show_player_hand()
            ai_decision_making()
    elif tiles_on_field[-1].openval == d.topval:
        number_tiles[d.topval] += 1
        number_tiles[d.bottomval] += 1
        if tiles_on_field[-1].x <= 450:
            if tiles_on_field[-1].x <= 100:
                if tiles_on_field[-1].y <=180:
                    t = place_tile(d,d.bottomval,90,tiles_on_field[-1].x+50,tiles_on_field[-1].y)
                else:
                   t = place_tile(d,d.bottomval,0,tiles_on_field[-1].x,tiles_on_field[-1].y-50)
            else:
                t = place_tile(d,d.bottomval,270,tiles_on_field[-1].x-50,tiles_on_field[-1].y)
        else: 
            if tiles_on_field[-1].x >= 800:
                if tiles_on_field[-1].y <= 180:
                    t = place_tile(d,d.bottomval,270,tiles_on_field[-1].x-50,tiles_on_field[-1].y)
                else:
                    t = place_tile(d,d.bottomval,0,tiles_on_field[-1].x,tiles_on_field[-1].y-50)
            else:
                t = place_tile(d,d.bottomval,90,tiles_on_field[-1].x+50,tiles_on_field[-1].y)
        tiles_on_field.append(t)
        removetile(d.f)
        if g == 0:
            show_ai_hand()
            show_player_hand()
            display()
        else:
            show_player_hand()
            ai_decision_making()
    elif tiles_on_field[-1].openval == d.bottomval:
        number_tiles[d.topval] += 1
        number_tiles[d.bottomval] += 1
        if tiles_on_field[-1].x <= 450:
            if tiles_on_field[-1].x <= 100:
                if tiles_on_field[-1].y <=180:
                    t = place_tile(d,d.topval,270,tiles_on_field[-1].x+50,tiles_on_field[-1].y)
                else:
                    t = place_tile(d,d.topval,0,tiles_on_field[-1].x,tiles_on_field[-1].y-50)
            else:
                t = place_tile(d,d.topval,90,tiles_on_field[-1].x-50,tiles_on_field[-1].y)
        else: 
            if tiles_on_field[-1].x >= 800:
                if tiles_on_field[-1].y >= 180:
                   t = place_tile(d,d.topval,90,tiles_on_field[-1].x-50,tiles_on_field[-1].y)
                else:
                    t = place_tile(d,d.topval,0,tiles_on_field[-1].x,tiles_on_field[-1].y-50)
            else:
                t = place_tile(d,d.topval,270,tiles_on_field[-1].x+50,tiles_on_field[-1].y)
        tiles_on_field.append(t)
        removetile(d.f)
        if g == 0:
            show_ai_hand()
            show_player_hand()
            display()
        else:
            show_player_hand()
            ai_decision_making()
    else:
        print("The tile cannot be added.")
        display()   
    
    
    
    
    
    

def create_tiles():
    images = os.listdir('images/')
    images.pop(len(images)-1)
    ln = 0
    rn = 0
    rl = 0
    for imagefile in images:
        imagefile = "images/" + imagefile
        dominop = domino.tile(imagefile,ln,rn)
        set_of_tiles.append(dominop)
        if rn == 6:
            rl+=1
            rn = rl
            ln+=1
        else:
            rn+=1
    minimax.set_up(set_of_tiles)

def show_ai_hand():
    x1 = 0
    y1 = 0
    for d in ai_hand:
        img = Image.open('images/blank.png')
        img = img.resize((40,40),Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img)
        l = Label(game_frame,image=img2).place(x=x1,y=y1)
        x1+=60
    
    
game_window = Tk(className="AI Domino Game")
game_window.geometry("900x680")
game_frame = Canvas(game_window, width=900, height=680)
game_frame.pack()

GAME_LOOP = True
while GAME_LOOP:
    game_window.update()
    
    if len(ai_hand) == 0:
        print("AI WINS Round")
        ai_score += add_(player_hand)
        af = open("ai.txt","a")
        af.write(str(ai_score) + "\n")
        af.close()
        if ai_score >= 100:
            print("AI Wins Game")
            cover = Label(game_frame, bg="white", width=1800,height=800).place(x=30,y=90)
            l = Label(game_frame, text="CPU WINS").place(x=450,y=320)
            game_window.after(5000, game_window.destroy())
        print("Pionts scored: " + str(ai_score))
        ais = "Pionts: " + str(ai_score)
        game_frame.delete('all')
        start_up()
    elif len(player_hand) == 0:
        print("Player Wins Round")
        player_score += add_(ai_hand)
        pf = open("player.txt","a")
        pf.write(str(player_score) + "\n")
        pf.close()
        if player_score >= 100:
            print("Player Wins Game")
            cover = Label(game_frame, bg="white", width=1800,height=800).place(x=30,y=90)
            l = Label(game_frame, text="PLAYERS WINS").place(x=450,y=320)
            game_window.after(5000, game_window.destroy())
        print("Pionts scored: " + str(ai_score))
        ps = "Pionts: " + str(player_score)
        game_frame.delete('all')
        start_up()
    
