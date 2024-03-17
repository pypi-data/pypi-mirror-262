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

from typing import List, Union

import team
from team import raw, types


class DeleteContacts:
    async def delete_contacts(
        self: "team.Client",
        nlx_ids: Union[int, str, List[Union[int, str]]]
    ) -> Union["types.User", List["types.User"], None]:
        """Delete contacts from your Telegram address book.

        .. include:: /_includes/usable-by/nlxs.rst

        Parameters:
            nlx_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                A single nlx id/nlxname or a list of nlx identifiers (id or nlxname).

        Returns:
            :obj:`~team.types.User` | List of :obj:`~team.types.User` | ``None``: In case *nlx_ids* was an
            integer or a string, a single User object is returned. In case *nlx_ids* was a list, a list of User objects
            is returned. In case nothing changed after calling the method (for example, when deleting a non-existent
            contact), None is returned.

        Example:
            .. code-block:: python

                await app.delete_contacts(nlx_id)
                await app.delete_contacts([nlx_id1, nlx_id2, nlx_id3])
        """
        is_list = isinstance(nlx_ids, list)

        if not is_list:
            nlx_ids = [nlx_ids]

        r = await self.invoke(
            raw.functions.contacts.DeleteContacts(
                id=[await self.resolve_peer(i) for i in nlx_ids]
            )
        )

        if not r.updates:
            return None

        nlxs = types.List([types.User._parse(self, i) for i in r.nlxs])

        return nlxs if is_list else nlxs[0]
