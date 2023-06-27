import random
import pickle
import string

grid = [['- ' for i in range(26)] for i in range(26)]

class Player:
    def __init__(self, name):  # Constructor for the Player class
        self.name = name
        self.ships = []
        self.destroyedShips = set()
        self.hiddenGrid = []

    def create_grid(self, size):  # Create a grid for the player
        self.hiddenGrid = [['- ' for _ in range(size)] for _ in range(size)]

    def place_ships(self, num_ships, max_ship_size, size):  # Place ships on the grid
        for _ in range(num_ships):  # Loop through the number of ships
            ship_size = random.randint(1, max_ship_size)  # Randomly generate the size of the ship
            self.ships.append(ship_size)
            self.place_ships_on_grids(ship_size, size)

    def place_ships_on_grids(self, ship_size, size):  # Place a ship on the grid
        while True:
            x = random.randint(0, size)  # Randomly generate the x-coordinate
            y = random.randint(0, size)  # Randomly generate the y-coordinate
            orientation = random.choice(['horizontal', 'vertical'])  # Randomly generate the orientation of the ship

            if self.ship_placing(ship_size, x, y, orientation, size):  # Check if the ship can be placed on the grid
                if orientation == 'horizontal':
                    for i in range(ship_size):
                        if x + i >= len(grid):
                            continue
                        else:
                            grid[y][x + i] = 'S '
                            self.hiddenGrid[y][x + i] = 'S '
                else:
                    for i in range(ship_size):
                        if y + i >= len(grid):
                            continue
                        else:
                            grid[y + i][x] = 'S '
                            self.hiddenGrid[y + i][x] = 'S '
                break
    def ship_placing(self, ship_size, x, y, orientation, size):  # Check if the ship can be placed on the grid
        if orientation == 'horizontal':
            for i in range(ship_size):
                if y >= size or x + i >= size or grid[y][x + i] == 'S ':
                    return False
        else:
            for i in range(ship_size):
                if y + i >= size or x >= size or grid[y + i][x] == 'S ':
                    return False
        return True
    
    def attack(self, opponent):  # Attack the opponent
        while True:
            try:
                if self.name == "Computer":
                    x = random.randint(0, len(grid) - 1)  # Randomly generate the x-coordinate for computer
                    y = random.randint(0, len(grid) - 1)  # Randomly generate the y-coordinate for computer
                else:
                    choice = input("Enter your choice (quit/save/attack <co-ordinates>): ")

                    if choice.lower() == "quit":
                        exit()
                    elif choice.lower() == "save":
                        self.save_game(opponent)
                        exit()

                    if choice.startswith("attack "):
                        coordinates = choice.split(" ")[1]
                        x = string.ascii_uppercase.index(coordinates[0].upper())
                        y = int(coordinates[1:]) - 1
                        if x < 0 or y < 0 or x >= len(grid) or y >= len(grid):
                            raise ValueError

                    else:
                        print("Invalid choice. Try again :<")
                        continue
                if opponent.hiddenGrid[y][x] == 'X ' or opponent.hiddenGrid[y][x] == 'M ':  # Check if the coordinates have been attacked or missed
                    print("You already attacked this coordinate. Try again :<")
                    continue

                if opponent.hiddenGrid[y][x] == 'S ':  # Check if the coordinates have a ship
                    print("You hit an opponent's ship :>")
                    opponent.hiddenGrid[y][x] = 'X '
                    for ship in opponent.ships:
                        if self.is_ship_destroyed(ship, grid):
                            print("\n\t\tYou destroyed an opponent's ship! :>)")
                            self.destroyedShips.add(ship)
                            opponent.ships.remove(ship)
                    break

                if opponent.hiddenGrid[y][x] == '- ':  # Check if the coordinates have no ship
                    print("You missed!")
                    grid[y][x] = 'M '
                    break

            except ValueError:
                print("Invalid coordinates. Try again :<")

    def is_ship_destroyed(self, ship, grid): # Check if the ship is destroyed
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == 'S ' and (i, j) not in self.destroyedShips:
                    return False
        return True

    def display_grid(self): # Display the grid
        size = len(self.grid)

        # Display column labels
        print("   ", end="")
        for i in range(size):
            print(f"{chr(i + ord('A')):2}", end=" ")
        print()

        # Display row labels and grid
        for i in range(size):
            print(f"{i+1:2}", end=" ")
            print(" ".join(self.grid[i]))

    def display_hidden_grid(self,opponent):  # Display the hidden grid
        size = len(self.hiddenGrid)

        # Display column labels
        print("   ", end="")
        for i in range(size):
            print(f"{chr(i + ord('A')):2}", end=" ")
        print()

        # Display row labels and grid
        for i in range(size):
            print(f"{i + 1:2}", end=" ")
            for j in range(size):
                if self.hiddenGrid[i][j] == 'S ' or self.hiddenGrid[i][j] == 'M ' or self.hiddenGrid[i][j] == 'X ':
                    print(self.hiddenGrid[i][j], end=" ")
                else:
                    print(self.hiddenGrid[i][j], end=" ")
            print()

    def save_game(self, obj2):  # Save the game
        with open("savegame.pickle", "wb") as file:
            pickle.dump(obj2, file)
            pickle.dump(self, file)
        print("\t\tGame saved successfully :>)")


def display_menu():
    print("\t\t----== Battle Ships Menu ----==")
    print("\t\t1. New Game")
    print("\t\t2. Load Game")
    print("\t\t3. Quit")


def display_menu2():
    print("\t\t 1. Play with a friend")
    print("\t\t 2. Play with a computer")
    print("\t\t 3. Back to main menu")

def load_game(): # Load the game
    try:
        list=[]
        with open("savegame.pickle", "rb") as file:
            p1=pickle.load(file)
            list.append(p1)
            p2=pickle.load(file)
            list.append(p2)
            return list
    except FileNotFoundError:
        print("No saved game found :<(")
        return None
def main():
    while True:
        display_menu()
        choice = input("\t\tEnter your choice: ")

        if choice == '1':
            while True:
                display_menu2()
                choice = input("\t\tEnter your choice: ")
                if choice == '1':
                    p = input("\t\tPlayer 1 Enter your name :) ")
                    p2 = input("\t\tPlayer 2 Enter your name :) ")
                    player1 = Player(p)
                    player2 = Player(p2)

                    player1.create_grid(26)
                    player2.create_grid(26)

                    player1.place_ships(6, 7, 26)
                    player2.place_ships(6, 7, 26)

                    while True:
                        print(f"\n\t\t---- {player1.name} Turn ----")
                        print(f"\t\t{player1.name} Grid: \n")
                        player1.display_hidden_grid(player2)
                        player1.attack(player2)

                        if not player2.ships:
                            print(f"\t\t\t{player1.name} wins! :>)")
                            break

                        print(f"\n\t\t---- {player2.name} Turn ----")
                        print(f"\t\t{player2.name} Grid: \n")
                        player2.display_hidden_grid(player1)
                        player2.attack(player1)

                        if not player1.ships:
                            print(f"\t\t\tKudos {player2.name} You wins! :>)")
                            break
    
                elif choice == '2':
                    p = input("\t\tEnter your name :) ")
                    player1 = Player(p)
                    player2 = Player("Computer")  # Create a computer player

                    player1.create_grid(26)
                    player2.create_grid(26)

                    player1.place_ships(6, 7, 26)
                    player2.place_ships(6, 7, 26)

                    while True:
                        print(f"\n\t\t---- {player1.name} Turn ----")
                        print(f"\t\t{player1.name} Grid: \n")
                        player1.display_hidden_grid(player2)
                        player1.attack(player2)

                        if not player2.ships:
                            print(f"\t\t\tKudos {player1.name} You wins! :>")
                            break

                        print("\n\t\t---- Computer's Turn ----")  # Computer player's turn
                        player2.attack(player1)

                        if not player1.ships:
                            print("\t\t\tComputer wins :>\n Better luck next time :<")
                            break

                elif choice == '3':
                    break
                else:
                    print("\n\t\tInvalid choice. Try again :<")

        elif choice == '2':
            saved_game = load_game()
            if saved_game:
                player1 = saved_game[0]
                player2 = saved_game[1]


                while True:
                    print(f"\n\t\t---- {player1.name} Turn ----")
                    print(f"\t\t{player1.name} Grid: \n")
                    player1.display_hidden_grid(player1)
                    player1.attack(player1)

                    if not player2.ships:
                        print(f"\n\t\tKudos {player1.name} You wins! :>)")
                        break

                    print(f"\n\t\t---- {player2.name} Turn ----")
                    print(f"\t\t{player2.name} Grid: \n")
                    player2.display_hidden_grid(player1)
                    player2.attack(player1)

                    if not player1.ships:
                        print(f"\n\t\tKudos {player2.name} You wins! :>)")
                        break

        elif choice == '3':
            print("\n\t\tThank you for playing :)")
            break

        else:
            print("\t\tInvalid choice. Please try again :<")


if __name__ == '__main__':
    main()

