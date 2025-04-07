import os
import time
import ffmpeg
import logging
import requests
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

## Extra Fns -------
# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


## Commands --------
@Client.on_message(filters.command(['start']))
async def start(client, message):
       await message.reply("➪ Hey., iam YTMusic bot(by- @PLAYZ_HACKING)\n➪ your music assistant 🎧\n➪ sent me a song name which you want...",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('👑Developer', url='https://t.me/.PLAYZ_90')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['help']))
async def help(client, message):
       await message.reply("<b><i>How many times have I said that just giving the name of a song\nPlease do not expect any other help from me.</i>\n\n<b>Eg</b> `Middle of the night`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('👑 CREATED BY', url='https://t.me/+CK4EXZbq7DRkZmE1')
                ]
            ]
        )
    )

@Client.on_message(filters.command(['about']))
async def about(client, message):
       await message.reply("➪ <b>Bot Name🤖</b> : [PLAY-Z YT MUSIC BOT Bot](https://t.me/PLAYZ_YT_MUSIC_BOT)\n➪ <b>👑CREATOR</b> : [👑⛥꯭ᴳᴼᴰ⛥꯭❖꯭𓂀⃝𝗣ʟᴀʏ-ᴢ𓂀⃝꯭❖⛥꯭](https://t.me(PLAYZ_90)\n➪ <b>Library</b> : Pyrogram",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('Search Inline', switch_inline_query_current_chat='')
                ]
            ]
        )
    )

@Client.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply('Searching the song🎵...')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            views = results[0]["views"]
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('nothing can can found!!')
            return
    except Exception as e:
        m.edit(
            "❎ 𝐒𝐨𝐫𝐫𝐲.\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖮𝗋 Spell it correctly.\n\nEg.`Faded`"
        )
        print(str(e))
        return
    m.edit("`Uploading Your Song,Please Wait...`🎧")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep =  f'🎧 ᴛɪᴛᴛʟᴇ : {title[:35]}\n ᴅᴜʀᴀᴛɪᴏɴ : {duration}\n ᴠɪᴇᴡs : {views}\n\nTo : {message.from_user.mention()}\nQueries : [@riz4d](https://instagram.com/riz.4d)'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=str(info_dict["uploader"]), thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('Failed\n\n`Plesase Try Again Later`')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
