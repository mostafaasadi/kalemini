import tempfile
import subprocess
import speech_recognition as sr
from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Telegram API
# access  bot via token
updater = Updater(token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
dispatcher = updater.dispatcher


def att(file, inputLang='fa-IR'):
    r = sr.Recognizer()
    toText = sr.AudioFile(file)
    with toText as source:
        audio = r.record(source)
    try:
        result = r.recognize_google(audio, language=inputLang)
        return result
    except Exception as e:
        print(e)
        return None


def start(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text='صوتی بفرستید')
    return True


def general_manager(bot, update):
    bot.sendMessage(
        chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text='صوتی بفرستید')
    return True


def voice_manager(bot, update):
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    tf = tempfile.mkstemp('.ogg')
    tf2 = tempfile.mkstemp('.wav')
    newFile.download(tf[1])
    try:
        subprocess.run(
            ['ffmpeg', '-i', tf[1], '-y', '-ab', '120k', tf2[1]],
            shell=False,
            stdout=subprocess.DEVNULL
        )
    except Exception as e:
        print(e)
    try:
        res = att(tf2[1])
    except Exception as e:
        print(e)
    try:
        bot.send_chat_action(
            chat_id=update.message.chat_id,
            action=ChatAction.TYPING)
        bot.sendMessage(
            chat_id=update.message.chat_id,
            reply_to_message_id=update.message.message_id,
            text='👂🏼  ' + res)
    except Exception as e:
        print(e)


def main():
    # handle dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.voice, voice_manager))
    dispatcher.add_handler(
        MessageHandler(
            Filters.photo | Filters.video | Filters.document | Filters.text |
            Filters.location | Filters.sticker | Filters.voice |
            Filters.audio | Filters.command | Filters.contact | Filters.venue,
            general_manager))

    # run
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
