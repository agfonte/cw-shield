import telebot
import os

#bot = telebot.TeleBot(os.environ.get('TOKEN'))
bot = telebot.TeleBot("1086641008:AAHL-Ab5YAt4Tu5CpyWc4xRZvtpkRxi1aGs")
saveMessagesChatId = -1001428707880
chatWarsBotId = 408101137

@bot.message_handler(commands=['mine'])
def send_welcome(message):
    print("aofnn")
    # Check it was a reply
    replyToMessage = getattr(message, 'reply_to_message')
    if not replyToMessage:
        return

    # Check the reply was to forwarded message
    forwardFrom = getattr(replyToMessage, 'forward_from')
    if not forwardFrom:
        return

    # Check it was forwarded from chatwars
    if forwardFrom.id != chatWarsBotId:
        return

    # Check it has text attribute
    replyToMessageText = getattr(replyToMessage, 'text')
    if not replyToMessageText:
        return

    # Check the text match "Current buyer is: You"
    if replyToMessageText.find("Current buyer is: You") == -1:
        return

    bidLines = replyToMessageText.splitlines();
    shieldMessageArray = []
    for line in bidLines:
        # Replace Current buyer is: You with Current buyer is: @{who_forwarded_message_username}
        if line.find("Current buyer is: You") != -1:
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
print("done")