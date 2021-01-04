"""
File:    pyopoly.py
Author:  Amarjot Gill
Date:    10/18/2020
Section: 44
E-mail:  agill3@umbc.edu
Description:
  This program will use a given board, load it, and then use it to
  play a 2 player monopoly game, using many functions players,
  can buy properties, look at player and properties info, and
  create buildings at already owned locations. Players will
  also move around the board with randomized dice rolls
  and will be charged rent if they land on a property
  owned by the opposing player. This program will work
  with any board loaded into the 3 parameter of the play_game function

"""

from sys import argv
from random import randint, seed
from board_methods import load_map, display_board

if len(argv) >= 2:
    seed(argv[1])
# starting amount and money earned from passing go
PASS_GO_AMOUNT = 200
STARTING_AMOUNT = 1500
# magical values used in the program
UPPER_A_VALUE = 65
UPPER_Z_VALUE = 90
CANNOT_BUY = -1
NOT_OWNED = "no"
YES_OWNED = "yes"
RENT = "Rent"
PLACE = "Place"
OWNED = "Owned"
ABBREV = "Abbrev"
PRICE = "Price"
BUILDING_OWNED = "Building_Owned"
BUILDING_COST = "BuildingCost"
BUILDING_RENT = "BuildingRent"

# list with option user can select
option_list = ["buy property", "get property info", "get player info",
               "build a building", "end turn"]

# user can choose to type the command or use this list and enter a number
option_numbered_list = ["1", "2", "3", "4", "5"]
# magic values for there list index in option list
BUY_PROPERTY_POSITION = 0
PROPERTY_INFO_POSITION = 1
PLAYER_INFO_POSITION = 2
BUILDING_POSITION = 3
END_TURN_POSITION = 4

# will keep track of properties purchased and buildings built for each player
player1_properties = []
player1_buildings = []

player2_properties = []
player2_buildings = []


# will format and create the board
def format_display(board):
    game_board = load_map(board)
    board1 = []
    for i in range(len(game_board)):
        board1.append(game_board[i][ABBREV].ljust(5) + "\n     ")
    return board1


# this function will add the Owned and Building_Owned key to the dictionary of the map loaded
def owned_loop(board):
    the_list = load_map(board)
    for i in range(len(the_list)):
        the_list[i][OWNED] = NOT_OWNED
        the_list[i][BUILDING_OWNED] = NOT_OWNED
    return the_list


# prints out the list in this program with a nice format
def print_list(list_given):
    for list1 in range(len(list_given)):
        print("{}:".format(list1 + 1), list_given[list1])


# will be used to take turns between the players
def take_turn(player):
    player += 1
    return player


# function used for buying properties
def buy_property_function(player_location, board, balance, player, other_player, properties):
    # will check if conditions are met to purchase and will if they do
    if board[player_location][OWNED] == YES_OWNED + player \
            or board[player_location][OWNED] == YES_OWNED + other_player:
        print("The property is already owned")
        return balance
    elif int(board[player_location][PRICE]) == CANNOT_BUY:
        print("Property is not purchasable")
        return balance
    elif int(board[player_location][PRICE]) > balance:
        print("You do not have enough money to purchase")
        return balance

    else:
        board[player_location][OWNED] = YES_OWNED + player
        print("You have purchased", board[player_location][PLACE] + "!")
        balance -= int(board[player_location][PRICE])
        properties.append(board[player_location][PLACE])
        return int(balance)


# function used to display a property's info
def property_info(board, player1, player2):
    property_to_view = input("Which Property do you want to view?")
    property_exist = False
    # to make sure the property exist
    while property_exist == False:
        for i in range(len(board)):
            if property_to_view == board[i][PLACE] or property_to_view == board[i][ABBREV]:
                print("Place:", board[i][PLACE])
                print("Price:", board[i][PRICE])
                if board[i][OWNED] == YES_OWNED + player1:
                    print("Owner:", player1)
                elif board[i][OWNED] == YES_OWNED + player2:
                    print("Owner:", player2)
                else:
                    print("Owner: None")
                if board[i][BUILDING_OWNED] == NOT_OWNED:
                    print("Building: None")
                elif board[i][BUILDING_OWNED] == YES_OWNED + player1:
                    print("Building built by", player1)
                elif board[i][BUILDING_OWNED] == YES_OWNED + player2:
                    print("Building built by", player2)

                print("Rent:", board[i][RENT])
                print("Building Rent:", board[i]["BuildingRent"])
                property_exist = True

        if property_exist == False:
            print("That property does not exist")
            property_to_view = input("Which Property do you want to view?")


# function used to display the player selected info
def player_info(player1, symbol1, balance1, player2, symbol2, balance2,):
    which_player = input("Which player info do you want to view?")
    # will go until the correct name is entered
    while which_player != player1 and which_player != player2:
        print("That player does not exist please reenter")
        which_player = input("Which player info do you want to view?")

    if which_player == player1:
        print("Name:", player1)
        print("Symbol:", symbol1)
        print("Balance:", balance1)
        print("Properties owned are")
        print_list(player1_properties)
        print("Buildings built are")
        print_list(player1_buildings)

    if which_player == player2:
        print("Name:", player2)
        print("Symbol:", symbol2)
        print("Balance:", balance2)
        print("Properties owned are")
        print_list(player2_properties)
        print("Buildings built are")
        print_list(player2_buildings)


# function used to create buildings only at places owned by player who's turn it is
def create_building(player_position, player, board, balance, buildings_list):
    which_building = input("Which property do you want to build on?")
    building = False

    while building == False:
        for i in range(len(board)):
            if board[i][PLACE] == which_building or board[i][ABBREV] == which_building:
                if board[i][OWNED] != YES_OWNED + player:
                    print("You must own the property to build a building")
                    building = True
                    return balance
                if board[i][OWNED] == YES_OWNED + player:
                    if board[player_position][BUILDING_OWNED] == YES_OWNED + player:
                        print("You have already built a building here")
                        building = True
                        return balance
                    if int(board[i][BUILDING_COST]) > balance:
                        print("You do not have enough money too build a building")
                        building = True
                        return balance
                    else:
                        print("A building has been built at", board[i][PLACE] + "!")
                        board[i][BUILDING_OWNED] = YES_OWNED + player
                        buildings_list.append(board[i][PLACE])
                        balance -= int(board[i][BUILDING_COST])
                        building = True
                        return int(balance)

        if building == False:
            print("That property does not exist please reenter")
            which_building = input("Which property do you want to build on?")

# play game function where the actual game is played
def play_game(starting_money, pass_go_money, board_file):
    # this new_board includes the dictionary keys I added
    new_board = owned_loop(board_file)
    player1_balance = int(starting_money)
    player2_balance = int(starting_money)

    player1 = input("First player, what is your name?")
    player1_symbol = input("First player, what symbol do you want your character to use?")
    # will check to make sure symbol is one uppercase letter
    if len(player1_symbol) > 1:
        while len(player1_symbol) > 1:
            print("Please reenter a symbol")
            player1_symbol = input("First player, what symbol do you want your character to use")
    if ord(player1_symbol) < UPPER_A_VALUE and len(player1_symbol) == 1:
        while ord(player1_symbol) < UPPER_A_VALUE:
            print("Please reenter a symbol")
            player1_symbol = input("First player, what symbol do you want your character to use?")
    if ord(player1_symbol) > UPPER_Z_VALUE and len(player1_symbol) == 1:
        while ord(player1_symbol) > UPPER_Z_VALUE:
            print("Please reenter a symbol")
            player1_symbol = input("First player, what symbol do you want your character to use")

    player2 = input("Second player, what is your name?")
    player2_symbol = input("Second player, what symbol do you want your character to use?")

    if len(player2_symbol) > 1:
        while len(player2_symbol) > 1:
            print("Please reenter a symbol")
            player2_symbol = input("Second player, what symbol do you want your character to use")
    if ord(player2_symbol) < UPPER_A_VALUE and len(player2_symbol) == 1:
        while ord(player2_symbol) < UPPER_A_VALUE:
            print("Please reenter a symbol")
            player2_symbol = input("Second player, what symbol do you want your character to use?")
    if ord(player2_symbol) > UPPER_Z_VALUE and len(player2_symbol) == 1:
        while ord(player2_symbol) > UPPER_Z_VALUE:
            print("Please reenter a symbol")
            player2_symbol = input("Second player, what symbol do you want your character to use")
    # will make sure symbols are not the same
    if player1_symbol == player2_symbol:
        while player1_symbol == player2_symbol:
            print("Symbols must be different!")
            player2_symbol = input("Second player, what symbol do you want your character to use")

    # will keep track of the players current position
    player1_position = 0
    player2_position = 0

    # will help keep track of who's turn it is
    player1_turn = 1
    player2_turn = 1
    # check tracks if players have passed go or not
    player1_pass_go = 0
    player2_pass_go = 0

    # will loop until either of the balances are less then 0 or are 0
    while int(player1_balance) > 0 and int(player2_balance) > 0:
        # the mod helps rotate turns
        while player1_turn % 2 != 0:

            dice_roll = randint(1, 6) + randint(1, 6)
            player1_position += dice_roll
            player1_pass_go += dice_roll
            board1 = format_display(board_file)
            player1_position %= len(board1)
            move_board = list(board1)
            # updates both players current position to the board
            move_board[player1_position] = move_board[player1_position][0:6] + player1_symbol
            move_board[player2_position] = move_board[player2_position][0:6] + player2_symbol
            display_board(move_board)

            print(player1, "it is your turn!")
            print(player1, "you have rolled a", dice_roll)
            print(player1, "you have landed at", new_board[player1_position][PLACE])

            # checks if the player has passed go and gives money if they have
            if player1_pass_go >= len(board1):
                player1_balance += pass_go_money
                print("You have passed go, Here is your money!")
                player1_pass_go = player1_position

            # first checks if a building is built by the opposite player on the property
            if new_board[player1_position][BUILDING_OWNED] == YES_OWNED + player2:
                # player who's turn it is loses the money other player gains it
                player1_balance -= int(new_board[player1_position][BUILDING_RENT])
                player2_balance += int(new_board[player1_position][BUILDING_RENT])
                print(player1, "you had to pay a building rent of",
                      new_board[player1_position][BUILDING_RENT], "to", player2)
            # if no building next it will be checked if rent exist and if its owned by
            # by the other player
            elif int(new_board[player1_position][RENT]) > 0 \
                    and new_board[player1_position][OWNED] == YES_OWNED + player2:
                player1_balance -= int(new_board[player1_position][RENT])
                player2_balance += int(new_board[player1_position][RENT])
                print(player1, "you had to pay a rent of", new_board[player1_position][RENT],
                      "to", player2)
            # if the balance becomes 0 or less by paying building rent or rent
            # the loop will end and the game will end
            if player1_balance <= 0:
                player1_turn = take_turn(player1_turn)

            # if the balance is good the option menu will be displayed
            if player1_turn % 2 != 0:
                print_list(option_list)

                which_option = input("Which option do you pick?").strip().lower()
                # loop will keep going until end turn or number 5 is inputted
                while which_option != option_list[END_TURN_POSITION] \
                        and which_option != option_numbered_list[END_TURN_POSITION]:
                    # will run if the phrase or number entered is not valid
                    if which_option not in option_list and which_option not in option_numbered_list:
                        print("The option you selected is not available try again")
                        which_option = input("Which option do you pick").strip().lower()
                    # all of these will call the function of whatever option the user selected
                    if which_option == option_list[BUY_PROPERTY_POSITION] \
                            or which_option == option_numbered_list[BUY_PROPERTY_POSITION]:
                        player1_balance = int(buy_property_function(player1_position,
                                                                    new_board, player1_balance, player1, player2, player1_properties))
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[PROPERTY_INFO_POSITION] \
                            or which_option == option_numbered_list[PROPERTY_INFO_POSITION]:
                        property_info(new_board, player1, player2)
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[PLAYER_INFO_POSITION] \
                            or which_option == option_numbered_list[PLAYER_INFO_POSITION]:
                        player_info(player1, player1_symbol, player1_balance, player2, player2_symbol, player2_balance)
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[BUILDING_POSITION] \
                            or which_option == option_numbered_list[BUILDING_POSITION]:
                        player1_balance = \
                            create_building(player1_position, player1, new_board, player1_balance, player1_buildings)
                        which_option = input("Which option do you pick?").strip().lower()

                # ends the current turn
                if which_option == option_list[END_TURN_POSITION] \
                        or which_option == option_numbered_list[END_TURN_POSITION]:
                    # updates both making player 1 no longer odd ending this loop
                    # while making player 2 even allowing their turn loop to start
                    player1_turn = take_turn(player1_turn)
                    player2_turn = take_turn(player2_turn)
        # this entire loop will work exactly like player 1s loop
        while player2_turn % 2 == 0:

            dice_roll2 = randint(1, 6) + randint(1, 6)
            player2_position += dice_roll2
            player2_pass_go += dice_roll2
            board1 = format_display(board_file)
            player2_position %= len(board1)
            move_board = list(board1)
            move_board[player1_position] = move_board[player1_position][0:6] + player1_symbol
            move_board[player2_position] = move_board[player2_position][0:6] + player2_symbol
            display_board(move_board)

            print(player2, "it is your turn!")
            print(player2, "you have rolled a", dice_roll2)
            print(player2, "you have landed at", new_board[player2_position][PLACE])

            if player2_pass_go >= len(board1):
                player2_balance += pass_go_money
                print("You have passed go, Here is your money!")
                player2_pass_go = player2_position

            if new_board[player2_position][BUILDING_OWNED] == YES_OWNED + player1:
                player2_balance -= int(new_board[player2_position][BUILDING_RENT])
                player1_balance += int(new_board[player2_position][BUILDING_RENT])
                print(player2, "you had to pay a building rent of",
                      new_board[player2_position][BUILDING_RENT], "to", player1)

            elif int(new_board[player2_position][RENT]) > 0 \
                    and new_board[player2_position][OWNED] == YES_OWNED + player1:
                player2_balance -= int(new_board[player2_position][RENT])
                player1_balance += int(new_board[player2_position][RENT])
                print(player2, "you had to pay a rent of", new_board[player2_position][RENT],
                      "to", player1)
            if player2_balance <= 0:
                player2_turn = take_turn(player2_turn)

            if player2_turn % 2 == 0:

                print_list(option_list)

                which_option = input("Which option do you pick?").lower().strip()

                while which_option != option_list[END_TURN_POSITION] \
                        and which_option != option_numbered_list[END_TURN_POSITION]:

                    if which_option not in option_list and which_option not in option_numbered_list:
                        print("The option you selected is not available try again")
                        which_option = input("Which option do you pick").strip().lower()

                    if which_option == option_list[BUY_PROPERTY_POSITION] \
                            or which_option == option_numbered_list[BUY_PROPERTY_POSITION]:
                        player2_balance = int(buy_property_function(player2_position,
                                                                    new_board, player2_balance, player2, player1, player2_properties))
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[PROPERTY_INFO_POSITION] \
                            or which_option == option_numbered_list[PROPERTY_INFO_POSITION]:
                        property_info(new_board, player1, player2)
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[PLAYER_INFO_POSITION] \
                            or which_option == option_numbered_list[PLAYER_INFO_POSITION]:
                        player_info(player1, player1_symbol, player1_balance, player2, player2_symbol, player2_balance)
                        which_option = input("Which option do you pick?").strip().lower()

                    if which_option == option_list[BUILDING_POSITION] \
                            or which_option == option_numbered_list[BUILDING_POSITION]:
                        player2_balance = \
                            create_building(player2_position, player2, new_board, player2_balance, player2_buildings)
                        which_option = input("Which option do you pick?").lower().strip()

                if which_option == option_list[END_TURN_POSITION] \
                        or which_option == option_numbered_list[END_TURN_POSITION]:
                    player1_turn = take_turn(player1_turn)
                    player2_turn = take_turn(player2_turn)
    # main game loop is broken this will print and the game will end
    print("A player has gone bankrupt the game has ended")


if __name__ == '__main__':
    """""
     function to play the game, all that is needed if the user
    to enter with quotations the board they want to use in
    the 3rd parameter of the function
     
    """""
    play_game(STARTING_AMOUNT, PASS_GO_AMOUNT, "proj1_board1.csv")