from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px


class CraftRecipie(object):

    ALLOWED_BUILDERS = ["any", "Developer", "Designer", "Team Lead"]

    def __init__(
        self, name, build_time, ingredients=None, builder="any", output_quantity=1
    ):
        if builder not in CraftRecipie.ALLOWED_BUILDERS:
            builder = "any"
        self.ingredients = ingredients or []
        self.name = name
        self.build_time = build_time or 0
        self.builder = builder
        self.output_quantity = output_quantity

        if ingredients is None:
            self.recipie_type = "base_component"
        elif self.builder == "Team Lead":
            self.recipie_type = "module"
        elif self.builder != "any":
            self.recipie_type = "element"
        else:
            self.recipie_type = "feature"
        

        
    def validate(self):

        if not self.ingredients or len(self.ingredients) == 0:
            return

        #for item in self.ingredients:
    
    def generate_tasks(self):
        # return pandas.dataframe with necessary tasks to product this and all pre-requisite parts
        print("Generating tasks: {}, Ingredients: {}".format(self.name, str(self.ingredients)))
        pd.set_option('display.width', 1000)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('max_colwidth', -1)
        pd.set_option('display.max_columns', 500)
        if not self.ingredients:
            return pd.DataFrame([dict(Task=self.name, Owner=self.builder, BuildTime=self.build_time, Requirements=None)])
        
        result = pd.DataFrame([dict(Task=self.name, Owner=self.builder, BuildTime=self.build_time, Requirements=self.ingredients)])        
        subtasks = [i.generate_tasks() for i in self.ingredients]
        result = result.append(subtasks)
        result.reset_index(drop=True, inplace=True)
        return result
    
    def __str__(self):

        output = "{}: Team: {}, Build Time: {}".format(self.name, self.builder, self.build_time)
        if self.ingredients:
            output += ", Ingredients: ["
            for item in self.ingredients:
                output += str(item) + ", "
            output=output.strip(", ")
            output += "]"
        return output
    
    def __repr__(self):
        return self.name
        
        



def main():

    now = datetime.now()
    df = pd.DataFrame(
        [
            dict(Task="Job A", Start=now, Finish=now + timedelta(days=10)),
            dict(
                Task="Job B",
                Start=now + timedelta(days=95),
                Finish=now + timedelta(days=121),
            ),
            dict(
                Task="Job C",
                Start=now + timedelta(days=45),
                Finish=now + timedelta(days=180),
            ),
        ]
    )
    # df['Finish'].max()
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
    fig.update_yaxes(
        autorange="reversed"
    )  # otherwise tasks are listed from the bottom up
    fig.show()

    # Developer components
    ui_component = CraftRecipie("UI Component", build_time=2, builder="Developer")
    video_component = CraftRecipie(
        "Video Component", build_time=14, builder="Developer"
    )
    backend_component = CraftRecipie(
        "Backend Component", build_time=4, builder="Developer"
    )
    network_component = CraftRecipie(
        "Network Component", build_time=6, builder="Developer"
    )

    # designer work
    blueprint_component = CraftRecipie(
        "Blueprint Component", build_time=2, builder="Designer"
    )
    graphics_component = CraftRecipie(
        "Graphics Component", build_time=4, builder="Designer"
    )
    wireframe_component = CraftRecipie(
        "Wireframe Component", builder="Designer", build_time=3
    )
    ui_element = CraftRecipie(
        "UI Element",
        build_time=6,
        builder="Designer",
        ingredients=[blueprint_component, graphics_component],
    )

    # team lead work
    backend_module = CraftRecipie(
        "Backend Module",
        builder="Team Lead",
        build_time=10,
        ingredients=[backend_component, network_component],
    )
    interface_module = CraftRecipie(
        "Interface Module",
        builder="Team Lead",
        build_time=15,
        ingredients=[ui_element, ui_element, wireframe_component],
    )
    frontend_module = CraftRecipie(
        "Frontend Module",
        builder="Team Lead",
        build_time=21,
        ingredients=[ui_element, interface_module],
    )
    video_playback_module = CraftRecipie(
        "Video Playback Module",
        builder="Team Lead",
        build_time=16,
        ingredients=[video_component, frontend_module, backend_module],
    )

    # Feature Recipies
    LandingPage = CraftRecipie(
        "Landing Page",
        build_time=0,
        ingredients=[
            ui_component,
            backend_module,
            blueprint_component,
            graphics_component,
        ],
    )
    VideoFunctionality = CraftRecipie(
        "Video Functionality",
        build_time=0,
        ingredients=[frontend_module, video_playback_module],
    )
    pd.set_option('display.width', 1000)
    print(LandingPage)
    print(LandingPage.generate_tasks())


if __name__ == "__main__":
    main()
