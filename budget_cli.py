#!/usr/bin/env python3
"""
Command line interface for interacting with budget.py
"""
import sys
import budget


def get_input(message, type_expected=None):
    """
    prompts the user with the given message and then waits for their response. If the type_expected argument is
    passed this function will attempt to convert the input to the given type. If it cannot be converted it will
    prompt the user to re-enter a value.
    :param message: message to display to the user.
    :param type_expected: type of input the calling function expects.
    :return: the input of the type_expected type, if supplied, and a string if not.
    """
    i = input(message)
    if type_expected == 'int':
        try:
            i = int(i)
        except ValueError:
            # recursively call this function and then return the result.
            return get_input("Please enter a number: ", type_expected)
    return i


def calc_budget(money):
    """
    Calculates the fortnightly budget and displays it in the terminal
    :param money: base money to deduct the expenses from.
    """
    pay, deduc, nondeduc = budget.calculate_budget(money)
    print('£%s left over' % str(pay / 100))
    if deduc:
        print("Deductions: ")
        for val in deduc:
            print(val['title'], val['cost'] / 100)
    if nondeduc:
        print("Not enough money: ")
        for val in nondeduc:
            print(val['title'], end=' ')
    print('\n')


def display_items(field=None, value=None, t_name=None):
    """
    searches for the items by the given value and then prints the items sorted by their priority to the console. If
    the field and value are not supplied it wil get all of the items in the table.
    :param field: database field to search in
    :param value: value to search for
    :param t_name: table to search
    """
    items = search_items(field, value, t_name)

    # sort the list with the highest priority at the top
    items = sorted(items, key=lambda x: x['priority'], reverse=True)

    for val in items:
        print("%s Title = %s, cost = %s" % (val['priority'], val['title'],  val['cost']))


def search_items(field=None, value=None, t_name=None):
    """
    Searches the database field for the given value and returns the results as a list. If no field and no value
    are passed then it will return all of the entries.
    :param field: database field.
    :param value: value to search for.
    :param t_name: table to search in.
    :return: a list of all matching items.
    """
    if field is None and value is None:
        # search all
        li = budget.search_item(t_name=t_name)
    else:
        li = budget.search_item(field, value, t_name=t_name)
    return li


def add_item(t_name=None):
    """
    Gets the values of the event from the user and then passes them to the database to be saved.
    :param t_name: name of the table to save the event to.
    :return: None
    """
    e_dict = {}
    for val in ['title', 'interval']:
        i = get_input(val)
        if i:
            e_dict[val] = i
    for val in ['cost', 'priority']:
        i = get_input(val, 'int')
        if i:
            e_dict[val] = i

    budget.add_item(title=e_dict['title'], cost=e_dict['cost'],
                    priority=e_dict['priority'], interval=e_dict['interval'], t_name=t_name)


def delete_item(name):
    """
    deletes an item from the database. If more than one entry has that name it will then ask the user whether to
    delete them all or a single one.
    :param name: name of the item to delete
    :return: None
    """
    items = budget.search_item('title', name)
    if len(items) > 1:
        print('Multiple items found with that name')
        return
    if len(items) == 0:
        print('No items found with that name')
        return
    if len(items) == 1:
        budget.delete_item('title', name)

"""
Endless loop that processes the user's input. The following are valid inputs:
    'calc' -- calculates the fortnightly budget.
    'add' -- adds an event to the database.
    'delete' -- deletes an event from the database.
    'items' -- lists all the items in the database.
    '-help' -- displays the help text."""
while True:
    cmd = get_input('>> ')

    if cmd == 'calc':
        mon = int(get_input('Enter fortnightly pay :')) * 100
        calc_budget(mon)
    elif cmd == 'add':
        add_item()
    elif cmd == 'delete':
        n = get_input("Name of item to delete: ")
        delete_item(n)
    elif cmd == 'items':
        display_items()
    elif cmd == 'x':
        print('Exiting . . .')
        sys.exit(1)
    elif cmd == '-help':
        print('calc - calculates the fortnightly budget \n add - adds an item to the database'
              ' \n delete - not implemented \n x - exits the program')
    else:
        print('Unrecognised command')
