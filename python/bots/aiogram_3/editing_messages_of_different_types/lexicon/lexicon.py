# editing_messages_of_different_types/lexicon/lexicon.py

# Словарь LEXICON содержит текст и ID для различных типов контента
LEXICON: dict[str, str] = {
    "audio": "🎶 Аудио",
    "text": "📃 Текст",
    "photo": "🖼 Фото",
    "video": "🎬 Видео",
    "document": "📑 Документ",
    "voice": "📢 Голосовое сообщение",
    "animation": "🌀Анимация",

    "text_1": "Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но "
              "нельзя отредактировать сообщением с медиа.",
    "text_2": "Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через "
              "редактирование.",

    "photo_id1": "AgACAgIAAxkBAAIJS2Xol-ocC7BWh60vi8r2JtiPXspKAAJNzzEb5lVBS2qdWAbCE2xtAQADAgADeQADNAQ",
    "photo_id2": "AgACAgIAAxkBAAIJTmXomBZUWXxKsSWRsVqFn1PuDm6CAAJh0TEb5lVBS_dSqdxDqWoAAQEAAwIAA3kAAzQE",

    "audio_id1": "CQACAgIAAxkBAAIJ0mXprgyc-xRMgisKBk4Rye77uVJJAAIpRwAC329QSxHuyqhz-A_zNAQ",
    "audio_id2": "CQACAgIAAxkBAAIJ1WXprkufQ2u3ZVv_baDqCepUiH8tAAIqRwAC329QSykmnCPXuhPaNAQ",

    "document_id1": "BQACAgIAAxkBAAIJ4WXpshECZEKbLppJXsfk-XThZ2KzAAJTRwAC329QSyriMv2jC0ZvNAQ",
    "document_id2": "BQACAgIAAxkBAAIJ5GXpslR6JsX1-eb0GjgDBTHhbq8uAAJXRwAC329QS2yZnRSmN2DFNAQ",

    "video_id1": "BAACAgIAAxkBAAIJrGXpfObRd1fe1LC5yz83lCHbeWIIAAKtSAAC329ISymbjqUlSUrvNAQ",
    "video_id2": "BAACAgIAAxkBAAIJr2XpfPcXh18eGEWlwrG68sNHqoR2AAKuSAAC329IS69TD6NxYHngNAQ",

    "animation_id1": "BAACAgIAAxkBAAIKG2Xq7Z6ZJxyaO5CI2Q27f5yzXc81AAJoQgAC329YSxTpvNJuQP4ZNAQ",
    "animation_id2": "BQACAgIAAxkBAAIKHmXq7a3taYR5WDu5hj-TuA9aqnenAAJqQgAC329YS71sTvT1lvVMNAQ",
}

# Словарь с текстовыми сообщениями для различных сценариев и типов контента на русском языке.
LEXICON_RU: dict[str, str] = {
    "/start": "Привет {first_name}👋!\n\nЯ эхо-бот для демонстрации работы роутеров!\n\n"
              "Если хотите - можете мне что-нибудь прислать или отправить команду /help",

    "ContentType.STICKER": "Here's your sticker\nfile_id is:\n{sticker_file_id}",
    "STICKER": "file_unique_id is:\n{sticker_file_unique_id}",

    "ContentType.ANIMATION": "Here's your animation\nfile_id is:\n{animation_file_id}",
    "ANIMATION": "file_unique_id is:\n{animation_file_unique_id}",

    "ContentType.PHOTO": "Here's your photo,\nfile_id is:\n{photo_file_id}",
    "PHOTO": "file_unique_id is:\n{photo_file_unique_id}",

    "ContentType.VIDEO": "Here's your video,\nfile_id is:\n{video_file_id}",
    "VIDEO": "file_unique_id is:\n{video_file_unique_id}",

    "ContentType.VIDEO_NOTE": "Here's your video_note,\nfile_id is:\n{video_note_file_id}",
    "VIDEO_NOTE": "file_unique_id is:\n{video_note_file_unique_id}",

    "ContentType.AUDIO": "Here's your audio,\nfile_id is:\n{audio_file_id}",
    "AUDIO": "file_unique_id is:\n{audio_file_unique_id}",

    "ContentType.VOICE": "Here's your voice,\nfile_id is:\n{voice_file_id}",
    "VOICE": "file_unique_id is:\n{voice_file_unique_id}",

    "ContentType.DOCUMENT": "Here's your document,\nfile_id is:\n{document_file_id}",
    "DOCUMENT": "file_unique_id is:\n{document_file_unique_id}",

    "no_echo": "Данный тип апдейтов не поддерживается методом send_copy",
}
