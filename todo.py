todos = []
import json


def maybeTodo():
    global todos
    try:
        with open('excellentsystemededonnees.json') as json_file:
            data = json.load(json_file)
            for p in data:
                todos.append(p)
    except:
        print("MERDE")


def addTodo(todo):
    global todos
    if len(todos) == 9:
        todos.append({"value": "finir mes autres todos", "color": 4})
    elif len(todos) < 10:
        todos.append({"value": todo[4:], "color": 4})
    syncTodos()

def checkTodo(cmd):
    global todos
    try:
        todos[int(cmd[5:6])]["color"] = 3
    except:
        print("MERDE")
    syncTodos()

def delTodo(cmd):
    global todos
    try:
        del(todos[int(cmd[4:5])])
    except:
        print("MERDE")
    syncTodos()

def delAllTodo():
    global todos
    todos = []
    syncTodos()

def syncTodos():
    global todos
    with open('excellentsystemededonnees.json', 'w') as outfile:
        json.dump(todos, outfile)