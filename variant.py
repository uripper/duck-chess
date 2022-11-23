# This file is part of the python-chess library.
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

import chess
import copy
import itertools

from typing import Dict, Generic, Hashable, Iterable, Iterator, List, Optional, Type, TypeVar, Union
from chess import scan_reversed

DuckBoardT = TypeVar("DuckBoardT", bound="DuckBoard")

class _DuckBoardState(Generic[DuckBoardT], chess._BoardState[DuckBoardT]):
    def __init__(self, board: DuckBoardT):
        super().__init__(board)
        self.pockets_w = board.pockets[chess.WHITE].copy()
        self.pockets_b = board.pockets[chess.BLACK].copy()
        
    def restore(self, board: DuckBoardT) -> None:
        super().restore(board)
        board.pockets[chess.WHITE] = self.pockets_w
        board.pockets[chess.BLACK] = self.pockets_b

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
        if self.duck_turn:
            self.duck = "d"
        else:
            self.duck = "D"
    def count(self) -> int:
        return len(self.duck)
    
    def copy(self: DuckPocketT) -> DuckPocketT:
        copy = DuckPocket()
        copy.duck = self.duck
        copy.duck_turn = self.duck_turn
        return copy

class DuckBoard(chess.Board):
    aliases = ["Duck", "Duck Chess"]
    uci_variant = "duck"
    xboard_variant = "duck"
    starting_fen = "8/8/8/d/8/8/krbnNBRK/ddddNBRQ w - - 0 1"    
    
    tbw_suffix = None
    tbz_suffix = None
    tbw_magic = None
    tbz_magic = None
    
    
    def __init__(self, fen: Optional[str] = starting_fen, chess960: bool = False) -> None:
        self.pockets = [DuckPocket(), DuckPocket()]
        super().__init__(fen, chess960=chess960)
        self.duck_move = False
        self.turn = chess.WHITE
        self.duck_turn = chess.BLACK
        self.push_final = False
        self.move_list = []
            
    def is_variant_win(self) -> bool:
        
        return self.is_stalemate() and self.pseudo_legal_moves.count() == 0
    def is_variant_draw(self) -> bool:
        
        return self.is_insufficient_material() or self.is_fifty_moves()
    def is_variant_loss(self) -> bool:
        
        return self.king(self.turn) == None
    
    def reset_board(self) -> None:
        super().reset_board()
        self.pockets[chess.WHITE].reset()
        self.pockets[chess.BLACK].reset()
        
    def clear_board(self) -> None:
        super().clear_board()
        self.pockets[chess.WHITE].reset()
        self.pockets[chess.BLACK].reset()
    
    def clear_duck(self) -> None:
        #delete all the duck pieces on the board
        duck_loc = self.find_duck(self.turn)
        if duck_loc == None:
            duck_loc = self.find_duck(not self.turn)
        if duck_loc != None:
            self.remove_piece_at(duck_loc)
            self.clear_duck()
        else:
            pass
    
    def _board_state(self: DuckBoardT) -> _DuckBoardState[DuckBoardT]:
        return _DuckBoardState(self)
    
    def duck_push(self, move: chess.Move) -> None:
        if not self.duck_move:
            raise ValueError(f"Move a piece with push before moving the duck, move was {move}")
        elif str(move).startswith("d") or str(move).startswith("D"):
            self.clear_duck()
            super().push(move)
            self.move_list.append(move)
            self.turn = not self.turn
            duck_loc = self.find_duck(not self.turn)
            self.remove_piece_at(duck_loc)
            self.set_piece_at(duck_loc, chess.Piece.from_symbol("D" if self.turn else "d"))
            self.pockets[self.turn].remove()
            self.duck_move = False
               
    def f_push(self, move: chess.Move) -> None:

        if str(move).startswith("d@") or str(move).startswith("D@"):
            raise ValueError(f"Move a piece with push before moving the duck, move was {move}")
        else:
            super().push(move)
            self.duck_move = True
            
            
    
        
    def generate_pseudo_legal_moves(self, from_mask: chess.Bitboard = chess.BB_ALL, to_mask: chess.Bitboard = chess.BB_ALL) -> Iterator[chess.Move]:
        our_pieces = self.occupied_co[self.turn]

        # Generate piece moves.
        non_pawns = our_pieces & ~self.pawns & from_mask
        for from_square in scan_reversed(non_pawns):
            moves = self.attacks_mask(from_square) & ~our_pieces & to_mask
            for to_square in scan_reversed(moves):
                yield chess.Move(from_square, to_square)

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
                chess.BB_PAWN_ATTACKS[self.turn][from_square] &
                self.occupied_co[not self.turn] & to_mask)

            for to_square in scan_reversed(targets):
                if chess.square_rank(to_square) in [0, 7]:
                    yield chess.Move(from_square, to_square, chess.QUEEN)
                    yield chess.Move(from_square, to_square, chess.ROOK)
                    yield chess.Move(from_square, to_square, chess.BISHOP)
                    yield chess.Move(from_square, to_square, chess.KNIGHT)
                else:
                    yield chess.Move(from_square, to_square)

        # Prepare pawn advance generation.
        if self.turn == chess.WHITE:
            single_moves = pawns << 8 & ~self.occupied
            double_moves = single_moves << 8 & ~self.occupied & (chess.BB_RANK_3 | chess.BB_RANK_4)
        else:
            single_moves = pawns >> 8 & ~self.occupied
            double_moves = single_moves >> 8 & ~self.occupied & (chess.BB_RANK_6 | chess.BB_RANK_5)

        single_moves &= to_mask
        double_moves &= to_mask

        # Generate single pawn moves.
        for to_square in scan_reversed(single_moves):
            from_square = to_square + (8 if self.turn == chess.BLACK else -8)

            if chess.square_rank(to_square) in [0, 7]:
                yield chess.Move(from_square, to_square, chess.QUEEN)
                yield chess.Move(from_square, to_square, chess.ROOK)
                yield chess.Move(from_square, to_square, chess.BISHOP)
                yield chess.Move(from_square, to_square, chess.KNIGHT)
            else:
                yield chess.Move(from_square, to_square)

        # Generate double pawn moves.
        for to_square in scan_reversed(double_moves):
            from_square = to_square + (16 if self.turn == chess.BLACK else -16)
            yield chess.Move(from_square, to_square)

        # Generate en passant captures.
        if self.ep_square:
            yield from self.generate_pseudo_legal_ep(from_mask, to_mask)
    
    def generate_duck_moves(self, from_mask: chess.Bitboard = chess.BB_ALL, to_mask: chess.Bitboard = chess.BB_ALL) -> Iterator[chess.Move]:
        """Generates duck moves."""
        # Generate duck moves.
        pt = chess.DUCK
        for to_square in chess.scan_forward(to_mask & ~self.occupied & (~chess.BB_BACKRANKS if pt == chess.PAWN else chess.BB_ALL)):
            yield chess.Move(to_square, to_square, drop=pt)



VARIANTS: List[Type[chess.Board]] = [
    chess.Board,
    DuckBoard,
]


def find_variant(name: str) -> Type[chess.Board]:
    """
    Looks for a variant board class by variant name. Supports many common
    aliases.
    """
    for variant in VARIANTS:
        if any(alias.lower() == name.lower() for alias in variant.aliases):
            return variant
    raise ValueError(f"unsupported variant: {name}")
