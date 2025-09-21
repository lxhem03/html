import os
import time
import asyncio
import sys
import humanize
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from helper.utils import Compress_Stats, skip, CompressVideo
from helper.database import db
from script import Txt


@Client.on_callback_query()
async def Cb_Handle(bot: Client, query: CallbackQuery):
    data = query.data

    if data == 'help':

        btn = [
            [InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='home')]
        ]

        await query.message.edit(text=Txt.HELP_MSG, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)

    if data == 'home':
        btn = [
            [InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'), InlineKeyboardButton(
                text='🌨️ Aʙᴏᴜᴛ', callback_data='about')],
            [InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/The_TGguy'), InlineKeyboardButton
                (text='💻 Support', url='https://t.me/Tg_Guy_Support')]
        ]
        await query.message.edit(text=Txt.PRIVATE_START_MSG.format(query.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))

    elif data == 'about':
        BUTN = [
            [InlineKeyboardButton(text='⟸ Bᴀᴄᴋ', callback_data='home')]
        ]
        botuser = await bot.get_me()
        await query.message.edit(Txt.ABOUT_TXT.format(botuser.username), reply_markup=InlineKeyboardMarkup(BUTN), disable_web_page_preview=True)

    if data.startswith('stats'):

        user_id = data.split('-')[1]

        try:
            await Compress_Stats(e=query, userid=user_id)

        except Exception as e:
            print(e)

    elif data.startswith('skip'):

        user_id = data.split('-')[1]

        try:

            await skip(e=query, userid=user_id)
        except Exception as e:
            print(e)

    elif data == 'option':
        file = getattr(query.message.reply_to_message,
                       query.message.reply_to_message.media.value)

        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{file.file_name}`\n\n**File Size** :- `{humanize.naturalsize(file.file_size)}`"""
        buttons = [[InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", ,url="https://t.me/TGXrenamerobot")],
                   [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{query.from_user.id}")]]

        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == 'setffmpeg':
        try:
            ffmpeg_code = await bot.ask(text=Txt.SEND_FFMPEG_CODE, chat_id=query.from_user.id, filters=filters.text, timeout=60, disable_web_page_preview=True)
        except:
            return await query.message.reply_text("**Eʀʀᴏʀ!!**\n\nRᴇǫᴜᴇsᴛ ᴛɪᴍᴇᴅ ᴏᴜᴛ.\nSᴇᴛ ʙʏ ᴜsɪɴɢ /set_ffmpeg")

        SnowDev = await query.message.reply_text(text="**Setting Your FFMPEG CODE**\n\nPlease Wait...")
        await db.set_ffmpegcode(query.from_user.id, ffmpeg_code.text)
        await SnowDev.edit("✅️ __**Fғᴍᴘᴇɢ Cᴏᴅᴇ Sᴇᴛ Sᴜᴄᴄᴇssғᴜʟʟʏ**__")


    # ── Compression Menu ────────────────────────────────────────────────
    elif data.startswith('compress'):
        user_id = data.split('-')[1]

        if int(user_id) not in [query.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Hᴇʏ {query.from_user.first_name}\nTʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏ ᴏᴘᴇʀᴀᴛɪᴏɴ",
                show_alert=True
            )

        BTNS = [
            [InlineKeyboardButton("🎞️ libx264", callback_data=f"x264-{user_id}")],
            [InlineKeyboardButton("🎞️ libx265", callback_data=f"x265-{user_id}")],
            [InlineKeyboardButton("Cᴜsᴛᴏᴍ FFMPEG 🗜️", callback_data="custompc")],
            [InlineKeyboardButton("✘ Cʟᴏsᴇ", callback_data="close"),
             InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="option")]
        ]
        await query.message.edit(
            text="**Select the Video Codec 👇**",
            reply_markup=InlineKeyboardMarkup(BTNS)
        )

# ── Codec → Quality Menu (libx264) ───────────────────────────────────
    elif data.startswith("x264-"):
        user_id = data.split("-")[1]
        BTNS = [
            [InlineKeyboardButton("144p", callback_data=f"x264-144-{user_id}"),
             InlineKeyboardButton("240p", callback_data=f"x264-240-{user_id}")],
            [InlineKeyboardButton("360p", callback_data=f"x264-360-{user_id}"),
             InlineKeyboardButton("480p", callback_data=f"x264-480-{user_id}")],
            [InlineKeyboardButton("540p", callback_data=f"x264-540-{user_id}"),
             InlineKeyboardButton("720p", callback_data=f"x264-720-{user_id}")],
            [InlineKeyboardButton("1080p", callback_data=f"x264-1080-{user_id}")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{user_id}")]
        ]
        await query.message.edit("**Codec Selected: libx264**\n\nNow choose a quality 👇",
                                 reply_markup=InlineKeyboardMarkup(BTNS))

# ── Codec → Quality Menu (libx265) ───────────────────────────────────
    elif data.startswith("x265-"):
        user_id = data.split("-")[1]
        BTNS = [
            [InlineKeyboardButton("144p", callback_data=f"x265-144-{user_id}"),
             InlineKeyboardButton("240p", callback_data=f"x265-240-{user_id}")],
            [InlineKeyboardButton("360p", callback_data=f"x265-360-{user_id}"),
             InlineKeyboardButton("480p", callback_data=f"x265-480-{user_id}")],
            [InlineKeyboardButton("540p", callback_data=f"x265-540-{user_id}"),
             InlineKeyboardButton("720p", callback_data=f"x265-720-{user_id}")],
            [InlineKeyboardButton("1080p", callback_data=f"x265-1080-{user_id}")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{user_id}")]
        ]
        await query.message.edit("**Codec Selected: libx265**\n\nNow choose a quality 👇",
                                 reply_markup=InlineKeyboardMarkup(BTNS))


# ── Final Compression Calls (libx264) ────────────────────────────────
    elif data.startswith("x264-144-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 256x144 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-240-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 426x240 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-360-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 640x360 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-480-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 854x480 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-540-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 960x540 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-720-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 1280x720 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x264-1080-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 1920x1080 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)


# ── Final Compression Calls (libx265) ────────────────────────────────
    elif data.startswith("x265-144-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 256x144 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-240-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 426x240 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-360-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 640x360 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-480-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 854x480 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-540-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx265 -s 960x540 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-720-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx265 -s 1280x720 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data.startswith("x265-1080-"):
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx265 -s 1920x1080 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == 'custompc':

        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg_code = await db.get_ffmpegcode(query.from_user.id)

            if ffmpeg_code:
                await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg_code, c_thumb=c_thumb)

            else:
                BUTT = [
                    [InlineKeyboardButton(
                        text='Sᴇᴛ Fғᴍᴘᴇɢ Cᴏᴅᴇ', callback_data='setffmpeg')],
                    [InlineKeyboardButton(
                        text='⟸ Bᴀᴄᴋ', callback_data=f'compress-{query.from_user.id}')]
                ]
                await query.message.edit(text="You Don't Have Any Custom FFMPEG Code. 🛃", reply_markup=InlineKeyboardMarkup(BUTT))
        except Exception as e:
            print(e)

    elif data.startswith("close"):

        user_id = data.split('-')[1]
        
        if int(user_id) not in [query.from_user.id, 0]:
            return await query.answer(f"⚠️ Hᴇʏ {query.from_user.first_name}\nTʜɪs ɪs ɴᴏᴛ ʏᴏᴜʀ ғɪʟᴇ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴅᴏ ᴀɴʏ ᴏᴘᴇʀᴀᴛɪᴏɴ", show_alert=True)
        
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
