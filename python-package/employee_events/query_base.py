from employee_events.sql_execution import QueryMixin


class QueryBase(QueryMixin):
    name = ""

    def names(self):
        return []

    def event_counts(self, id):
        query = f"""
            SELECT event_date, 
                   SUM(positive_events) AS positive_events, 
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events USING({self.name}_id)
            WHERE {self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date;
        """
        # Execute the query and return a pandas dataframe
        return self.pandas_query(query)

    def notes(self, id):
        query = f"""
            SELECT note_date, note
            FROM notes
            JOIN {self.name}
                ON {self.name}.{self.name}_id = notes.{self.name}_id
            WHERE {self.name}.{self.name}_id = {id}
            ORDER BY note_date;
        """
        return self.pandas_query(query)
