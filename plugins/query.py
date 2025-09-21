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
        buttons = [[InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", url="https://t.me/TGXrenamerobot")],
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
            [InlineKeyboardButton("🎞️ libx264", callback_data="avc")],
            [InlineKeyboardButton("🎞️ libx265", callback_data="hevc")],
            [InlineKeyboardButton("Cᴜsᴛᴏᴍ FFMPEG 🗜️", callback_data="custompc")],
            [InlineKeyboardButton("✘ Cʟᴏsᴇ", callback_data="close"),
             InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="option")]
        ]
        await query.message.edit(
            text="**Select the Video Codec 👇**",
            reply_markup=InlineKeyboardMarkup(BTNS)
        )

# ── Codec → Quality Menu (libx264) ───────────────────────────────────
    elif data == 'avc':
        user_id = data.split("-")[1]
        BTNS = [
            [InlineKeyboardButton("144p", callback_data="144avc"),
             InlineKeyboardButton("240p", callback_data="240avc")],
            [InlineKeyboardButton("360p", callback_data="360avc"),
             InlineKeyboardButton("480p", callback_data="480avc")],
            [InlineKeyboardButton("540p", callback_data="540avc"),
             InlineKeyboardButton("720p", callback_data="720avc")],
            [InlineKeyboardButton("1080p", callback_data="1080avc")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{query.from_user.id}")]
        ]
        await query.message.edit("**Codec Selected: __libx264 (AVC)__**\n\nNow choose a quality 👇",
                                 reply_markup=InlineKeyboardMarkup(BTNS))

# ── Codec → Quality Menu (libx265) ───────────────────────────────────
    elif data == 'hevc':
        user_id = data.split("-")[1]
        BTNS = [
            [InlineKeyboardButton("144p", callback_data="144hevc"),
             InlineKeyboardButton("240p", callback_data="240hevc")],
            [InlineKeyboardButton("360p", callback_data="360hevc"),
             InlineKeyboardButton("480p", callback_data="480hevc")],
            [InlineKeyboardButton("540p", callback_data="540hevc"),
             InlineKeyboardButton("720p", callback_data="720hevc")],
            [InlineKeyboardButton("1080p", callback_data="1080hevc")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{query.from_user.id}")]
        ]
        await query.message.edit("**Codec Selected: __libx265 (HEVC)__**\n\nNow choose a quality 👇",
                                 reply_markup=InlineKeyboardMarkup(BTNS))


# ── Final Compression Calls (libx264) ────────────────────────────────
    elif data == '144avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 256x144 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '240avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 426x240 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '360avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 640x360 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '480avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx264 -s 854x480 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '540avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 960x540 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '720avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 1280x720 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '1080avc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx264 -s 1920x1080 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)


# ── Final Compression Calls (libx265) ────────────────────────────────
    elif data == '144hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 256x144 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '240hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 426x240 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '360hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 640x360 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '480hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset faster -c:v libx265 -s 854x480 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '540hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx265 -s 960x540 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '720hevc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg = "-preset veryfast -c:v libx265 -s 1280x720 -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"
            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            print(e)

    elif data == '1080hevc':
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
