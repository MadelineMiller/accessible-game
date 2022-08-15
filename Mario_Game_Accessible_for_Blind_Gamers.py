# collaborated on this project with Jonah Fernandez, Uni Huang, & Nhan Nguyen
# during the course titled CMPM 80A - Accessible Games at UC Santa Cruz
# the course was taught by Instructor Sri Kurniawan

import pyttsx3
import random

# https://medium.com/analytics-vidhya/speech-synthesizer-using-python-b3f1c83a1fc8
# https://pynative.com/python-random-choice/
# https://www.w3schools.com/python/ref_random_shuffle.asp

# attempt to make Mario Party Superstars - Bowser's Big Blast be audio only
# https://www.youtube.com/watch?v=SJK9Ka9hrQA&t=4s

synthesizer = pyttsx3.init()
voices = synthesizer.getProperty('voices')
synthesizer.setProperty('voice', voices[0].id)
rate = synthesizer.getProperty('rate')
synthesizer.setProperty('rate', 150)
volume = synthesizer.getProperty('volume')
synthesizer.setProperty('volume', 1.3)    # was at 0.7, changed the volume to 1.3 based on Playtest Feedback
lever_choices = ["1", "2", "3", "4", "5"]


def speech(text):
    """Function takes text and says the text
    """
    print(text)
    synthesizer.say(text)
    synthesizer.runAndWait()
    synthesizer.stop()


def wrong_lever(numlevers):
    """Function randomly chooses the lose lever and returns it
    """
    lose_levers = []
    while len(lose_levers) < numlevers:    # generate until the number of lose levers are generated as specified
        gen = random.choice(lever_choices)
        if gen not in lose_levers:
            lose_levers.append(gen)
    return lose_levers


def a_round(levers_choices, round, curstar):
    """Function takes the list with the available levers to choose from.
    And runs through a full round of the game
    """
    print("levers:", lever_choices)
    numlevers = random.randint(1, len(lever_choices) - 1)
    the_wrong_levers = wrong_lever(numlevers)
    #print("wrong:",the_wrong_levers)
    space_bar = 0
    if numlevers > 1:
        speech("\nFor round " + str(round) + ", you will have " + str(numlevers) + " levers that, if pressed, will make you lose the game.")
    else:
        speech("\nFor round " + str(round) + ", you will have " + str(numlevers) + " lever that, if pressed, will make you lose the game.")
    if curstar >= 3:
        speech("\nYou currently have this many stars: " + str(curstar) + ". Would you like to spend 3 stars to skip the level?")
        speech("\nPress the space bar and then enter to skip this round or just press Enter to not skip this round.")
        user_input = input("")
        if user_input == " ":
            speech("\nSkipping Round: " + str(round))
            return "skip"
    else:
        if curstar != 1: 
            speech("\nYou now have "+str(curstar) + " stars.")
        else:
            speech("\nYou now have "+str(curstar) + " star.")
    while True:
        speech("\nCurrently, you are hovering over the lever that is number: " + lever_choices[space_bar] + ".")
        speech("\nHit the space bar and then enter to move to the next lever or just hit enter to push down this lever.")
        user_input = input("")
        if user_input == " ":  # inputted a space
            space_bar = (space_bar + 1) % len(lever_choices) #Save an if statement
        elif user_input == "":  # push down the lever
            if lever_choices[space_bar] in the_wrong_levers:
                speech("Tick...")
                speech("Tick...")
                speech("Boom...")
                speech("Bowser's head blew up.")
                speech("You lost, because you chose the wrong lever, which was: " + str(lever_choices[space_bar]))
                return "lose"
            else:
                speech("Tick...")
                speech("Tick...")
                if len(the_wrong_levers) > 1:
                    speech("Just kidding, you win!!!! The wrong levers were: " + str(the_wrong_levers))
                else:
                    speech("Just kidding, you win!!!! The wrong lever was: " + str(the_wrong_levers))
                speech("Onwards!")
                return "win"


def intro():
    speech("\nHello and welcome to the Mario Party Superstars Minigame called Bowser's Big Blast.")
    speech(
        "\nWould you like to skip the directions? Hit any key and then hit enter to skip, just hit enter to hear the directions.")
    user_input = input("")
    if user_input != "":  # skip directions
        speech("Skipping directions.")
    else:
        speech("In this game, you will be choosing one out of the five levers available to push down.")
        speech("\nThe goal of the game is to choose the lever that will not result in Bowser blowing up.")
        speech("\nThere will be a specific amount of levers per round that will result in Bowser blowing up.")
        speech("\nThe specific amount of wrong levers will be specified at the beginning of each round.")
        speech("\nThe game will continue until you push down a lever that causes Bowser to blow up.")
        speech("\nEvery round that you win, you will get 1 star. You spend 3 stars to skip a round.")
        speech("\nYou can spend 1 star to revive after blowing up Bowser's head. Good luck!")


# playing the game:
intro()
round = 0
starcnt = 0
while True:
    round += 1
    print("\n----------------------------------------------------------------------------------------------------------------------------------")
    speech("\nRound: " + str(round))
    verdict = a_round(lever_choices, round, starcnt) # The result of that game round
    if verdict == "win":
        starcnt += 1
    if verdict == "skip":
        starcnt -= 3
    elif verdict == "lose":
        speech("Unfortunately, you lost the game.")
        if starcnt > 0:
            speech("But you can use a star to continue playing.")
            speech("Would you like to use a star? Hit enter for yes. Hit any key and then enter for no to stop playing the game.")
            your_input = input("")
            if your_input == "": # == yes
                speech("Alright, let us continue playing. Now, onto the next round!")
                starcnt -= 1
                continue
        speech("Thank you for playing Bowser's Big Blast.")
        speech("Goodbye.")
        break # you lose the game
    
