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

"""-Known_Bugs-
            
        > Whenever an enemy occupies a space previously occupied by another enemy there is a chance they will disappear
          becoming white and will reappear after the player moves
            - If the player purposefully runs into an enemy sometime the cell where the player is in combat will be white
            and the enemy will be one cell away
        
        > Clearing the top right info frame is not working right now, will fix soon.
        
    -In_Development-
    
        > Combat system
            X Show the player is in combat
            X Run system
            ~ Show if the enemies are overlapping
            - Player/Enemy health
            - Player/Enemy Attack
            
        > Working health bar/actions on bottom left frame
        
        > Refreshing the floor after reaching the exit
            ~ Works but should be implemented on further
        
        > Some sort of API implementation into the combat system
    
"""


def settings():
    return webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


def destroy_window():
    window.destroy()
    game_start()


def game_start():
    dungeon_floor = tk.Tk()
    dungeon_floor.configure(background=window_bg, cursor='dot')
    dungeon_floor.title('Dungeon Crawler')
    dungeon_floor.geometry('820x720')

    enemy_pos = {}
    player_pos = [0]

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
                chest = labels[x][y].config(bg='Gold')
        for z in range(1):
            y = randint(0, 4)
            labels[0][y].config(bg='Blue')
            player_pos.append(y)

        p_exit = labels[4][4].config(bg='Black')

    """Logic for the enemy AI, will flip a coin and choose a direction to move based on the flip as well as the (x, y)
       position of the player and will also run a check to see if it occupies the same square as the player"""

    def enemy_movement():
        print(f'Before: {enemy_pos}')
        for x in range(len(enemy_pos)):
            if player_pos == enemy_pos[0] or player_pos == enemy_pos[1]:
                combat()
            print(x)
            direction = randint(0, 1)
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
        for enemy in range(len(enemy_pos)):
            if player_pos == enemy_pos[enemy]:
                combat()
        if enemy_pos[1] == enemy_pos[0]:
            labels[enemy_pos[0][0]][enemy_pos[0][1]].config(bg='Dark Red')
            labels[enemy_pos[1][0]][enemy_pos[1][1]].config(bg='Dark Red')

    def quit_game():
        quit()

    """This frame will display the instructions, damage values, and whether or not you are in combat or not"""
    t_r_frame = tk.Frame(dungeon_floor, width=200, height=600, border=10, background=text_frame_bg)
    t_r_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=5)
    t_r_frame.propagate(False)

    """The combat method... more later"""

    b_l_frame = tk.Frame(dungeon_floor, width=600, height=200, border=10, background=input_frame_bg)
    b_l_frame.grid(row=1, column=0, padx=5, pady=5)

    # HEALTH SLIDER!!!
    player_hp = 99.9
    hp_slider = ttk.Progressbar(b_l_frame, orient=tk.HORIZONTAL, length=400)
    hp_slider.grid(column=0, row=0, rowspan=1, ipady=5)
    hp_slider.step(player_hp)

    def run():
        global in_combat
        count = 0
        count += 1
        run_chance = randint(1, 3)
        print(run_chance)
        if not in_combat:
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are not in combat, you cannot run.',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()
        else:
            if run_chance == 1:
                in_combat = False
                for widget in t_r_frame.winfo_children():
                    widget.destroy()
                text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are out of combat!!',
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()

            else:
                text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou fail to run and are still in combat!!',
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
        if count >= 5:
            for widget in t_r_frame.winfo_children():
                widget.destroy()

    def combat():
        global player_hp
        global in_combat
        in_combat = True
        player_turn = False
        turn_order = randint(1, 2)
        labels[player_pos[0]][player_pos[1]].config(bg='teal')
        text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are in combat!!',
                          font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                          fg="Light Gray")
        text_2.pack()
        # Turn order: 1 = enemy goes first, 2 = Player goes first
        if turn_order == 1:
            hit_chance = randint(1, 7)
            if hit_chance >= 5:
                dmg = randint(7, 15)
                player_hp -= dmg
        elif turn_order == 2:
            player_turn = True
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\n-It is your turn in combat-',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()

    def attack():
        pass

    """List of player actions. At the moment I don't really like this but it works for now"""

    hp_text = tk.Label(b_l_frame, text=f'HP: 100/{player_hp}', font=font, bg=button_bg)
    hp_text.grid(column=0, row=1)

    attack_btn = tk.Button(b_l_frame, text='ATTACK', bg=button_bg, command=attack)
    attack_btn.grid(row=0, column=1, padx=25, pady=5)

    run_btn = tk.Button(b_l_frame, text='RUN', bg=button_bg, command=run)
    run_btn.grid(row=1, column=1, padx=25, pady=5, ipadx=10)

    open_btn = tk.Button(b_l_frame, text='OPEN', command='', bg=button_bg)
    open_btn.grid(row=0, column=2, padx=15, pady=5)

    quit_btn = tk.Button(b_l_frame, text='QUIT', bg=button_bg, command=quit_game)
    quit_btn.grid(row=1, column=2, padx=15, pady=5)


    """These methods are the movement actions for the Player"""

    def up():
        global in_combat
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                y = player_pos[1]
                y -= 1
                player_pos[1] = y
                if y < 0:
                    raise IndexError
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                y = player_pos[1]
                y += 1
                player_pos[1] = y
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(len(enemy_pos)):
                if player_pos == enemy_pos[enemy]:
                    combat()
                    in_combat = True
                    break
            enemy_movement()

        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def down():
        global in_combat
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                y = player_pos[1]
                y += 1
                player_pos[1] = y
                if y > 4:
                    raise IndexError
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError:
                y = player_pos[1]
                y -= 1
                player_pos[1] = y
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            if player_pos == [4, 4]:
                dungeon_floor.destroy()
                game_start()
            for enemy in range(len(enemy_pos)):
                if player_pos == enemy_pos[enemy]:
                    combat()
                    in_combat = True
                    break
            enemy_movement()

        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def right():
        global in_combat
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                x = player_pos[0]
                x += 1
                player_pos[0] = x
                if x > 4:
                    raise IndexError
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError or player_pos[0] > 4:
                x = player_pos[0]
                x -= 1
                player_pos[0] = x
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            if player_pos == [4, 4]:
                dungeon_floor.destroy()
                game_start()
            for enemy in range(len(enemy_pos)):
                if player_pos == enemy_pos[enemy]:
                    combat()
                    in_combat = True
                    break
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def left():
        global in_combat
        if not in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                x = player_pos[0]
                x -= 1
                player_pos[0] = x
                if x < 0:
                    raise IndexError
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            except IndexError or player_pos[0] < 0:
                x = player_pos[0]
                x += 1
                player_pos[0] = x
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            for enemy in range(len(enemy_pos)):
                if player_pos == enemy_pos[enemy]:
                    combat()
                    in_combat = True
                    break
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
start_button = tk.Button(window, text="Start", command=destroy_window, bg=button_bg, fg='Black', pady=20, width=100,
                         font=font)
settings_button = tk.Button(window, text="Settings", command=settings, bg=button_bg, fg='Black', pady=20, width=100,
                            font=font)

text = tk.Label(window, wraplength=700, text="Use the on screen arrow keys to move."
                                             "\n\n -Your goal is the black square in the bottom right"
                                             "\n\n -There will be one \"chest\" that also randomly spawns"
                                             "\n\n -The red squares are enemies, run or fight do with them as you please.",
                font=(font, 15, "bold"), pady=20, bg=input_frame_bg,
                fg="Light Gray")

exit_button = tk.Button(window, text="Exit", bg=button_bg, fg='Black', command=exit, font=font)
title.pack(fill='x')
start_button.pack(pady=20)
settings_button.pack(pady=5)
text.pack(fill='x')
exit_button.pack(side='bottom', fill='x', ipady=15)

window.mainloop()
