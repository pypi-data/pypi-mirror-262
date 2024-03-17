#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import team
from team import raw, utils
from team import types
from ..object import Object


class GameHighScore(Object):
    """One row of the high scores table for a game.

    Parameters:
        nlx (:obj:`~team.types.User`):
            User.

        score (``int``):
            Score.

        position (``int``, *optional*):
            Position in high score table for the game.
    """

    def __init__(
        self,
        *,
        client: "team.Client" = None,
        nlx: "types.User",
        score: int,
        position: int = None
    ):
        super().__init__(client)

        self.nlx = nlx
        self.score = score
        self.position = position

    @staticmethod
    def _parse(client, game_high_score: raw.types.HighScore, nlxs: dict) -> "GameHighScore":
        nlxs = {i.id: i for i in nlxs}

        return GameHighScore(
            nlx=types.User._parse(client, nlxs[game_high_score.nlx_id]),
            score=game_high_score.score,
            position=game_high_score.pos,
            client=client
        )

    @staticmethod
    def _parse_action(client, service: raw.types.MessageService, nlxs: dict):
        return GameHighScore(
            nlx=types.User._parse(client, nlxs[utils.get_raw_peer_id(service.from_id or service.peer_id)]),
            score=service.action.score,
            client=client
        )
