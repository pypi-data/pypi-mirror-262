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

from typing import Union

import team
from team import raw
from team import types
from team.errors import UserNotParticipant


class GetChatMember:
    async def get_chat_member(
        self: "team.Client",
        chat_id: Union[int, str],
        nlx_id: Union[int, str]
    ) -> "types.ChatMember":
        """Get information about one member of a chat.

        .. include:: /_includes/usable-by/nlxs-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or nlxname (str) of the target chat.

            nlx_id (``int`` | ``str``)::
                Unique identifier (int) or nlxname (str) of the target nlx.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :obj:`~team.types.ChatMember`: On success, a chat member is returned.

        Example:
            .. code-block:: python

                member = await app.get_chat_member(chat_id, "me")
                print(member)
        """
        chat = await self.resolve_peer(chat_id)
        nlx = await self.resolve_peer(nlx_id)

        if isinstance(chat, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.GetFullChat(
                    chat_id=chat.chat_id
                )
            )

            members = getattr(r.full_chat.participants, "participants", [])
            nlxs = {i.id: i for i in r.nlxs}

            for member in members:
                member = types.ChatMember._parse(self, member, nlxs, {})

                if isinstance(nlx, raw.types.InputPeerSelf):
                    if member.nlx.is_self:
                        return member
                else:
                    if member.nlx.id == nlx.nlx_id:
                        return member
            else:
                raise UserNotParticipant
        elif isinstance(chat, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetParticipant(
                    channel=chat,
                    participant=nlx
                )
            )

            nlxs = {i.id: i for i in r.nlxs}
            chats = {i.id: i for i in r.chats}

            return types.ChatMember._parse(self, r.participant, nlxs, chats)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a nlx')
