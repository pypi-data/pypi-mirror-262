"""
This file contains code for the game "Gemini Sample Game".
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries


import sys
import uuid
import copy
import google.generativeai as gemini
import os
from dotenv import load_dotenv
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary class.


class GameCharacter:
    """
    This class contains attributes of a game character.
    """

    def __init__(self, name, max_hp, attack_power, defense):
        # type: (str, mpf, mpf, mpf) -> None
        self.id: str = str(uuid.uuid1())
        self.name: str = name
        self.max_hp: mpf = max_hp
        self.curr_hp: mpf = max_hp
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "ID: " + str(self.id) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack Power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        return res

    def restore(self):
        # type: () -> None
        self.curr_hp = self.max_hp

    def get_is_alive(self):
        # type: () -> bool
        return self.curr_hp > 0

    def attack(self, other, is_crit, crit_damage):
        # type: (GameCharacter, bool, mpf) -> None
        raw_damage: mpf = self.attack_power * crit_damage - other.defense if is_crit else self.attack_power - other.defense
        damage: mpf = raw_damage if raw_damage > 0 else mpf("0")
        other.curr_hp -= damage
        print(str(self.name) + " dealt " + str(damage) + " damage on " + str(other.name) + "!")

    def clone(self):
        # type: () -> GameCharacter
        return copy.deepcopy(self)


# Creating main function used to run the game.


def main() -> int:
    """
    This main function is used to run the game.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Asking user input values for generation config
    temperature: str = input("Please enter temperature (0 - 1): ")
    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

    float_temperature: float = float(temperature)

    top_p: str = input("Please enter Top P (0 - 1): ")
    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

    float_top_p: float = float(top_p)

    top_k: str = input("Please enter Top K (at least 1): ")
    while not is_number(top_k) or int(top_k) < 1:
        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

    float_top_k: int = int(top_k)

    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

    int_max_output_tokens: int = int(max_output_tokens)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    # Gemini safety settings
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-1.0-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    name: str = input("Please enter your name: ")

    while True:
        clear()
        convo.send_message("Please enter any float between 100 and 150 inclusive!")
        player_max_hp: mpf = mpf(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 20 and 50 inclusive!")
        player_attack_power: mpf = mpf(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 10 and 20 inclusive!")
        player_defense: mpf = mpf(convo.last.text.split("\n")[0])
        player: GameCharacter = GameCharacter(name, player_max_hp, player_attack_power, player_defense)
        convo.send_message("Please enter any float between 100 and 150 inclusive!")
        enemy_max_hp: mpf = mpf(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 20 and 50 inclusive!")
        enemy_attack_power: mpf = mpf(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 10 and 20 inclusive!")
        enemy_defense: mpf = mpf(convo.last.text.split("\n")[0])
        enemy: GameCharacter = GameCharacter("CPU", enemy_max_hp, enemy_attack_power, enemy_defense)

        turn: int = 0
        while player.get_is_alive() and enemy.get_is_alive():
            clear()
            print(str(player.name) + "'s stats:\n\n" + str(player))
            print(str(enemy.name) + "'s stats:\n\n" + str(enemy))

            turn += 1
            if turn % 2 == 1:
                print("It is " + str(player.name) + "'s turn to move!")
                input("Enter anything to attack the enemy: ")
                convo.send_message("Enter \"CRITICAL\" or \"NORMAL\"!")
                is_crit: bool = str(convo.last.text) == "CRITICAL"
                convo.send_message("Please enter any float between 1.5 and 5 inclusive!")
                crit_damage: mpf = mpf(convo.last.text.split("\n")[0])
                player.attack(enemy, is_crit, crit_damage)
            else:
                print("It is " + str(enemy.name) + "'s turn to move!")
                convo.send_message("Enter \"CRITICAL\" or \"NORMAL\"!")
                is_crit: bool = str(convo.last.text) == "CRITICAL"
                convo.send_message("Please enter any float between 1.5 and 5 inclusive!")
                crit_damage: mpf = mpf(convo.last.text.split("\n")[0])
                enemy.attack(player, is_crit, crit_damage)

        if not player.get_is_alive():
            print(str(player.name) + " was defeated!")
        elif not enemy.get_is_alive():
            print(str(player.name) + " won!")

        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing: str = input("Do you want to continue playing \"Gemini Sample Game\"? ")
        if continue_playing != "Y":
            return 0


if __name__ == '__main__':
    main()
