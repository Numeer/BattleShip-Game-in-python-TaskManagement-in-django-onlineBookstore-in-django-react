import random
import pickle
import string

GRID_SIZE = 26
grid = [['- ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


class Player:
    def __init__(self, name):  # Constructor for the Player class
        self.name = name
        self.ships = []

    def place_ships(self, num_ships, max_ship_size):  # Place ships on the grid
        for _ in range(num_ships):  # Loop through the number of ships
            # Randomly generate the size of the ship
            ship_size = random.randint(1, max_ship_size)
            self.ships.append(ship_size)
            self.place_ships_on_grids(ship_size)

    def place_ships_on_grids(self, ship_size):  # Place a ship on the grid
        while True:
            x, y = self.generate_random_coordinates()
            orientation = random.choice(['horizontal', 'vertical'])

            if self.ship_placing(ship_size, x, y, orientation):
                if orientation == 'horizontal':
                    for i in range(ship_size):
                        # append the first letter of the name to the grid
                        grid[y][x + i] = 'S ' + self.name
                else:
                    for i in range(ship_size):
                        # append the first letter of the name to the grid
                        grid[y + i][x] = 'S ' + self.name
                break

    # Check if the ship can be placed on the grid
    def ship_placing(self, ship_size, x, y, orientation, ):
        if orientation == 'horizontal':
            for i in range(ship_size):
                if y >= GRID_SIZE or x + i >= GRID_SIZE or grid[y][x + i] == 'S ':
                    return False
        else:
            for i in range(ship_size):
                if y + i >= GRID_SIZE or x >= GRID_SIZE or grid[y + i][x] == 'S ':
                    return False
        return True

    # Generate random coordinates for computer's attack
    def generate_random_coordinates(self):
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        return x, y

    # Parse user input coordinates into x, y values
    def set_coordinates(self, coordinates):
        x = string.ascii_uppercase.index(coordinates[0].upper())
        y = int(coordinates[1:]) - 1
        return x, y

    # Check if the coordinates are within the valid range
    def is_valid_coordinates(self, x, y):
        return 0 <= x <= GRID_SIZE and 0 <= y <= GRID_SIZE

    # Check if the coordinates have already been attacked or missed
    def is_already_attacked(self, x, y):
        return grid[y][x] == 'X ' or grid[y][x] == 'M '

    # Check if the coordinates have an opponent's ship and mark it as hit
    def hit_opponent_ship(self, x, y, opponent):
        if grid[y][x] == 'S ' + opponent.name:
            grid[y][x] = 'X '
            return True
        return False

    # Check if any of the opponent's ships are destroyed and update the state
    def destroy_ships(self, opponent):
        for ship in opponent.ships:
            if self.is_ship_destroyed():
                print(f"\n\t\tYou destroyed {self.name} ships! :>)")
                return True
        return False

    def hit_own_ship(self, x, y):  # Check if the coordinates have the player's own ship
        return grid[y][x] == 'S ' + self.name

    def mark_missed(self, x, y):  # Mark the coordinates as missed
        grid[y][x] = 'M '

    def is_ship_destroyed(self):  # Check if the ship is destroyed
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 'S ' + self.name and (i, j):
                    return False
        return True

    def attack(self, opponent):
        while True:
            try:
                if self.name == "Computer":
                    # Generate random coordinates for computer's attack
                    x, y = self.generate_random_coordinates()
                else:
                    choice = input(
                        "Enter your choice (quit/save/attack <co-ordinates>): ")

                    if choice.lower() == "quit":
                        exit()
                    elif choice.lower() == "save":
                        self.save_game(opponent)
                        exit()

                    if choice.startswith("attack "):
                        coordinates = choice.split(" ")[1]
                        x, y = self.set_coordinates(coordinates)
                        if not self.is_valid_coordinates(x, y):
                            raise ValueError
                    else:
                        print("Invalid choice. Try again :<")
                        continue

                if self.is_already_attacked(x, y):
                    print("You already attacked this coordinate. Try again :<")
                    continue

                if self.hit_opponent_ship(x, y, opponent):
                    print(f"You hit {opponent.name}'s ship :>")
                    if opponent.destroy_ships(self):
                        break

                elif self.hit_own_ship(x, y):
                    print("You can't hit your own ship :<")
                    continue
                else:
                    print(f"{self.name} You missed!")
                    self.mark_missed(x, y)

                break
            except ValueError:
                print("Invalid coordinates. Try again :<")

    def display_grid(self, opponent):  # Display the grid
        size = len(grid)

        # Display column labels
        print("   ", end="")
        for i in range(size):
            print(f"{chr(i + ord('A')):2}", end=" ")
        print()

        # Display row labels and grid
        for i in range(size):
            print(f"{i + 1:2}", end=" ")
            for j in range(size):
                # if the owner is not the current player print -
                if grid[i][j] == 'S ' + opponent.name:
                    print("- ", end=" ")
                # if the owner is the current player print S
                elif grid[i][j] == 'S ' + self.name:
                    print("S ", end=" ")
                else:
                    print(grid[i][j], end=" ")
            print()

    def save_game(self, obj2):  # Save the game
        with open("savegame.pickle", "wb") as file:
            pickle.dump(obj2, file)
            pickle.dump(self, file)
            pickle.dump(grid, file)  # Save the grid

        print("\t\tGame saved successfully :>)")

    def win_game(self, opponent):
        if opponent.is_ship_destroyed():
            print(f"\t\t\tKudos {self.name} wins! :>)")
            return True
        return False

    def turn_grid(self):
        print(f"\n\t\t---- {self.name} Turn ----")
        print(f"\t\t{self.name} Grid: \n")


def display_menu():
    print("\t\t----== Battle Ships Menu ----==")
    print("\t\t1. New Game")
    print("\t\t2. Load Game")
    print("\t\t3. Quit")


def display_menu2():
    print("\t\t 1. Play with a friend")
    print("\t\t 2. Play with a computer")
    print("\t\t 3. Back to main menu")


def load_game():  # Load the game
    try:
        list = []
        with open("savegame.pickle", "rb") as file:
            global grid
            p1 = pickle.load(file)
            list.append(p1)
            p2 = pickle.load(file)
            list.append(p2)
            grid = pickle.load(file)
            return list
    except FileNotFoundError:
        print("No saved game found :<(")
        return None


def check_win(player1, player2, choice):
    flag = False
    while True:
        player1.turn_grid()
        player1.display_grid(player2)
        player1.attack(player2)

        if player1.win_game(player2):
            flag = True
            return flag

        if choice != '2':
            player2.turn_grid()
            player2.display_grid(player1)

        player2.attack(player1)

        if player2.win_game(player1):
            flag = True
            return flag


def play_game(ships, ships_size, choice):
    opponent = input("\t\tPlayer 1 Enter your name :) ")
    flag = True
    if choice != '2':
        opponent2 = input("\t\tPlayer 2 Enter your name :) ")
        while flag:
            if opponent2 == opponent:
                print("\t\tName already taken. Try again :<")
                opponent2 = input("\t\tPlayer 2 Enter your name :) ")
            flag = False
    else:
        while flag:
            if opponent == "Computer":
                print("\t\tName already taken. Try again :<")
                opponent2 = input("\t\tPlayer 1 Enter your name :) ")
            flag = False
        player2 = Player("Computer")  # Create a computer player

    player1 = Player(opponent)
    if choice != '2':
        player2 = Player(opponent2)

    player1.place_ships(ships, ships_size)
    player2.place_ships(ships, ships_size)

    if check_win(player1, player2, choice):
        exit()


def main():
    while True:
        display_menu()
        choice = input("\t\tEnter your choice: ")
        ships = 6  # no  of ships per player
        ships_size = 5  # size of each ship it is random from 1 to 5 in place_ships function
        if choice == '1':
            while True:
                display_menu2()
                choice = input("\t\tEnter your choice: ")
                if choice == '1':
                    play_game(ships, ships_size, choice)

                elif choice == '2':
                    play_game(ships, ships_size, choice)

                elif choice == '3':
                    break
                else:
                    print("\n\t\tInvalid choice. Try again :<")

        elif choice == '2':
            saved_game = load_game()
            if saved_game:
                player1 = saved_game[0]
                player2 = saved_game[1]
                check_win(player1, player2, choice)

        elif choice == '3':
            print("\n\t\tThank you for playing :)")
            break

        else:
            print("\t\tInvalid choice. Please try again :<")


if __name__ == '__main__':
    main()
