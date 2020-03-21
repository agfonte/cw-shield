import telebot
import os
# import logging

# Enabling logging
# logging.basicConfig(level=logging.INFO,
#                     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger()

bot = telebot.TeleBot(os.environ.get('HOME'))

saveMessagesChatId = -1001428707880
chatWarsBotId = 408101137


@bot.message_handler(commands=['mine'])
def send_welcome(message):
    # Check it was a replying
    replyToMessage = getattr(message, 'reply_to_message')
    if not replyToMessage:
        # logger.error("DIDNT FOUND REPLY MESSAGE")
        return

    # Check the replying was forwarded
    forwardFrom = getattr(replyToMessage, 'forward_from')
    if not forwardFrom:
        # logger.error("DIDNT FOUND FORWARD FROM")
        return

    # Check it was forwarded from chatwars
    if forwardFrom.id != chatWarsBotId:
        # logger.error("WASNT FORWARD FROM CHATWARS")
        return

    # Check it has text
    replyToMessageText = getattr(replyToMessage, 'text')
    if not replyToMessageText:
        # logger.error("DIDNT FOUND REPLY TO MESSAGE TEXT")
        return

    # Check the text match Current buyer is: You
    if replyToMessageText.find("Current buyer is: You") == -1:
        # logger.error("DIDNT FOUND CURRENT BUYER IS YOU IN THE TEXT")
        return

    bidLines = replyToMessageText.splitlines();
    shieldMessageArray = []
    for line in bidLines:
        if line.find("Current buyer is:") != -1:
            # logger.error(line)
            shieldMessageArray.append("Current buyer is: @"+replyToMessage.from_user.username)
            continue

        shieldMessageArray.append(line)

    # Concat shield message array as string with breaklines
    shieldMessageAsString = '\n'.join(shieldMessageArray)

    # Send shield message to a specific chat
    bot.send_message(saveMessagesChatId, shieldMessageAsString)

    # Delete /mine and forwarded message
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, replyToMessage.message_id)


bot.polling()
