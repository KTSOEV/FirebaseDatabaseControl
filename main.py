import os
import json
import click
import requests
from pyfiglet import Figlet
from pyautogui import typewrite
from colorama import Fore, Back, Style

prew = Figlet(font='slant')
database_url = 'https://<database>.firebaseio.com/'
database_keys = '.json?auth=<token>'
database_json = requests.get(database_url+database_keys).text
database_dict = json.loads(database_json)
choise = ''
parent = ''
child = ''

if os.name == 'nt':
    clear_command = 'cls'
else:
    clear_command = 'clear'
os.system(clear_command)
print(Fore.GREEN)

def RemoveParent():
    if(click.confirm(f'Are you sure you want to remove parent "{parent}"?', default=False)):
        requests.delete(f'{database_url}{parent}/{database_keys}')
        print('Removed')
        input()
def CreateChild():
    print('Enter child name or path and value \nAttention! If you are creating a child of string type, then put ". For example: "Ktsoev"')
    newChild = input('Name> ')
    childValue = input('Value> ')
    print(requests.put(f'{database_url}{parent}/{newChild}/{database_keys}', data=childValue))
    input()
def ChildOprions():
    print('Child options')
    print('1. Remove')
    print('2. Edit')
    choise = input('>')
    if(choise == '1'):
        if(click.confirm(f'Are you sure you want to remove child "{child}"?', default=False)):
            requests.delete(f'{database_url}{parent}/{child}/{database_keys}')
            print('Removed')
            input()
    elif(choise == '2'):
        print('Enter new name or path for child')
        new_child_name = input('>')
        old_child_value = requests.get(f'{database_url}{parent}/{child}/{database_keys}').text
        requests.delete(f'{database_url}{parent}/{child}/{database_keys}')
        requests.put(f'{database_url}{parent}/{new_child_name}/{database_keys}', data=old_child_value)
    else:
        print('ERROR: Invalid option')
        input()
def Childs():
    print(database_dict[parent])
    child = input('Select child: ')
    if(requests.get(f'{database_url}{parent}/{child}/{database_keys}').text != 'null'):
        ChildOprions()
    else:
        print('ERROR: Child does not exist')
        input()
def EditParent():
    print('Enter new name or path for parent')
    new_parent_name = input('>')
    old_parent_value = requests.get(f'{database_url}{parent}/{database_keys}').text
    requests.delete(f'{database_url}{parent}/{database_keys}')
    requests.put(f'{database_url}{new_parent_name}/{database_keys}', data=old_parent_value)
def ParentSettings():
    print('Parent options')
    print('1. Remove')
    print('2. Create new child')
    print('3. Childs')
    print('4. Edit')
    choise = input('>')
    if(choise == '1'):
        RemoveParent()
    elif(choise == '2'):
        CreateChild()
    elif(choise == '3'):
        Childs()
    elif(choise == '4'):
        EditParent()
    else:
        print('ERROR: Invalid option')
def Struct():
    print(database_dict.keys())
    print('Select Parent')
    parent = input("Parent> ")
    if(requests.get(f'{database_url}{parent}/{database_keys}').text != 'null'):
        ParentSettings()
    else:
        print('ERROR: Parent does not exist')
        input()

def JsonEdit():    
    print('Edit database json')
    database_json = requests.get(database_url+database_keys).text
    typewrite(database_json)
    new_json = input('>')
    requests.put(database_url + database_keys, data=new_json)
    return

while True:
    database_json = requests.get(database_url+database_keys).text
    database_dict = json.loads(database_json)
    print(prew.renderText('Firebase Database'))
    print('1. Struct')
    print('2. Json edit')
    print('3. Exit')
    choice = input('>')
    choice = choice.strip()
    if(choice == '1'):
        Struct()
    elif(choice == '2'):
        JsonEdit()
    elif(choice == '3'):
        exit()
    else:
        print('ERROR: Invalid option')
        input()
    os.system(clear_command)