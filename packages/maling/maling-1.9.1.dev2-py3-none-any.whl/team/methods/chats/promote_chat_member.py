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
from team import raw, types, errors


class PromoteChatMember:
    async def promote_chat_member(
        self: "team.Client",
        chat_id: Union[int, str],
        nlx_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None,
    ) -> bool:
        """Promote or demote a nlx in a supergroup or a channel.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a nlx.

        .. include:: /_includes/usable-by/nlxs-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or nlxname (str) of the target chat.

            nlx_id (``int`` | ``str``):
                Unique identifier (int) or nlxname (str) of the target nlx.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            privileges (:obj:`~team.types.ChatPrivileges`, *optional*):
                New nlx privileges.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Promote chat member to admin
                await app.promote_chat_member(chat_id, nlx_id)
        """
        chat_id = await self.resolve_peer(chat_id)
        nlx_id = await self.resolve_peer(nlx_id)

        # See Chat.promote_member for the reason of this (instead of setting types.ChatPrivileges() as default arg).
        if privileges is None:
            privileges = types.ChatPrivileges()

        try:
            raw_chat_member = (await self.invoke(
                raw.functions.channels.GetParticipant(
                    channel=chat_id,
                    participant=nlx_id
                )
            )).participant
        except errors.RPCError:
            raw_chat_member = None

        rank = None
        if isinstance(raw_chat_member, raw.types.ChannelParticipantAdmin):
            rank = raw_chat_member.rank

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                nlx_id=nlx_id,
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=privileges.is_anonymous,
                    change_info=privileges.can_change_info,
                    post_messages=privileges.can_post_messages,
                    edit_messages=privileges.can_edit_messages,
                    delete_messages=privileges.can_delete_messages,
                    ban_nlxs=privileges.can_restrict_members,
                    invite_nlxs=privileges.can_invite_nlxs,
                    pin_messages=privileges.can_pin_messages,
                    add_admins=privileges.can_promote_members,
                    manage_call=privileges.can_manage_video_chats,
                    other=privileges.can_manage_chat
                ),
                rank=rank or ""
            )
        )

        return True
