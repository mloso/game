from __future__ import annotations

from metadata import GAME_FIELD_SIZE, MAX_PLAYERS
from redis_accessor import RedisAccessor
from schemas import Game, Player


def check_game_ended(game: Game) -> bool:
    return (
        sum(1 for row in game.field for cell in row if cell.player is not None)
        == GAME_FIELD_SIZE * GAME_FIELD_SIZE
    )


def end_game(game: Game) -> list[Player]:
    game.is_started = False
    game.is_over = True

    return [
        player
        for player in game.players
        if player.score == max(player.score for player in game.players)
    ]


class GameManager:
    def __init__(self, game_id: str, redis_accessor: RedisAccessor) -> None:
        self.game_id = game_id
        self.redis_accessor = redis_accessor

    async def start(self) -> bool:
        async with self.redis_accessor.access(self.game_id, model=Game) as data:
            game = data[self.game_id]
            if not game or len(game.players) != MAX_PLAYERS:
                return False
            if any(player.color is None for player in game.players):
                return False

            game.is_started = True
            data[self.game_id] = game

        return True

    async def add_player(self, new_player: Player) -> bool:
        async with self.redis_accessor.access(self.game_id, model=Game) as data:
            game = data[self.game_id]

            if not game or game.is_started or game.is_over:
                return False

            if len(game.players) == MAX_PLAYERS:
                return False

            if any(player.connection_id == new_player.connection_id for player in game.players):
                return False

            game.players.append(new_player)
            data[self.game_id] = game

        return True

    async def remove_player(self, connection_id: str) -> bool:
        async with self.redis_accessor.access(self.game_id, model=Game) as data:
            game = data[self.game_id]
            if not game or game.is_started:
                return False
            game.players = [
                player
                for player in data[self.game_id].players
                if player.connection_id != connection_id
            ]
            data[self.game_id] = game

        return True

    async def select_color(self, connection_id: str, color: str | None) -> bool:
        async with self.redis_accessor.access(self.game_id, model=Game) as data:
            game = data[self.game_id]
            if not game or game.is_started or game.is_over:
                return False
            if color not in game.colors:
                return False
            if any(player.color == color for player in game.players):
                return False

            for player in game.players:
                if player.connection_id == connection_id:
                    player.color = color
            data[self.game_id] = game

        return True

    async def make_move(self, connection_id: str, x: int, y: int) -> bool | list[Player]:
        async with self.redis_accessor.access(self.game_id, model=Game) as data:
            game = data[self.game_id]
            if not game or not game.is_started or game.is_over:
                return False
            if not (0 <= x < GAME_FIELD_SIZE) or not (0 <= y < GAME_FIELD_SIZE):
                return False

            found_player = None
            for player in game.players:
                if player.connection_id == connection_id:
                    found_player = player

            if not found_player:
                return False

            if game.field[y][x].player is not None:
                found_player.unsuccessfully_score += 1
                data[self.game_id] = game

                return False

            game.field[y][x].player = found_player
            found_player.score += 1

            if check_game_ended(game):
                data[self.game_id] = game
                return end_game(game)

            data[self.game_id] = game

        return True
