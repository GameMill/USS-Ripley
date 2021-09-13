from math import fabs
import time
import random
import os

################### Start of Global Variables ###################
Version = 0.25

lives = 10
player_name = ""
navigation_key = False
medical_bay_key = False
engine_room_key = False
holodeck_key = False
Storage_key = False
debug = True

################### Start of Global function ###################

def clear_screen():
    print ("\n" * 100)
    

def print_with_color(text, color):
    try:
        print("\33[38;5;" + str(color) + "m",end="",flush=True)
        terminal_text(str(text))
        print("\33[0m",end="",flush=True) # reset after printing text
    except print(0):
        pass

def terminal_text(text):
    global debug
    for c in text:
        print(c,end="",flush=True)
        if debug == False:
            seconds = "0.0" + str(random.randint(3, 8))
        else:
            seconds = "0.0"
        time.sleep(float(seconds))
    print("")

def int_input(text,min, max):
    try:
        user_input = int(input(text))
        if user_input >= min and user_input <= max:
            return user_input
        else:
            print("invalid input")
            return int_input(text,min,max)
    except:
        print("invalid input")
        return int_input(text,min,max)

def true_false_converter(value):
    if value == True:
        return "(Completed)"
    else:
        return ""

def yes_no_input(text):
    yes = ['y' , 'yes']
    no = ['n' , 'no']
    user_input = input(text).lower()
    if(user_input in yes):
        return "y"
    elif(user_input in no):
        return "n"
    else:
        print(f"Invalid input: {user_input}")
        return yes_no_input(text)

################### End of Global function ###################


#################### Start of Storage room ######################


def storage_room_start():
    global Storage_key
    hit_or_stike_game()
    print("t")

cards = []
users_cards = []
dealer_cards = []
user_bust = False
dealer_bust = False

def restart_game():
    global cards
    global users_cards
    global dealer_cards
    global user_bust
    global dealer_bust
    cards = []
    users_cards = []
    dealer_cards = []
    user_bust = False
    dealer_bust = False
    clear_screen()
    

def reset_cards():
    global cards
    cards = []
    for suits in ["Heart","Diamond","Club", "Spade"]:
        for card in range(13):

            cards.append({"suits":suits,"card":card+1});
      
    
def get_card_name(number):
    if number == 13:
        return "Ace"
    elif number == 12:
        return "king"
    elif number == 11:
        return "Quean"
    elif number == 10:
        return "Jack"
    else:
        return number

def get_card_value(number,bust):
    if number > 9:
        if number == 13:
            if bust:
                return 1
            else:
                return 11
        else:
            return 10
    else:
        return number

def hit_or_stike_game():
    global user_bust
    global dealer_bust
    restart_game()
    
    print("")
    print("Welcome to a game of 21. Good Luck")
    print("")
    reset_cards()
    print("The Dealer shuffle the card and start drawing the cards.")
    if(debug == False):
        time.sleep(5)
    draw_users_cards()
    draw_dealer_cards()
    user_turn()

def user_input_stick_twist(text):
    stick = ["s","stick"]
    twist = ["t","twist"]
    u_input = input(text).lower()
    if u_input in stick:
        return "s"
    elif u_input in twist:
        return "t"
    else:
        print("Invalid Input")
        return user_input_stick_twist(text);

def user_turn():
    global users_cards
    global user_bust
    print("")
    print("Your card are")
    print("")
    for item in range(len(users_cards)):
        print(f"{get_card_name(users_cards[item]['card'])} of {users_cards[item]['suits']}")
    print("")
    u_input = user_input_stick_twist("Stick or Twist: ")
    if u_input == "t":
        extra_card = draw_extra_users_card()
        print("The Dealer Drawing a card.")
        if(debug == False):
            time.sleep(5)

        if(get_total(users_cards,False) > 21 and get_total(users_cards,True) < 21):
            user_bust = True

        if get_total(users_cards,user_bust) > 21:
            print(f"Your extra card was {get_card_name(extra_card['card'])} of {extra_card['suits']}")
            print("You Lose!")
            if(debug == False):
                time.sleep(5)
            hit_or_stike_game()
        else:
            if len(users_cards) == 5:
                print("5 Card Trick!")
                print("You Win!")
                exit()
            else:
                user_turn()
    else:
        dealer_turn()
    

def dealer_turn():
    global dealer_cards
    global users_cards
    global user_bust
    global dealer_bust
    global Storage_key
    global lives
    dealer_total = get_total(dealer_cards,dealer_bust)
    users_total = get_total(users_cards,user_bust)

    print("The Dealer flip his cards.")
    if(debug == False):
        time.sleep(3)
    
    print("")
    print("dealers card are")
    print("")
    for item in range(len(dealer_cards)):
        if(debug == False):
            time.sleep(1)
        print(f"{get_card_name(dealer_cards[item]['card'])} of {dealer_cards[item]['suits']}")
    
    print("Dealer is thinking")
    if(debug == False):
        time.sleep(5)
    if(get_total(dealer_cards,False) > 21 and get_total(dealer_cards,True) <= 21):
            dealer_bust = True

    if get_total(dealer_cards,dealer_bust) >= get_total(users_cards,user_bust) and get_total(dealer_cards,dealer_bust) <= 21:
        lives -= 1
        if lives == 0:
            game_over()
        print("You Lose!")
        if(debug == False):
            time.sleep(5)
        hit_or_stike_game() 
    if dealer_total < 15 or get_total(dealer_cards,True) < 10 or get_total(dealer_cards,dealer_bust) < get_total(users_cards,user_bust) and get_total(dealer_cards,dealer_bust) < 21:
        card = draw_extra_dealer_card()
        print("Dealer draws an extra card")
        if(debug == False):
            time.sleep(5)
        print(f"the Dealer extra card was {get_card_name(card['card'])} of {card['suits']}")
            
        dealer_turn()
    elif get_total(dealer_cards,dealer_bust) > 21:
        print("Dealer is bust")
        print("You Win!")
        if(debug == False):
            time.sleep(5)

        
        Storage_key = True
        Corridor()
    else:
        if get_total(users_cards, user_bust) > 21:
            lives -= 1
            if lives == 0:
                game_over()
            print("You Lose!")
            if(debug == False):
                time.sleep(5)
            hit_or_stike_game()    
        elif get_total(dealer_cards, dealer_bust) > 21:
            print("You Win!")
            Corridor()
        elif users_total > dealer_total:
            print("You Win!")
            Corridor()
        elif users_total < dealer_total:
            lives -= 1
            if lives == 0:
                game_over()
            print("You Lose!")
            if(debug == False):
                time.sleep(5)
            hit_or_stike_game()
        else:
            lives -= 1
            if lives == 0:
                game_over()
            print("Draw. Sorry i mean you Lose!")
            if(debug == False):
                time.sleep(5)
            hit_or_stike_game()
    
def get_total(cards,bust):
    total = 0
    for item in cards:
        total += get_card_value(item["card"],bust)
    return total
    

def draw_extra_users_card():
    global users_cards
    global cards
    card1_index = random.randint(0,len(cards)-1)
    card1= cards[card1_index]
    cards.pop(card1_index)
    users_cards.append(card1)
    return card1

def draw_extra_dealer_card():
    global dealer_cards
    global cards
    card1_index = random.randint(0,len(cards)-1)
    card1= cards[card1_index]
    cards.pop(card1_index)
    dealer_cards.append(card1)
    return card1


def draw_users_cards():
    global cards
    global users_cards

    card1_index = random.randint(0,len(cards)-1)

    card2_index = random.randint(0,len(cards)-1)
    while card1_index == card2_index:
        card2 = random.randint(0,len(cards)-1)


    card1 = cards[card1_index];
    card2= cards[card2_index]
    if card1_index < card2_index:
        cards.pop(card2_index)
        cards.pop(card1_index)
    else:
        cards.pop(card1_index)
        cards.pop(card2_index)

    users_cards = [card1,card2]

def draw_dealer_cards():
    global cards
    global dealer_cards

    card1_index = random.randint(0,len(cards)-1)

    card2_index = random.randint(0,len(cards)-1)
    while card1_index == card2_index:
        card2 = random.randint(0,len(cards)-1)


    card1 = cards[card1_index];
    card2 = cards[card2_index]
    
    if card1_index < card2_index:
        cards.pop(card2_index)
        cards.pop(card1_index)
    else:
        cards.pop(card1_index)
        cards.pop(card2_index)

    dealer_cards = [card1,card2]





#################### End of Storage room #########################
def game_over(died_in_boss_fight):
    if died_in_boss_fight:
        print("""
        Exploded fuel barrels litter the floor, expended plasma cartridges fizzing vile green fumes into the air. And yet, it still stands. When it rushes you this time, there's no energy left in your legs, no focus left in your head - just the brief acknowledgement that you'd rather close your eyes than see what it intends to do with those claws.

        This time, as hard as you tried, you didn't escape.

        \u001b[31m
          ▄████     ▄▄▄          ███▄ ▄███▓   ▓█████     ▒█████      ██▒   █▓   ▓█████     ██▀███  
         ██▒ ▀█▒   ▒████▄       ▓██▒▀█▀ ██▒   ▓█   ▀    ▒██▒  ██▒   ▓██░   █▒   ▓█   ▀    ▓██ ▒ ██▒
        ▒██░▄▄▄░   ▒██  ▀█▄     ▓██    ▓██░   ▒███      ▒██░  ██▒    ▓██  █▒░   ▒███      ▓██ ░▄█ ▒
        ░▓█  ██▓   ░██▄▄▄▄██    ▒██    ▒██    ▒▓█  ▄    ▒██   ██░     ▒██ █░░   ▒▓█  ▄    ▒██▀▀█▄  
        ░▒▓███▀▒    ▓█   ▓██▒   ▒██▒   ░██▒   ░▒████▒   ░ ████▓▒░      ▒▀█░     ░▒████▒   ░██▓ ▒██▒
         ░▒   ▒     ▒▒   ▓▒█░   ░ ▒░   ░  ░   ░░ ▒░ ░   ░ ▒░▒░▒░       ░ ▐░     ░░ ▒░ ░   ░ ▒▓ ░▒▓░
          ░   ░      ▒   ▒▒ ░   ░  ░      ░    ░ ░  ░     ░ ▒ ▒░       ░ ░░      ░ ░  ░     ░▒ ░ ▒░
        ░ ░   ░      ░   ▒      ░      ░         ░      ░ ░ ░ ▒          ░░        ░        ░░   ░ 
              ░          ░  ░          ░         ░  ░       ░ ░           ░        ░  ░      ░     
                                                                          ░                         
        """)
    else:
        print("""
        Cursing your bad luck at another failed puzzle, you stumble back into the main corridor, hearing the whoosh and whirr of the door re-locking behind you. If you only had a few more seconds, or some kind of clue...

        There's a noise. Only momentarily, mind you - a sharp sound, like a harshly exhaled breath - cut almost precisely in half. A faint pitter-patter of liquid on metal. You feel oddly comfortable, all of a sudden - the odd warmth of pre-detonation power couplets under your feet has faded, and the ache in your legs from running down endless corridors is gone.

        You look down.

        A silver hand is protruding from your chest - just below your ribcage. Surreally, there's no blood on its' bladed fingers - whatever metallic thing stabbed you, blood slides off it with zero friction. The hand pulls back, and you can see your legs give way, see the floor come up to meet you, and then there is blackness.

        This time, you didn't escape.

        \u001b[31m
          ▄████     ▄▄▄          ███▄ ▄███▓   ▓█████     ▒█████      ██▒   █▓   ▓█████     ██▀███  
         ██▒ ▀█▒   ▒████▄       ▓██▒▀█▀ ██▒   ▓█   ▀    ▒██▒  ██▒   ▓██░   █▒   ▓█   ▀    ▓██ ▒ ██▒
        ▒██░▄▄▄░   ▒██  ▀█▄     ▓██    ▓██░   ▒███      ▒██░  ██▒    ▓██  █▒░   ▒███      ▓██ ░▄█ ▒
        ░▓█  ██▓   ░██▄▄▄▄██    ▒██    ▒██    ▒▓█  ▄    ▒██   ██░     ▒██ █░░   ▒▓█  ▄    ▒██▀▀█▄  
        ░▒▓███▀▒    ▓█   ▓██▒   ▒██▒   ░██▒   ░▒████▒   ░ ████▓▒░      ▒▀█░     ░▒████▒   ░██▓ ▒██▒
         ░▒   ▒     ▒▒   ▓▒█░   ░ ▒░   ░  ░   ░░ ▒░ ░   ░ ▒░▒░▒░       ░ ▐░     ░░ ▒░ ░   ░ ▒▓ ░▒▓░
          ░   ░      ▒   ▒▒ ░   ░  ░      ░    ░ ░  ░     ░ ▒ ▒░       ░ ░░      ░ ░  ░     ░▒ ░ ▒░
        ░ ░   ░      ░   ▒      ░      ░         ░      ░ ░ ░ ▒          ░░        ░        ░░   ░ 
              ░          ░  ░          ░         ░  ░       ░ ░           ░        ░  ░      ░     
                                                                          ░                         
        \u001b[0m
        """)
    exit()



########### Start of holodeck ###########


guesses_remaining = 4



def holodeck_start():
    global guesses_remaining
    global holodeck_key
    global debug
    intro = ("You are now are entering the Holodeck.\n\n After the eerie quiet of the corridor, the noise of an excited audience roar is unnaturally loud in your ears. When the audience finally quiets, you realise they are all turned to face you. Through the sudden hush 'Nice to see you! To see you nice!' ring's through the auditorium as an aging figure in a tan polyester suit sidles his way towards you, pushing a big 20th century microphone in your face. The crowd starts to chant 'Brucey, Brucey, Brucey.' He waves his hand over the crowd and they hush themselves in anticipation of his next words. 'Ladies and Gentlemen! Here is our saviour! We are in an infinate loop, if you can guess the right number we are all saved! will you play?' It's all too much, the leering crowd, the appalling suit, you can't think straight. Brucey's voice comes booming through your haze.")
    print("")
    print(intro)
    print("")
    if debug == False: 
        time.sleep(20)

    bruce = random.randint(1,5)  
    
    keep_playing = True
    while keep_playing == True: 
        guess = int_input("Pick a number  between 1 and 5! ",1,5)#do we want to change this to make the odds better for the player?
        
        # Decrease guess counter by one each time to limit to four guesses.
        guesses_remaining =- 1
        if guess == bruce:
            print ("You win! We're saved! Suddenly Brucey is wearing a smart pair of PJ's holding a cup of cocoa and waving his other hand over the crowd. 'Go home! Keep dancing! the crowd fades away and the holodeck goes dark as you return to the corridor.")
            # End game after correct guess.
            keep_playing = False
            holodeck_key = True
        # Counter to determine amount of guesses left
        elif guesses_remaining == 0:
            print (f" Ah what a shame. You're out of tries! The number was {bruce} Better luck next time!")
            # End game after max attempts.
            keep_playing = False
        elif guess != bruce:
            print("Oh, wasn’t that a shame, not to worry, try again.")
        else:
            print()
    if debug == False:  
        time.sleep(10)
    Corridor()

##################################### Start Of Starting Into #####################################

def start_game(): ##Game function wrapper to send user to beginning if they fail
    global debug
    global player_name
    global lives

    ##INTRODUCTION SCENE
    print(f"""
Game Version: V{Version}
    \u001b[32m
     ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄       ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄ 
    ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░▌       ▐░▌
    ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀      ▐░█▀▀▀▀▀▀▀█░▌ ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀█░▌▐░▌          ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌
    ▐░▌       ▐░▌▐░▌          ▐░▌               ▐░▌       ▐░▌     ▐░▌     ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌       ▐░▌
    ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░█▄▄▄▄▄▄▄█░▌     ▐░▌     ▐░█▄▄▄▄▄▄▄█░▌▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
    ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
    ▐░▌       ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌     ▐░█▀▀▀▀█░█▀▀      ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌          ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ 
    ▐░▌       ▐░▌          ▐░▌          ▐░▌     ▐░▌     ▐░▌       ▐░▌     ▐░▌          ▐░▌          ▐░▌               ▐░▌     
    ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌      ▐░▌  ▄▄▄▄█░█▄▄▄▄ ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     
    ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     
     ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀      
    \u001b[0m""")                                                                                                                           


    ##Introductory text crawl
    print("You awaken, cold and alone in your quarters. The ship beneath you pitches and shakes, the sound of metal-on-metal filling your ears. The only light comes from your personal terminal, pulsing violently with lines of green and red light.\n\
    You get up from your bunk. There is a film of condensation on the floor, an odd warmth under your feet despite the coolness of the air. Not a good sign. Time to check the terminal.")

    #TERMINAL TEXT HERE
    print_with_color("""//ALL HANDS: ALARM ALARM ALARM
    //STATUS REPORT: USS RIPLEY HAS SUFFERED UNEXPECTED CATASTROPHIC DAMAGE
    //RECOMMENDATION: IMMEDIATE EVACUATION""",124)
    
    print("\n Underneath the ominous warning is a single flashing input cursor:")

    #Function provides information about the ship
    player_name = input("PROVIDE USER NAME - ").strip()
    while(player_name == ""):
        print("Invalid Input")
        player_name = input("PROVIDE USER NAME - ").strip()
    def know_more():
        global lives
        player_action = input("WELCOME {}. The USS Ripley is critically damaged. Would you like to know more? Y/N     ".format(player_name)).lower().strip()
        if player_action in ["y","yes"]:
            ##system status 'variables' - can be edited based on puzzle design per room: this will combine info from all 3 lists and print it out aesthetically
            systems = ['Engineering','Navigation','Medbay','Holodeck']
            statuses = ['damaged','damaged','damaged','damaged']
            details = ['Electrical systems compromised, power flow interrupted.','Overflow error in primary navcomputer.','Medical computer lockdown.','Infinite loop detected - please troubleshoot.']
            for sys, stat, det in zip(systems,statuses,details):
                print_with_color("{0} is {1}. {2}".format(sys, stat, det),2)
        elif player_action in ["n","no"]:
            print_with_color("OK. GOOD LUCK.",2)
            lives = 5 ##Optional hard mode for funsies 
        else:
            print_with_color("INCORRECT COMMAND. REPEAT?",2)
            know_more()
    know_more()

    print("With your newfound knowledge, you set out in order to save your life. Anyone else will have to fend for themselves.")
    if debug == False:
        time.sleep(5)

    ##Changes the player room to the corridor
    Corridor()

####################################### End Of Starting Into ######################################


####################################### Starting Of Navigation Room ######################################

navigation_actual_words = [
    "superman" , # 1
    "spaceship", # 2
    "explosion", # 3
    "engineer",  # 4
    "alien",     # 5
    "bitcoin",   # 6
    "python",    # 7
    "integer",   # 8
    "avatar",    # 9
    "jumanji",   # 10
]

def jumble(word):
    argsArray = []
    data = ""
    for i in range(len(word)):
        argsArray.append(word[i])
    
    for i in range(len(word)):
        i2 = random.randint(0,len(argsArray)-1)
        data += argsArray[i2]
        argsArray.pop(i2)
    return data
        
        
    

def navigation_start():
    global navigation_key
    print_with_color("CRITICAL ERROR: Default navstate has been compromised - UNKNOWN LOCATION. Please correct 3 anagrams in order to reset stellar matrices.",2)
    current_round = 0
    
    for item in range(3):
        current_round += 1
        terminal_text("")
        terminal_text(f"Round: {current_round}")
        terminal_text("")
        word = random.choice(navigation_actual_words)
        navigation_2(word)
    print("")
    print("You have been given a keycard")
    print("")
    if debug == False:
        time.sleep(5)
    navigation_key = True
    Corridor()

# function to print from jumbled words and intake answer
def navigation_2(word):
    global navigation_jumbled_words
    global navigation_actual_words
    global lives

    word_index = navigation_actual_words.index(word)

    terminal_text (f"Un-jumble this word: \u001b[33m{jumble(word)}\u001b[0m")
    entered_word = (input("please enter your answer: ").lower().strip())
    if entered_word == "":
        print("Invalid Input")
        navigation_2(word)
    else:
        if entered_word in navigation_actual_words:
            entered_word_index = navigation_actual_words.index(entered_word)
            if word_index == entered_word_index:
                terminal_text(f"{entered_word} is \u001b[32mcorrect!\u001b[0m")
                navigation_actual_words.pop(word_index)
            else:
                
                lives -= 1;
                if lives == 0:
                    game_over(False)
                else:
                    print("")
                    print(f"Lives Remaining: {lives}")
                    print("")
                    terminal_text (f"\u001b[31mIncorrect\u001b[0m, try again")
                    navigation_2(word)
        else:
            lives -= 1;
            if lives == 0:
                game_over(False)
            else:
                print("")
                print(f"Lives Remaining: {lives}")
                print("")
                terminal_text (f"\u001b[31mIncorrect\u001b[0m, try again")
            navigation_2(word)


####################################### End Of Navigation Room ######################################





####################################### Start of Engine Room #######################################

engine_room_wires = ["red","blue","green","black","brown","white"]
engine_room_wires_tried = ["","","","","",""]

engine_room_correct_wire = random.choice(engine_room_wires);

engine_room_correct_wire_number = engine_room_wires.index(engine_room_correct_wire)


if (engine_room_correct_wire_number+1) < 4:
    engine_room_x1 = (4 - random.randint(0,engine_room_correct_wire_number+1)); # cylinders
else:
    engine_room_x1 = (4 - random.randint(0,3)); # cylinders



engine_room_corrent_wire_numnbr_re = 14-(engine_room_correct_wire_number+1)
engine_room_x2 = engine_room_corrent_wire_numnbr_re - engine_room_x1




####################### Start of Room code #######################

def engine_room_start():
    global debug
    global engine_room_key
    if engine_room_key == True:
        print("You already have the key for the engine room")
        Corridor()

    text = """You enter the engine room - seeing sights of devastation and brutality. Your comrades in engineering lie strewn around the room, in various iterations of death. Some asphyxiated before the emergency forcefield covered up the hole left by whatever ripped through the ship. Some were lucky enough to be smashed to pieces by it directly. Troublingly, a few lie on the floor missing most of their entrails - smears of partially-frozen blood around them. You pick up a survival knife from the stiff hand of one of your former friends, sliding it into your toolbelt.

    Having a closer look, you see the main engine, a hastily-opened toolbox, and the primary engineering computer - which is running loop after loop of error functions.
    """
    print(text)
    if debug == False:
        time.sleep(4)

    text = """
    The computer is festooned with blinking emergency lights.
    """
    print(text)
    if debug == False:
        time.sleep(2)

    
    text = """
    Do you want to go over to the computer?  
    Y: Use the computer
    N: Go back to the corridor
    >>> """

    answer = yes_no_input(text);
    
    if answer == "y":
        print("")
        engine_room_2()
    else:
        Corridor()

def engine_room_2():
    global debug
    print("You press the start button and a progress bar appears, sliding down the screen.")
    if debug == False:
        time.sleep(2)
    i = 1
    while(i < 25):
        print(f"Progress: {i}%");
        if(debug == False):
            time.sleep(.1)
        i += 1

    text = """
    //ERROR: Subsystem engine managment failed 0x2146721.
    Do you want to attempt to restart the system?
    """
    print(text)

    if debug == False:
        time.sleep(5)

    text = """
    Y: Restart the engine managment system
    N: Go back to the corridor
    >>> """

    answer = yes_no_input(text);
    
    if answer == "y":
        engine_room_computer(True)
    else:
        Corridor()

def engine_room_computer(show_panel_text):
    global lives
    global engine_room_wires_tried
    global engine_room_correct_wire
    global debug
    global engine_room_x1
    global engine_room_x2
    global engine_room_correct_wire_number

    if show_panel_text == True:
        text = """
    Nothing happens. You notice that there is a panel open behind the screen, having been pulled open earlier by some unlucky soul. You have a closer look.
        """
        print(text)
        if debug == False: 
            time.sleep(5)
     
    text = """
    
    There are 6 wires that have been cut: a 
    red wire, a blue wire, a green wire,
    a black wire, a brown wire and a white wire.
    You also have one extra wire carrying power to the console, and 
    you need to connect it to the right wire.
    """
    print(text)

    if(debug == False):
        time.sleep(10)
        
    extra = ""
    if(debug):
        extra = f"""
    Correct answer is 14-({engine_room_x1}+{engine_room_x2}) = {14-(engine_room_x1+engine_room_x2)} | {engine_room_correct_wire_number+1}"""

    text = f"""
    Which wire do you choose?

    1: Red wire {engine_room_wires_tried[0]}
    2: Blue wire {engine_room_wires_tried[1]}
    3: Green wire {engine_room_wires_tried[2]}
    4: Black wire {engine_room_wires_tried[3]}
    5: Brown wire {engine_room_wires_tried[4]}
    6: White wire {engine_room_wires_tried[5]}
    7: Leave the wires and look around the room again
    {extra}
    >>> """
    if debug == True: 
        wire_chosen = int_input(text,1,8) # 1 is index
    else:
        wire_chosen = int_input(text,1,7) # 1 is index

    if wire_chosen == 8:
        print(f"The correct wire is {engine_room_correct_wire}")
        engine_room_computer(False)

    elif wire_chosen == 7:
            engine_room_look_around()

    elif engine_room_wires_tried[wire_chosen-1] != "":
        print("You have already tried that wire")
        engine_room_computer(False)
    else:
        if engine_room_correct_wire == engine_room_wires[wire_chosen-1]: # 0 is index
            engine_room_4()
        else:
            print("A brutal shock issues up your arm, even through your protective gloves.")
            lives -= 1
            engine_room_one_shot_complete = False
            print(f"Lives Remaning: {lives}")
            engine_room_wires_tried[wire_chosen-1] = "(Tried)"

            if debug == False:
                time.sleep(5)

            
            if lives > 0:
                text = """
    Do you want to try again?

    1: Back to Computer
    2: Look around
    
    >>> """
                user_input = int_input(text,1,2)
                if user_input == 1:
                    engine_room_computer(False)
                else:
                    engine_room_look_around()
            else:
                game_over(False)




def engine_room_look_around():
    text = """
    You see the main engine, a hastily-opened toolbox, and the primary engineering computer - which is still running loop after loop of error functions.
    
    1: Goto Engine
    2: Goto Toolbox
    3: Back to Computer
    
    >>> """
    user_input = int_input(text, 1, 3);
    if user_input == 1:
        engine_room_engine()
    elif user_input == 2:
        engine_room_toolbox()
    else:
        engine_room_computer(False)




def engine_room_engine(): # puzzle complate
    global debug
    global engine_room_x1
    text = f"""
    You have a closer look at the engine.

    An older model, the engine has \33[38;5;1m4 massive cylinders and 3 panels.\33[0m
    """
    if engine_room_x1 > 0:
        text += f"There is also an \33[38;5;2mx symbol on {engine_room_x1} of the cylinders.\33[0m"
    print(text)
    if debug == False:
        time.sleep(4)

    if engine_room_x1 > 0:
        text = "    Why is that there? What is the significance?"
    else:
        text = ""

    text += """

    1: Goto Toolbox
    2: Goto Computer
    
    >>> """
    user_input = int_input(text, 1, 2);
    if user_input == 1:
        engine_room_toolbox()
    else:
        engine_room_computer(False)

def engine_room_toolbox(): # puzzle complate
    global engine_room_x2
    global engine_room_x1
    global debug
    if engine_room_x1 == 0:
        cx_text = "     "
    else:
        cx_text = "Cx - "
    
    if engine_room_x2 == 0:
        Is_text = "  "
    else:
        Is_text = "Is"
    text = f"""
    You have opened the toolbox and are looking inside.
    There are \33[38;5;1m7 screwdriver sets\33[0m and 13 different little parts."""
    if engine_room_x2 != 0:
        text += f"""
    You have a closer look and \33[38;5;2m{engine_room_x2} items have an \"S\"\33[0m, 
    """
    text += f"""
    There is also a note saying:

    \"
    ------------------------------------------------------------------------
    | I've been trying to fix the engine managment system                  |
    | but I can`t remember which wire to connect to the power line.        |
    |                                                                      |
    |                                                                      |
    | Jeff wrote a sum to remember, but I don`t know where the numbers go. |
    |                                                                      |
    |  T = C + Sd + P                                                      |
    |  Power Line = T - {cx_text}{Is_text}                                            |
    |                                                                      |
    | Why didn't that jerk just tell me which one to connect?              |
    |                                                                      |
    --^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-
    \"
    """
    print(text)
    if debug == False:
        time.sleep(15)
    text = """
    
    1: Goto Engine
    2: Goto Computer
    
    >>> """
    user_input = int_input(text, 1, 2);
    if user_input == 1:
        engine_room_engine()
    else:
        engine_room_computer(False)


def engine_room_4(): # puzzle complate
    global debug
    global engine_room_key

    print("You have connected the wire, and  return to the screen.")
    if debug == False:
        time.sleep(3)
    
    text = """
    //ERROR: Subsystem engine managment failed 0x2146721.
    Do you want to attempt to restart the system?
    """
    print(text)

    if debug == False:
        time.sleep(5)

    text = """
    Press the enter key to restart the engine managment system 
    >>> """
    answer = input(text);
    
    i = 1
    while(i <= 100):
        print(f"Progress: {i}%");
        if(debug == False):
            time.sleep(.1)
        i += 1
    text = """
    //SUCCESS: The system is now fully operational

    POP!

    A panel opens, with an override keycard inside for the emergency doors.
    You pick up the keycard.
    """
    print(text)
    if debug == False:
        time.sleep(5)
    text = "You are returning to the corridor."
    if debug == False:
        time.sleep(5)
    engine_room_key = True
    Corridor()





####################################### Starting Of Medical Bay Room ######################################

def medical_bay_start():
    print("")
    print ("You have entered the medical bay. Ironically, considering the state of the crew, the bio-beds are empty, the doctor lying dead in his chair.")
    print ("You remember something about a medical computer lockdown - you must need to crack the password.")
    print("Time to look around the medical bay until you find a clue.")
   
    look_around()

def look_around():
    look_at = int_input("""
    There's not much that'd be relevant to the doctor in here...
    You can see a picture on his desk, a half-opened drawer, and  the terminal.
    1. Picture
    2. Drawer
    3. Terminal
    what do you want to look at: """,1,3)

    if look_at == 1:
        print("You find a photo of the doctor's family, with a\u001b[32m brown\u001b[0m furred dog happily slobbering in front of them.")
        look_around()
    if look_at == 2:
        print("Looking in the drawer, you find a note the doctor wrote to his wife - while her name isn't in it, it mentions something about\u001b[32m Bailey\u001b[0m needing to be taken to the groomers.")
        look_around()
    elif look_at == 3:
        medical_bay_crack_the_password ("bailey")

def medical_bay_crack_the_password(password):
    print("")
    print_with_color("You have accessed the terminal. Please enter a password.",2)
    print("")
    global lives
    global medical_bay_key
    user_inputed_password = input("Please enter the password: ").lower().strip()
    if user_inputed_password == password:
        print("You have successfully hacked the terminal.")

        print("")
        print("A 3D printer on the doctor's desk whirrs into action, dispensing what you need - you've been given a door-override keycard.")
        print("")
        
        if debug == False:
            time.sleep(5)

        medical_bay_key = True
        Corridor()
    else:
        print_with_color("You have entered the wrong password. Please try again.",2)
        lives -= 1;
        if(lives == 0):
            game_over(False)
        else:
            print("")
            print(f"Lives Remaining: {lives}")
            print("")
            print("Sorry. Please Try Again! ")
            medical_bay_crack_the_password(password)
  
####################################### Eng Of Navigation Room ######################################










###################################### Start Of Flight Desk ######################################

def get_health_visual(health,player,extra):
     # Player health visual markers start #
    health_visual = ""
    if health == 100: 
        health_visual = f"\n\n                                        {player} Health: ██████████{extra}"
    
    elif health >= 90:
        health_visual = f"\n\n                                        {player} Health: █████████▬{extra}"
     
    elif health >= 80:
        health_visual = f"\n\n                                        {player} Health: ████████▬▬{extra}"

    elif health >= 70:
        health_visual = f"\n\n                                        {player} Health: ███████▬▬▬{extra}"
     
    elif health >= 60:
        health_visual = f"\n\n                                        {player} Health: ██████▬▬▬▬{extra}"

    elif health >= 50:
        health_visual = f"\n\n                                        {player} Health: █████▬▬▬▬▬{extra}"

    elif health >= 40:
        health_visual = f"\n\n                                        {player} Health: ████▬▬▬▬▬▬{extra}"

    elif health >= 30:
        health_visual = f"\n\n                                        {player} Health: ███▬▬▬▬▬▬▬{extra}"

    elif health >= 20:
        health_visual = f"\n\n                                        {player} Health: ██▬▬▬▬▬▬▬▬{extra}"
    
    elif health >= 10:
        health_visual = f"\n\n                                        {player} Health: █▬▬▬▬▬▬▬▬▬{extra}"

    elif health >= 1:
        health_visual = f"\n\n                                        {player} Health: ▬CRITICAL▬{extra}"

    elif health == 0:
        health_visual = f"\n\n                                        {player} Health: ▬Expired▬{extra}"
    return health_visual
    

def flight_deck_start():
    global debug
    if debug == False:
        time.sleep(2)

    print("""
         __.,,------.._
      ,'"   _      _   "`.
     /.__, ._  -=- _"`    Y
    (.____.-.`      ""`   j
     VvvvvvV`.Y,.    _.,-'       ,     ,     ,
        Y    ||,   '"\         ,/    ,/    ./
        |   ,'  ,     `-..,'_,'/___,'/   ,'/   ,
   ..  ,;,,',-'"\,'  ,  .     '     ' ""' '--,/    .. ..
 ,'. `.`---'     `, /  , Y -=-    ,'   ,   ,. .`-..||_|| ..
ff\\\\`. `._        /f ,'j j , ,' ,   , f ,  \=\ Y   || ||`||_..
l` \` `.`."`-..,-' j  /./ /, , / , / /l \   \=\l   || `' || ||...
 `  `   `-._ `-.,-/ ,' /`"/-/-/-/-"'''"`.`.  `'.\--`'--..`'_`' || ,
            "`-_,',  ,'  f    ,   /      `._    ``._     ,  `-.`'//         ,
          ,-"'' _.,-'    l_,-'_,,'          "`-._ . "`. /|     `.'\ ,       |
        ,',.,-'"          \=) ,`-.         ,    `-'._`.V |       \ // .. . /j
        |f\\\\               `._ )-."`.     /|         `.| |        `.`-||-\\\\/
        l` \`                 "`._   "`--' j          j' j          `-`---'
         `  `                     "`,-  ,'/       ,-'"  /
                                 ,'",__,-'       /,, ,-'
                                 Vvv'            VVv'
""")
    print("""\n\n\n
    
    You have entered the flight deck!\n
    
    The flight deck is pristine - the only part of the ship unaffected by whatever brutal collision impacted it. Even so, it seems oddly barren - devoid of human life and empty of all sound except the faint background trill of the all hands alarm. The shuttle is here - the last escape from the USS Ripley. It's a squat, ugly thing - an engine core shaped like the abdomen of some harmless insect. Even so, that ugly spaceship represents your hope of survival.

    It - whatever 'it' is - is between you and the shuttle. The thing that's been hunting you all this time. Following you from room to room. Watching and waiting.

    At first glance, it looks like a fighter jet's dream of a shark - sharp, silver, and lethally aerodynamic. Its' eyeless head turns towards you as you approach the shuttle, descending on digitigrade feet into a low crouch. The way its' head tilts at you doesn't remind you of any earthly animal. There is no scream or roar to herald its' approach - instead it stalks towards you with calm, emotionless grace.

    All you have left is your wits and what little you managed to find aboard the ship - survive!
    
    """)

    if debug == False:
        time.sleep(10)
    print("The main flight console is a shredded mess - it looks as if it was torn apart piece by piece until it was totally useless. Resetting it and saving the USS Ripley won't be possible - your only hope now is to escape in the shuttle. \n")
    if debug == False:
        time.sleep(10)
    print("In your dazed state, you look towards the left. You see the alien fronting you. You panic. \n\n")
    if debug == False:
        time.sleep(10)
    print("                    █▓▒▒░░░ The battle begins! ░░░▒▒▓█")
    if debug == False:
        time.sleep(10)

    alien_health_visual = ""
    alien_health = 100
    player_health_visual = ""
    player_health = lives*20
    if debug == False:
        time.sleep(2)
    turn = "player"

    #Weapons
    explosive_barrel = 3
    gun_shots = 2
    fire_alarm = 1

    #Alien weapons
    death_glare = 1


    ## Alien critical hit##
    alien_critical_hit = random.randint(0,10) #Works as a multiplier. 




    ## Rare chance for the alien to outright kill player. Scripted for it to happen twice.
    alien_death_glare = 0




    while alien_health > 0.0 and player_health > 0.0:
        ## This is effectively the dice roll.
        fight_call = random.randint(0,21)
        damage_output = random.randint(4,10)
        coin_flip = random.randint(1,2)


       
        player_health_visual = get_health_visual(player_health/2,"Player","");
        alien_health_visual = get_health_visual(alien_health, " Alien","\n\n");


        # Begin the game itself. PLAYERS TURN
    

        if turn == "player":
            ## FIGHT CALL: 0 ## Instadeath! Must run three times before it'll work. 
            if fight_call == 0:
                if gun_shots > 0:
                    print(f"{player_health_visual}{alien_health_visual} You find a gun and attempt to shoot the alien but it dodged the projectile, plasma fizzing through the air.")
                    gun_shots -= 1
                else: 
                    print(f"{player_health_visual}{alien_health_visual}You find a gun and shoot the alien square in the head, killing it outright - its' silvery skull tunnelled through from one side to the other by bright green plasma.")
                    alien_health == 0
        
        # Fight call 1 # Explosive barrels!!
            elif fight_call == 1:
                if explosive_barrel > 0:
                
                    print(f"{player_health_visual}{alien_health_visual}You notice there are some barrels! Do you use them to fight the alien?")
                    user_input = int_input ("""
                1: Use the explosive barrel
                2: Don't use the explosive barrel   
                """,1,2)
                    if user_input == 1:
                        print("You use the explosive barrel! The alien has taken damage, but you also have taken some splash damage.")
                        player_health -= damage_output * 2
                        alien_health -= damage_output * 3
                        explosive_barrel -= 1
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                    elif user_input == 2:
                        print("You have decided to avoid the explosive barrel. The slight delay allowed the alien to jab you.")
                        player_health -= damage_output / 2
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                    else:
                        print()
                else: 
                    print("You check for some barrels. You do not find any more. The alien hits as you as you do so.")
                    player_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

            # Fight call 2 # Sword attack
            elif fight_call == 2:
                
                print(f"{player_health_visual}{alien_health_visual}You notice that there is a sword on the flight deck. Why it's there, you don't know. It'll come in handy right now though, right?")
                user_input = int_input ("""
            1: Leave the sword
            2: Take the sword and stab the alien with it.   
            """,1,2)
                if user_input == 1:
                    print("You have left the sword and attack it with the knife instead. You do mininal damage.")
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("You quickly take the sword and stab the creature with it! You cause great damage!.")
                    alien_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                else:
                    print()

            # Fight call 3 through 5 # Simple knife attack. Most common
            elif fight_call in [3, 4, 5, 6]:
                
                print(f"{player_health_visual}{alien_health_visual}You have a knife in your posession and the alien is staring you down. Do you attempt to attack the alien?")
                user_input = int_input ("""
            1: Attack the alien
            2: Don't attack the alien
            """,1,2)
                if user_input == 1:
                    print("You attack the alien! You managed to deal a blow but it also caused you a minor bruise.")
                    alien_health -= damage_output
                    player_health -= damage_output / 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("By not fighting, you have allowed the alien to seriously maim you!")
                    player_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                else:
                    print()

        
            # Fight call 7 # Essentially a skip-a-turn round
        
            elif fight_call == 7:
                print(f"{player_health_visual}{alien_health_visual} You banged your head on something, but you're not sure what. The way the alien's head tilts at you seems almost mocking.\n\n")
                player_health -= damage_output / 2
                if debug == False:
                    time.sleep(2)
                turn = "alien"

            #Fight call 8 # Dangling wire (random for electric)
            elif fight_call == 8:
                
                print(f"{player_health_visual}{alien_health_visual}You see a dangling cluster of power wires above the alien. You might be able to do something with it!")
                user_input = int_input ("""
            1: Use the wire against the alien
            2: Ignore the wire and attack the alien with your knife   
            """,1,2)
                if user_input == 1:
                    if fight_call < 7:
                        print(f"You use the wire and it is electrified! You do substantial damage to the alien!")
                        alien_health -= damage_output * 3
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"

                    else: 
                        print(f"You use the wire to strangulate the alien. It's a little breathless!")
                        alien_health -= damage_output
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"

                elif user_input == 2:
                    print(f"{player_health_visual}{alien_health_visual}You use the wire and strangulate the alien! It's a little choked.")
                    alien_health -= damage_output 
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                else:
                    print()

            #Fight call 9 Poisoness goo
            elif fight_call == 9:
                
                print(f"{player_health_visual}{alien_health_visual}You see some silvery liquid metal on the floor. You're not sure what it is but you could try using it??")
                user_input = int_input ("""
            1: Use the liquid metal against the alien
            2: Leave the liquid metal and stab the alien
            """,1,2)
                if user_input == 1:
                    print("The liquid metal scalds your skin - inexplicably boiling hot. You feel very light-headed for a moment before you shake it off.")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("You attack the alien with your knife. You do some damage.")
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            #Fight call 10 Fire alarm
            elif fight_call == 10:
                
                print(f"{player_health_visual}{alien_health_visual}You notice the fire alarms. The liquid foam might do some damage to the alien! What do you do?")
                user_input = int_input ("""
            1: Pull the fire alarm
            2: Leave the fire alarm alone
            """,1,2)
                if user_input == 1:
                    if fire_alarm > 0:
                        print("You have pulled the fire alarm! The foam releases. In the confusion, you both slip. The alien takes moderate damage, you take a little.") 
                        player_health -= damage_output
                        alien_health -= damage_output * 2
                        fire_alarm -= 1
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"

                    else:
                        print("The fire alarm has already been pulled. In your confusion, the alien has thrown you to the other side of the room!")
                        player_health -= damage_output * 2
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"


                elif user_input == 2:
                    print("You leave the fire-alarm, but the momentary stop has allowed the alien to grab you.")
                    player_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                else:
                    print()

            #Fight call 11 Alien runs for the exit door
            elif fight_call == 11:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is trying to run into the corridor!")
                user_input = int_input ("""
            1: Attack it whilst it runs
            2: Let it go
            """,1,2)
                if user_input == 1:
                    print("You manage to scar the alien!.")
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("The alien heads for the door but is unable to pass through it. It must be locked. The aliens tail hits you as it panics!")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()


            #Fight call 12 Console panel
            elif fight_call == 12:
                
                print(f"{player_health_visual}{alien_health_visual} A console panel falls from the ceiling onto the aliens head dazing it for a moment. Do you strike it?")
                user_input = int_input ("""
            1: Strike the alien
            2: Leave it, it might still be dangerous, right? 
            """,1,2)
                if user_input == 1:
                    print("You strike the alien! It is now dazed.")
                    alien_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("Why did you leave it? The alien is dazed. As it recovers, it hits you with one of its arms that you didn't see!")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            #Fight call 13 Sharp object. If fight_call < 5, fail the collection of sword.
            elif fight_call == 13:
                
                print(f"{player_health_visual}{alien_health_visual} You find a sharp object underneath a bit of rubble. The pilots in this craft must've had a fascination for old blades.")
                user_input = int_input ("""
            1: You try for the blade and attack the alien
            2: Leave the blade and just use your knife instead 
            """,1,2)
                if user_input == 1:
                    if fight_call <= 5:
                        print("As you scrambled for the blade, the alien caught you and threw you against the ceiling twice! You take serious damage.")
                        player_health -= damage_output * 3
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                    else:
                        print("You successfully managed to retrieve the sword and do massive damage to the alien!")
                        alien_health -= damage_output *3
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"


                elif user_input == 2:
                    print("Your knife is getting blunt. You do not cause any damage to the alien")
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            # Fight call 14 | Weariness!
            elif fight_call == 14:
                
                print(f"{player_health_visual}{alien_health_visual} You're starting to feel tired and it's suddenly dark in the room.")
                user_input = int_input ("""
            1: Throw the knife at the alien and hope it penetrates.
            2: Withdraw to the back of the room.
            """,1,2)
                if user_input == 1:
                    print("The knife does some damage to the alien and confuses it for a moment whilst you take a breather. You manage to take the knife back.")
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("Whilst you withdraw, the alien manages to grab you and throw you around the room!")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            # Fight call 15 and 16 | Simple weariness!
            elif fight_call in [15, 16]:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is doing something weird with its mouth. You have no idea but you think you can cut it with your knife. Do you try?")
                user_input = int_input ("""
            1: Cut the mouth
            2: Just watch and see
            """,1,2)
                if user_input == 1:
                    print("The alien was building up liquid metal spit! By attacking the tongue you managed to stop it and cause some damage to its mouth! The alien screams in pain!")
                    alien_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("The alien was building up some liquid metal spit! By leaving it and watching, you now feel incredibly weak and the alien attacks you.")
                    player_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            # Fight call 17 | Alien's sharp tail
            elif fight_call == 17:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is turning around revealing its extremely sharp tail. You do not see any parts of the alien exposed to the weapons you have.")
                user_input = int_input ("""
            1: Back away from the alien.
            2: Attack the alien on the shell
            """,1,2)
                if user_input == 1:
                    print("The alien takes a swing at you with its tail and misses you. It cuts itself instead in the attack.")
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("You run right into the path of the alien's tail strike causing you a significant wound!")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()


            # Fight call 18 | Ship shakes leaving room in darkness. 
            elif fight_call == 18:
                
                print(f"{player_health_visual}{alien_health_visual} The ship shakes suddenly; you're both sent flying into opposite walls. How do you recover?")
                user_input = int_input ("""
            1: There's a medipack! 
            2: You attack the alien whilst it's down
            """,1,2)
                if user_input == 1:
                    print("You reach the medipack and have rejuventated some health!")
                    player_health += damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"
                elif user_input == 2:
                    print("You attack the alien, but in the confusion you're both slightly injured.")
                    player_health -= damage_output
                    alien_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()


            # Fight call 19 | Ship shakes leaving room in darkness. 
            elif fight_call == 19:
                
                print(f"{player_health_visual}{alien_health_visual} The engines on the ship cut out momentarily and all the lights go out leaving you in compplete darkness You can't see the alien because your eyes have yet to adjust.")
                user_input = int_input ("""
            1: Blindly throw the knife and hope it hits. 
            2: Cower in the corner and wait for the lights to come back on.
            """,1,2)
                if user_input == 1:
                    if coin_flip == 1:
                        print("You throw the knife but it just lands on the floor. The alien hits you in the darkness just before the lights come back on.")
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                    else:
                        print("You hear a sharp hiss in the darkness! You must have hit the alien!")
                        alien_health -= damage_output * 2
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                elif user_input == 2:
                    print("The alien has much better night time vision that you have now just learned. You have been seriously hit!")
                    player_health -= damage_output * 3 
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            # Fight call 20 | Medipack possibility.  
            elif fight_call == 20:
                
                print(f"{player_health_visual}{alien_health_visual} You have noticed an unused medipack!")
                user_input = int_input ("""
            1: Rush for  the medipack to regain some health
            2: Leave the medipack and prod the alien
            """,1,2)
                if user_input == 1:
                    if fight_call < 7:
                        print("In your rush to get the medipack, the alien has caught you and thrown you around.")
                        player_health -= damage_output * 2
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                    else:
                        print("You successfully managed to retrieve the medipack. There is not much in it frustratingly!")
                        player_health += damage_output / 2
                        if debug == False:
                            time.sleep(2)
                        turn = "alien"
                elif user_input == 2:
                    print("You attempt to hit the alien with the knife, but you do mininal damage.")
                    alien_health -= damage_output 
                    if debug == False:
                        time.sleep(2)
                    turn = "alien"

                else:
                    print()

            # Fight call 21 | Missed opportunity.  
            elif fight_call == 21:
                print("\n\nIn your dazed state, you missed your opportunity to attack the alien!\n\n")
                if debug == False:
                    time.sleep(2)
                turn = "alien"

            # Undefined fight calls
            else:
                print(f"{fight_call} Undefined fight_call. Switching to alien turn.")
                if debug == False:
                    time.sleep(2)
                turn = "alien"



        # ALIENS TURN
        elif turn == "alien":
        
            # Fight call 0. 
            if fight_call == 0:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is beginning to 'stare' at you very oddly, its' eyeless head eerily fixated on you. You wait for a moment and then realise it's doing a death-glare!")
                if debug == False:
                    time.sleep(12)
                if death_glare > 0:
                    print("\n\nThe alien missed you! You survive to continue the battle.\n\n")
                    if debug == False:
                        time.sleep(2)
                    turn = "player"
                    death_glare -= 1


                else:
                    print("\n\nThrough its' flat metal skull, a red glow pierces through you, a madness overtaking you. Your heart beats very slow and you fall to the floor.\n\n")
                    player_health -= damage_output * 5
                    death_glare = random.randint(0,2)
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

        
            # Fight call 1.
            elif fight_call == 1:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is 'looking' at you strangely. What do you do?\n")
                user_input = int_input ("""
            1: Attack the alien with a knife
            2: Wait to see what it does
            """,1,2)
                if user_input == 1:
                    if fight_call < 15:
                        print("Your attack against the alien fails. It injures you seriously instead!")
                        player_health -= damage_output * 3
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    else:
                        print("You succesfully hit the alien, causing minor damage!")
                        alien_health -= damage_output
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                elif user_input == 2:
                    print("The alien waits too. What is going on here?")
                    alien_health -= damage_output 
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    print() 



            # Fight call 2
            elif fight_call == 2:
                
                print(f"{player_health_visual}{alien_health_visual} You could swear the alien is enjoying your agony!")
                user_input = int_input ("""
            1: Search for a medipack
            2: Attempt to attack the alien
            """,1,2)
                if user_input == 1:
                    if coin_flip == 1:
                        print("You were not able to find a medipack and the alien attacked as you looked!")
                        player_health -= damage_output 
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    else:
                        print("You found a medipack! Your health has been rejuvenated!")
                        player_health += damage_output * 2
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                elif user_input == 2:
                    print("The alien dodges with preternatural grace.")
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    print()             

            # Fight call 3
            elif fight_call == 3:
                
                if alien_health < 30:
                    print("The alien shoots liquid metal from its mouth! You are unable to dodge as there's so much of it!")
                    player_health -= damage_output * 2
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    print("\nThe alien seems to be waiting. What's it doing?\n")
                    if debug == False:
                        time.sleep(2)
                    turn = "player"


            # Fight call 4
            elif fight_call == 4:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is making a run for the airvents!")
                user_input = int_input ("""
            1: Throw a knife at it!
            2: Let it go. What's it gonna do? 
            """,1,2)
                if user_input == 1:
                    if coin_flip == 1:
                        print("The knife hits the alien! You stop it in its tracks!")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"

                    else:
                        print("The knife misses the alien but you hear it come out the other vent and able to safely dodge it.")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                elif user_input == 2:
                    print("The alien enters the airvents and sneaks out behind you! You are shook at the speed!")
                    player_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    print()    


            # Fight call 5
            elif fight_call == 5:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is getting into position to attack you with its tail.")
                user_input = int_input ("""
            1: Attack the alien with your knife
            2: Move out of its way
            """,1,2)
                if user_input == 1:
                    print("You charged right into the sharp limbs of the alien! You've caused serious damage to yourself.")
                    player_health -= damage_output * 3
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                elif user_input == 2:
                    print("You managed to stay safely away from the alien!")
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    print()  


            # Fight call 6
            elif fight_call == 6:
                
                if alien_health < 30:
                    print(f"{player_health_visual}{alien_health_visual}The alien is seriously injured. It is attempting to heal itself.")
                    if coin_flip == 1:               
                        alien_health += damage_output * 2
                        print("The alien manages to heal itself.")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"

                    elif coin_flip == 2:
                        player_health += damage_output
                        print(f"{player_health_visual}{alien_health_visual}The alien was not able to concentrate! It has somehow healed you instead!")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    else:
                        if debug == False:
                            time.sleep(2)
                        turn = "player" 


            # Fight call 7
            elif fight_call == 7:
                
                if player_health < 30:
                    print(f"{player_health_visual}{alien_health_visual} You are trying to find a medipack.\n")
                    if coin_flip == 1:
                        print("You have found a medipack!")
                        player_health += damage_output * 2
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    elif coin_flip == 2:
                        print(f"{player_health_visual}{alien_health_visual} Unfortunately, you weren't able to find a medipack.\n")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
               
                else:
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

            # Fight call 8
            elif fight_call == 8:
                
                print(f"{player_health_visual}{alien_health_visual} The alien is attempting to spit liquid metal at you! ")
                user_input = int_input ("""
            1: Move to the side of the wall!
            2: Move underneath the alien!
            """,1,2)
                if user_input == 1:
                    if coin_flip == 1:
                        print("You managed to safely evade the liquid metal!")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    elif coin_flip == 2:
                        print("You got hit with the liquid metal unforunately.")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                        player_health -= damage_output

                elif user_input == 2:
                    if coin_flip == 1:
                        print("You managed to safely evade the liquid metal!")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                    elif coin_flip == 2:
                        print("You got hit with the liquid metal unforunately.")
                        if debug == False:
                            time.sleep(2)
                        turn = "player"
                        player_health -= damage_output

                else:
                    print()


            # Fight call 9, 10, 11, 12, 13, 14
            elif fight_call in [9,10,11,12,13,14]:
                if alien_health < 40:
                    print(f"{player_health_visual}{alien_health_visual} The alien is injured. It is desperately clawing at you!")
                    player_health -= damage_output    
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

                else:
                    turn = "player"

            # Fight call 15, 16, 17
            elif fight_call in [15, 16, 17]:
                if alien_health < 50:
                    print(f"{player_health_visual}{alien_health_visual} The alien is attempting to hit you with its tail twice! It's getting very desperate! ")
                    user_input = int_input ("""
                1: Run at it with your knife! It's nearly dead!
                2: Stay back!
                """,1,2)
                    if user_input == 1:
                        if coin_flip == 1:
                            print("You have charged straight into its tail! You got hit twice!")
                            player_health -= damage_output * 3
                            if debug == False:
                                time.sleep(2)
                            turn = "player"
                        elif coin_flip == 2:
                            print("You managed to avoid the alien causing you any damage.")
                            if debug == False:
                                time.sleep(2)
                            turn = "player"

                        else:
                            print("You managed to avoid the alien causing you any damage.")
                            if debug == False:
                                time.sleep(2)
                            turn = "player"

                else: 
                    turn = "player"


            # Fight call 18, 19, 20
            elif fight_call in [18, 19, 20]:
                print(f"{player_health_visual}{alien_health_visual} The alien has slipped on debris on the floor. It curls up.")
                user_input = int_input ("""
            1: Attack it!
            2: Stay back!
            """,1,2)
                if user_input == 1:
                    print("You just attacked the shell of the alien! You were not able to penetrate its defenses but it caught you with one of its claws!")
                    player_health -= damage_output
                    if debug == False:
                        time.sleep(2)
                    turn = "player"
            
                elif user_input == 2:
                    print("You were able to safely prevent the alien from attacking you.")
                    if debug == False:
                        time.sleep(2)
                    turn = "player"

            ## Fight call 21
            elif fight_call == 21:
                print("\n\nThe alien missed its opportunity to attack you! It must be feeling dazed.\n\n")
                if debug == False:
                    time.sleep(2)
                turn = "player"

            ## Undefined fight calls
            else:
                print(f"{fight_call}Undefined alien fightcall.\n")

        else:
            print()







    if player_health <= 0:
        player_health = 0
    if alien_health <= 0:
        alien_health = 0
        



    # Attempt to force the EXPIRED health when dead. Not working as yet!
        
    if player_health == 0:
        player_health_visual = get_health_visual(player_health/2,"Player","");
        alien_health_visual = get_health_visual(alien_health/2, " Alien","\n\n");
        print(f"\n{player_health_visual}{alien_health_visual}\nYou died. The alien killed you.\n\n")
        if debug == False:   
            time.sleep(5)
        game_over(True)
        exit()
    elif alien_health == 0:
        player_health_visual = get_health_visual(player_health/2,"Player","");
        alien_health_visual = get_health_visual(alien_health/2, " Alien","\n\n");
        print(f"""\n\n{player_health_visual}{alien_health_visual}
               
        It's dead. A metal corpse lies inanimate, a vile parody of the warmth of life. If you hadn't just fought it with every ounce of your effort, you could have easily assumed it was some strange space debris, strewn haphazardly across the floor.

        Unreal liquid-mercury blood oozes out onto the deck, almost indistinguishable from the plasteel surface. You tread carefully around the corpse - no point abandoning caution now. It's only a few steps to the shuttle, but each one is exhausting to the point of agony. Only your determination keeps you going, to open the entry hatch, to slide yourself into the pilots' chair.

        Under your hands, the controls of the shuttle feel warm and inviting - a haptic rumble notifying you of active systems. Green strings flash by on an embedded console - this time, everything's in working order. Some other poor bastard managed to power and fuel the thing before he was vivisected and deposited somewhere else. The hatch shuts at the flick of a switch, smoothing back into place with a soft hiss.

        Takeoff forces you back into the seat with a jolt, and the ugly little shuttle blasts past the flight deck forcefield, emerging out into the black. Outside of the ship, the sensory overload dims - without the sound of exploding hardware, rending steel, and the alarm's insistent blare, it seems almost quiet. Even reassuring.

        You look back through the rear viewscreen, seeing the USS Ripley in its' final moments - as the engine room finally detonates and superheated fuel blasts through the ship's bulkheads in a flowering explosion. Despite it being your home and livelihood, the sight of that fireball consuming whatever monstrosity killed your comrades fills you with relief.

        You're safe.

        For now.

        \u001b[32;1m
         ______   __  __     ______        ______     __   __     _____    
        /\__  _\ /\ \_\ \   /\  ___\      /\  ___\   /\ "-.\ \   /\  __-.  
        \/_/\ \/ \ \  __ \  \ \  __\      \ \  __\   \ \ \-.  \  \ \ \/\ \ 
           \ \_\  \ \_\ \_\  \ \_____\     \ \_____\  \ \_\\"\_\  \ \____- 
            \/_/   \/_/\/_/   \/_____/      \/_____/   \/_/ \/_/   \/____/ 
        \u001b[0m

        Thank you for playing 'USS Ripley' by the Ripley's Roughnecks team!
        We are:
        Pip Allen
        Christopher Boardman
        John Bress
        Kurtis Chamberlain
        Alexander R. Wayland
        Dyllan Whitney

        """)
        exit()




###################################### End Of Flight Deck ######################################





















###################################### Start Of Corridor ######################################


def Corridor_flight_deck_status():
    global navigation_key
    global medical_bay_key
    global engine_room_key
    global holodeck_key
    if navigation_key and medical_bay_key and engine_room_key and holodeck_key:
        return "(Unlocked)"
    else:
        return "(Locked)"

def Corridor_flight_deck_blocker():
    global navigation_key
    global medical_bay_key
    global engine_room_key
    global holodeck_key
    if navigation_key and medical_bay_key and engine_room_key and holodeck_key:
        return " "
    else:
        return "▬"
    

def Corridor():
    global navigation_key
    global medical_bay_key
    global engine_room_key
    global holodeck_key
    global Storage_key
    global debug
    global lives  
    clear_screen() 
    print("""
    Health: {7}%

             Ship Map
             ┌───────┐
            ┌┘◘◘◘◘◘◘◘└┐
        ┌───┘◘       ◘└───┐
        │     Room 6      │  
        │                 │    Navigation = 1 {0}
        ├──────┐   ┌──────┤   Engine room = 2 {1}
        │ Room │▬{6}▬│ Room │      Holodeck = 3 {2}
        │   4  │   │  5   │   Medical bay = 4 {3}
        │      │   │      │  Storage room = 5 {4}
        │      │   │      │   Flight deck = 6 {5}
        │      │   │      │
        │      ░   ░      │
        ├──────┤   ├──────┤
        │ Room │   │ Room │
        │  2   ░   ░  3   │
        │      │   │      │
        │      │   │      │
        │      │   │      │
        │   ┌──┘░░░└──┐   │
        └───┤ Room 1  ├───┘
            └─────────┘

        """.format(
            true_false_converter(navigation_key),  # 0
            true_false_converter(engine_room_key), # 1
            true_false_converter(holodeck_key),    # 2
            true_false_converter(medical_bay_key), # 3
            true_false_converter(Storage_key),     # 4
            Corridor_flight_deck_status(),         # 5
            Corridor_flight_deck_blocker(),        # 6
            lives*10 ) )                              # 7

    if debug == False:
        time.sleep(5)

    room_number = int_input("Please choose a room number from the list above (1, 2, 3, 4, 5, 6): ",1,6)

    clear_screen()

    if room_number == 1:
        if navigation_key:
            print("You have already completed this room")
            if debug == False:
                time.sleep(5)
            Corridor()
        else:
            navigation_start()
    elif room_number == 2:
        if engine_room_key:
            print("You have already completed this room")
            if debug == False:
                time.sleep(5)
            Corridor()
        else:
            engine_room_start()
    elif room_number == 3:
        if holodeck_key:
            print("You have already completed this room")
            if debug == False:
                time.sleep(5)
            Corridor()
        else:
            holodeck_start()
    elif room_number == 4:
        if medical_bay_key:
            print("You have already completed this room")
            if debug == False:
                time.sleep(5)
            Corridor()
        else:
            medical_bay_start()
    elif room_number == 5:
        if Storage_key:
            print("You have already completed this room")
            if debug == False:
                time.sleep(5)
            Corridor()
        else:
            storage_room_start()
    elif room_number == 6:
        if navigation_key and medical_bay_key and engine_room_key and holodeck_key:
            flight_deck_start()
        else:
            print("Sorry. Room locked. there are 4 keycard required to unlock this door")
            if debug == False:
                time.sleep(5)

            Corridor()
start_game()
