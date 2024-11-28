"""
Some example strategies for people who want to create a custom, homemade bot.

With these classes, bot makers will not have to implement the UCI or XBoard interfaces themselves.
"""

from __future__ import annotations
import chess
from chess.engine import PlayResult, Limit
import random
from engine_wrapper import MinimalEngine, MOVE
from typing import Any
import logging


# Use this logger variable to print messages to the console or log files.
# logger.info("message") will always print "message" to the console or log file.
# logger.debug("message") will only print "message" if verbose logging is enabled.
logger = logging.getLogger(__name__)


class ExampleEngine(MinimalEngine):
    """An example engine that all homemade engines inherit."""

    pass


# Strategy names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    """Get a random move."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose a random move."""
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    """Get the first move when sorted by san representation."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose the first move alphabetically."""
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Get the first move when sorted by uci representation."""

    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        """Choose the first move alphabetically in uci representation."""
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class ComboEngine(ExampleEngine):
    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def search(self, board: chess.Board, time_limit: Limit, ponder: bool, draw_offered: bool, root_moves: MOVE) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        if isinstance(time_limit.time, int):
            my_time = time_limit.time
            my_inc = 0
        elif board.turn == chess.WHITE:
            my_time = time_limit.white_clock if isinstance(time_limit.white_clock, int) else 0
            my_inc = time_limit.white_inc if isinstance(time_limit.white_inc, int) else 0
        else:
            my_time = time_limit.black_clock if isinstance(time_limit.black_clock, int) else 0
            my_inc = time_limit.black_inc if isinstance(time_limit.black_inc, int) else 0

        possible_moves = root_moves if isinstance(root_moves, list) else list(board.legal_moves)

        if my_time / 60 + my_inc > 10:
            # Choose a random move.
            move = random.choice(possible_moves)
        else:
            # Choose the first move alphabetically in uci representation.
            possible_moves.sort(key=str)
            move = possible_moves[0]
        return PlayResult(move, None, draw_offered=draw_offered)


# taken from https://gist.github.com/niklasf/933053f76a418cfe4d52f2f1af997c6f
# https://github.com/flok99/feeks/blob/master/psq.py

# fmt: off
PSQT = {
    chess.PAWN: [
         0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 21,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-31,-31, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 11,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ],
    chess.ROOK: [
          0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
          1, 30, 10,  0,  0, 10, 30,  2
    ]
}
# fmt: on


def _piece_value(color, piece_type, square):
    return PSQT[piece_type][
        square if color == chess.BLACK else chess.square_mirror(square)
    ]


def _move_value(board, move):
    piece_type = board.piece_type_at(move.from_square)
    return _piece_value(board.turn, piece_type, move.to_square) - _piece_value(
        board.turn, piece_type, move.from_square
    )


def _pawn_attacks(board, move):
    pawn_attacks = board.pieces(chess.PAWN, not board.turn) & board.attacks(
        move.to_square
    )
    return 6 if not bool(pawn_attacks) else (5 - board.piece_type_at(move.from_square))


def _score_move(board, move):
    score = (
        ((move.promotion or 0) << 26)
        + (board.is_capture(move) << 25)
        + (_pawn_attacks(board, move) << 22)
        + (512 + (_move_value(board, move) << 12))
        + (move.to_square << 6)
        + move.from_square
    )
    return score

RANDOM = False
DEBUG = False
MAX_DEPTH = -1

INF = int(10**32)
NEG_INF = -int(10**32)


def _score_board(board):
    return max((_score_move(board, m) for m in board.legal_moves), default=NEG_INF)


class CompressorEngine(ExampleEngine):
    move_counter = 0

    """
    Get a move using multiple different methods.

    This engine demonstrates how one can use `time_limit`, `draw_offered`, and `root_moves`.
    """

    def _ab_search(self, board, MAX_DEPTH=MAX_DEPTH):

        def _recur(depth, board, maximize, alpha=NEG_INF, beta=INF):
            if depth <= 0:
                return None, (
                    NEG_INF
                    if len(list(board.legal_moves)) == 0
                    else _score_board(board)
                )

            if maximize:
                legal_moves = list(board.legal_moves)
                if len(legal_moves) == 0:
                    return None, NEG_INF
                if DEBUG:
                    print(f"NUM LEGAL MOVES: {len(legal_moves)}")
                best_move, best_val = legal_moves[0], NEG_INF
                for m in legal_moves:
                    CompressorEngine.move_counter += 1
                    board.push(m)
                    _, s = _recur(depth - 1, board, False, alpha=alpha, beta=beta)
                    board.pop()
                    if s > best_val:
                        best_val = s
                        best_move = m
                    if alpha < best_val:
                        if DEBUG:
                            print(
                                f"#################### INCREASING ALPHA {alpha} -> {best_val}"
                            )
                    alpha = max(best_val, alpha)
                    if beta < s:
                        if DEBUG:
                            print("########## MAX BREAK")
                        break
                return best_move, best_val
            else:
                legal_moves = list(board.legal_moves)
                if len(legal_moves) == 0:
                    return None, NEG_INF
                if DEBUG:
                    print(f"NUM LEGAL MOVES: {len(legal_moves)}")
                best_move, best_val = legal_moves[0], INF
                for m in legal_moves:
                    CompressorEngine.move_counter += 1
                    board.push(m)
                    _, s = _recur(depth - 1, board, True, alpha=alpha, beta=beta)
                    board.pop()
                    if s < best_val:
                        best_val = s
                        best_move = m
                    if best_val < beta:
                        if DEBUG:
                            print(
                                f"#################### REDUCING BETA {beta} -> {best_val}"
                            )
                    beta = min(best_val, beta)
                    if s <= alpha:
                        if DEBUG:
                            print("########## MIN BREAK")
                        break
                return best_move, best_val

        return _recur(MAX_DEPTH, board, True)[0]

    def search(
        self,
        board: chess.Board,
        time_limit: Limit,
        ponder: bool,
        draw_offered: bool,
        root_moves: MOVE,
    ) -> PlayResult:
        """
        Choose a move using multiple different methods.

        :param board: The current position.
        :param time_limit: Conditions for how long the engine can search (e.g. we have 10 seconds and search up to depth 10).
        :param ponder: Whether the engine can ponder after playing a move.
        :param draw_offered: Whether the bot was offered a draw.
        :param root_moves: If it is a list, the engine should only play a move that is in `root_moves`.
        :return: The move to play.
        """
        # sorted_moves = sorted(list(board.legal_moves), key = lambda m: score(board, m), reverse=True)
        if RANDOM:
            return PlayResult(
                random.choice(list(board.legal_moves)), None, draw_offered=draw_offered
            )
        if MAX_DEPTH == -1:
            best_move = sorted(
                list(board.legal_moves),
                key=lambda move: _score_move(board, move),
                reverse=True,
            )[0]
        else:
            best_move = self._ab_search(board)
        if DEBUG:
            print(best_move)
        print(f"NUM MOVES EVALUATED: {CompressorEngine.move_counter}")
        CompressorEngine.move_counter = 0
        return PlayResult(best_move, None, draw_offered=draw_offered)
