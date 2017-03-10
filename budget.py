#!/usr/bin/env python3

import argparse
from collections import namedtuple
from database import Connection

db = Connection('items.json')


def add_item(title, cost, priority=0, interval='fortnightly', t_name=None):
    """
    Constructs a dictionary from the given parameters and then inserts it into the database.
    :param title: title of the item. String
    :param cost: cost of the item. Int
    :param priority: priority of the item. Int between 0-10
    :param interval: how often the item should be paid. String. Either 'weekly', 'fortnightly', or 'monthly'
    :param t_name: name of table to insert the item into.
    """
    item = {'title': title, 'cost': cost, 'priority': priority, 'interval': interval}
    db.insert(item, t_name)


def search_item(field=None, value=None, t_name=None):
    """
    searches the database for the given parameters. If none are supplied then it will return all of the items in the
    given table.
    :param field: the database field to search for. For example, 'title' or 'priority'
    :param value: value of the given field.
    :param t_name: name of the table to search in.
    :return: a list containing all of the results
    """

    return db.search(field, value, t_name)


def delete_item(field, value, t_name=None):
    """
    Deletes an item matching the value from the database.
    :param field: database field to match the value to.
    :param value: value to search for
    :param t_name: table to search in.
    """
    db.delete(field, value, t_name)


def calculate_budget(pay):
    """
    sorts the items in the list by priority (highest priority first) and then loops through the list deducting the
    items cost from the given pay.

    :param pay: base pay for that interval
    :return: a named tuple with the following values:
                 - pay: pay after all of the deductions have been made.
                 - deducted: list of items that have been deducted from the pay.
                 - non-deducted: list of items that have not been deducted from the pay.
    """
    Budget = namedtuple('Budget', 'pay, deducted, nondeduc')
    items = search_item()
    sorted_items = sorted(items, key=sort_dict, reverse=True)  # reversed so the highest priority is at the top
    deduc = []  # list of items that have been deducted from the pay
    nondeduc = []  # list of items that have NOT been deducted from the pay

    for pos, val in enumerate(sorted_items):
        if val['interval'] == 'monthly':
            deduct = int(val['cost'] / 3)
        else:
            deduct = val['cost']

        # no more money left. Add the current item and all of the following items to the nondeduc list
        if pay - deduct <= 0:
            nondeduc.extend(sorted_items[pos:])
            return Budget(pay, deduc, nondeduc)

        deduc.append(val)
        pay = pay - deduct
    
    return Budget(pay, deduc, nondeduc)


def sort_dict(item):
    """
    key used by the sorted function in the calculate_budget function to order the items by their priority.
    """
    return item['priority']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('pay', type=int, help='pay for the fortnight')

    args = parser.parse_args()

    # set the variables from arg parse
    base_pay = args.pay

    left_over, bought, remaining = calculate_budget(base_pay)
    # divided by 100 to convert to a decimal
    print("\nBase pay is £" + str(base_pay / 100))
    print("Money spent on items is £" + str((base_pay - left_over) / 100))
    print("Money left over is £" + str(left_over / 100))

if __name__ == '__main__':
    main()
