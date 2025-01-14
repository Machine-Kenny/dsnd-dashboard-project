# Import the QueryBase class
#### YOUR CODE HERE
from employee_events.query_base import QueryBase

# Import dependencies needed for sql execution
# from the `sql_execution` module
#### YOUR CODE HERE
from employee_events.sql_execution import QueryMixin

# Define a subclass of QueryBase
# called Employee
#### YOUR CODE HERE
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    #### YOUR CODE HERE
    name = "employee"

    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
    def names(self):
        
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
        #### YOUR CODE HERE
        sql_query = f"""
        SELECT first_name || ' ' || last_name AS full_name, employee_id
                FROM {self.name}
                """
        
        return self.query(sql_query)

    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE
    def username(self, id):
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
        #### YOUR CODE HERE
        sql_query = f"""
        SELECT first_name || ' ' || last_name AS full_name
                FROM {self.name}
                WHERE employee_id = {id}
                """

        return self.query(sql_query)


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE
    def model_data(self, id):
        query_string = f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """
        # Execute the query and return a Pandas DataFrame
        return self.pandas_query(query_string)
    
    #def model_data(self, id):

        #return f"""
                    #SELECT SUM(positive_events) positive_events
                         #, SUM(negative_events) negative_events
                    #FROM {self.name}
                    #JOIN employee_events
                        #USING({self.name}_id)
                    #WHERE {self.name}.{self.name}_id = {id}
                #"""