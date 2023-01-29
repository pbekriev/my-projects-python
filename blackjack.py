import random
from colorama import Fore, Back, Style
import os
from time import sleep


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_deck():  # Create a DECK
    suits = ['\u2660', '\u2665', '\u2666', '\u2663']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(f"{rank}{suit}")

    return deck


def deal_cards(deck, players_hand, dealer_hand, number_of_players):
    for _ in range(2):
        for player in range(1, number_of_players + 1):
            if player not in players_hand:
                players_hand[player] = [deck.pop()]
            else:
                players_hand[player].append(deck.pop())
        dealer_hand.append(deck.pop())

    return deck, players_hand, dealer_hand


def calculate_hand(hand):
    value = 0
    ace_count = 0
    for card in hand:
        rank = card[0]
        if rank == 'A':
            ace_count += 1
        elif rank in ['J', 'Q', 'K']:
            value += 10
        else:
            value += int(rank)

    # Check for aces and adjust the value if necessary
    for i in range(ace_count):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value


def place_bet(players_cash, players_bet):
    for player in players_cash:
        while True:
            players_bet[player] = input(f"Player {player} place you BET:")
            if players_cash[player] >= int(players_bet[player]) > 0:
                players_bet[player] = int(players_bet[player])
                break
            elif players_bet[player].isdigit() and players_bet[player] != "0":
                print(Fore.RED + f"Not enough funds! You have: {players_cash[player]}BGN" + Fore.RESET)
            else:
                print(Fore.RED + "Invalid input. Try again..." + Fore.RESET)

        players_cash[player] -= players_bet[player]

    return players_cash, players_bet


def print_hands(players_hand, dealer_hand, hidden_dealer_card):
    cls()
    for_print = "DEALER CARDS:"
    if hidden_dealer_card:
        for_print += f"[{dealer_hand[0]}] [**]"
    else:
        for card in dealer_hand:
            for_print += f"[{card}] "
    for_print += "\n"
    for player in players_hand:
        for_print += f"Player {player} cards:"
        for card in players_hand[player]:
            for_print += f"[{card}] "
        for_print += f"BET:{players_bet[player]}BGN CASH:{players_cash[player]}BGN"
        for_print += "\n"
    return print(for_print)


def check_player_funds(players_cash):
    for player in players_cash.copy():
        if players_cash[player] == 0:
            print(Fore.RED + f"Player {player} don't have funds!\n"
                             f"Do you want to enter funds? y/n: " + Fore.RESET)
            while True:
                answer = input()
                if answer in ["y", "n"]:
                    break
                print(Fore.RED + "Invalid input. Enter 'y' or 'n': " + Fore.RESET)
            if answer == "y":
                players_cash[player] = int(input())
            else:
                del players_cash[player]
                del players_hand[player]


def hit_or_stand(deck, players_hand, hidden_dealer_card):
    for player in players_hand:
        while True:
            print_hand = ""
            for card in players_hand[player]:
                print_hand += f"[{card}] "
            while True:
                hit_stand = input(f"Player {player} CARDS: {print_hand} [h]it or [s]tand: ")
                if hit_stand in ["h", "s"]:
                    break
                print(Fore.RED + "Invalid input. Enter 'h' or 's': " + Fore.RESET)
            if hit_stand == "h":
                players_hand[player].append(deck.pop())
            else:
                break
    hidden_dealer_card = False
    return deck, players_hand, hidden_dealer_card


# Main Program
deck = create_deck()

while True:
    players_cash = {}
    players_hand = {}
    dealer_hand = []

    # Shuffle the deck
    random.shuffle(deck)

    # Welcome print
    welcome = "Welcome to BLACKJACK GAME"
    i = 0
    while i < len(welcome):  # Print character by character
        sleep(0.2)
        print(Fore.BLUE + welcome[i] + Fore.RESET, end='')
        i += 1
    print()

    # Enter number of Players
    while True:
        number_of_players = input("Enter number of players:")
        if number_of_players.isdigit() and number_of_players != "0":
            number_of_players = int(number_of_players)
            break
        print(Fore.RED + "Invalid input. Try again..." + Fore.RESET)

    # Enter amount of BGN for each player
    for player in range(1, number_of_players + 1):
        while True:
            amount = input(f"Player {player} enter amount BGN:")
            if amount.isdigit() and amount != "0":
                players_cash[player] = int(amount)
                break
            print(Fore.RED + "Invalid input. Try again..." + Fore.RESET)

    # The GAME
    deal_cards(deck, players_hand, dealer_hand, number_of_players)

    while players_hand:
        hidden_dealer_card = True
        players_bet = {}

        check_player_funds(players_cash)

        place_bet(players_cash, players_bet)

        print_hands(players_hand, dealer_hand, hidden_dealer_card)

        hit_or_stand(deck, players_hand, hidden_dealer_card)

        print_hands(players_hand, dealer_hand, hidden_dealer_card)

        # print(players_hand)
        # print(dealer_hand)
        # print(players_cash)
        # print(players_bet)
