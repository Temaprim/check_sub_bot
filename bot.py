import asyncio
import logging
import sys
from typing import List

from aiogram import Bot, Dispatcher, types, exceptions
from aiogram.filters import CommandStart, Text

import database
import messages
import keyboards
import config
import log_messages


# Проверяет, есть ли бот в каналах или нет.
async def validate_channel_connection(bot: Bot, db: List[dict]) -> None:
    bot_client = await bot.me()

    for channel in db:
        try:
            await bot.get_chat_member(
                        chat_id=channel['channel_id'],
                        user_id=bot_client.id
                    )
        except exceptions.TelegramBadRequest:
            logging.error(
                    log_messages.FORGET_ADD_BOT_IN_CHANNEL.format(
                        channel['name'],
                        channel['invite_link']
                    )
            ) 
            sys.exit(1)
 

async def main() -> None:
    dp = Dispatcher()
    bot = Bot(config.TOKEN, parse_mode="HTML")

    db = database.get_csv_db(config.DATABASE_PATH)

   
    # Прикольная тема с коммандами из aiogram 3.x. Мне очень зашла.
    @dp.message(CommandStart)
    async def command_start_handler(message: types.Message) -> None:
        await message.answer(
            text=messages.HELLO.format(message.from_user.full_name),
            reply_markup=keyboards.START,
            disable_web_page_preview = True
        )

        
    @dp.callback_query(Text(text="gift"))
    async def gift(callback: types.CallbackQuery) -> None:
        for channel in db:
            # Тут проверка, есть ли пользователь в канале.
            if isinstance(
                    await bot.get_chat_member(
                        chat_id=channel['channel_id'],
                        user_id=callback.from_user.id
                    ),
                    (
                        types.ChatMemberLeft,
                        types.ChatMemberBanned
                    )
                ):
                await callback.message.answer(messages.CHECK_ERROR)
                await callback.message.answer(
                    text=messages.AFTER_CHECK_ERROR,
                    reply_markup=keyboards.CHECK_ERROR,
                    disable_web_page_preview=True
                )
                break
        # Если вложенное условие с break ни разу не сработало - значит
        # пользователь есть во всех каналах из бд. А значит дарим подарок.
        else:
            await callback.message.answer(
                text=messages.AFTER_CHECK_SUCCESS,
                reply_markup=keyboards.CHECK_SUCCESS,
                disable_web_page_preview=True
            )
            # "Пользователь {полное имя} получил свой подарок!"
            logging.info(
                log_messages.LOG_CHECK_SUCCESS.format(
                    callback.from_user.full_name
                )
            )

    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

