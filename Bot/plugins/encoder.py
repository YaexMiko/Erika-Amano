from enum import auto
import time, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

from Bot.plugins.database.mongo_db import ensure_user_exists, check_vcodec_settings, check_preset_settings, check_resolution_settings, check_audio_type_mdb
from Bot.utils.decorators import ffmpeg_settings
from Bot import encoder, OWNER_ID, LOG, FILES_CHANNEL, SESSION_STRING , ubot
from Bot.utils.progress_pyro import progress_for_pyrogram
from Bot.utils.ffmpeg import ffmpeg_progress

encoder_is_on = []
flood = []

async def on_task_complete():
    del encoder_is_on[0]
    if len(encoder_is_on) > 0:
        if encoder_is_on[0]:
            await add_task(encoder_is_on[0])   
        
async def add_task(message):
    try:
        msg = await message.reply_text("<code>Downloading Files...</code>")
        c_time = time.time()
        FT = time.time()
        try:
            filepath = await message.download(progress=progress_for_pyrogram,progress_args=("**Downloading...**", msg, c_time))   
            check_resolution = check_resolution_settings(message.from_user.id)
            cmd = ffmpeg_settings(message.from_user.id, filepath, FT)  
            await msg.edit_text('**Encoding...**')
            try:
                await ffmpeg_progress(cmd, filepath,f'progress-{FT}.txt',FT, msg, '**Encoding Started**\n\n')
            except Exception as e:
                LOG.info(f'Error while ffmpeg progress\n{str(e)}')  
            output = filepath.rsplit('.',1)[0]
            if '.mkv' in filepath:
                output = output+'_IA.mkv'    
            else:
                output = output+'_IA.mp4'       
                
            file_name = output.rsplit('/', 1)[1].replace('_IA', "")
            try: #MSG EDIT AND EDIT
                await msg.edit(f'**Encoding Completed**')   
                if ubot == None:
                    file =  await encoder.send_document(chat_id = FILES_CHANNEL, document = output, caption=f"**{check_resolution}**", file_name=file_name)  
                else:
                    file =  await ubot.send_document(chat_id = FILES_CHANNEL, document = output, caption=f"**{check_resolution}**", file_name=file_name)  
                
            except Exception as e: 
                LOG.info(f'Error while file sending\n{str(e)}')  
            try:
                await encoder.copy_message(chat_id = msg.chat.id, from_chat_id = FILES_CHANNEL, message_id= file.id)                
            except Exception as e: 
                LOG.info(f'Error while file copy\n{str(e)}')
                
            try: #FILE DELETE
                os.remove(filepath)
                os.remove(output)
                os.remove(f'progress-{FT}.txt')
            except Exception as e: 
                LOG.info(f'Error while removing files\n{str(e)}')      
           
            try: #MSG DELETE
                await msg.delete() 
            except:
                pass       
                       
        except Exception as e: 
            LOG.info(f'Error while downloading/encoding\n{str(e)}')    
    except Exception as e: 
        LOG.info(f'Error in add_task\n{str(e)}')
        
    try:
        await on_task_complete()   
    except Exception as e: 
        LOG.info(f'Error while task complete\n{str(e)}') 

video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    'application/zip',
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]      
                  
@encoder.on_message(filters.document | filters.video & filters.private)
async def encoder_process(client, message):
    if message.document and message.video and message.document.mime_type and message.video.mime_type not in video_mimetype:
        return 
    
    # Auto-create user settings if they don't exist (removes approval requirement)
    ensure_user_exists(message.from_user.id)
    
    msf = await message.reply('📥 Added to the queue')
    encoder_is_on.append(message)
    if len(encoder_is_on) == 1:
        await msf.delete()
        await add_task(message)           

@encoder.on_message(filters.command(['start', 'help'], prefixes=['/']))
async def start_handler(client, message):
    # Auto-create user settings on first interaction
    ensure_user_exists(message.from_user.id)
    
    text = f'**Hi There** `{message.from_user.first_name}`,\n\nI am a video encoder bot, which reduces the size of the video and gives it in good quality.\n\n✅ **No approval required** - You can start using the bot immediately!\n\nTo see all my features, click the buttons below'
    
    buttons = IKM([
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
        ], 
        [
            IKB('ʀᴇsᴏʟᴜᴛɪᴏɴ', 'answer_resolution'),
            IKB('ᴀᴜᴅɪᴏ', 'answer_audio'),
            IKB('ᴄʀғ', 'answer_crf')
        ],
        [
           IKB('ᴠᴄᴏᴅᴇᴄ', 'answer_vcodec'),
           IKB('ᴘʀᴇsᴇᴛ', 'answer_preset'), 
        ]
    ])
    
    await message.reply(text, reply_markup=buttons)
