from employee_events.query_base import QueryBase


class Team(QueryBase):
    name = "team"

    def names(self):
        sql_query = f"""
            SELECT team_name, team_id
            FROM {self.name};
        """

        return self.query(sql_query)

    def username(self, id):
        sql_query = f"""
            SELECT team_name
            FROM {self.name}
            WHERE team_id = {id};
        """

        return self.query(sql_query)

    def model_data(self, id):
        query = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        return self.pandas_query(query)
