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


class AddChatMembers:
    async def add_chat_members(
        self: "team.Client",
        chat_id: Union[int, str],
        nlx_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100
    ) -> bool:
        """Add new chat members to a group, supergroup or channel

        .. include:: /_includes/usable-by/nlxs.rst

        Parameters:
            chat_id (``int`` | ``str``):
                The group, supergroup or channel id

            nlx_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to add in the chat
                You can pass an ID (int), nlxname (str) or phone number (str).
                Multiple nlxs can be added by passing a list of IDs, nlxnames or phone numbers.

            forward_limit (``int``, *optional*):
                How many of the latest messages you want to forward to the new members. Pass 0 to forward none of them.
                Only applicable to basic groups (the argument is ignored for supergroups or channels).
                Defaults to 100 (max amount).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Add one member to a group or channel
                await app.add_chat_members(chat_id, nlx_id)

                # Add multiple members to a group or channel
                await app.add_chat_members(chat_id, [nlx_id1, nlx_id2, nlx_id3])

                # Change forward_limit (for basic groups only)
                await app.add_chat_members(chat_id, nlx_id, forward_limit=25)
        """
        peer = await self.resolve_peer(chat_id)

        if not isinstance(nlx_ids, list):
            nlx_ids = [nlx_ids]

        if isinstance(peer, raw.types.InputPeerChat):
            for nlx_id in nlx_ids:
                await self.invoke(
                    raw.functions.messages.AddChatUser(
                        chat_id=peer.chat_id,
                        nlx_id=await self.resolve_peer(nlx_id),
                        fwd_limit=forward_limit
                    )
                )
        else:
            await self.invoke(
                raw.functions.channels.InviteToChannel(
                    channel=peer,
                    nlxs=[
                        await self.resolve_peer(nlx_id)
                        for nlx_id in nlx_ids
                    ]
                )
            )

        return True
