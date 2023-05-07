# /home/meziane/anaconda3/bin/conda

import random
import numpy as np

DES = [
    ['L', 'E', 'N', 'U', 'Y', 'G'],
    ['E', 'L', 'U', 'P', 'S', 'T'],
    ['Z', 'D', 'V', 'N', 'E', 'A'],
    ['S', 'D', 'T', 'N', 'O', 'E'],
    ['A', 'M', 'O', 'R', 'I', 'S'],
    ['F', 'X', 'R', 'A', 'O', 'I'],
    ['M', 'O', 'Q', 'A', 'B', 'J'],
    ['F', 'S', 'H', 'E', 'E', 'I'],
    ['H', 'R', 'S', 'N', 'E', 'I'],
    ['E', 'T', 'N', 'K', 'O', 'U'],
    ['T', 'A', 'R', 'I', 'L', 'B'],
    ['T', 'I', 'E', 'A', 'O', 'A'],
    ['A', 'C', 'E', 'P', 'D', 'M'],
    ['R', 'L', 'A', 'S', 'E', 'C'],
    ['U', 'L', 'I', 'W', 'E', 'R'],
    ['V', 'G', 'T', 'N', 'I', 'E']]

random.shuffle(DES)
board = np.array([random.choice(de) for de in DES]).reshape((4, 4))
for i in board:
    print(i)

alpha = {'A': 0,
         'B': 1,
         'C': 2,
         'D': 3,
         'E': 4,
         'F': 5,
         'G': 6,
         'H': 7,
         'I': 8,
         'J': 9,
         'K': 10,
         'L': 11,
         'M': 12,
         'N': 13,
         'O': 14,
         'P': 15,
         'Q': 16,
         'R': 17,
         'S': 18,
         'T': 19,
         'U': 20,
         'V': 21,
         'W': 22,
         'X': 23,
         'Y': 24,
         'Z': 25}

alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
digit_board = [[alpha[board[row, i]] for i in range(len(board[row]))] for row in range(len(board))]
for i in digit_board:
    print(i)

class digit_tree():
    def __init__(self, lettre_id, parent=None):
        self.lettre_id = lettre_id
        self.parent = parent
        self.child = []
        self.word = False



class dict_object():
    def __init__(self, lettre, parent=None):
        self.lettre = lettre
        self.word = False
        self.child = []
        self.parent = parent

    def get_word(self):
        word = ''
        noeud = self
        while noeud.parent:
            word = noeud.lettre + word
            noeud = noeud.parent

        return word


def build_tree(input_file):
    dictionnaire = dict_object('')
    with open(input_file, 'r') as words:
        for word in words:
            page = dictionnaire
            # print(word, end='')
            for i, lettre in enumerate(word[:-1]):
                # if lettre == "\n":
                #   break

                if not lettre in [p.lettre for p in page.child]:
                    page.child.append(dict_object(lettre, parent=page))
                    # print('ajoute', lettre)

                for p in page.child:
                    # print(p.lettre)
                    if lettre == p.lettre:
                        # print('lettre found')
                        page = p
                        if word[i + 1] == "\n":
                            p.word = True
                            # print('word found')
                        break
    return dictionnaire

def build_digit_tree(input_file):
    tree = digit_tree(None)
    with open(input_file, 'r') as words:
        for word in words:
            branch = tree
            for i, lettre in enumerate(word[:-1]):
                lettre_id = alpha[lettre]
                if not lettre_id in [b.lettre_id for b in branch.child]:
                    branch.child.append(digit_tree(lettre_id, parent=branch))

                for b in branch.child:
                    if lettre_id == b.lettre_id:
                        branch = b
                        if word[i+1]=='\n':
                            b.word = True

                        break

    return tree


def show_tree(noeud, indent=''):
    print(indent + noeud.lettre, end='')
    if noeud.word:
        print(' -> ', noeud.get_word())
    else:
        print('')

    for n in noeud.child:
        show_tree(n, indent=indent + '  ')

def show_digit_tree(noeud, indent=''):
    print(indent + str(noeud.lettre_id), end='')
    if noeud.word:
        print(' -> ', noeud.get_word())
    else:
        print('')

    for n in noeud.child:
        show_digit_tree(n, indent=indent + '  ')

#dictionnaire = build_tree('words.txt')
dictionnaire = build_digit_tree('words.txt')
show_digit_tree(dictionnaire)

# à voir
# arbre de patricia
# arbre préfix   suffix

def finder(key, tree):
    for branche in tree.child:
        if key == branche.lettre:
            return branche
    return False

directions = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]

def parser(y, x, board, tree):

    #tree = finder(board[(y, x)], tree)
    #print(tree.lettre)
    for d in directions:
        if 0<=y+d[0]<=3 and 0<=x+d[1]<=3 and not board[y+d[0],x+d[1]] in passed:
            y+=d[0]
            x+=d[1]
            lettre = board[y][x]
            #print(lettre)

            #print([branche.lettre for branche in tree.child])
            if lettre in [branche.lettre for branche in tree.child]:
                test = finder(lettre, tree) #board[(y, x)]
                if test != False:
                    passed.append(lettre)
                    if test.word:
                        print(test.get_word())
                    #print(len(passed))
                    #print(board, x, y)
                    parser(y, x, board, test)
                else:
                    passed.pop()

for y in range(4):
    for x in range(4):
        print('-', board[y,x])
        passed = []
        #parser(y, x, board, dictionnaire)
