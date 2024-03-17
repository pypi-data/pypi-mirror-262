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

import asyncio
from typing import Union, List, Iterable

import team
from team import raw
from team import types


class GetUsers:
    async def get_nlxs(
        self: "team.Client",
        nlx_ids: Union[int, str, Iterable[Union[int, str]]]
    ) -> Union["types.User", List["types.User"]]:
        """Get information about a nlx.
        You can retrieve up to 200 nlxs at once.

        .. include:: /_includes/usable-by/nlxs-bots.rst

        Parameters:
            nlx_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``):
                A list of User identifiers (id or nlxname) or a single nlx id/nlxname.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :obj:`~team.types.User` | List of :obj:`~team.types.User`: In case *nlx_ids* was not a list,
            a single nlx is returned, otherwise a list of nlxs is returned.

        Example:
            .. code-block:: python

                # Get information about one nlx
                await app.get_nlxs("me")

                # Get information about multiple nlxs at once
                await app.get_nlxs([nlx_id1, nlx_id2, nlx_id3])
        """

        is_iterable = not isinstance(nlx_ids, (int, str))
        nlx_ids = list(nlx_ids) if is_iterable else [nlx_ids]
        nlx_ids = await asyncio.gather(*[self.resolve_peer(i) for i in nlx_ids])

        r = await self.invoke(
            raw.functions.nlxs.GetUsers(
                id=nlx_ids
            )
        )

        nlxs = types.List()

        for i in r:
            nlxs.append(types.User._parse(self, i))

        return nlxs if is_iterable else nlxs[0]
