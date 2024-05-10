import tkinter as tk
import tkinter.ttk as ttk
from random import randint
from Player import Player
from Enemy import Enemy

# Palett for the program
window_bg = '#2A2D43'
input_frame_bg = '#414361'
text_frame_bg = '#7F2CCB'
button_bg = '#B880F7'
font = 'Arial'

in_combat = False
score = 0

rand_y = randint(0, 4)
player = Player(99, [0, rand_y])
enemy_1 = Enemy(20)
enemy_2 = Enemy(20)

"""-Known_Bugs-

        > Whenever an enemy occupies a space previously occupied by another enemy there is a chance they will disappear
          becoming white and will reappear after the player moves
            -If the player purposefully runs into an enemy sometime the cell where the player is in combat will be white
            and the enemy will be one cell away
        
        > HP slider is accepting enemy_hp and updating the slider with enemy & player values

        > Score is a bit buggy at times

        > Tried importing the cat pictures into the window but kept running into a 403 error
            - not sure why it wasn't authenticating I'll figure it out later

    -In_Development-

        > Combat system --COMPLETE--

        > Refreshing the floor after reaching the exit -COMPLETE-

"""


def settings():
    """A little "easter egg" I guess..."""
    pass


def destroy_window():
    """Mainly used for refreshing the floor after the player reaches [4, 4]"""
    player.in_combat = False
    window.destroy()
    game_start()


def game_start():
    """Main game window with alot of functions nested inside"""
    global score

    dungeon_floor = tk.Tk()
    dungeon_floor.configure(background=window_bg, cursor='dot')
    dungeon_floor.title('Dungeon Crawler')
    dungeon_floor.geometry('860x720')

    enemy_pos = [enemy_1.spawn(), enemy_2.spawn()]
    player_pos = Player.get_pos(player)
    coin_pos = []

    t_l_frame = tk.Frame(dungeon_floor, width=600, height=500, background=text_frame_bg)
    t_l_frame.grid(row=0, column=0, padx=5, pady=5)

    """Creates the floor grid using a for loop and list comprehension
        - Nabbed some of this code from Chat GPT because I was pulling my hair out trying to make a modular grid
    """
    labels = [[x for x in range(5)] for _ in range(5)]

    for i in range(5):
        for j in range(5):
            label_text = ''
            label = tk.Label(t_l_frame, text=label_text, borderwidth=1, relief="solid", width=16, height=7)
            label.grid(column=j, row=i, )
            labels[j][i] = label

    """This method randomly generates TWO enemies, ONE coin, and also handles spawning the Player
  The first column is dedicated specifically to the player spawn zone and cell (4, 4) is strictly the exit"""

    def create_rooms():
        labels[player_pos[0]][player_pos[1]].config(bg='Blue')
        labels[4][4].config(bg='Black')

        for g in enemy_pos:
            labels[g[0]][g[1]].config(bg='Red')
        for g in range(1):
            x = randint(1, 4)
            y = randint(0, 4)
            if x == 4 and y == 4:
                labels[4][3].config(bg='Gold')
                coin_pos.append([4, 3])
            else:
                labels[x][y].config(bg='Gold')
                coin_pos.append([x, y])

        print(enemy_pos[0], enemy_pos[1])

    def enemy_movement():
        """Logic for the enemy AI, will flip a coin and choose a direction to move based on the flip as well as the (x, y)
            position of the player and will also run a check to see if it occupies the same square as the player"""
        try:
            labels[coin_pos[0][0]][coin_pos[0][1]].config(bg='Gold')
        except IndexError:
            pass
        if in_combat:
            start_turn_order()
        else:
            try:
                e1_pos = enemy_1.get_position()
                labels[e1_pos[0]][e1_pos[1]].config(bg='White')

                e1_pos = enemy_1.movement(player_pos)
                labels[e1_pos[0]][e1_pos[1]].config(bg='Red')
            except IndexError:
                pass

            try:
                e2_pos = enemy_2.get_position()
                labels[e2_pos[0]][e2_pos[1]].config(bg='White')

                e2_pos = enemy_2.movement(player_pos)
                labels[e2_pos[0]][e2_pos[1]].config(bg='Red')
            except IndexError:
                pass
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
        """Quits the game from the dungeon scene"""
        quit()

    """This frame will display the instructions, damage values, and whether or not you are in combat or not"""
    t_r_frame = tk.Frame(dungeon_floor, width=200, height=600, border=10, background=text_frame_bg)
    t_r_frame.grid(row=0, column=1, padx=5, pady=5, ipadx=5)
    t_r_frame.propagate(False)

    """This frame is for player interaction with the game"""
    b_l_frame = tk.Frame(dungeon_floor, width=600, height=200, border=10, background=input_frame_bg)
    b_l_frame.grid(row=1, column=0, padx=5, pady=5)

    """HEALTH SLIDER - still broken unfortunately"""
    hp_slider = ttk.Progressbar(b_l_frame, orient=tk.HORIZONTAL, length=400)
    hp_slider.grid(column=0, row=0, rowspan=1, ipady=5)
    hp_slider.step(player.health)

    def run():
        """This function will check if you are in combat and if you are it will roll a 1/3 chance for you to escape the
            battle, on success combat will become False and the player can move again and on a fail the enemy will have
            its turn"""
        p_run = player.run()
        if p_run[0] == 0:
            text_2 = tk.Label(t_r_frame, wraplength=200, text=p_run[1],
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()
        else:
            if p_run[0] == 1:
                for widget in t_r_frame.winfo_children():
                    widget.destroy()
                text_2 = tk.Label(t_r_frame, wraplength=200, text=p_run[1],
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
            elif p_run[0] == 2:
                text_2 = tk.Label(t_r_frame, wraplength=200, text=p_run[1],
                                  font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                  fg="Light Gray")
                text_2.pack()
                player.player_turn = False
                enemy_combat(player.player_turn)
        player.player_turn = False

    def attack():
        """The attack button triggers this function and will roll a 1/6 random int on a roll higher than a 3 the player
         will attack for 7-15 damage, on miss the combat will flip to the enemies turn"""
        global enemy_hp
        global score
        for widget in t_r_frame.winfo_children():
            widget.destroy()

        if not player.in_combat:
            text_non = tk.Label(t_r_frame, wraplength=200, text='\nYou are not in combat, you cannot attack.',
                                font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                fg="Light Gray")
            text_non.pack()
        elif player.in_combat:
            att = player.attack(enemy_hp)
            enemy_hp = att[0]
            if att[1] == 'miss':
                text_miss = tk.Label(t_r_frame, wraplength=200, text=f'\nYou missed the enemy, it is their turn.',
                                     font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                     fg="Light Gray")
                text_miss.pack()
                player.player_turn = False
                enemy_combat(player.player_turn)

            elif att[1] != 'miss':
                if enemy_hp <= 0:
                    for enemy in range(0, 2):
                        if player_pos == enemy_pos[enemy]:
                            enemy_pos.pop(enemy)
                            break
                    text_beat = tk.Label(t_r_frame, wraplength=200, text='\nYou beat the enemy! you are out of combat.',
                                         font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                         fg="Light Gray")
                    text_beat.pack()
                    player.in_combat = False
                    score += 5
                    update_score(score)
                elif enemy_hp != 0:
                    text_non = tk.Label(t_r_frame, wraplength=200, text=f'\nYou hit the enemy for {att[1]} they '
                                                                        f'have {enemy_hp} health remaining.',
                                        font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                        fg="Light Gray")
                    text_non.pack()

    def start_turn_order():
        """Whenever combat is initiated this function will run, setting the enemy health to 20 and flipping a coin to
        see which side will make the first move. This function also turns the player & enemy teal to show where the
        player is"""
        global enemy_hp
        for widget in t_r_frame.winfo_children():
            widget.destroy()

        enemy_hp = 20

        labels[player_pos[0]][player_pos[1]].config(bg='teal')
        text_2 = tk.Label(t_r_frame, wraplength=200, text='\nYou are in combat!!',
                          font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                          fg="Light Gray")
        text_2.pack()
        player.in_combat = True
        enemy_combat(player.start_combat())

    def enemy_combat(player_turn):
        """Works very similar to the combat function but a hit will occur on a 5 or higher. This function is also
        responsible for checking if the player is 'dead' or not, if they are you will be sent back to the title screen
        """
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
                player.health -= dmg

                text_hit = tk.Label(t_r_frame, wraplength=200,
                                    text=f'\n-It is the enemies turn and they delt {dmg} damage.-',
                                    font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                                    fg="Light Gray")
                if player.health <= 0:
                    score = 0
                    main_menu()
                    dungeon_floor.destroy()

                text_hit.pack()

                player.player_turn = True

                update_health(player.health)
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
                player.player_turn = True
        elif player_turn:
            for widget in t_r_frame.winfo_children():
                widget.destroy()
            text_2 = tk.Label(t_r_frame, wraplength=200, text='\n-It is your turn in combat-',
                              font=(font, 10, "bold"), pady=20, bg=input_frame_bg,
                              fg="Light Gray")
            text_2.pack()

    """These labels are responsible for relaying health and score to the player"""
    score_text = tk.Label(b_l_frame, text=f'Score:{score}', font=font, bg=input_frame_bg, fg='White')
    score_text.grid(column=1, row=1)

    hp_text = tk.Label(b_l_frame, text=f'HP: {player.health}/99', font=font, bg=button_bg)
    hp_text.grid(column=0, row=1)

    def update_health(hp):
        """Updates the health label"""
        hp_text = tk.Label(b_l_frame, text=f'HP: {hp}/99', font=font, bg=button_bg)
        hp_slider.step(hp)
        hp_text.grid(column=0, row=1)

    def update_score(player_score):
        """Updates the player score label"""
        score_text = tk.Label(b_l_frame, text=f'Score:{player_score}', font=font, bg=input_frame_bg, fg='White')
        score_text.grid(column=1, row=1)

    """The buttons are the actions the user can make during their time in the dungeon scene"""
    attack_btn = tk.Button(b_l_frame, text='ATTACK', bg=button_bg, command=attack)
    attack_btn.grid(row=0, column=1, padx=25, pady=5)

    run_btn = tk.Button(b_l_frame, text='RUN', bg=button_bg, command=run)
    run_btn.grid(row=0, column=2, padx=25, pady=5, ipadx=10)

    quit_btn = tk.Button(b_l_frame, text='QUIT', bg=button_bg, command=quit_game)
    quit_btn.grid(row=1, column=2, padx=15, pady=5)

    def check_coin():
        """This function poorly solves an issue where and enemy would make coins disappear if the ever went on its
        cell"""
        global score
        try:
            if player_pos == coin_pos[0]:
                score += 2
                labels[coin_pos[0][0]][coin_pos[0][1]].config(bg='Blue')
                coin_pos.pop()
                update_score(score)
        except IndexError:
            pass

    """These methods are the movement actions for the Player. Down and Right are special however because those contain
    logic for if the player escapes the floor, they also take care of the API calling"""

    def up():
        if not player.in_combat:
            print(player_pos)
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                p_up = player.movement('up')
                if p_up[1] < 0:
                    raise IndexError
                labels[p_up[0]][p_up[1]].config(bg='Blue')
            except IndexError:
                player.movement('down')
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        player.in_combat = True
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
        global score
        if not player.in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                p_up = player.movement('down')
                if p_up[1] > 4:
                    raise IndexError
                labels[p_up[0]][p_up[1]].config(bg='Blue')
            except IndexError:
                player.movement('up')
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        player.in_combat = True
                        break
            except IndexError:
                pass
            if player_pos == [4, 4]:
                player.reset_pos()
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
        global score
        if not player.in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                p_up = player.movement('right')
                if p_up[0] > 4:
                    raise IndexError
                labels[p_up[0]][p_up[1]].config(bg='Blue')
            except IndexError:
                player.movement('left')
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        player.in_combat = True
                        break
            except IndexError:
                pass
            if player_pos == [4, 4]:
                player.reset_pos()
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
        if not player.in_combat:
            labels[player_pos[0]][player_pos[1]].config(bg='White')
            try:
                p_up = player.movement('left')
                if p_up[0] < 0:
                    raise IndexError
                labels[p_up[0]][p_up[1]].config(bg='Blue')
            except IndexError:
                player.movement('right')
                labels[player_pos[0]][player_pos[1]].config(bg='Blue')
            try:
                for enemy in range(0, 2):
                    if player_pos == enemy_pos[enemy]:
                        player.in_combat = True
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

    """this frame contains movement, and the buttons below are for player movement"""
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
