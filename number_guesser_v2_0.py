# Anzeigen wie viel Spiele man gebraucht hat, um Score zu erreichen

import os
import random
import csv

# ################
# global variables
# ################

# clear cmd
clear = lambda: os.system('cls')
terminal_width = os.get_terminal_size()[0]

game_active = True
player_name = None
player_score = 0
lives = 3

# Variable für Runde
turn = 1

# ##########
# Funktionen
# ##########

# Funktion gibt Test in der Mitte der CMD aus und nicht linksbündig
def print_centered(text):
    text = str(text)
    print(text.center(terminal_width))

def print_game_title():
    clear()
    print('')
    print_centered('############################################')
    print_centered('##########  NUMBER GUESSING GAME  ##########')
    print_centered('############################################')
    print('')

def print_game_info():
    print_game_title()
    print_centered('The aim of the game is to guess the random number given by the computer.')
    print_centered('You can choose from three different levels of difficulty.')
    print_centered('The heavier, the more points you get. However, more points are also deducted from you.')
    print()
    print_centered('Back to menu?')
    input()
    start_game()

def print_menu():
    print_centered('1 - Play Game')
    print_centered('2 - Highscore')
    print_centered('3 - Info     ')
    print()
    print_centered('Type in menu number: ')

# Liefert vom Schwierigkeitsgrad abhängige Parameter
def get_setting_dif_level(level):
    # max_choices_comp, max_turns, score_raiser, score_downer
    if level == 1:
        return 5, 2, 5, 2
    elif level == 2:
        return 10, 3, 10, 3
    elif level == 3:
        return 50, 5, 50, 10

# Speichert den aktuellen Score mit Namen in der CSV Datei
def save_game():
    print_centered('Do you want to safe youre Score? Type in y or n: ')
    save_game = input()
    if save_game == 'y':
        with open(os.path.join(os.sys.path[0], "scores.csv"), 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([player_name, player_score])
        print_centered('Score saved for ' + player_name)
        input()

# Läd Daten aus CSV / sortiert nach Bubble Sort Algorithmus
def show_highscore():
    lst_highscore = []

    with open(os.path.join(os.sys.path[0], "scores.csv"), mode='r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            lst_highscore.append(row)
    # Äußere Schleife die jedes Element nimmt die innere durchführt
    for i in range(1, len(lst_highscore)):
        # Vergleicht äußeres ausgewähltes Element nochmals mit jedem, dass danach kommt, wenn kleiner werden Plätze getauscht
        for j in range(1, len(lst_highscore) - 1):
            if lst_highscore[j][1] < lst_highscore[j + 1][1]:
                lst_highscore[j], lst_highscore[j + 1] = lst_highscore[j + 1], lst_highscore[j]
    
    print_game_title()
    ranking = 0
    for score in lst_highscore:
        if ranking == 0:
            print_centered('Ranking'.ljust(10) + score[0].ljust(20) + score[1].ljust(10))
            print_centered('')
        else:
            print_centered(str(ranking).ljust(10) + score[0].ljust(20) + score[1].ljust(10))
        ranking += 1
    
    input()
    start_game()

# Startet Spiel mit Titel und Menü
def start_game():    
    menu_choice = 0
    print_game_title()
    print_menu()
    menu_choice = get_correct_input([1, 2, 3])
    menu_choice = int(menu_choice)
    if menu_choice == 1:
        print_game_title()
        global player_name
        if player_name == None:
            print_centered('Type in your username: ')
            player_name = input()
        play_game()
    elif menu_choice == 2:
        show_highscore()
    elif menu_choice == 3:
        print_game_info()

# Zwingt User so lange eine Eingabe zu machen, bis richtige Möglichkeit vorhanden --> Param: Mögliche Antworten (liste)
# anpassen, dass liste erst in liste mit strings umgewandelt wird
def get_correct_input(lst_right_inps):

    lst_strs = []
    for elem in lst_right_inps:
        lst_strs.append(str(elem))
    right_input = False
    while (right_input == False):           
        inp = input()   
        if inp in lst_strs:
            right_input = True
        else:
            if len(lst_right_inps) < 4:
                items = ' or '.join(lst_strs)
                print_centered('Please type in {} and press Enter!'.format(items))
            else:
                print_centered('Enter a number between ' + lst_strs[0] + ' and ' + lst_strs[-1] + '!')
    return inp

# Spiel
def play_game():
    # Player Score und lives auf global setzen, da scope globaö
    global player_score
    global lives

    # Schleifen Variable für jeweilige Runde
    turn_active = True
    # Spielinformationen
    dif_level = 0
    turn = 1
    comp_choice = 0
    player_choice = 0
    play_again = ''

    # Vom Schwierigkeitsgrad abhängige Variablen für Spieldynamik
    max_choices_comp = 0
    max_turns = 0    
    score_raiser = 0
    score_downer = 0

    print_game_title()
    print_centered('Choose your difficulty level: ')
    print_centered('1 - easy  ')
    print_centered('2 - middle')
    print_centered('3 - hard  ')
    print_centered('Type in your level of difficulty: ')
    dif_level = get_correct_input([1, 2, 3])
    dif_level = int(dif_level)
    max_choices_comp, max_turns, score_raiser, score_downer = get_setting_dif_level(dif_level)
    
    print_game_title()
    comp_choice = random.randint(1, max_choices_comp)
    # print_centered(comp_choice)
    print_centered('Computers number is between 1 and ' + str(max_choices_comp))
    print_centered('You got ' + str(max_turns) + ' trys.')
    
    # Schleife für jeweilige Runde
    while (turn_active == True and turn <= max_turns):
        print()
        print_centered('###### Turn ' + str(turn) + ' ######')
        print_centered('Lives:        ' + str(lives))
        print_centered('Player Score: ' + str(player_score))
        print()
        print_centered('Make a guess: ')
        player_choice = get_correct_input(list(range(1, max_choices_comp + 1)))
        player_choice = int(player_choice)
        print()
        # Eigentliche Spieldynamik (Abfrage ob eingegebene Zahl die richtige ist)
        if player_choice == comp_choice:
            print_centered('Computers Secret Number: ' + str(comp_choice))
            print_centered('You won! :)')
            print_centered('+ ' + str(score_raiser) + ' Points')
            player_score += score_raiser
            # Falls man die Zahl beim ersten Versuch erraten hat bekommt man ein extra Leben
            if turn == 1:
                print_centered('+ 1 live!')
                lives +=1
            print_centered('Player Score: ' + str(player_score))
            turn_active = False
            input()
        else:
            # Gibt Hinweis ob Zahl höher oder kleiner ist
            if player_choice > comp_choice:
                print_centered('Hint: to big!')
            else:
                print_centered('Hint: to small!')
            score_raiser -= score_downer
            # Falls keine Versuche zu raten mehr möglich sind
            if turn == max_turns:
                print()
                print_centered('You Loose!')
                print_centered('No trys left!')
                print_centered('Computers Secret Number was: ' + str(comp_choice))
                print_centered('- 1 Live :(')
                lives -= 1
                input()
            else:
                print_centered('Try again!')
            turn += 1
        print()
    
    print_game_title()
    print_centered('Player Score: ' + str(player_score))
    print_centered('Lives:        ' + str(lives))
    print()
    if lives > 0:
        print_centered('Play again? Type in y or n: ')
        play_again = get_correct_input(['y', 'n'])
        if play_again == 'y':
            start_game()
        elif play_again == 'n':
            global game_active
            game_active = False         
            save_game()
    else:
        print_centered('No lives left!')
        save_game()
        input()
        
# GAME
while(game_active == True):
    start_game()
