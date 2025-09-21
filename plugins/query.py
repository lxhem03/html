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
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@Client.on_callback_query()
async def Cb_Handle(bot: Client, query: CallbackQuery):
    data = query.data

    if data == 'help':
        btn = [[InlineKeyboardButton('⟸ Bᴀᴄᴋ', callback_data='home')]]
        await query.message.edit(
            text=Txt.HELP_MSG,
            reply_markup=InlineKeyboardMarkup(btn),
            disable_web_page_preview=True
        )

    elif data == 'home':
        btn = [
            [
                InlineKeyboardButton(text='❗ Hᴇʟᴘ', callback_data='help'),
                InlineKeyboardButton(text='🌨️ Aʙᴏᴜᴛ', callback_data='about')
            ],
            [
                InlineKeyboardButton(text='📢 Uᴘᴅᴀᴛᴇs', url='https://t.me/The_TGguy'),
                InlineKeyboardButton(text='💻 Support', url='https://t.me/Tg_Guy_Support')
            ]
        ]
        await query.message.edit(
            text=Txt.PRIVATE_START_MSG.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(btn)
        )

    elif data == 'about':
        btn = [[InlineKeyboardButton(text='⟸ Bᴀᴄᴋ', callback_data='home')]]
        botuser = await bot.get_me()
        await query.message.edit(
            text=Txt.ABOUT_TXT.format(botuser.username),
            reply_markup=InlineKeyboardMarkup(btn),
            disable_web_page_preview=True
        )

    elif data.startswith('stats'):
        user_id = data.split('-')[1]
        try:
            await Compress_Stats(e=query, userid=user_id)
        except Exception as e:
            logger.error(f"Error in stats callback for user {user_id}: {e}")
            await query.message.reply_text("⚠️ An error occurred while fetching stats. Please try again.")

    elif data.startswith('skip'):
        user_id = data.split('-')[1]
        try:
            await skip(e=query, userid=user_id)
        except Exception as e:
            logger.error(f"Error in skip callback for user {user_id}: {e}")
            await query.message.reply_text("⚠️ An error occurred while skipping. Please try again.")

    elif data == 'option':
        # Validate reply message and media
        if not query.message.reply_to_message or not hasattr(query.message.reply_to_message, 'media'):
            await query.message.reply_text("⚠️ Please reply to a valid media file.")
            return

        file = getattr(query.message.reply_to_message, query.message.reply_to_message.media.value)
        text = f"""**__What do you want me to do with this file?__**\n\n**File Name**: `{file.file_name}`\n\n**File Size**: `{humanize.naturalsize(file.file_size)}`"""
        buttons = [
            [InlineKeyboardButton("Rᴇɴᴀᴍᴇ 📝", url="https://t.me/TGXrenamerobot")],
            [InlineKeyboardButton("Cᴏᴍᴘʀᴇss 🗜️", callback_data=f"compress-{query.from_user.id}")]
        ]
        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(buttons))

    elif data == 'setffmpeg':
        try:
            ffmpeg_code = await bot.ask(
                text=Txt.SEND_FFMPEG_CODE,
                chat_id=query.from_user.id,
                filters=filters.text,
                timeout=60,
                disable_web_page_preview=True
            )
            snow_dev = await query.message.reply_text(text="**Setting Your FFMPEG CODE**\n\nPlease Wait...")
            await db.set_ffmpegcode(query.from_user.id, ffmpeg_code.text)
            await snow_dev.edit("✅️ __**FFMPEG Code Set Successfully**__")
        except asyncio.TimeoutError:
            await query.message.reply_text("**Error!**\n\nRequest timed out. Set using /set_ffmpeg")
        except Exception as e:
            logger.error(f"Error in setffmpeg callback: {e}")
            await query.message.reply_text("⚠️ An error occurred while setting FFMPEG code. Please try again.")

    # ── Compression Menu ────────────────────────────────────────────────
    elif data.startswith('compress'):
        user_id = data.split('-')[1]
        if int(user_id) != query.from_user.id:
            return await query.answer(
                f"⚠️ Hey {query.from_user.first_name}\nThis is not your file, you can't perform any operation",
                show_alert=True
            )

        buttons = [
            [InlineKeyboardButton("🎞️ libx264", callback_data="avc")],
            [InlineKeyboardButton("🎞️ libx265", callback_data="hevc")],
            [InlineKeyboardButton("Cᴜsᴛᴏᴍ FFMPEG 🗜️", callback_data="custompc")],
            [
                InlineKeyboardButton("✘ Cʟᴏsᴇ", callback_data=f"close-{query.from_user.id}"),
                InlineKeyboardButton("⟸ Bᴀᴄᴋ", callback_data="option")
            ]
        ]
        await query.message.edit(
            text="**Select the Video Codec 👇**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ── Codec → Quality Menu (libx264) ───────────────────────────────────
    elif data == 'avc':
        buttons = [
            [
                InlineKeyboardButton("144p", callback_data="144avc"),
                InlineKeyboardButton("240p", callback_data="240avc")
            ],
            [
                InlineKeyboardButton("360p", callback_data="360avc"),
                InlineKeyboardButton("480p", callback_data="480avc")
            ],
            [
                InlineKeyboardButton("540p", callback_data="540avc"),
                InlineKeyboardButton("720p", callback_data="720avc")
            ],
            [InlineKeyboardButton("1080p", callback_data="1080avc")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{query.from_user.id}")]
        ]
        await query.message.edit(
            text="**Codec Selected: __libx264 (AVC)__**\n\nNow choose a quality 👇",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ── Codec → Quality Menu (libx265) ───────────────────────────────────
    elif data == 'hevc':
        buttons = [
            [
                InlineKeyboardButton("144p", callback_data="144hevc"),
                InlineKeyboardButton("240p", callback_data="240hevc")
            ],
            [
                InlineKeyboardButton("360p", callback_data="360hevc"),
                InlineKeyboardButton("480p", callback_data="480hevc")
            ],
            [
                InlineKeyboardButton("540p", callback_data="540hevc"),
                InlineKeyboardButton("720p", callback_data="720hevc")
            ],
            [InlineKeyboardButton("1080p", callback_data="1080hevc")],
            [InlineKeyboardButton("⟸ Back", callback_data=f"compress-{query.from_user.id}")]
        ]
        await query.message.edit(
            text="**Codec Selected: __libx265 (HEVC)__**\n\nNow choose a quality 👇",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ── Final Compression Calls (libx264) ────────────────────────────────
    elif data in ['144avc', '240avc', '360avc', '480avc', '540avc', '720avc', '1080avc']:
        try:
            # Map callback data to resolution and preset
            resolution_map = {
                '144avc': '256x144',
                '240avc': '426x240',
                '360avc': '640x360',
                '480avc': '854x480',
                '540avc': '960x540',
                '720avc': '1280x720',
                '1080avc': '1920x1080'
            }
            preset = 'veryfast' if data in ['540avc', '720avc', '1080avc'] else 'faster'
            resolution = resolution_map[data]
            ffmpeg = f"-preset {preset} -map 0 -c:v libx264 -s {resolution} -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"

            c_thumb = await db.get_thumbnail(query.from_user.id)
            if c_thumb is None:
                logger.warning(f"No thumbnail found for user {query.from_user.id}")
                

            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            logger.error(f"Error in {data} compression: {e}")
            await query.message.reply_text(f"⚠️ An error occurred during compression. Please try again.\n\nError: `{e}`")

    # ── Final Compression Calls (libx265) ────────────────────────────────
    elif data in ['144hevc', '240hevc', '360hevc', '480hevc', '540hevc', '720hevc', '1080hevc']:
        try:
            # Map callback data to resolution and preset
            resolution_map = {
                '144hevc': '256x144',
                '240hevc': '426x240',
                '360hevc': '640x360',
                '480hevc': '854x480',
                '540hevc': '960x540',
                '720hevc': '1280x720',
                '1080hevc': '1920x1080'
            }
            preset = 'veryfast' if data in ['540hevc', '720hevc', '1080hevc'] else 'faster'
            resolution = resolution_map[data]
            ffmpeg = f"-preset {preset} -map 0 -c:v libx265 -s {resolution} -pix_fmt yuv420p -crf 30 -c:a libopus -b:a 32k -ac 2 -vbr 2"

            c_thumb = await db.get_thumbnail(query.from_user.id)
            if c_thumb is None:
                logger.warning(f"No thumbnail found for user {query.from_user.id}")
                

            await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg, c_thumb=c_thumb)
        except Exception as e:
            logger.error(f"Error in {data} compression: {e}")
            await query.message.reply_text(f"⚠️ An error occurred during compression. Please try again.\n\nError: `{e}`")

    elif data == 'custompc':
        try:
            c_thumb = await db.get_thumbnail(query.from_user.id)
            ffmpeg_code = await db.get_ffmpegcode(query.from_user.id)
            if ffmpeg_code:
                await CompressVideo(bot=bot, query=query, ffmpegcode=ffmpeg_code, c_thumb=c_thumb)
            else:
                buttons = [
                    [InlineKeyboardButton(text='Sᴇᴛ Fғᴍᴘᴇɢ Cᴏᴅᴇ', callback_data='setffmpeg')],
                    [InlineKeyboardButton(text='⟸ Bᴀᴄᴋ', callback_data=f'compress-{query.from_user.id}')]
                ]
                await query.message.edit(
                    text="You don't have any custom FFMPEG code. 🛃",
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
        except Exception as e:
            logger.error(f"Error in custompc callback: {e}")
            await query.message.reply_text(f"⚠️ An error occurred with custom FFMPEG. Please try again.\n\nError: `{e}`")

    elif data.startswith("close"):
        user_id = data.split('-')[1] if '-' in data else query.from_user.id
        if int(user_id) != query.from_user.id:
            return await query.answer(
                f"⚠️ Hey {query.from_user.first_name}\nThis is not your file, you can't perform any operation",
                show_alert=True
            )
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception as e:
            logger.error(f"Error in close callback: {e}")
            await query.message.reply_text("⚠️ An error occurred while closing. Please try again.")
