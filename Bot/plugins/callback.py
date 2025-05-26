import random, os
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM, Message
from Bot import OWNER_ID, encoder, TRIGGERS
from Bot.plugins.database.mongo_db import ensure_user_exists, check_vcodec_settings, update_vcodec_settings, check_preset_settings, update_preset_settings, check_resolution_settings, check_audio_type_mdb, update_audio_type_mdb, update_resolution_settings, check_crf_mdb, update_crf

BUTTONS_RESOLUTIONS = IKM(
    [
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
            IKB('ʜᴇʟᴘ', 'answer_help'),
        ],
        [
            IKB('sᴇᴛ 𝟺𝟾𝟶ᴘ', 'settings_encoding_480p'),
            IKB('sᴇᴛ 𝟽𝟸𝟶ᴘ', 'settings_encoding_720p'),
            IKB('ѕєт 1080ρ', 'settings_encoding_1080p'),
        ]
    ]
)

BUTTONS_CRF = IKM(
    [
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
            IKB('ʜᴇʟᴘ', 'answer_help')
        ],
        [
            IKB('ᴄʀғ + 𝟷', 'settings_crf_plus'),
            IKB('ᴄʀғ - 𝟷', 'settings_crf_minus'),
        ]
    ]
)

BUTTONS_AUDIO = IKM(
    [
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
            IKB('ʜᴇʟᴘ', 'answer_help')
        ],
        [
            IKB('sᴇᴛ ᴀᴀᴄ', 'settings_encoding_aac'),
            IKB('ѕєт ᴏᴘᴜs', 'settings_encoding_opus'),
            IKB('sᴇᴛ ʟɪʙᴏᴘᴜs', 'settings_encoding_libopus'),
        ]
    ]
)

BUTTONS_PRESET = IKM(
    [
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
            IKB('ʜᴇʟᴘ', 'answer_help')
        ],
        [
            IKB('sᴇᴛ ғᴀsᴛ', 'settings_encoding_fast'),
            IKB('ѕєт sʟᴏᴡ', 'settings_encoding_slow'),
        ]
    ]
)

BUTTONS_VCODEC = IKM(
    [
        [
            IKB("ᴅᴇᴠᴇʟᴏᴘᴇʀ", 'answer_about_dev'),
            IKB('ʜᴇʟᴘ', 'answer_help')
        ],
        [
            IKB('sᴇᴛ x𝟸𝟼𝟺', 'settings_encoding_x264'),
            IKB('ѕєт x𝟸𝟼𝟻', 'settings_encoding_x265'),
        ]
    ]
)

BUTTONS_DEV = IKM(
    [
        [
            IKB('ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/sohailkhan_indianime'),
            IKB('ɢɪᴛʜᴜʙ', url = 'https://github.com/soheru')
        ],
        [
            IKB('ᴡᴇʙsɪᴛᴇ', url='https://teamyokai.tech'),
            IKB('ᴄʜᴀɴɴᴇʟ', url='https://t.me/aboutmesk'),
        ],
        [
            IKB('ɪɴsᴛᴀɢʀᴀᴍ', url='https://instagram.com/_soheru'),
            IKB('ʜᴇʟᴘ', 'answer_help')
        ]
    ]
)

BUTTONS_HELP = IKM(
    [
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
    ]
)

@Client.on_callback_query(filters.regex('settings'))
async def settings_callback(client:Client, callback_query): 
    # Auto-create user settings if they don't exist
    ensure_user_exists(callback_query.from_user.id)
    
    if 'encoding_480p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '480p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ ᴛᴏ 480p',reply_markup=BUTTONS_RESOLUTIONS)
    elif 'encoding_720p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '720p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ ᴛᴏ 720p',reply_markup=BUTTONS_RESOLUTIONS)  
    elif 'encoding_1080p' in callback_query.data:
        update_resolution_settings(callback_query.from_user.id, '1080p')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ʀᴇsᴏʟᴜᴛɪᴏɴ ᴛᴏ 1080p',reply_markup=BUTTONS_RESOLUTIONS)          
    elif 'encoding_aac' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'aac')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ᴀᴀᴄ', reply_markup=BUTTONS_AUDIO)  
    elif 'encoding_opus' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'opus')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ᴏᴘᴜs', reply_markup=BUTTONS_AUDIO) 
    elif 'encoding_libopus' in callback_query.data:
        update_audio_type_mdb(callback_query.from_user.id, 'libopus')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴀᴜᴅɪᴏ ᴛʏᴘᴇ ᴛᴏ ʟɪʙᴏᴘᴜs', reply_markup=BUTTONS_AUDIO) 
    elif 'encoding_x264' in callback_query.data:
        update_vcodec_settings(callback_query.from_user.id, 'x264')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ ᴛᴏ x𝟸𝟼𝟺', reply_markup=BUTTONS_VCODEC)       
    elif 'encoding_x265' in callback_query.data:
        update_vcodec_settings(callback_query.from_user.id, 'x265')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄᴏᴅᴇᴄ ᴛᴏ x𝟸𝟼𝟻', reply_markup=BUTTONS_VCODEC)    
    elif 'encoding_slow' in callback_query.data:
        update_preset_settings(callback_query.from_user.id, 'slow')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴘʀᴇsᴇᴛ ᴛᴏ sʟᴏᴡ', reply_markup=BUTTONS_PRESET)  
    elif 'encoding_fast' in callback_query.data:
        update_preset_settings(callback_query.from_user.id, 'fast')
        await callback_query.message.edit('ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴘʀᴇsᴇᴛ ᴛᴏ ғᴀsᴛ', reply_markup=BUTTONS_PRESET) 
    elif 'crf_plus' in callback_query.data:
        crf_current = check_crf_mdb(callback_query.from_user.id)
        update = crf_current+1
        update_crf(callback_query.from_user.id, update)
        await callback_query.message.edit(f'ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄʀғ ᴛᴏ {update}', reply_markup=BUTTONS_CRF) 
    elif 'crf_minus' in callback_query.data:
        crf_current = check_crf_mdb(callback_query.from_user.id)
        update = crf_current-1
        update_crf(callback_query.from_user.id, update)
        await callback_query.message.edit(f'ᴜᴘᴅᴀᴛᴇᴅ ᴠɪᴅᴇᴏ ᴄʀғ ᴛᴏ {update}', reply_markup=BUTTONS_CRF)    
            
@Client.on_callback_query(filters.regex('blankquery'))
async def blankcallback_answer(client:Client, callback_query): 
    await callback_query.answer('Oops Empty')
        
@Client.on_callback_query(filters.regex('answer'))
async def callback_answer(client:Client, callback_query): 
    # Auto-create user settings if they don't exist
    ensure_user_exists(callback_query.from_user.id)
    
    if 'help' in callback_query.data:
        text = f'**Hi There** `{callback_query.from_user.first_name}`,\n\nI am a video encoder bot, which reduces the size of the video and gives it in good quality.\n\n✅ **No approval required** - You can use all features immediately!\n\nTo see all my features, click the buttons below'
        await callback_query.message.edit(text, reply_markup=BUTTONS_HELP) 
    elif 'crf' in callback_query.data:
        text = '**To change the video crf of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video crf  is** : `{check_crf_mdb(callback_query.from_user.id)}`\n\n**[Created By Soheru](https://t.me/aboutmesk)**'
        await callback_query.message.edit(text, reply_markup=BUTTONS_CRF) 
    elif 'resolution' in callback_query.data:
        text = '**To change the video resolution of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video resolution is** : `{check_resolution_settings(callback_query.from_user.id)}`\n\n**[Created By Soheru](https://t.me/aboutmesk)**'
        await callback_query.message.edit(text, reply_markup=BUTTONS_RESOLUTIONS) 
    elif 'audio' in callback_query.data:  
        text = '**To change the audio type of this bot, use the buttons given below**.\n\n'
        text += f'**Your current audio type is** : `{check_audio_type_mdb(callback_query.from_user.id)}`\n\n**[Created By Soheru](https://t.me/aboutmesk)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_AUDIO) 
    elif 'vcodec' in callback_query.data:  
        text = '**To change the video codec of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video codec is** : `{check_vcodec_settings(callback_query.from_user.id)}`\n\n**[Created By Soheru](https://t.me/aboutmesk)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_VCODEC)  
    elif 'preset' in callback_query.data:  
        text = '**To change the video preset of this bot, use the buttons given below**.\n\n'
        text += f'**Your current video preset is** : `{check_preset_settings(callback_query.from_user.id)}`\n\n**[Created By Soheru](https://t.me/aboutmesk)**'  
        await callback_query.message.edit(text, reply_markup=BUTTONS_PRESET)  
    elif 'about_dev' in callback_query.data:
        await callback_query.message.edit('**Developer Information**', reply_markup=BUTTONS_DEV)

@Client.on_message(filters.command(['start', 'help'], prefixes=['/']))
async def start_(client: Client, message: Message):
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
