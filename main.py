import telebot
import time
import schedule
import threading
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('AUTH_TOKEN')

bot = telebot.TeleBot(bot_token)
conf_order_ids = []
cust_ord_list = []


# in case of commands- /start or /help- show welcome message + add to costumers list-cust_ord_list
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global cust_ord_list
    it = [message.chat.id, "", ""]
    flag = False
    # if user id exists so flag = true and don't add him. if he is not there- flag=false and add him
    for item in cust_ord_list:
        if item[0] == it[0]:
            flag = True
    if not flag:
        cust_ord_list.append(it)
        print("welcome " + str(it[0]) + " " + str(it[1]) + " " + str(it[2]))

    bot.reply_to(message, "Hi " + message.chat.first_name + """!\nWelcome to Noy's Place!
Our menu includes pizza, toast, or falafel. Every dish with its special toppings!
Click on your preferred meal today:
/pizza for ordering pizza- 5$.
/toast for ordering toast- 3$.
/falafel for ordering falafel- 5$.
We are waiting for your order!""")
    bot.send_message(message.chat.id, "Notice that you can order only once!")


# in case of commands- /pizza & /toast & /falafel- add the info to the right client id's and check if already ordered!
@bot.message_handler(commands=['pizza', 'toast', 'falafel'])
def ordering_dish(message):
    # finding user id in the ordered id's- deny ordering again
    if message.chat.id in conf_order_ids:
        bot.reply_to(message, "Sorry, " + str(
            message.chat.first_name) + ", you already ordered today, please wait patiently for tomorrow :)")

    # adding user's id to conf_order_ids, so we know he already ordered+adding the order details to cust_ord_list
    else:
        for item in cust_ord_list:
            if item[0] == message.chat.id:
                item[1] = message.text[1:int(len(message.text))]
                print("chose dish " + str(item[0]) + " " + str(item[1]))
                topping_keyboard_def(message, "Choose topping:")


# defining the keyboard of the toppings
def topping_keyboard_def(message, reply):
    markup = telebot.types.ReplyKeyboardMarkup()
    tomato = telebot.types.KeyboardButton('/tomato')
    onion = telebot.types.KeyboardButton('/onion')
    olives = telebot.types.KeyboardButton('/olives')
    mushrooms = telebot.types.KeyboardButton('/mushrooms')

    markup.row(tomato, onion)
    markup.row(olives, mushrooms)
    bot.reply_to(message, reply, reply_markup=markup)


# in case of commands of toppings- add the info to the right client id's and check if already ordered!
@bot.message_handler(commands=['tomato', 'onion', 'olives', 'mushrooms'])
def add_topping(message):
    if message.chat.id in conf_order_ids:
        bot.reply_to(message, "Sorry, " + str(
            message.chat.first_name) + ", you already ordered today, please wait patiently for tomorrow :)")
    else:
        for item in cust_ord_list:
            if item[0] == message.chat.id:
                if item[1] == "":
                    bot.reply_to(message,
                                 "First you need to choose what kind of meal do you want, /pizza, /toast or /falafel")
                else:
                    item[2] = message.text[1:int(len(message.text))]
                    conf_order_ids.append(message.chat.id)
                    bot.reply_to(message,
                                 str(message.chat.first_name) + ", Thanks for ordering!\n Our delivery is on it's way :)")
                    print("chose " + str(item[0]) + " " + str(item[1]) + " " + str(item[2]))
                    make_order(message.chat.id, str(item[1]), str(item[2]))


def make_order(id, dish, top):
    print("Chef, please start making " + str(id) + " order: \n" + dish + " with " + top + " as quickly as you can.")
    print("Order is ready!")


# in case any other unknown message
@bot.message_handler(regexp="[a-z]")
def handle_any_message(message):
    bot.reply_to(message, "I don't know what you're talking about.")


# the next 3 functions- threading treatment for cleaning the ordered list (conf_order_id) every midnight 00:00
def clearing_list():
    print("	Now you can order again :)")
    for item in cust_ord_list:
        print(item)
        item[1] = ""
        item[2] = ""
    return conf_order_ids.clear()


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_threaded(schedule_checker):
    job_thread = threading.Thread(target=schedule_checker)
    job_thread.daemon = True
    job_thread.start()


def main():
    # adding event to schedule-- CLEANING LIST
    schedule.every().day.at("20:31").do(clearing_list)

    # run_pending the event of schedule on new thread
    run_threaded(schedule_checker)

    bot.infinity_polling(timeout=10, long_polling_timeout=5)  # looking for message


if __name__ == '__main__':
    main()

# idOrd[idOrd.index(item)]=
# idOrd.append(["",""])
# ind = int(len(idOrd))
# idOrd[ind] = message.chat.id


# print("I'm on thread %s" % threading.current_thread()+" "+str(message.chat.first_name))
