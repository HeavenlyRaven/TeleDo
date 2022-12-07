import telebot
import csv

with open('token.txt', 'r') as token_file:
    TOKEN = token_file.read()

bot = telebot.TeleBot(TOKEN)


def add_item(user_id, item):
    with open(f"TODO/{user_id}/tasks.csv", 'r+', newline='') as tasks_file:
        # Для номера новой задачи выбираем номер последней задачи + 1
        data = list(csv.DictReader(tasks_file))
        if data:
            new_id = int(data[-1]['id'])+1
        else:
            new_id = 1
        csv.DictWriter(tasks_file, fieldnames=('id', 'description')).writerow({'id': new_id, 'description': item})
    bot.send_message(user_id, f"Задача {item} была успешно добавлена в ваш список под номером {new_id}.")


def show_all_items(user_id):
    task_list = ""
    with open(f"TODO/{user_id}/tasks.csv", 'r', newline='') as tasks_file:
        reader = csv.DictReader(tasks_file)
        for row in reader:
            task_list += f"{row['id']}, {row['description']}\n"
    if task_list:
        bot.send_message(user_id, task_list)
    else:
        bot.send_message(user_id, "У вас еще нет ни одной задачи в списке. Для того, чтобы добавить задачу, "
                                  "воспользуйтесь командой /new_item")


def delete_item(user_id, item_id):
    new_data = []
    found = False
    with open(f"TODO/{user_id}/tasks.csv", 'r', newline='') as inp:
        for row in csv.DictReader(inp):
            if row['id'] == item_id:
                found = True
            else:
                new_data.append(row)
    if found:
        with open(f"TODO/{user_id}/tasks.csv", 'w', newline='') as out:
            writer = csv.DictWriter(out, fieldnames=('id', 'description'))
            writer.writeheader()
            writer.writerows(new_data)
        bot.send_message(user_id, f"Задача с номером {item_id} была успешно удалена из вашего списка.")
    else:
        bot.send_message(user_id, f"Задачи с номером {item_id} нет в вашем списке.")


def refresh_tasks(user_id):
    new_data = []
    with open(f"TODO/{user_id}/tasks.csv", 'r', newline='') as inp:
        for i, row in enumerate(csv.DictReader(inp), 1):
            row['id'] = i
            new_data.append(row)
    with open(f"TODO/{user_id}/tasks.csv", 'w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=('id', 'description'))
        writer.writeheader()
        writer.writerows(new_data)
    bot.send_message(user_id, f"Номера ваших задач были успешно обновлены.")
