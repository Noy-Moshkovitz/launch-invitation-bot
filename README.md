# launch-invitation-bot
Search for "noy'splace" in the telegram

## Keywords
Dish = pizza, toast or falafel
Topping = tomatoes, onions, olives, mushrooms


## At a glance
1. The client starts the call with the bot using / start.
2. The bot offers the customer 3 options for a meal: pizza, toast or falafel.
3. The customer chooses one of the options.
4. The bot offers the customer using a unique keyboard to choose an addition to his dish - tomatoes, onions, olives, mushrooms.
5. The customer chooses one of the options.
6. The bot sends an instruction to the kitchen to prepare the order and it is sent to the customer successfully.

## End cases
- Only a customer who started at start can continue to select a dose. A kind of "registration" to be a customer of a restaurant.
- Customer who chose the dish (before choosing an addition) and regretted- The order is updated for the new decision.
- Customer who tried to choose a supplement before choosing a portion- will not receive anything and will receive a referral to choose a portion because there is nothing to do with a supplement without a portion (:
- A customer who chose a dish and then chose a supplement and received a message that the order is ready and sent to him - will not be able to order again until midnight.
- It is possible to place an order for several people at the same time.
- The system remembers the customer, and can the next day start straight from choosing a dose.


## Tools used-
- Importing a telebot telegram from the link https://github.com/eternnoir/pyTelegramBotAPI
- Import threading, schedule, time in order to implement resetting the customer list at midnight. Runs in a separate procession to check every second whether it has arrived at 00:00.
- schedule- From the link https://github.com/mrhwick/schedule
- threading- Built in Python, from the link https://docs.python.org/3/library/threading.html

## Explanation of variables:
*bot* = Bot definition.
*conf_order_ids* = Confirmtioned orderd id's - This is a list containing all the ids of customers who have already ordered today. I entered an ID number only when the order was actually completed and delivered to the chef.
*cust_ord_list* = Costumer orders id's - This is a list containing lists. Each item in this list contains the customer's order details. Used as a DB.
### for example:
- cust_ord_list = [["3965895312", "toast", "olives"], ["310987612", "falafel", "onion"], ["3112312312", "pizza", "tomato"]]
- conf_order_ids = ["3112312312", "310987612", "3965895312"]


## Explanation per function:
(There are comments inside the code for each function. I know they are not in Python documentation format, sorry in advance. I preferred to focus on working code and perfect.)

### send_welcome
If you type a help or start command:
Checks if the customer exists in the system and if not - adds it.
Sends "Welcome" and the "Pizza Toast or Falafel" menu.
Sends one-time order restriction.

### ordering_dish
If you typed pizza or toast or falafel:
Checks in the list of orders already completed conf_order_ids Whether this user has already placed an order.
If so - send him that "It is not possible to make 2 orders a day."
If not - check that this person registered via start and it exists in our db.
And if so - saves the customer's dish selection along with his id.
And sends him "choose extra onion tomatoes, onions or mushrooms"
And uploads a unique keyboard (by calling the toppingsKeyboardDef function) to select the desired add-on.

### toppingsKeyboardDef
If someone chose a dish in the previous function - we want him to choose an addition.
A function that defines a special keyboard with the possible additions.

### add_topping
If you typed the Onion command or tomato or olives or mashrooms:
Checks in the list of orders already completed conf_order_ids Whether this user has already placed an order.
If so - send him that "It is not possible to make 2 orders a day."
If not - check that this person registered via start and it exists in our db.
And if so, register - check that you have chosen a dish first. After all, you need a dish for a side dish.
If you do not choose a dish - tell him to "choose a dish first"
And if so, choose a dose - and save the customer's extra choice along with his dose and ID.
Sends him "Order paid, thank you for ordering from us."
Sends the invitation to the chef in the make_order function.

### make_order:
Prints the chef the exact order, and he executes it.

### handle_any_message
Handles any other message in English that is not the commands the bot knows.

### The following functions:
- clearing_list
- schedule_checker
- run_threaded

These are 3 functions that take care of another process so that we can initialize the list every night at 12.

### clearing_list
Defines the new process that will run. Gets the name of the function that needs to be run.

### schedule_checker
This is the function he wanted in the procession to the world. It basically instructs the schedule to check if there are any tasks that need to run a constant check every second.

### clearing_list
This is the function with the task to reset the list. Ran only once a day.

### main
- I put the task in the schedule at 00:00.
- I actually registered clearing_list as a 00:00 task.
- And I ran the bot constantly with polling.