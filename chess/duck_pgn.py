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

def prepare_pgn(duck_moves):
    pgn = header
    