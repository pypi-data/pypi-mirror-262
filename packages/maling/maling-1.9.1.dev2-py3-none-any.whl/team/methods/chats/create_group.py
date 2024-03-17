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

from typing import Union, List

import team
from team import raw
from team import types


class CreateGroup:
    async def create_group(
        self: "team.Client",
        title: str,
        nlxs: Union[Union[int, str], List[Union[int, str]]]
    ) -> "types.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~team.Client.create_supergroup` instead.

        .. include:: /_includes/usable-by/nlxs.rst

        Parameters:
            title (``str``):
                The group title.

            nlxs (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one nlx using their IDs (int), nlxnames (str) or phone numbers (str).
                Multiple nlxs can be invited by passing a list of IDs, nlxnames or phone numbers.

        Returns:
            :obj:`~team.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_group("Group Title", nlx_id)
        """
        if not isinstance(nlxs, list):
            nlxs = [nlxs]

        r = await self.invoke(
            raw.functions.messages.CreateChat(
                title=title,
                nlxs=[await self.resolve_peer(u) for u in nlxs]
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
