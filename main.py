import os
import bot_commands as commands
bot = commands.bot

COMMAND_MAP = {'new_item': commands.add_item,
               'all': commands.show_all_items,
               'delete': commands.delete_item,
               'refresh': commands.refresh_tasks}

# Список команд без параметров
NP_COMMANDS = ('all', 'refresh')

INFO = """Описание функций бота:

/start - идентификация пользователя
/new_item <название задачи> - добавить новую задачу
/all - посмотреть список задач в формате “id, описание задачи”
/delete <номер задачи> - удалить задачу с заданным номером
/refresh - изменить номера списка задач на номера от 1 по порядку
/info - информация о боте"""


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f"Добро пожаловать, {message.from_user.first_name}")
    if not os.path.exists(f"TODO/{user_id}"):
        # Отсылаем пользователю информацию о боте, если он ещё не был инициализорван
        bot.send_message(user_id, INFO)
        os.mkdir(f"TODO/{user_id}")
        with open(f"TODO/{user_id}/tasks.csv", 'w', newline='') as tasks_file:
            # Добавляем заголовок
            commands.csv.writer(tasks_file).writerow(("id", "description"))


@bot.message_handler(commands=['info'])
def info_handler(message):
    bot.send_message(message.from_user.id, INFO)


@bot.message_handler(commands=COMMAND_MAP.keys())
def command_handler(message):
    user_id = message.from_user.id
    if os.path.exists(f"TODO/{user_id}"):
        params = message.text.split(' ', 1)
        command_name = params.pop(0)[1:]
        if command_name in NP_COMMANDS:
            COMMAND_MAP[command_name](user_id)
        else:
            try:
                COMMAND_MAP[command_name](user_id, *params)
            except TypeError:
                bot.send_message(user_id, "Команда была использована неправильно. Воспользуйтесь командой /info, "
                                          "чтобы получить подсказку")
    else:
        bot.send_message(user_id, "Пользователь не инициализирован. Пожалуйста, воспользуйтесь командой /start")


bot.polling()
