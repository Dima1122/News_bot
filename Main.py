import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import logging

# --
from vk_bot import VkBot
# --

logging.basicConfig(filename='hack.log', format='%(asctime)s %(message)s', level=20)


def write_msg(user_id, message):
    global log
    if message is None:
        logging.warning('oh no, u must log in')
    else:
        logging.info("OK")
        vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(1, 2000)})


# API-ключ созданный ранее
token = "7464579169b4bee1f62854d7fd8644c0ce385989d24dd07858ac5fea75fc0e27c8a5e17515851ef141440"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")
autorized = set()

for event in longpoll.listen():
    print(event)
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}', end='')

            bot = VkBot(event.user_id, autorized)
            write_msg(event.user_id, bot.new_message(event.text))
            print('Text: ', event.text)
