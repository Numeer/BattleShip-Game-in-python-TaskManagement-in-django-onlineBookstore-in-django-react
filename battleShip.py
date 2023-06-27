import random
import pickle
import string

grid_size = 26
grid = [['- ' for i in range(grid_size)] for i in range(grid_size)]
# with open("savegame.txt", "w") as file:
#     file.writelines(str(grid))
# with open("savegame.txt", "r") as file:
#     grid = file.readlines()
class Player:
    def __init__(self, name):  # Constructor for the Player class
        self.name = name
        self.ships = []
        self.destroyed_ships = set()

    def place_ships(self, num_ships, max_ship_size, size):  # Place ships on the grid
        for _ in range(num_ships):  # Loop through the number of ships
            ship_size = random.randint(1, max_ship_size)  # Randomly generate the size of the ship
            self.ships.append(ship_size)
            self.place_ships_on_grids(ship_size, size)

    def place_ships_on_grids(self, ship_size, size):  # Place a ship on the grid
        while True:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            orientation = random.choice(['horizontal', 'vertical'])

            if self.ship_placing(ship_size, x, y, orientation, size):
                if orientation == 'horizontal':
                    for i in range(ship_size):
                        grid[y][x + i] = 'S ' + self.name[0]  # append the first letter of the name to the grid
                else:
                    for i in range(ship_size):
                        grid[y + i][x] = 'S ' + self.name[0]  # append the first letter of the name to the grid
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
                        if x < 0 or y < 0 or x >= grid_size or y >= grid_size:
                            raise ValueError

                    else:
                        print("Invalid choice. Try again :<")
                        continue
                if grid[y][x] == 'X ' or grid[y][x] == 'M ':  # Check if the coordinates have been attacked or missed
                    print("You already attacked this coordinate. Try again :<")
                    continue

                if grid[y][x] == 'S ' + opponent.name[0]:  # Check if the coordinates have an opponent's ship
                    print("You hit an opponent's ship :>")
                    grid[y][x] = 'X '
                    for ship in opponent.ships:
                        if self.is_ship_destroyed(ship):
                            print("\n\t\tYou destroyed an opponent's ship! :>)")
                            self.destroyed_ships.add(ship)
                            opponent.ships.remove(ship)
                    break
                if grid[y][x] == 'S ' +self.name[0]:  # Check if the coordinates have your own ship
                    print("You can't hit your own ship :<")
                    continue

                if grid[y][x] == '- ':  # Check if the coordinates have no ship
                    print("You missed!")
                    grid[y][x] = 'M '
                    break

            except ValueError:
                print("Invalid coordinates. Try again :<")

    def is_ship_destroyed(self, ship):  # Check if the ship is destroyed
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == 'S '+self.name[0] and (i, j) not in self.destroyed_ships:
                    return False
        return True

    def display_grid(self,opponent):  # Display the grid
        size = len(grid)

        # Display column labels
        print("   ", end="")
        for i in range(size):
            print(f"{chr(i + ord('A')):2}", end=" ")
        print()

        # Display row labels and grid
        for i in range(size):
            print(f"{i+1:2}", end=" ")
            for j in range(size):
                if grid[i][j] == 'S '+ opponent.name[0]: # if the owner is not the current player print -
                    print("- ", end=" ")
                elif grid[i][j] == 'S '+ self.name[0]: # if the owner is the current player print S
                    print("S ", end=" ")
                else:
                    print(grid[i][j], end=" ")
            print()

    def save_game(self, obj2):  # Save the game
        with open("savegame.pickle", "wb") as file:
            pickle.dump(obj2, file)
            pickle.dump(self, file)
        print("\t\tGame saved successfully :>)")
        with open("savegame.txt", "w") as file:
            file.writelines(str(grid))
    def win_game(self,opponent):
        if not opponent.ships:
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

def load_game(): # Load the game
    try:
        list=[]
        with open("savegame.pickle", "rb") as file:
            p1=pickle.load(file)
            list.append(p1)
            p2=pickle.load(file)
            list.append(p2)
        with open("savegame.txt", "r") as file:
            grid=file.readlines()
            print(grid)
            print(type(grid))
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
                    opponent = input("\t\tPlayer 1 Enter your name :) ")
                    opponent2 = input("\t\tPlayer 2 Enter your name :) ")
                    player1 = Player(opponent)
                    player2 = Player(opponent2)

                    player1.place_ships(6, 5, 26)
                    player2.place_ships(6, 5, 26)

                    while True:
                        player1.turn_grid()
                        player1.display_grid(player2)
                        player1.attack(player2)

                        if player1.win_game(player2):
                            break
                        
                        player2.turn_grid()
                        player2.display_grid(player1)
                        player2.attack(player1)

                        if player2.win_game(player1):
                            break
    
                elif choice == '2':
                    opponent = input("\t\tEnter your name :) ")
                    player1 = Player(opponent)
                    player2 = Player("Computer")  # Create a computer player


                    player1.place_ships(6, 5, 26)
                    player2.place_ships(6, 5, 26)

                    while True:
                        player1.turn_grid()
                        player1.display_grid(player2)
                        player1.attack(player2)

                        if player1.win_game(player2):
                            break

                        print("\n\t\t---- Computer's Turn ----")  # Computer player's turn
                        player2.attack(player1)

                        if player2.win_game(player1):
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
                    player1.turn_grid()
                    player1.display_grid(player2)
                    player1.attack(player1)

                    if player1.win_game(player2):
                        break

                    player2.turn_grid()
                    player2.display_grid(player1)
                    player2.attack(player1)

                    if player2.win_game(player1):
                        break

        elif choice == '3':
            print("\n\t\tThank you for playing :)")
            break

        else:
            print("\t\tInvalid choice. Please try again :<")


if __name__ == '__main__':
    main()

