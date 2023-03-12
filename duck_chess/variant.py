# This file is part of the python-duck_chess library.
# Copyright (C) 2016-2021 Niklas Fiekas <niklas.fiekas@backscattering.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import annotations

import duck_chess
import copy
import itertools

from typing import Dict, Generic, Hashable, Iterable, Iterator, List, Optional, Type, TypeVar, Union
from duck_chess import scan_reversed

DuckBoardT = TypeVar("DuckBoardT", bound="DuckBoard")

class _DuckBoardState(Generic[DuckBoardT], duck_chess._BoardState[DuckBoardT]):
    def __init__(self, board: DuckBoardT):
        super().__init__(board)
        self.pockets_w = board.pockets[duck_chess.WHITE].copy()
        self.pockets_b = board.pockets[duck_chess.BLACK].copy()
        
    def restore(self, board: DuckBoardT) -> None:
        super().restore(board)
        board.pockets[duck_chess.WHITE] = self.pockets_w
        board.pockets[duck_chess.BLACK] = self.pockets_b

DuckPocketT = TypeVar("DuckPocketT", bound="DuckPocket")

class DuckPocket:
    """Stores the duck in your pocket"""
    
    def __init__(self, duck= "", duck_turn=False) -> None:
        self.reset()
        self.duck = duck
        self.duck_turn = duck_turn
        
    def reset(self) -> None:
        self.duck = ""
        self.duck_turn = False
        
    def remove(self) -> None:
        self.duck = ""
        
    def add(self) -> None:
        self.duck = "z" if self.duck_turn else "Z"
    def count(self) -> int:
        return len(self.duck)
    
    def copy(self: DuckPocketT) -> DuckPocketT:
        copy = DuckPocket()
        copy.duck = self.duck
        copy.duck_turn = self.duck_turn
        return copy

class DuckBoard(duck_chess.Board):
    aliases = ["Duck", "Duck Chess"]
    uci_variant = "duck"
    xboard_variant = "duck"
    starting_fen = "8/8/8/d/8/8/krbnNBRK/ddddNBRQ w - - 0 1"    
    
    tbw_suffix = None
    tbz_suffix = None
    tbw_magic = None
    tbz_magic = None
    
    
    def __init__(self, fen: Optional[str] = starting_fen, duck_chess960: bool = False) -> None:
        self.pockets = [DuckPocket(), DuckPocket()]
        super().__init__(fen, duck_chess960=duck_chess960)
        self.duck_move = False
        self.turn = duck_chess.WHITE
        self.duck_turn = duck_chess.BLACK
        self.push_final = False
        self.move_list = []
            
    def is_variant_win(self) -> bool:
        
        return self.is_stalemate() and self.pseudo_legal_moves.count() == 0
    def is_variant_draw(self) -> bool:
        
        return self.is_insufficient_material() or self.is_fifty_moves()
    def is_variant_loss(self) -> bool:
        
        return self.king(self.turn) is None
    
    def reset_board(self) -> None:
        super().reset_board()
        self.pockets[duck_chess.WHITE].reset()
        self.pockets[duck_chess.BLACK].reset()
        
    def clear_board(self) -> None:
        super().clear_board()
        self.pockets[duck_chess.WHITE].reset()
        self.pockets[duck_chess.BLACK].reset()
    
    def clear_duck(self) -> None:
        #delete all the duck pieces on the board
        duck_loc = self.find_duck(self.turn)
        if duck_loc is None:
            duck_loc = self.find_duck(not self.turn)
        if duck_loc != None:
            self.remove_piece_at(duck_loc)
            self.clear_duck()
    
    def _board_state(self: DuckBoardT) -> _DuckBoardState[DuckBoardT]:
        return _DuckBoardState(self)
    
    def duck_push(self, move: duck_chess.Move) -> None:
        if not self.duck_move:
            raise ValueError(f"Move a piece with push before moving the duck, move was {move}")
        elif str(move).startswith("z@") or str(move).startswith("Z@"):
            self.clear_duck()
            super().push(move)
            self.move_list.append(move)
            self.turn = not self.turn
            duck_loc = self.find_duck(not self.turn)
            self.remove_piece_at(duck_loc)
            self.set_piece_at(duck_loc, duck_chess.Piece.from_symbol("Z" if self.turn else "z"))
            self.pockets[self.turn].remove()
            self.duck_move = False
               
    def f_push(self, move: duck_chess.Move) -> None:

        if str(move).startswith("z@") or str(move).startswith("Z@"):
            raise ValueError(f"Move a piece with push before moving the duck, move was {move}")
        super().push(move)
        self.duck_move = True
            
            
    
        
    def generate_pseudo_legal_moves(self, from_mask: duck_chess.Bitboard = duck_chess.BB_ALL, to_mask: duck_chess.Bitboard = duck_chess.BB_ALL) -> Iterator[duck_chess.Move]:
        our_pieces = self.occupied_co[self.turn]

        # Generate piece moves.
        non_pawns = our_pieces & ~self.pawns & from_mask
        for from_square in scan_reversed(non_pawns):
            moves = self.attacks_mask(from_square) & ~our_pieces & to_mask
            for to_square in scan_reversed(moves):
                yield duck_chess.Move(from_square, to_square)

        # Generate castling moves.
        if from_mask & self.kings:
            yield from self.generate_castling_moves(from_mask, to_mask)

        # The remaining moves are all pawn moves.
        pawns = self.pawns & self.occupied_co[self.turn] & from_mask
        if not pawns:
            return

        # Generate pawn captures.
        capturers = pawns
        for from_square in scan_reversed(capturers):
            targets = (
                duck_chess.BB_PAWN_ATTACKS[self.turn][from_square] &
                self.occupied_co[not self.turn] & to_mask)

            for to_square in scan_reversed(targets):
                if duck_chess.square_rank(to_square) in [0, 7]:
                    yield duck_chess.Move(from_square, to_square, duck_chess.QUEEN)
                    yield duck_chess.Move(from_square, to_square, duck_chess.ROOK)
                    yield duck_chess.Move(from_square, to_square, duck_chess.BISHOP)
                    yield duck_chess.Move(from_square, to_square, duck_chess.KNIGHT)
                else:
                    yield duck_chess.Move(from_square, to_square)

        # Prepare pawn advance generation.
        if self.turn == duck_chess.WHITE:
            single_moves = pawns << 8 & ~self.occupied
            double_moves = single_moves << 8 & ~self.occupied & (duck_chess.BB_RANK_3 | duck_chess.BB_RANK_4)
        else:
            single_moves = pawns >> 8 & ~self.occupied
            double_moves = single_moves >> 8 & ~self.occupied & (duck_chess.BB_RANK_6 | duck_chess.BB_RANK_5)

        single_moves &= to_mask
        double_moves &= to_mask

        # Generate single pawn moves.
        for to_square in scan_reversed(single_moves):
            from_square = to_square + (8 if self.turn == duck_chess.BLACK else -8)

            if duck_chess.square_rank(to_square) in [0, 7]:
                yield duck_chess.Move(from_square, to_square, duck_chess.QUEEN)
                yield duck_chess.Move(from_square, to_square, duck_chess.ROOK)
                yield duck_chess.Move(from_square, to_square, duck_chess.BISHOP)
                yield duck_chess.Move(from_square, to_square, duck_chess.KNIGHT)
            else:
                yield duck_chess.Move(from_square, to_square)

        # Generate double pawn moves.
        for to_square in scan_reversed(double_moves):
            from_square = to_square + (16 if self.turn == duck_chess.BLACK else -16)
            yield duck_chess.Move(from_square, to_square)

        # Generate en passant captures.
        if self.ep_square:
            yield from self.generate_pseudo_legal_ep(from_mask, to_mask)
    
    def generate_duck_moves(self, from_mask: duck_chess.Bitboard = duck_chess.BB_ALL, to_mask: duck_chess.Bitboard = duck_chess.BB_ALL) -> Iterator[duck_chess.Move]:
        """Generates duck moves."""
        # Generate duck moves.
        pt = duck_chess.DUCK
        for to_square in duck_chess.scan_forward(to_mask & ~self.occupied & (~duck_chess.BB_BACKRANKS if pt == duck_chess.PAWN else duck_chess.BB_ALL)):
            yield duck_chess.Move(to_square, to_square, drop=pt)



VARIANTS: List[Type[duck_chess.Board]] = [
    duck_chess.Board,
    DuckBoard,
]


def find_variant(name: str) -> Type[duck_chess.Board]:
    """
    Looks for a variant board class by variant name. Supports many common
    aliases.
    """
    for variant in VARIANTS:
        if any(alias.lower() == name.lower() for alias in variant.aliases):
            return variant
    raise ValueError(f"unsupported variant: {name}")
