from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import config



START = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Получить подарки 🎁",
                callback_data='gift'
            )
        ],
        [
            InlineKeyboardButton(
                text="Тех поддержка ⚒",
                url='https://t.me/matveeva_pr'
            )
        ]
    ],
)

CHECK_ERROR = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Получить подарки 🎁",
                callback_data='gift'
            )
        ],
        [
            InlineKeyboardButton(
                text="Тех поддержка ⚒",
                url='https://t.me/matveeva_pr'
            )
        ]
    ],
)

CHECK_SUCCESS = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Получить подарки 🎁",
                url=config.GIFT_CHANNEL_INVITE_LINK
            )
        ]
    ]
)

