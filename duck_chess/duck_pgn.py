"""

[Variant "FFA"]
[RuleVariants "DuckChess EnPassant Play4Mate Stalemate=win"]
[TimeControl "5 | 4"]
[StartFen4 "2PC"]
[CurrentMove "9"]

1. g5-g7Θ-g9 .. h10-h8Θg9-h10
2. Nj4-i6Θh10-i9 .. h8xg7Θi9-d9
3. Qg4xg7Θd9-f9 .. i10-i8Θf9-d8
4. Qg7xg10Θd8-e7+ .. Ne11-f9Θe7-g4
5. Qg10xKh11#

Why is everything shifted so much? No clue

everything is plus 3

a = d2c3, b = d2- y = d, z = xc3, u = dxc3 last_duck = Z@d8
d2-dxc3Θc7-d8

A = D
B = E
C = F
D = G
E = H
F = I
G = J
H = K

1 = 4 ... and so on
"""

header = """
[Variant "Duck Chess"]
[RuleVariants "DuckChess EnPassant Play4Mate Stalemate=win"]
"""

ran_words = ["strawberry", "boy", "monkey", "glacier","banana", "chicken", "potato", "borgo", "heehaw", "cat", "dog", "mouse", "rat", 
             "penguin", "pancakes", "waffles", "eggs", "toast", "cheese", "milk", "water", "juice", "coffee", "tea", "soda", 
             "beer", "wine", "whiskey", "vodka", "rum", "gin", "scotch", "brandy", "cognac", "champagne", "sake", "rice", "noodles", 
             "spaghetti", "pizza", "hamburger", "hotdog", "sandwich", "taco", "burrito", "sushi", "ramen", "chips", "doritos", "fritos", 
             "tortilla", "chips", "large", "hadron", "collider", "whiteboard", "orange", "lamp", "table", "chair", "desk", "couch",
             "movie", "book", "paper", "pen", "pencil", "eraser", "ruler", "notebook", "computer", "laptop", "phone", "tablet",
             "enormous", "tiny", "small", "big", "giant", "tiny", "large", "huge", "gigantic", "gargantuan", "colossal", "massive",
             "sad", "happy", "angry", "mad", "excited", "bored", "tired", "sleepy", "hungry", "thirsty", "dehydrated", "sick",
             "day", "night", "morning", "afternoon", "evening", "dawn", "dusk", "sunrise", "sunset", "spring", "summer", "fall",
             "christmas", "easter", "halloween", "thanksgiving", "new years", "birthday", "anniversary", "wedding", "funeral"]

import random


def make_pgn(move_list):
    shifted_move_list = []
    temp_list = []
    for i in move_list:
        for j in i:
            if j == "Θ":
                pass
            elif j == "a":
                j = "d"
            elif j == "b":
                j = "e"
            elif j == "c":
                j = "f"
            elif j == "d":
                j = "g"
            elif j == "e":
                j = "h"
            elif j == "f":
                j = "i"
            elif j == "g":
                j = "j"
            elif j == "h":
                j = "k"
            try:
                x = int(j)
                j = str(x + 3)
            except ValueError:
                pass
            temp_list.extend(j)
        shifted_move_list.append(temp_list)
        temp_list = []
    k = 1
    parsed = []
    for i in range(len(shifted_move_list)):
        j = i+1
        first = "".join(shifted_move_list[i-1])
        second = "".join(shifted_move_list[i])

        if j % 2 == 0:
            parsed.append(f"{k}. {first} .. {second}")
            k+=1
        elif i == len(shifted_move_list)-1:
            parsed.append(f"{k}. {second}")
            
    word_1 = random.choice(ran_words)
    word_2 = random.choice(ran_words)
    word_3 = random.choice(ran_words)
    num = random.randint(0, 100000)

    string = f"{word_1}_{word_2}_{word_3}_{num}"
    with open(f"pgn_games\{string}.pgn.txt", "w", encoding="utf-8") as f:
        f.write("""
[StartFen4 "2PC"]
[Variant "FFA"]
[RuleVariants "DuckChess EnPassant Play4Mate Stalemate=win"]
                """)
        f.write("\n")
        for i in parsed:
            q = " ".join(i)
            q = q.replace(" ","").replace(".",". ").replace(". ."," ..")
            
            f.write("\n")
            f.write(q)