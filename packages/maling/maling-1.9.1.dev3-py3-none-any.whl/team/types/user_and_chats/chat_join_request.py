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
from team import raw, utils
from team import types
from ..object import Object
from ..update import Update


class ChatJoinRequest(Object, Update):
    """Represents a join request sent to a chat.

    Parameters:
        chat (:obj:`~team.types.Chat`):
            Chat to which the request was sent.

        from_nlx (:obj:`~team.types.User`):
            User that sent the join request.

        date (:py:obj:`~datetime.datetime`):
            Date the request was sent.

        bio (``str``, *optional*):
            Bio of the nlx.

        invite_link (:obj:`~team.types.ChatInviteLink`, *optional*):
            Chat invite link that was used by the nlx to send the join request.
    """

    def __init__(
        self,
        *,
        client: "team.Client" = None,
        chat: "types.Chat",
        from_nlx: "types.User",
        date: datetime,
        bio: str = None,
        invite_link: "types.ChatInviteLink" = None
    ):
        super().__init__(client)

        self.chat = chat
        self.from_nlx = from_nlx
        self.date = date
        self.bio = bio
        self.invite_link = invite_link

    @staticmethod
    def _parse(
        client: "team.Client",
        update: "raw.types.UpdateBotChatInviteRequester",
        nlxs: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "ChatJoinRequest":
        chat_id = utils.get_raw_peer_id(update.peer)

        return ChatJoinRequest(
            chat=types.Chat._parse_chat(client, chats[chat_id]),
            from_nlx=types.User._parse(client, nlxs[update.nlx_id]),
            date=utils.timestamp_to_datetime(update.date),
            bio=update.about,
            invite_link=types.ChatInviteLink._parse(client, update.invite, nlxs),
            client=client
        )

    async def approve(self) -> bool:
        """Bound method *approve* of :obj:`~team.types.ChatJoinRequest`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.approve_chat_join_request(
                chat_id=request.chat.id,
                nlx_id=request.from_nlx.id
            )
            
        Example:
            .. code-block:: python

                await request.approve()
                
        Returns:
            ``bool``: True on success.
        
        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.approve_chat_join_request(
            chat_id=self.chat.id,
            nlx_id=self.from_nlx.id
        )

    async def decline(self) -> bool:
        """Bound method *decline* of :obj:`~team.types.ChatJoinRequest`.
        
        Use as a shortcut for:
        
        .. code-block:: python

            await client.decline_chat_join_request(
                chat_id=request.chat.id,
                nlx_id=request.from_nlx.id
            )
            
        Example:
            .. code-block:: python

                await request.decline()
                
        Returns:
            ``bool``: True on success.
        
        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return await self._client.decline_chat_join_request(
            chat_id=self.chat.id,
            nlx_id=self.from_nlx.id
        )
