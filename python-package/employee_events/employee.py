from employee_events.query_base import QueryBase


class Employee(QueryBase):
    name = "employee"

    def names(self):
        sql_query = f"""
        SELECT first_name || ' ' || last_name AS full_name, employee_id
                FROM {self.name}
                """
        
        return self.query(sql_query)

    def username(self, id):
        sql_query = f"""
        SELECT first_name || ' ' || last_name AS full_name
                FROM {self.name}
                WHERE employee_id = {id}
                """

        return self.query(sql_query)

    def model_data(self, id):
        query_string = f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """
        return self.pandas_query(query_string)