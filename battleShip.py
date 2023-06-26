import random
import pickle


class Ship:
    def __init__(self, size): # Constructor for the Ship class
        self.size = size

class Player:
    def __init__(self, name): # Constructor for the Player class
        self.name = name
        self.ships = []
        self.destroyedShips = set()
        self.grid = []

    def createGrid(self, size): # Create a grid for the player
        self.grid = [['O ' for i in range(size)] for i in range(size)]

    def placeShips(self, num_ships, max_ship_size, size): # Place ships on the grid
        for i in range(num_ships): # Loop through the number of ships
            ship_size = random.randint(1, max_ship_size) # Randomly generate the size of the ship
            ship = Ship(ship_size)
            self.ships.append(ship)
            self.placeShipOnGrids(ship, size) 

    def placeShipOnGrids(self, ship, size): # Place a ship on the grid
        while True:
            x = random.randint(0, size - 1) # Randomly generate the x-coordinate
            y = random.randint(0, size - 1) # Randomly generate the y-coordinate
            orientation = random.choice(['horizontal', 'vertical']) # Randomly generate the orientation of the ship

            if self.shipPlacing(ship, x, y, orientation, size): # Check if the ship can be placed on the grid
                if orientation == 'horizontal':
                    for i in range(ship.size): 
                        self.grid[y][x + i] = 'S '
                else:
                    for i in range(ship.size):
                        self.grid[y + i][x] = 'S '
                break

    def shipPlacing(self, ship, x, y, orientation, size): # Check if the ship can be placed on the grid
        if orientation == 'horizontal':
            if x + ship.size > size: # Check if the ship can be placed horizontally
                return False
            for i in range(ship.size):
                if self.grid[y][x + i] == 'S ':
                    return False
        else:
            if y + ship.size > size: # Check if the ship can be placed vertically
                return False
            for i in range(ship.size):
                if self.grid[y + i][x] == 'S ':
                    return False
        return True

    def attack(self, opponent): # Attack the opponent
        while True:
            try:
                if self.name == "Computer":  # Check if current player is the computer
                    x = random.randint(0, len(opponent.grid) - 1) # Randomly generate the x-coordinate for computer
                    y = random.randint(0, len(opponent.grid) - 1) # Randomly generate the y-coordinate for computer
                else:
                    try:
                        x = int(input("Enter the x-coordinate to attack: "))
                        y = int(input("Enter the y-coordinate to attack: "))
                        if x < 0 or y < 0 or x >= len(opponent.grid) or y >= len(opponent.grid): # Check if the coordinates are valid
                            raise ValueError

                    except ValueError:
                        print("Invalid coordinates. Try again :<")
                        continue

                if opponent.grid[y][x] == 'X ' or opponent.grid[y][x] == 'M ': # Check if the coordinates have been attacked or missed
                    print("You already attacked this coordinate. Try again :<")
                    continue

                if opponent.grid[y][x] == 'S ': # Check if the coordinates have ship
                    print("You hit an opponent's ship :>")
                    opponent.grid[y][x] = 'X '
                    for ship in opponent.ships:
                        if self.isShipDestroyed(ship, opponent.grid):
                            print("\n\t\tYou destroyed an opponent's ship! :>)")
                            self.destroyedShips.add(ship)
                            opponent.ships.remove(ship)
                    break

                if opponent.grid[y][x] == 'O ': # Check if the coordinates have no ship
                    print("You missed!")
                    opponent.grid[y][x] = 'M '
                    break

            except ValueError:
                print("Invalid coordinates. Try again :<")

    def isShipDestroyed(self, ship, grid): # Check if the ship is destroyed
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == 'S ' and (i, j) not in self.destroyedShips:
                    return False
        return True

    def displayGrid(self): # Display the grid
        size = len(self.grid)

        # Display column labels
        print("  ", end="")
        for i in range(size):
            print(f"{i:2}", end=" ")
        print()

        # Display row labels and grid
        for i in range(size):
            print(f"{i:2}", end=" ")
            print(" ".join(self.grid[i]))



def displayMenu():
    print("\t\t----== Battle Ships Menu ----==")
    print("\t\t1. New Game")
    print("\t\t2. Load Game")
    print("\t\t3. Quit")


def displayMenu2():
    print("\t\t 1. Play with a friend")
    print("\t\t 2. Play with a computer")
    print("\t\t 3. Back to main menu")

def saveGame(obj1,obj2): # Save the game
    with open("savegame.pickle", "wb") as file: 
        pickle.dump(obj1, file)
        pickle.dump(obj2, file)
    print("\t\tGame saved successfully :>)")

def loadGame(): # Load the game
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
        displayMenu()
        choice = input("\t\tEnter your choice: ")

        if choice == '1':
            while True:
                displayMenu2()
                choice = input("\t\tEnter your choice: ")
                if choice == '1':
                    p = input("\t\tPlayer 1 Enter your name :) ")
                    p2 = input("\t\tPlayer 2 Enter your name :) ")
                    player1 = Player(p)
                    player2 = Player(p2)

                    player1.createGrid(26)
                    player2.createGrid(26)

                    player1.placeShips(6, 7, 26)
                    player2.placeShips(6, 7, 26)

                    while True:
                        print(f"\n\t\t---- {player1.name} Turn ----")
                        print(f"\t\t {player1.name} Grid: \n")
                        player1.displayGrid()
                        player1.attack(player2)

                        if not player2.ships:
                            print(f"\t\t\t{player1.name} wins! :>)")
                            break

                        print(f"\n\t\t---- {player2.name} Turn ----")
                        print(f"\t\t{player2.name} Grid: \n")
                        player2.displayGrid()
                        player2.attack(player1)

                        if not player1.ships:
                            print(f"\t\t\tKudos {player2.name} You wins! :>)")
                            break
                        while True:
                            print("\n\t\t Do you want to save the game? (y/n) :>")
                            print("\t\t Quit the game? (q) :>s")
                            saveChoice = input("\n\t\t Enter your choice:> ")
                            if saveChoice.lower() == 'y':
                                saveGame(player1, player2)
                            elif saveChoice.lower() == 'n':
                                break
                            elif saveChoice.lower() == 'q':
                                exit()
                            else:
                                print("\t\tInvalid choice. Try again :<")
                                continue
                elif choice == '2':
                    p = input("\t\tEnter your name :) ")
                    player1 = Player(p)
                    player2 = Player("Computer")  # Create a computer player

                    player1.createGrid(26)
                    player2.createGrid(26)

                    player1.placeShips(6, 7, 26)
                    player2.placeShips(6, 7, 26)

                    while True:
                        print(f"\n\t\t---- {player1.name} Turn ----")
                        print(f"\t\t{player1.name} Grid: \n")
                        player1.displayGrid()
                        player1.attack(player2)

                        if not player2.ships:
                            print(f"\t\t\tKudos {player1.name} You wins! :>")
                            break

                        print("\n\t\t---- Computer's Turn ----")  # Computer player's turn
                        player2.attack(player1)

                        if not player1.ships:
                            print("\t\t\tComputer wins :>\n Better luck next time :<")
                            break

                        saveChoice = input("\n\t\tDo you want to save the game? (y/n) :> ")
                        if saveChoice.lower() == 'y':
                            saveGame(player1,player2)
                            break
                elif choice == '3':
                    break
                else:
                    print("\n\t\tInvalid choice. Try again :<")

        elif choice == '2':
            saved_game = loadGame()
            if saved_game:
                player1 = saved_game[0]
                player2 = saved_game[1]

                player2.createGrid(26)
                player2.placeShips(6, 7, 26)

                while True:
                    print(f"\n\t\t---- {player1.name} Turn ----")
                    print(f"\t\t{player1.name} Grid: \n")
                    player1.displayGrid()
                    player1.attack(player2)

                    if not player2.ships:
                        print(f"\n\t\tKudos {player1.name} You wins! :>)")
                        break

                    print(f"\n\t\t---- {player2.name} Turn ----")
                    print(f"\t\t{player2.name} Grid: \n")
                    player2.displayGrid()
                    player2.attack(player1)

                    if not player1.ships:
                        print(f"\n\t\tKudos {player2.name} You wins! :>)")
                        break

                    saveChoice = input("\n\t\tDo you want to save the game? (y/n) :> ")
                    if saveChoice.lower() == 'y':
                        saveGame(player1,player2)
                        break

        elif choice == '3':
            print("\n\t\tThank you for playing :)")
            break

        else:
            print("\t\tInvalid choice. Please try again :<")


if __name__ == '__main__':
    main()

