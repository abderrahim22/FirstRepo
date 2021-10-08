# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
sites = spacex_df['Launch Site'].unique()
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                 dcc.Dropdown(id='site-dropdown', 
                                        options=[
                                                {'label': 'All Sites', 'value': 'All'},
                                                {'label': sites[0], 'value': sites[0]},
                                                {'label': sites[1], 'value': sites[1]},
                                                {'label': sites[2], 'value': sites[2]},
                                                {'label': sites[3], 'value': sites[3]}
                                                ],
                                        value='All',
                                        placeholder="Select a Launch Site here",
                                        searchable = True), 

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                              dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[spacex_df['Payload Mass (kg)'].min(),spacex_df['Payload Mass (kg)'].max()],
                                    marks = {0: {'label': '0'}, 2500:{'label': '2500'},5000:{'label': '5000'},7500:{'label': '7500'},10000:{'label': '10000'}}
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
	         Input(component_id='site-dropdown', component_property='value'))
def get_graph(entered_site):      
	        if entered_site == 'All':
	            figP = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches')
	            return figP
	        else:
	            data = spacex_df[0:0]
	            data= data[['class']]
	            data['class'] = data['class'].astype(int)
	            listR=[]
	            for launch_site,rate in zip(spacex_df['Launch Site'],spacex_df['class']):
	                if launch_site == entered_site:
	                    listR.append(rate)
	            data['class'] = listR
	            figP = px.pie(data, names='class', title=' Success and failed Launches for site %s'% entered_site)
	            return figP

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')
               ])

def get_graph_load(entered_site, payload_range):      
        if entered_site == 'All':
            scat_fig = px.scatter(spacex_df, x = "Payload Mass (kg)", y = "class", color = 'Booster Version Category', title='Correlation between Payload and Success for all Sites')
            return scat_fig
        else:
            
            data= spacex_df[0:0]
            data= data[['class','Payload Mass (kg)','Booster Version Category']]
            data['class'] = data['class'].astype(int)
            listR=[]
            mas_Load=[]
            color_lst=[]
            for launch_site,rate,mass,color in zip(spacex_df['Launch Site'],spacex_df['class'],spacex_df['Payload Mass (kg)'],spacex_df['Booster Version Category']):
                if launch_site == entered_site:
                    listR.append(rate)
                    mas_Load.append(mass)
                    color_lst.append(color)
            data['class'] = listR
            data['Payload Mass (kg)']=mas_Load
            data['Booster Version Category'] = color_lst
            scat_fig = px.scatter(data, x = "Payload Mass (kg)", y = "class", color = 'Booster Version Category', title='Correlation between Payload and Success for site %s'% entered_site)
            return scat_fig


# Run the app
if __name__ == '__main__':
    app.run_server()
