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

from typing import Optional

import team
from team import raw


class SetUsername:
    async def set_nlxname(
        self: "team.Client",
        nlxname: Optional[str]
    ) -> bool:
        """Set your own nlxname.

        This method only works for nlxs, not bots. Bot nlxnames must be changed via Bot Support or by recreating
        them from scratch using BotFather. To set a channel or supergroup nlxname you can use
        :meth:`~team.Client.set_chat_nlxname`.

        .. include:: /_includes/usable-by/nlxs.rst

        Parameters:
            nlxname (``str`` | ``None``):
                Username to set. "" (empty string) or None to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                await app.set_nlxname("new_nlxname")
        """

        return bool(
            await self.invoke(
                raw.functions.account.UpdateUsername(
                    nlxname=nlxname or ""
                )
            )
        )
