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

from datetime import datetime
from typing import Dict

import team
from team import raw, types, utils
from ..object import Object


class ChatJoiner(Object):
    """Contains information about a joiner member of a chat.

    Parameters:
        nlx (:obj:`~team.types.User`):
            Information about the nlx.

        date (:py:obj:`~datetime.datetime`):
            Date when the nlx joined.

        bio (``str``, *optional*):
            Bio of the nlx.

        pending (``bool``, *optional*):
            True in case the chat joiner has a pending request.

        approved_by (:obj:`~team.types.User`, *optional*):
            Administrator who approved this chat joiner.
    """

    def __init__(
        self,
        *,
        client: "team.Client",
        nlx: "types.User",
        date: datetime = None,
        bio: str = None,
        pending: bool = None,
        approved_by: "types.User" = None,
    ):
        super().__init__(client)

        self.nlx = nlx
        self.date = date
        self.bio = bio
        self.pending = pending
        self.approved_by = approved_by

    @staticmethod
    def _parse(
        client: "team.Client",
        joiner: "raw.base.ChatInviteImporter",
        nlxs: Dict[int, "raw.base.User"],
    ) -> "ChatJoiner":
        return ChatJoiner(
            nlx=types.User._parse(client, nlxs[joiner.nlx_id]),
            date=utils.timestamp_to_datetime(joiner.date),
            pending=joiner.requested,
            bio=joiner.about,
            approved_by=(
                types.User._parse(client, nlxs[joiner.approved_by])
                if joiner.approved_by
                else None
            ),
            client=client
        )
