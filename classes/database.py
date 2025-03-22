from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, insert, select, update
from typing import Any


class DatabaseEngine(object):
    def __init__(self, connection_string: str = "postgresql:///postgres"):
        """
        Initialize the Engine instance by setting up SQLAlchemy components.

        This includes automapping of the database schema, creating the engine, and
        reflecting the database tables.

        Args:
            connection_string (str): The database connection string. Defaults to "postgresql:///postgres".
        """
        self.base = automap_base()
        self.engine = create_engine(connection_string, convert_unicode=True)
        self.base.prepare(self.engine, reflect=True)
        self.tables = self.base.classes
        self.session = None

    def start_session(self):
        """
        Start a new SQLAlchemy session using the current engine.
        """
        self.session = Session(self.engine)

    def end_session(self):
        """
        Close the current SQLAlchemy session.
        """
        self.session.close()

    def get_session(self):
        """
        Retrieve the current SQLAlchemy session.

        Returns:
            Session: The active SQLAlchemy session.
        """
        return self.session

    def get_tables(self):
        """
        Retrieve the automapped table classes from the database.

        Returns:
            dict or list: The mapped table classes available in the database.
        """
        return self.tables

    def get_table(self, name: str = None):
        """
        Retrieve a table class by its name.

        Args:
            name (str): The name of the table to retrieve.

        Raises:
            ValueError: If no name is provided or if the table is not found.
            AttributeError: If the SQLAlchemy session has not been started.

        Returns:
            class: The table class corresponding to the given name.
        """
        if not name:
            raise ValueError("Invalid Table")
        if not self.session:
            raise AttributeError("No SQLAlchemy Session")
        for table in self.tables:
            if table.__name__ == name:
                return table
        raise ValueError("Invalid Table")

    def commit(self):
        """
        Commit the current transaction.
        """
        self.session.commit()

    def rollback(self):
        """
        Roll back the current transaction.
        """
        self.session.rollback()

    def update(self, table_name: str = None, row_id: int = None, values: dict = None):
        """
        Update an existing record in the specified table with new values.

        Args:
            table_name (str): The name of the table where the update will occur.
            row_id (int): The ID of the row to update.
            values (dict): A dictionary of column names and their new values.

        Raises:
            ValueError: If the provided values are invalid or row_id is not a valid integer.
            ValueError: If the table_name is invalid (handled within get_table).
        """
        if not values or not isinstance(values, dict):
            raise ValueError("Invalid Update values!")
        if not row_id or not isinstance(row_id, int):
            raise ValueError("Invalid Row ID!")
        table = self.get_table(name=table_name)
        self.session.execute(update(table).where(
            table.id == row_id).values(**values))

    def insert(self, table_name: str = None, values: dict = None):
        """
        Insert a new record into the specified table or update it if it already exists.

        This function first checks if a record with the same values already exists.
        If found, it updates the existing record; otherwise, it inserts a new record.
        Finally, it commits the transaction.

        Args:
            table_name (str): The name of the table where the record will be inserted.
            values (dict): A dictionary of column names and their corresponding values.

        Raises:
            ValueError: If the provided values are invalid or table_name is invalid (handled within get_table).
        """
        if not values or not isinstance(values, dict):
            raise ValueError("Invalid Insert values!")
        table = self.get_table(name=table_name)
        row = self.session.query(table).filter_by(**values).first()
        if row:
            row_id = row.id
            self.update(table_name=table_name, row_id=row_id, values=values)
        else:
            self.session.execute(insert(table).values(**values))
        self.session.commit()

    def get_all(self, table_name: str = None):
        """
        Retrieve all records from the specified table.

        Args:
            table_name (str): The name of the table to query.

        Raises:
            ValueError: If the table_name is invalid (handled within get_table).

        Returns:
            list: A list of all records in the table.
        """
        table = self.get_table(name=table_name)
        result = self.session.query(table).all()
        return result

    def get_by_id(self, table_name: str = None, row_id: int = None):
        """
        Retrieve a single record from the specified table by its ID.

        Args:
            table_name (str): The name of the table to query.
            row_id (int): The ID of the record to retrieve.

        Raises:
            ValueError: If the table_name is invalid (handled within get_table).

        Returns:
            object: The record that matches the given ID, or None if not found.
        """
        table = self.get_table(name=table_name)
        result = self.session.query(table).filter_by(id=row_id).first()
        return result

    def get_by_column_value(self, table_name: str = None, column_name: str = None, column_value: Any = None):
        """
        Retrieve all records from the specified table where a column matches a given value.

        Args:
            table_name (str): The name of the table to query.
            column_name (str): The name of the column to filter by.
            column_value: The value to match in the specified column.

        Raises:
            ValueError: If the table_name is invalid (handled within get_table).

        Returns:
            list: A list of records that match the given column value.
        """
        table = self.get_table(name=table_name)
        column = table.__table__.c[column_name]
        result = self.session.query(table).filter(column == column_value).all()
        return result
