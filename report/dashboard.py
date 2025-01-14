from fasthtml.common import *
import matplotlib.pyplot as plt
import sys
import os

# Adding python-package to PYTHONPATH
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python-package')))



# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE
from employee_events import QueryBase, Employee, Team

# import the load_model function from the utils.py file
#### YOUR CODE HERE
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
#### YOUR CODE HERE
class ReportDropdown(Dropdown):
    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE
    def build_component(self, entity_id, model):
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        #### YOUR CODE HERE
        label = model.name
        
        # Return the output from the
        # parent class's build_component method
        #### YOUR CODE HERE
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE
    def component_data(self, entity_id, model):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        return model.names()


# Create a subclass of base_components/BaseComponent
# called `Header`
#### YOUR CODE HERE
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE
    def build_component(self, entity_id, model):
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        #### YOUR CODE HERE
        return H1(model.name)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
#### YOUR CODE HERE
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    #### YOUR CODE HERE
    def visualization(self, entity_id, model, *args, **kwargs):
    

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        #### YOUR CODE HERE
        breakpoint()
        data = model.event_counts(entity_id)
        
        # Use the pandas .fillna method to fill nulls with 0
        #### YOUR CODE HERE
        data = data.fillna(0)
        
        # User the pandas .set_index method to set
        # the date column as the index
        #### YOUR CODE HERE
        data = data.set_index('event_date')

        
        # Sort the index
        #### YOUR CODE HERE
        data = data.sort_index()
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        #### YOUR CODE HERE
        data = data.cumsum()
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        #### YOUR CODE HERE
        data.columns = ['Positive', 'Negative']
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        #### YOUR CODE HERE
        fig, ax = plt.subplots()
        
        # call the .plot method for the
        # cumulative counts dataframe
        #### YOUR CODE HERE
        data.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax)
        
        # Set title and labels for x and y axis
        #### YOUR CODE HERE
        ax.set_title(f"{model.name} Events Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Event Count")


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE
class BarChart(MatplotlibViz):

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE
    breakpoint()
    def visualization(self, entity_id, model, **kwargs):

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE
        data = model.model_data(entity_id)
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE
        prob = self.predictor.predict_proba(data)
        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE
        prob = prob[:, 1]
        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE
        if model.name == "team":
            pred = prob.mean()
        else:
            pred = prob[0]
        

        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE -- answered up in the else statement 
        
        
        # Initialize a matplotlib subplot
        #### YOUR CODE HERE
        fig, ax = plt.subplots()
        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE
        self.set_axis_styling(ax)
 
# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
#### YOUR CODE HERE
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE
    children = [
        LineChart(),
        BarChart()
    ]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
#### YOUR CODE HERE
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE
    def component_data(self, entity_id, model, **kwargs):
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        #### YOUR CODE HERE
        return model.notes(entity_id)
    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize a fasthtml app 
#### YOUR CODE HERE
app = FastHTML()


# Initialize the `Report` class
#### YOUR CODE HERE
report = Report()


# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE
@app.get('/')
def home(r):

    # Call the initialized report
    # pass None and an instance
    # of the QueryBase class as arguments
    # Return the result
    #### YOUR CODE HERE
    return report("1", Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
#### YOUR CODE HERE
@app.get('/employee/{id:str}')
def employee(r, id):

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    return report(id, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
#### YOUR CODE HERE
@app.get('/team/{id:str}')
def team(r, id):

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    #### YOUR CODE HERE
    return report(id, Team())


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    
    
#Execute the code
serve()