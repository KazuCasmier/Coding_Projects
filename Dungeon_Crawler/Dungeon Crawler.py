import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from PIL import Image
import json
import urllib.request
from random import randint
import requests

# Palett for the program
window_bg = '#2A2D43'
input_frame_bg = '#414361'
text_frame_bg = '#7F2CCB'
button_bg = '#B880F7'
font = 'Arial'

a_url = "https://api.thecatapi.com/v1/images/search"
api_key = 'live_ehTh1jGqE3KtAPJPAkEoxXZZQ7E1IixoCJTnaFUQm3WkaQDEufJWx2CaJzkH136k'
query_params = {'x-api-key': api_key, 'limit': 1}

in_combat = False
player_turn = True
player_hp = 99
enemy_hp = 20
score = 0

"""-Known_Bugs-
            
        > Whenever an enemy occupies a space previously occupied by another enemy there is a chance they will disappear
          becoming white and will reappear after the player moves
            -If the player purposefully runs into an enemy sometime the cell where the player is in combat will be white
            and the enemy will be one cell away
        
        > Clearing the top right info frame is not working right now, will fix soon.
            - works but is ugly
        
        > HP slider is accepting enemy_hp and updating the slider with enemy & player values
        
    -In_Development-
    
        > Combat system --COMPLETE--
            X Show the player is in combat
            X Run system
            X Show if the enemies are overlapping
            X Player/Enemy health
            X Player/Enemy Attack
        
        > Refreshing the floor after reaching the exit
            X Refreshes floor
            X Adds to score with a treasure bonus (if collected)
        
        > Some sort of API implementation into the combat system
            - Looking for a suitable api
    
"""


def settings():
    return webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


def destroy_window():
    global in_combat
    in_combat = False
    window.destroy()
    game_start()


def game_start():
    global player_hp
    global score

    dungeon_floor = tk.Tk()
    dungeon_floor.configure(background=window_bg, cursor='dot')
    dungeon_floor.title('Dungeon Crawler')
    dungeon_floor.geometry('860x720')

    in_combat = False
    enemy_pos = []
    player_pos = [0]
    coin_pos = []

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
                enemy_pos.append([x, y])
            else:
                labels[x][y].config(bg='Red')
                enemy_pos.append([x, y])
                print(enemy_pos)
        for g in range(1):
            x = randint(1, 4)
            y = randint(0, 4)
            if x == 4 and y == 4:
                labels[4][3].config(bg='Gold')
                coin_pos.append([4, 3])
            else:
                labels[x][y].config(bg='Gold')
                coin_pos.append([x, y])
        for z in range(1):
            y = randint(0, 4)
            labels[0][y].config(bg='Blue')
            player_pos.append(y)

        labels[4][4].config(bg='Black')
        print(enemy_pos[0], enemy_pos[1])

    """Logic for the enemy AI, will flip a coin and choose a direction to move based on the flip as well as the (x, y)
       position of the player and will also run a check to see if it occupies the same square as the player"""

    def enemy_movement():
        print(f'Before: {enemy_pos}')
        try:
            labels[coin_pos[0][0]][coin_pos[0][1]].config(bg='Gold')
        except IndexError:
            pass
        if in_combat:
            start_turn_order()
        else:
            for x in range(len(enemy_pos)):
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
                    start_turn_order()
            try:
                if enemy_pos[1] == enemy_pos[0]:
                    labels[enemy_pos[0][0]][enemy_pos[0][1]].config(bg='Dark Red')
                    labels[enemy_pos[1][0]][enemy_pos[1][1]].config(bg='Dark Red')
            except IndexError:
                pass

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
    hp_slider = ttk.Progressbar(b_l_frame, orient=tk.HORIZONTAL, length=400)
    hp_slider.grid(column=0, row=0, rowspan=1, ipady=5)
    hp_slider.step(player_hp)

    def run():
        global player_turn
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
        elif in_combat:
            if run_chance == 1:
                for widget in t_r_frame.winfo_children():
                    widget.destroy()
                text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are out of combat!!',
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
                in_combat = False
            else:
                text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou fail to run and are still in combat!!',
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
                player_turn = False
                enemy_combat()
        player_turn = False

    def attack():
        global player_turn
        global enemy_hp
        global in_combat
        global score

        enemy_img = ''
        if not in_combat:
            text_non = tk.Label(t_r_frame, wraplength=200, text='\nYou are not in combat, you cannot attack.',
                                font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                fg="Light Gray")
            text_non.pack()
        elif in_combat:
            hit_chance = randint(1, 6)
            if hit_chance > 3:
                player_dmg = randint(7, 15)
                enemy_hp -= player_dmg
                if enemy_hp <= 0:
                    print(enemy_pos)
                    for widget in t_r_frame.winfo_children():
                        widget.destroy()
                    for enemy in range(0, 2):
                        if player_pos == enemy_pos[enemy]:
                            enemy_pos.pop(enemy)
                            break
                    print(enemy_pos)

                    in_combat = False
                    text_beat = tk.Label(t_r_frame, wraplength=200, text='\nYou beat the enemy! you are out of combat.',
                                         font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                         fg="Light Gray")
                    text_beat.pack()
                    response = requests.request('GET', url=a_url, params=query_params)
                    response = response.json()
                    print(response)
                    enemy_img = response[0]['url']
                    print(enemy_img)
                    # urllib.request.urlretrieve(enemy_img, 'test.png')

                    webbrowser.open(enemy_img)
                    score += 5
                    update_score(score)
                elif enemy_hp != 0:
                    text_non = tk.Label(t_r_frame, wraplength=200, text=f'\nYou hit the enemy for {player_dmg} they '
                                                                        f'have {enemy_hp} health remaining.',
                                        font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                        fg="Light Gray")
                    text_non.pack()
            else:
                for widget in t_r_frame.winfo_children():
                    widget.destroy()
                text_miss = tk.Label(t_r_frame, wraplength=200, text=f'\nYou missed the enemy, it is their turn.',
                                     font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                     fg="Light Gray")
                text_miss.pack()

            player_turn = False
            enemy_combat()

    def start_turn_order():
        global player_turn
        global enemy_hp
        global in_combat
        for widget in t_r_frame.winfo_children():
            widget.destroy()

        enemy_hp = 20
        in_combat = True
        turn_order = randint(1, 2)

        labels[player_pos[0]][player_pos[1]].config(bg='teal')
        text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are in combat!!',
                          font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                          fg="Light Gray")
        text_2.pack()

        if turn_order == 1:
            player_turn = False
        elif turn_order == 2:
            player_turn = True

        enemy_combat()

    def enemy_combat():
        global player_hp
        global player_turn
        global in_combat
        global score

        if not player_turn:
            text_turn = tk.Label(t_r_frame, wraplength=200,
                                 text=f'\n-Enemy Turn-',
                                 font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                 fg="Light Gray")
            text_turn.pack()
            hit_chance = randint(1, 7)
            if hit_chance >= 5:
                print("hit")
                dmg = randint(7, 15)
                player_hp -= dmg

                text_hit = tk.Label(t_r_frame, wraplength=200,
                                    text=f'\n-It is the enemies turn and they delt {dmg} damage.-',
                                    font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                    fg="Light Gray")
                if player_hp <= 0:
                    score = 0
                    main_menu()
                    dungeon_floor.destroy()

                text_hit.pack()
                player_turn = True
                update_health(player_hp)
                text_2 = tk.Label(t_r_frame, wraplength=200, text='\n-It is now your turn.-',
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
            else:
                text_miss = tk.Label(t_r_frame, wraplength=200,
                                     text=f'\n-The enemy missed its attack! It is your turn.-',
                                     font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                     fg="Light Gray")
                text_miss.pack()
                player_turn = True
        elif player_turn:
            for widget in t_r_frame.winfo_children():
                widget.destroy()
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\n-It is your turn in combat-',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()

    """List of player actions. At the moment I don't really like this but it works for now"""
    score_text = tk.Label(b_l_frame, text=f'Score:{score}', font=font, bg=input_frame_bg, fg='White')
    score_text.grid(column=1, row=1)

    hp_text = tk.Label(b_l_frame, text=f'HP: {player_hp}/99', font=font, bg=button_bg)
    hp_text.grid(column=0, row=1)

    def update_health(hp):
        hp_text = tk.Label(b_l_frame, text=f'HP: {hp}/99', font=font, bg=button_bg)
        hp_slider.step(hp)
        hp_text.grid(column=0, row=1)

    def update_score(player_score):
        score_text = tk.Label(b_l_frame, text=f'Score:{score}', font=font, bg=input_frame_bg, fg='White')
        score_text.grid(column=1, row=1)

    attack_btn = tk.Button(b_l_frame, text='ATTACK', bg=button_bg, command=attack)
    attack_btn.grid(row=0, column=1, padx=25, pady=5)

    run_btn = tk.Button(b_l_frame, text='RUN', bg=button_bg, command=run)
    run_btn.grid(row=0, column=2, padx=25, pady=5, ipadx=10)

    quit_btn = tk.Button(b_l_frame, text='QUIT', bg=button_bg, command=quit_game)
    quit_btn.grid(row=1, column=2, padx=15, pady=5)

    def check_coin():
        global score
        try:
            if player_pos == coin_pos[0]:
                score += 2
                labels[coin_pos[0][0]][coin_pos[0][1]].config(bg='Blue')
                coin_pos.pop()
                update_score(score)
        except IndexError:
            pass

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
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        in_combat = True
                        break
            except IndexError:
                pass
            check_coin()
            enemy_movement()

        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def down():
        global in_combat
        global score
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
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        in_combat = True
                        break
            except IndexError:
                pass
            if player_pos == [4, 4]:
                dungeon_floor.destroy()
                score += 2
                game_start()
            check_coin()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    def right():
        global in_combat
        global score
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
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        in_combat = True
                        break
            except IndexError:
                pass
            if player_pos == [4, 4]:
                dungeon_floor.destroy()
                score += 2
                game_start()
            check_coin()
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
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        in_combat = True
                        break
            except IndexError:
                pass
            check_coin()
            enemy_movement()
        else:
            text_3 = tk.Label(t_r_frame, wraplength=200, text='You cannot move, you are in combat',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_3.pack()

    b_r_frame = tk.Frame(dungeon_floor, width=200, height=200, border=10, background=input_frame_bg)
    b_r_frame.grid(row=1, column=1, padx=5, pady=5)

    left_btn = tk.Button(b_r_frame, text='<-', command=left)
    left_btn.grid(row=2, column=0, padx=5)

    up_btn = tk.Button(b_r_frame, text='/\\', command=up)
    up_btn.grid(row=1, column=1, padx=5)

    down_btn = tk.Button(b_r_frame, text='\/', command=down)
    down_btn.grid(row=3, column=1, padx=5)

    right_btn = tk.Button(b_r_frame, text='->', command=right)
    right_btn.grid(row=2, column=2, padx=5)

    create_rooms()


"""Sets up the main menu screen"""


def main_menu():
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
                                                 "\n\n -The red squares are enemies, run or fight do with them as you "
                                                 "please.",
                    font=(font, 15, "bold"), pady=20, bg=input_frame_bg,
                    fg="Light Gray")

    exit_button = tk.Button(window, text="Exit", bg=button_bg, fg='Black', command=exit, font=font)
    title.pack(fill='x')
    start_button.pack(pady=20)
    settings_button.pack(pady=5)
    text.pack(fill='x')
    exit_button.pack(side='bottom', fill='x', ipady=15)

    window.mainloop()


window = tk.Tk()
main_menu()
