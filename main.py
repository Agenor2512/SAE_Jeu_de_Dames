from asyncio.windows_events import NULL
from typing import Final
from Move import Move
import numpy as np 

gridSize: Final[int] = 10

grid = np.empty((gridSize, gridSize), dtype=str)
grid[:] = " "
row: int = 0
column: int = 0

### TODO ###
#
# - robustesse askToChooseCapture() (empêcher l'utilisateur d'entrer n'importe quoi, etc)
# 
#

## Initialisation de la grille en plaçant les pions aux bons endroits ##
def initGrid():
    for i in range(0, 4):
        for j in range((i+1)%2, gridSize, 2):
            grid[i][j] = "n"

    for i in range(gridSize-4, gridSize):
        for j in range((i+1)%2, gridSize, 2):
            grid[i][j] = "b"


## Affichage de la grille avec les index de colonnes et de lignes ##
def displayGrid():
    print("   1 2 3 4 5 6 7 8 9 10")
    for i in range(0, gridSize):
        if i < 9:
            print(i+1, end=" |")
        else:
            print(i+1, end="|")

        for j in range(0, gridSize):
                print(grid[i][j], end="|")
        print()
    print("\n")




## Test si le joueur peut jouer (s'il n'a pas choisit un pion adverse pour jouer, si la position du pion choisit est bonne) ##
def isPawnValid(pawnRowPos, pawnColumnPos, player):
    
    # Test si la position du pion choisie est bonne
    if (pawnRowPos > 9 or pawnColumnPos > 9) or (pawnRowPos < 0 or pawnColumnPos < 0):
        print("La position entrée pour le pion à jouer est hors du damier.\n")
        return False

    # Test si le joueur n'a pas choisit un pion adverse pour jouer
    # On utilise lower pour éviter que le test considère qu'une dame B par exemple, n'appartient pas au joueur blanc
    if grid[pawnRowPos][pawnColumnPos] != str(player).lower() and grid[pawnRowPos][pawnColumnPos] != " ":
        print("Vous avez choisi un pion qui n'est pas le vôtre.\n")
        return False
    
    if grid[pawnRowPos][pawnColumnPos] == " ":
        print("Il n'y a rien à la position que vous avez choisi.\n")
        return False
    return True
    
    

## Test si le joueur peut jouer (si la position de la case choisie pour y mettre le pion est bonne et si la case est bien vide) ##
def isMoveValid(cellRowPos, cellColumnPos, pawnRowPos, pawnColumnPos, player):

    # Test si la position de la case sur laquelle le joueur veut placer son pion est en dehors du damier
    if (cellRowPos > 9 or cellColumnPos > 9) or (cellRowPos < 0 or cellColumnPos < 0):
        print("La position entrée pour la case à jouer est hors du damier.\n")
        return False

    # Test si la case sur laquelle le joueur veut placer son pion est bien en diagonale devant lui
    if player == "b" and not (cellRowPos == pawnRowPos-1 and (cellColumnPos == pawnColumnPos-1 or cellColumnPos == pawnColumnPos+1)):
        print("Il faut que vous placiez votre pion en diagonale vers l'avant.\n")
        return False 
    elif player == "n" and not (cellRowPos == pawnRowPos+1 and (cellColumnPos == pawnColumnPos-1 or cellColumnPos == pawnColumnPos+1)):
        print("Il faut que vous placiez votre pion en diagonale vers l'avant.\n")
        return False

    # Test si la case sur laquelle le joueur veut placer son pion est vide ou non
    if grid[cellRowPos][cellColumnPos] != " ":
        print("La case n'est pas vide.")
        return False
    return True



## Test si un pion peut en prendre un autre dans chaque diagonale ##
def isMoveAbove(player, row, col):
    if grid[row][col] == player: 

        if row >= 3 and col >= 3:
            # Test la diagonale haut gauche (s'il y a bien un pion à prendre et si la case d'après est vide)
            if (grid[row][col] != grid[row-1][col-1]) and (grid[row-1][col-1] != " ") and (grid[row-2][col-2] == " "):
                return Move(row, col, row-2, col-2)

        if row >= 3 and col <= gridSize - 3:
            # Test la diagonale haut droite (s'il y a bien un pion à prendre et si la case d'après est vide)
            if (grid[row][col] != grid[row-1][col+1]) and (grid[row-1][col+1] != " ") and (grid[row-2][col+2] == " "):
                return Move(row, col, row-2, col+2)

        if row <= gridSize - 3 and col >= 3:
            # Test la diagonale bas gauche (s'il y a bien un pion à prendre et si la case d'après est vide)
            if (grid[row][col] != grid[row+1][col-1]) and (grid[row+1][col-1] != " ") and (grid[row+2][col-2] == " "):
                return Move(row, col, row+2, col-2)

        if row <= gridSize - 3 and col <= gridSize - 3:
            # Test la diagonale bas droite (s'il y a bien un pion à prendre et si la case d'après est vide)
            if (grid[row][col] != grid[row+1][col+1]) and (grid[row+1][col+1] != " ") and (grid[row+2][col+2] == " "):
                return Move(row, col, row+2, col+2)
    return NULL



## Déplace un pion ou une dame et transforme le pion en dame si nécessaire ##
def movePart(pawnRowPos, pawnColumnPos, cellRowPos, cellColumnPos):
    if cellRowPos != 0 and cellRowPos != gridSize-1:

        grid[cellRowPos][cellColumnPos] = grid[pawnRowPos][pawnColumnPos]
        grid[pawnRowPos][pawnColumnPos] = " "

    # Transformation du pion en dame lors de son déplacement sur la dernière ligne du damier du camp adverse (ici on met juste b ou n en majuscule)
    else:
        grid[cellRowPos][cellColumnPos] = str(grid[pawnRowPos][pawnColumnPos]).upper()
        grid[pawnRowPos][pawnColumnPos] = " "



# Cette fonction effectue un calcul pour trouver les diagonales du damier en prenant les coordonnées de départ et d'arrivées
# On utilise la fonction valeur absolue pour s'abstraire d'avoir un résultat négatif 
def calculateDiagonal(cellRowPos, cellColumnPos, pawnRowPos, pawnColumnPos):

    result_1 = abs(cellRowPos - pawnRowPos) 
    result_2 = abs(cellColumnPos - pawnColumnPos)

    if result_1 == result_2:
        return True
    return False




# Vérifie si on entre les bonnes positions pour déplacer la dame, si le joueur n'entre pas ses propres coordonnées
def isKingMoveValid(cellRowPos, cellColumnPos, pawnRowPos, pawnColumnPos, player):

      # Test si la position pour placer la dame est bien en diagonale
    if grid[pawnRowPos][pawnColumnPos] == str(player).upper() and calculateDiagonal(cellRowPos, cellColumnPos, pawnRowPos, pawnColumnPos) == False:
        print("Vous ne pouvez déplacer votre dame qu'en diagonale.")
        return False

    # Test si la position entrée pour jouer la dame n'est pas la position actuelle du joueur 
    if grid[pawnRowPos][pawnColumnPos] == str(player).upper() and (cellRowPos == pawnRowPos and cellColumnPos == pawnColumnPos):
        print("Attention vous venez d'entrer votre position actuelle. Veuillez jouer sur une autre position.")
        return False



grid[1,2]

## Recherche les potentielles prises en série ##
def searchCaptures(player):
    moves = []
    foundMove = NULL

    for i in range(0, gridSize):
        for j in range(0, gridSize):

            foundMove = isMoveAbove(player, i, j)
            if foundMove != NULL:
                moves.append(foundMove)
    return moves
    



## Force la prise du pion adverse ##
def forceCaptures(player, move:Move):

    print("Une prise est possible avec le pion", player, "se trouvant à la position", move.startMove.rowIndex+1, move.startMove.columnIndex+1)
    input("Appuyez sur entrée pour effectuer la prise.")
    print("\n")

    grid[move.endMove.rowIndex][move.endMove.columnIndex] = grid[move.startMove.rowIndex][move.startMove.columnIndex]
    midPos = move.calculateMidPos()
    grid[midPos.rowIndex][midPos.columnIndex] = " "
    grid[move.startMove.rowIndex][move.startMove.columnIndex] = " "

    # On stocke les coordonnées d'arrivées du pion pour le prochain mouvement
    nextMove = isMoveAbove(player, move.endMove.rowIndex, move.endMove.columnIndex)

    # On test si isMoveAbove() est bien différent de NULL et si c'est le cas on force de nouveau la capture
    # On affiche la grille avant chaque capture pour que ce soit plus clair pour l'utilisateur 
    if  nextMove != NULL:
        displayGrid()
        forceCaptures(player, nextMove)




# En cas de possibilité de prendre 2 pions en simultanés, on demande à l'utilisateur de choisir laquelle il veut effectuer 
def askToChooseCapture(player, moveList:list[Move]):
    print("Plusieurs prises sont possibles avec les pions", player,"qui sont aux positions")

    # On parcours la liste pour afficher les prises possibles au joueur
    for i in range(0, moveList.__len__()):
        print(i+1, ".", moveList[i].startMove.rowIndex+1, moveList[i].startMove.columnIndex+1)

    # On stocke le choix de l'utilisateur qu'on envoie à la fonction forceCaptures()
    chosenCapture = int(input("Quel prise voulez vous effectuer ? (choisissez le numéro associé) :"))
    forceCaptures(player, moveList[chosenCapture-1])




# Gère les tours des joueurs
def playerTurn(player):

    print("C'est le tour du joueur", player, "\n")

    # On parcours la grille à la recherche de prises en série possible
    # Les "return" permettent de gérer le fait qu'un utilisateur ne puisse pas jouer deux fois pendant son tour
    moves = searchCaptures(player) 
    if moves.__len__() == 1:
        forceCaptures(player, moves[0])
        return 
    elif moves.__len__() > 1:
        askToChooseCapture(player, moves)
        return
        
    # On demande la position du pion que l'utilisateur veut choisir pour jouer
    # Dans le while, on re-demande la position du pion si jamais celle-ci est invalide
    pawnRowPos = int(input("Entrez le numéro correspondant à la ligne où se trouve le pion que vous voulez jouer :"))
    pawnColumnPos = int(input("Entrez le numéro de la colonne :"))
    print("\n")

    while not isPawnValid(pawnRowPos-1, pawnColumnPos-1, player):

        pawnRowPos = int(input("Entrez un numéro valide pour la ligne où se trouve le pion que vous voulez jouer :"))
        pawnColumnPos = int(input("Entrez un numéro valide pour la colonne :"))
        print("\n")

    # On demande la position de la case à laquelle l'utilisateur veut jouer
    # Dans le while, on re-demande la position de la case sur laquelle l'utilisateur veut jouer si celle-ci n'est pas valide
    cellRowPos = int(input("Entrez le numéro correspondant à la ligne où se trouve la case sur laquelle vous voulez jouer :"))
    cellColumnPos = int(input("Entrez le numéro de la colonne :"))
    print("\n")

    while not isMoveValid(cellRowPos-1, cellColumnPos-1, pawnRowPos-1, pawnColumnPos-1, player):

        cellRowPos = int(input("Entrez un numéro valide pour la ligne où se trouve la case sur laquelle vous voulez jouer :"))
        cellColumnPos = int(input("Entrez un numéro valide pour la colonne :"))
        print("\n")

    movePart(pawnRowPos-1, pawnColumnPos-1, cellRowPos-1, cellColumnPos-1)




## Gère les tours des joueurs ##
def gameLoop(): 
    while True:
        playerTurn("b")
        playerTurn("n")


## Stop la partie si un des joueurs à gagner, s'il y a égalité ##
def endGame():
    return True



## Appels des fonctions ##
initGrid()
displayGrid()

while endGame():
    playerTurn("b")
    displayGrid()
    endGame()
    playerTurn("n")
    displayGrid()
    endGame()