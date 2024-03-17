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

from typing import Union, Optional

import team
from team import raw


class SetChatUsername:
    async def set_chat_nlxname(
        self: "team.Client",
        chat_id: Union[int, str],
        nlxname: Optional[str]
    ) -> bool:
        """Set a channel or a supergroup nlxname.

        To set your own nlxname (for nlxs only, not bots) you can use :meth:`~team.Client.set_nlxname`.

        .. include:: /_includes/usable-by/nlxs.rst

        Parameters:
            chat_id (``int`` | ``str``)
                Unique identifier (int) or nlxname (str) of the target chat.

            nlxname (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the nlxname.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case a chat id belongs to a nlx or chat.

        Example:
            .. code-block:: python

                await app.set_chat_nlxname(chat_id, "new_nlxname")
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return bool(
                await self.invoke(
                    raw.functions.channels.UpdateUsername(
                        channel=peer,
                        nlxname=nlxname or ""
                    )
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a nlx or chat')
