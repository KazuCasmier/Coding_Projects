import tkinter as tk
import tkinter.ttk as ttk
import collections
import urllib
import webbrowser
from random import randint

# Palett for the program
window_bg = '#2A2D43'
input_frame_bg = '#414361'
text_frame_bg = '#7F2CCB'
button_bg = '#B880F7'
font = 'Arial'

in_combat = False
enemy_pos = {}
player_pos = [0]

"""-Known_Bugs-

        > Player can get OOB really easily and break the game
            - Player can now *wrap* around the screen but will still break enemy AI
            
        > Some of the enemy spawn are still buggy and will not display movement correctly
            - Maybe not bugged entirely, pretty sure it has something to do with the try and except statements
            
        > Clearing the top right info frame is not working right now, will fix soon.
        
    -In_Development-
    
        > Combat system
    
        > Working health bar/actions on bottom left frame
        
        > Refreshing the floor after reaching the exit
        
        > Some sort of API implementation into the combat system
    
"""


def settings():
    return webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


def game_start():
    window.destroy()
    dungeon_floor = tk.Tk()
    dungeon_floor.configure(background=window_bg, cursor='dot')
    dungeon_floor.title('Dungeon Crawler')
    dungeon_floor.geometry('820x720')

    t_l_frame = tk.Frame(dungeon_floor, width=600, height=500, background=text_frame_bg)
    t_l_frame.grid(row=0, column=0, padx=5, pady=5)


    """Creates the floor grid using a for loop and list comprehension
  - Nabbed some of this code from Chat GPT because I was pulling my hair out trying to make a modular grid"""
    labels = [[x for x in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            label_text = ''
            label = tk.Label(t_l_frame, text=label_text, borderwidth=1, relief="solid", width=16, height=7)
            label.grid(column=j, row=i, )
            labels[j][i] = label

    """This method randomly generates TWO enemies, ONE treasure, and also handles spawning the Player
  The first column is dedicated specifically to the player spawn zone and cell (4, 4) is strictly the exit"""

    def create_rooms():
        for e in range(2):
            x = randint(1, 4)
            y = randint(0, 4)
            if x == 4 and y == 4:
                labels[3][4].config(bg='Red')
                enemy_pos.update({e: [x, y]})
            else:
                labels[x][y].config(bg='Red')
                enemy_pos.update({e: [x, y]})
        for g in range(1):
            x = randint(1, 4)
            y = randint(0, 4)
            if x == 4 and y == 4:
                pass
            else:
                labels[x][y].config(bg='Gold')
        for z in range(1):
            y = randint(0, 4)
            labels[0][y].config(bg='Blue')
            player_pos.append(y)

        p_exit = labels[4][4].config(bg='Black')

    """Logic for the enemy AI, will flip a coin and choose a direction to move based on the flip as well as the (x, y)
       position of the player and will also run a check to see if it occupies the same square as the player"""

    def enemy_movement():
        print(f'Before: {enemy_pos}')
        for x in range(2):
            print(x)
            direction = randint(0, 1)
            # print(f'Enemy: {x}, {direction}, {enemy_pos[x][1]}')
            labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='White')
            # Direction 0 = x, 1 = y
            if direction == 0:
                if player_pos[0] >= enemy_pos[x][0]:
                    labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='White')
                    enemy_pos[x][0] += 1
                    try:
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                    except IndexError:
                        enemy_pos[x][0] -= 1
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                elif player_pos[0] < enemy_pos[x][0]:
                    labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='White')
                    enemy_pos[x][0] -= 1
                    try:
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                    except IndexError:
                        enemy_pos[x][0] += 1
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
            elif direction == 1:
                if player_pos[1] >= enemy_pos[x][1]:
                    labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='White')
                    enemy_pos[x][1] += 1
                    try:
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                    except IndexError:
                        enemy_pos[x][1] -= 1
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                elif player_pos[1] < enemy_pos[x][1]:
                    try:
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
                    except IndexError:
                        enemy_pos[x][1] += 1
                        labels[enemy_pos[x][0]][enemy_pos[x][1]].config(bg='Red')
        for enemy in range(2):
            if player_pos == enemy_pos[enemy]:
                combat()

    def quit_game():
        quit()

    """This frame will display the instructions, damage values, and whether or not you are in combat or not"""
    t_r_frame = tk.Frame(dungeon_floor, width=200, height=600, border=10, background=text_frame_bg)
    t_r_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=5)
    text = tk.Label(t_r_frame, wraplength=200, text="Use the arrow keys below to move."
                                                    "\n\n  Your goal is the gray square in the bottom left"
                                                    "\n\n  There will be one \"chest\" that also randomly spawns"
                                                    "\n\n  The red squares are enemies, run or fight do with them as you please.",
                    font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                    fg="Light Gray")
    text.pack()
    t_r_frame.propagate(False)

    """The combat method... more later"""
    def combat():
        global in_combat
        in_combat = True
        turn_order = randint(1, 2)
        text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are in combat!!',
                          font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                          fg="Light Gray")
        text_2.pack()
        # Turn order: 1 = enemy goes first, 2 = Player goes first
        if turn_order == 1:
            pass

        elif turn_order == 2:
            pass

    def run():
        global in_combat
        run_chance = randint(1, 3)
        print(run_chance)
        if run_chance == 1:
            in_combat = False
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are out of combat!!',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()

        else:
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou fail to run and are still in combat!!',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()

    """List of player actions. At the moment I don't really like this but it works for now"""
    b_l_frame = tk.Frame(dungeon_floor, width=600, height=200, border=10, background=text_frame_bg)
    b_l_frame.grid(row=1, column=0, padx=5, pady=5)

    # HEALTH SLIDER!!!
    hp_slider = (ttk.Progressbar(b_l_frame, orient=tk.HORIZONTAL, length=400, mode="determinate")
                 .grid(column=0, row=0, rowspan=2, ipady=10))

    attack_btn = (tk.Button(b_l_frame, text='ATTACK', bg=button_bg)
                  .grid(row=0, column=1, padx=25, pady=5))
    run_btn = (tk.Button(b_l_frame, text='RUN', bg=button_bg, command=run)
               .grid(row=1, column=1, padx=25, pady=5, ipadx=10))
    open_btn = (tk.Button(b_l_frame, text='OPEN', command='', bg=button_bg)
                .grid(row=0, column=2, padx=15, pady=5))
    quit_btn = (tk.Button(b_l_frame, text='QUIT', bg=button_bg, command=quit_game)
                .grid(row=1, column=2, padx=15, pady=5))

    """These methods are the movement actions for the Player"""

    def up():
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            y = player_pos[1]
            y -= 1
            player_pos[1] = y
            try:
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                y += 1
                player_pos[1] = y
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(2):
                if player_pos == enemy_pos[enemy]:
                    combat()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def down():
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            y = player_pos[1]
            y += 1
            player_pos[1] = y
            try:
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                y -= 1
                player_pos[1] = y
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(2):
                if player_pos == enemy_pos[enemy]:
                    combat()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def right():
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            x = player_pos[0]
            x += 1
            player_pos[0] = x
            try:
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                x -= 1
                player_pos[0] = x
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(2):
                if player_pos == enemy_pos[enemy]:
                    combat()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def left():
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            x = player_pos[0]
            x -= 1
            player_pos[0] = x
            try:
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                x += 1
                player_pos[0] = x
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(2):
                if player_pos == enemy_pos[enemy]:
                    combat()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    b_r_frame = tk.Frame(dungeon_floor, width=200, height=200, border=10, background=input_frame_bg)
    b_r_frame.grid(row=1, column=1, padx=5, pady=5)
    left_btn = (tk.Button(b_r_frame, text='<-', command=left)
                .grid(row=2, column=0, padx=5))
    up_btn = (tk.Button(b_r_frame, text='/\\', command=up)
              .grid(row=1, column=1, padx=5))
    down_btn = (tk.Button(b_r_frame, text='\/', command=down)
                .grid(row=3, column=1, padx=5))
    right_btn = (tk.Button(b_r_frame, text='->', command=right)
                 .grid(row=2, column=2, padx=5))
    create_rooms()


"""Sets up the main menu screen"""

window = tk.Tk()
window.configure(background=window_bg, cursor='dot')
window.title('Dungeon Crawler')
window.geometry('700x600')
title = tk.Label(window, text="Dungeon Crawler!!!", font=(font, 28, "bold"), pady=20, bg=input_frame_bg,
                 fg="Light Gray")
start_button = tk.Button(window, text="Start", command=game_start, bg=button_bg, fg='Black', pady=20, width=100,
                         font=font)
settings_button = tk.Button(window, text="Settings", command=settings, bg=button_bg, fg='Black', pady=20, width=100,
                            font=font)
exit_button = tk.Button(window, text="Exit", bg=button_bg, fg='Black', command=exit, font=font)
title.pack(fill='x')
start_button.pack(pady=20)
settings_button.pack(pady=5)
exit_button.pack(side='bottom', fill='x', ipady=15)

window.mainloop()
