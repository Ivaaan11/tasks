import sqlite3
from os import system
from rich import print

system('cls')

connection = sqlite3.connect('tasks.db')
cursor = connection.cursor()



def sort_tasks():
    cursor.executescript(
'''
DROP TABLE IF EXISTS tasks_sorted;

CREATE TABLE tasks_sorted (
    name TEXT,
    commited INTEGER DEFAULT 0
);

INSERT INTO tasks_sorted (name, commited)
SELECT name, commited
FROM tasks;

DROP TABLE tasks;

ALTER TABLE tasks_sorted RENAME TO tasks;

''')

sort_tasks()


# the commands functional
def command():
    print('command: ', end='')
    ans = input()

    system('cls')

    if ans == 'q':
        command_list()
    elif ans == 'm':
        main_menu()
    elif ans == 'e':
        exit()
    

    elif ans[:4] == 'add ':
        cursor.execute('insert into tasks ( name ) values ( ? )', (ans[4:],))
        connection.commit()

    elif ans[:7] == 'delete ':
        sort_tasks()
        cursor.execute('select name from tasks')
        tasks = cursor.fetchall()
        try:
            cursor.execute('delete from tasks where name = ?', (tasks[int(ans[7:]) - 1]))
            connection.commit()
        except:
            main_menu(error='invalid id')
    
    elif ans[:7] == 'commit ':
        sort_tasks()
        cursor.execute('select name from tasks')
        tasks = cursor.fetchall()
        try:
            cursor.execute('update tasks set commited = not commited where name = ?', (tasks[int(ans[7:]) - 1]))
            connection.commit()
        except:
            main_menu(error='invalid id')


    else:
        main_menu(error='invalid command')
        

# main menu function
def main_menu(error: str = ''):
    if error:
        print(f'[red]{error}')

    print('Current tasks:')
    cursor.execute('select commited, name from tasks order by commited')
    tasks = cursor.fetchall()
    i = 1
    for task in tasks:
        color = 'white'
        if task[0] == 0: color = 'white'
        elif task[0] == 1: color = 'bright_black'

        print(f'  {i}.[{color}] {task[1]}')
        i += 1

    print('\ntype q to see all commands')
    command()


# shows the list of all commands
def command_list():
    print(
'''
add [task name] - adds a new task
delete [task id] - removes a task
commit [task id] - commits a task

q - list of all commands
m - go to main menu
e - exit the programm

''')
    command()


# running the programm
while 1:
    main_menu()


connection.close()
