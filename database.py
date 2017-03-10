#!/usr/bin/env python3
"""
This file controls all the interaction with the database.
"""
from tinydb import TinyDB, where


class Connection(object):
    """
    Connection object acts as the interface between the tinyDB and the library
    """

    def __init__(self, loc):
        self.conn = TinyDB(loc)

    def _get_table(self, t_name=None):
        """
        Returns a database table. If the t_name is not supplied it will return the default table.
        :param t_name: name of table to return.
        :return: tinydb.database.Table
        """
        if t_name is None:
            table = self.conn.table()
        else:
            table = self.conn.table(t_name)

        return table

    def insert(self, data, t_name=None):
        """
        Inserts an item into the given table of the database. If t_name is not supplied it will insert the item
        into the default table.

        :param data: item to insert.
        :type data: dictionary
        :param t_name: name of table to insert into.
        """
        if not isinstance(data, dict):
            raise TypeError("Data is not of type dict.")

        table = self._get_table(t_name)
        return table.insert(data)

    def search(self, field=None, value=None, t_name=None):
        """
        Searches the database for the field for the given value. If field and value are not supplied it will return
        all items in the table.
        :param field: database field to search.
        :param value: value to search for.
        :param t_name: table to search in.
        :return: a list of matching items
        """
        table = self._get_table(t_name)

        if field is None and value is None:
            return table.all()
        if field is None or value is None:
            raise ValueError("Both field and value must be supplied, or none of them supplied.")

        return table.search(where(field) == value)

    def delete(self, field, value, t_name=None):
        """
        Deletes an item from the database.
        :param field: database field to search.
        :param value: value to search for
        :param t_name: table to delete from
        """
        table = self._get_table(t_name)
        table.remove(where(field) == value)


def main():
    """
    Used for testing purposes
    """
    pass


if __name__ == '__main__':
    main()
