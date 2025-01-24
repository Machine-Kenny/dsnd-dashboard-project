from fasthtml.common import H1, Div, FastHTML, serve
import matplotlib.pyplot as plt

from employee_events import Employee, Team
from utils import load_model
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable
from combined_components import FormGroup, CombinedComponent


class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(model.name)


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model, *args, **kwargs):
        data = model.event_counts(entity_id)
        data = data.fillna(0)
        data = data.set_index("event_date")
        data = data.sort_index()
        data = data.cumsum()
        data.columns = ["Positive", "Negative"]
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        self.set_axis_styling(ax)
        ax.set_title(f"{model.name} Events Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Event Count")


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model, **kwargs):
        data = model.model_data(entity_id)
        prob = self.predictor.predict_proba(data)
        prob = prob[:, 1]
        if model.name == "team":
            pred = prob.mean()
        else:
            pred = prob[0]

        fig, ax = plt.subplots()

        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax)


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]

    outer_div_type = Div(cls="grid")


class NotesTable(DataTable):
    def component_data(self, entity_id, model, **kwargs):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name="profile_type",
            hx_get="/update_dropdown",
            hx_target="#selector",
        ),
        ReportDropdown(id="selector", name="user-selection"),
    ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app = FastHTML()

report = Report()


@app.get("/")
def home(r):
    return report("3", Employee())


# @app.get('/employee/{id:int}')
# def employee(r, id):
#     return report(id, Employee())


@app.get("/employee/{id}")
def employee(r, id: str):
    return report(id, Employee())


# @app.get('/team/{id:int}')
# def team(r, id):
#     return report(id, Team())


@app.get("/team/{id}")
def team(r, id: str):
    return report(id, Team())


# @app.get('/update_dropdown{r}')
# def update_dropdown(r):
#     dropdown = DashboardFilters.children[1]
#     print('PARAM', r.query_params['profile_type'])
#     if r.query_params['profile_type'] == 'Team':
#         return dropdown(None, Team())
#     elif r.query_params['profile_type'] == 'Employee':
#         return dropdown(None, Employee())


@app.get("/update_dropdown")
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params.get("profile_type")
    if not profile_type:
        raise ValueError("Profile type is required.")

    print("PARAM", profile_type)  # Debugging

    if profile_type == "Team":
        return dropdown(None, Team())
    elif profile_type == "Employee":
        return dropdown(None, Employee())


# @app.post('/update_data')
# async def update_data(r):
#     from fasthtml.common import RedirectResponse
#     data = await r.form()
#     profile_type = data._dict['profile_type']
#     id = data._dict['user-selection']
#     if profile_type == 'Employee':
#         return RedirectResponse(f"/employee/{id}", status_code=303)
#     elif profile_type == 'Team':
#         return RedirectResponse(f"/team/{id}", status_code=303)


@app.post("/update_data")
async def update_data(r):
    from fasthtml.common import RedirectResponse

    data = await r.form()
    profile_type = data._dict["profile_type"]
    id = data._dict.get(
        "user-selection"
    )  # Use `get` to avoid KeyError if `user-selection` is missing
    if not id:
        raise ValueError("Invalid ID selected.")  # Validate ID early

    if profile_type == "Employee":
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == "Team":
        return RedirectResponse(f"/team/{id}", status_code=303)


serve()
