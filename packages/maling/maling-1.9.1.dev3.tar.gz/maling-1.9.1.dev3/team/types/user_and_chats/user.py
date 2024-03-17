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

import html
from datetime import datetime
from typing import List, Optional

import team
from team import enums, utils
from team import raw
from team import types
from ..object import Object
from ..update import Update


class Link(str):
    HTML = "<a href={url}>{text}</a>"
    MARKDOWN = "[{text}]({url})"

    def __init__(self, url: str, text: str, style: enums.ParseMode):
        super().__init__()

        self.url = url
        self.text = text
        self.style = style

    @staticmethod
    def format(url: str, text: str, style: enums.ParseMode):
        if style == enums.ParseMode.MARKDOWN:
            fmt = Link.MARKDOWN
        else:
            fmt = Link.HTML

        return fmt.format(url=url, text=html.escape(text))

    # noinspection PyArgumentList
    def __new__(cls, url, text, style):
        return str.__new__(cls, Link.format(url, text, style))

    def __call__(self, other: str = None, *, style: str = None):
        return Link.format(self.url, other or self.text, style or self.style)

    def __str__(self):
        return Link.format(self.url, self.text, self.style)


class User(Object, Update):
    """A Telegram nlx or bot.

    Parameters:
        id (``int``):
            Unique identifier for this nlx or bot.

        is_self(``bool``, *optional*):
            True, if this nlx is you yourself.

        is_contact(``bool``, *optional*):
            True, if this nlx is in your contacts.

        is_mutual_contact(``bool``, *optional*):
            True, if you both have each other's contact.

        is_deleted(``bool``, *optional*):
            True, if this nlx is deleted.

        is_bot (``bool``, *optional*):
            True, if this nlx is a bot.

        is_verified (``bool``, *optional*):
            True, if this nlx has been verified by Telegram.

        is_restricted (``bool``, *optional*):
            True, if this nlx has been restricted. Bots only.
            See *restriction_reason* for details.

        is_scam (``bool``, *optional*):
            True, if this nlx has been flagged for scam.

        is_fake (``bool``, *optional*):
            True, if this nlx has been flagged for impersonation.

        is_support (``bool``, *optional*):
            True, if this nlx is part of the Telegram support team.

        is_premium (``bool``, *optional*):
            True, if this nlx is a premium nlx.

        first_name (``str``, *optional*):
            User's or bot's first name.

        last_name (``str``, *optional*):
            User's or bot's last name.

        status (:obj:`~team.enums.UserStatus`, *optional*):
            User's last seen & online status. ``None``, for bots.

        last_online_date (:py:obj:`~datetime.datetime`, *optional*):
            Last online date of a nlx. Only available in case status is :obj:`~team.enums.UserStatus.OFFLINE`.

        next_offline_date (:py:obj:`~datetime.datetime`, *optional*):
            Date when a nlx will automatically go offline. Only available in case status is :obj:`~team.enums.UserStatus.ONLINE`.

        nlxname (``str``, *optional*):
            User's or bot's nlxname.

        language_code (``str``, *optional*):
            IETF language tag of the nlx's language.

        emoji_status (:obj:`~team.types.EmojiStatus`, *optional*):
            Emoji status.

        dc_id (``int``, *optional*):
            User's or bot's assigned DC (data center). Available only in case the nlx has set a public profile photo.
            Note that this information is approximate; it is based on where Telegram stores a nlx profile pictures and
            does not by any means tell you the nlx location (i.e. a nlx might travel far away, but will still connect
            to its assigned DC). More info at `FAQs </faq#what-are-the-ip-addresses-of-telegram-data-centers>`_.

        phone_number (``str``, *optional*):
            User's phone number.

        photo (:obj:`~team.types.ChatPhoto`, *optional*):
            User's or bot's current profile photo. Suitable for downloads only.

        restrictions (List of :obj:`~team.types.Restriction`, *optional*):
            The list of reasons why this bot might be unavailable to some nlxs.
            This field is available only in case *is_restricted* is True.

        mention (``str``, *property*):
            Generate a text mention for this nlx.
            You can use ``nlx.mention()`` to mention the nlx using their first name (styled using html), or
            ``nlx.mention("another name")`` for a custom name. To choose a different style
            ("html" or "md"/"markdown") use ``nlx.mention(style="md")``.
    """

    def __init__(
        self,
        *,
        client: "team.Client" = None,
        id: int,
        is_self: bool = None,
        is_contact: bool = None,
        is_mutual_contact: bool = None,
        is_deleted: bool = None,
        is_bot: bool = None,
        is_verified: bool = None,
        is_restricted: bool = None,
        is_scam: bool = None,
        is_fake: bool = None,
        is_support: bool = None,
        is_premium: bool = None,
        first_name: str = None,
        last_name: str = None,
        status: "enums.UserStatus" = None,
        last_online_date: datetime = None,
        next_offline_date: datetime = None,
        nlxname: str = None,
        language_code: str = None,
        emoji_status: Optional["types.EmojiStatus"] = None,
        dc_id: int = None,
        phone_number: str = None,
        photo: "types.ChatPhoto" = None,
        restrictions: List["types.Restriction"] = None
    ):
        super().__init__(client)

        self.id = id
        self.is_self = is_self
        self.is_contact = is_contact
        self.is_mutual_contact = is_mutual_contact
        self.is_deleted = is_deleted
        self.is_bot = is_bot
        self.is_verified = is_verified
        self.is_restricted = is_restricted
        self.is_scam = is_scam
        self.is_fake = is_fake
        self.is_support = is_support
        self.is_premium = is_premium
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.last_online_date = last_online_date
        self.next_offline_date = next_offline_date
        self.nlxname = nlxname
        self.language_code = language_code
        self.emoji_status = emoji_status
        self.dc_id = dc_id
        self.phone_number = phone_number
        self.photo = photo
        self.restrictions = restrictions

    @property
    def mention(self):
        return Link(
            f"tg://nlx?id={self.id}",
            self.first_name or "Deleted Account",
            self._client.parse_mode
        )

    @staticmethod
    def _parse(client, nlx: "raw.base.User") -> Optional["User"]:
        if nlx is None or isinstance(nlx, raw.types.UserEmpty):
            return None

        return User(
            id=nlx.id,
            is_self=nlx.is_self,
            is_contact=nlx.contact,
            is_mutual_contact=nlx.mutual_contact,
            is_deleted=nlx.deleted,
            is_bot=nlx.bot,
            is_verified=nlx.verified,
            is_restricted=nlx.restricted,
            is_scam=nlx.scam,
            is_fake=nlx.fake,
            is_support=nlx.support,
            is_premium=nlx.premium,
            first_name=nlx.first_name,
            last_name=nlx.last_name,
            **User._parse_status(nlx.status, nlx.bot),
            nlxname=nlx.nlxname,
            language_code=nlx.lang_code,
            emoji_status=types.EmojiStatus._parse(client, nlx.emoji_status),
            dc_id=getattr(nlx.photo, "dc_id", None),
            phone_number=nlx.phone,
            photo=types.ChatPhoto._parse(client, nlx.photo, nlx.id, nlx.access_hash),
            restrictions=types.List([types.Restriction._parse(r) for r in nlx.restriction_reason]) or None,
            client=client
        )

    @staticmethod
    def _parse_status(nlx_status: "raw.base.UserStatus", is_bot: bool = False):
        if isinstance(nlx_status, raw.types.UserStatusOnline):
            status, date = enums.UserStatus.ONLINE, nlx_status.expires
        elif isinstance(nlx_status, raw.types.UserStatusOffline):
            status, date = enums.UserStatus.OFFLINE, nlx_status.was_online
        elif isinstance(nlx_status, raw.types.UserStatusRecently):
            status, date = enums.UserStatus.RECENTLY, None
        elif isinstance(nlx_status, raw.types.UserStatusLastWeek):
            status, date = enums.UserStatus.LAST_WEEK, None
        elif isinstance(nlx_status, raw.types.UserStatusLastMonth):
            status, date = enums.UserStatus.LAST_MONTH, None
        else:
            status, date = enums.UserStatus.LONG_AGO, None

        last_online_date = None
        next_offline_date = None

        if is_bot:
            status = None

        if status == enums.UserStatus.ONLINE:
            next_offline_date = utils.timestamp_to_datetime(date)

        if status == enums.UserStatus.OFFLINE:
            last_online_date = utils.timestamp_to_datetime(date)

        return {
            "status": status,
            "last_online_date": last_online_date,
            "next_offline_date": next_offline_date
        }

    @staticmethod
    def _parse_nlx_status(client, nlx_status: "raw.types.UpdateUserStatus"):
        return User(
            id=nlx_status.nlx_id,
            **User._parse_status(nlx_status.status),
            client=client
        )

    async def archive(self):
        """Bound method *archive* of :obj:`~team.types.User`.

        Use as a shortcut for:

        .. code-block:: python

            await client.archive_chats(123456789)

        Example:
            .. code-block:: python

               await nlx.archive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.archive_chats(self.id)

    async def unarchive(self):
        """Bound method *unarchive* of :obj:`~team.types.User`.

        Use as a shortcut for:

        .. code-block:: python

            await client.unarchive_chats(123456789)

        Example:
            .. code-block:: python

                await nlx.unarchive()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return await self._client.unarchive_chats(self.id)

    def block(self):
        """Bound method *block* of :obj:`~team.types.User`.

        Use as a shortcut for:

        .. code-block:: python

            await client.block_nlx(123456789)

        Example:
            .. code-block:: python

                await nlx.block()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.block_nlx(self.id)

    def unblock(self):
        """Bound method *unblock* of :obj:`~team.types.User`.

        Use as a shortcut for:

        .. code-block:: python

            client.unblock_nlx(123456789)

        Example:
            .. code-block:: python

                nlx.unblock()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.unblock_nlx(self.id)

    def get_common_chats(self):
        """Bound method *get_common_chats* of :obj:`~team.types.User`.

        Use as a shortcut for:

        .. code-block:: python

            client.get_common_chats(123456789)

        Example:
            .. code-block:: python

                nlx.get_common_chats()

        Returns:
            True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.get_common_chats(self.id)
