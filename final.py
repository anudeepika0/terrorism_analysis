# -----importing the libraries-----

import pandas as pd

import webbrowser

# !pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc 
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.graph_objects as go  
import plotly.express as px

# -----declaring global variables-----

app = dash.Dash()

project_name= None

# -----defining functions-----

def load_data():
    
    dataset_name = 'global_terror.csv'
    
    global df
    df = pd.read_csv(dataset_name)
    
    month = {
           "January":1,
           "February":2,
           "March":3,
           "April":4,
           "May":5,
           "June":6,
           "July":7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }
    global month_list
    month_list = [ {'label':key, 'value':value}  for key,value in month.items()]
    
    global date_list
    date_list = [ x for x in range(1, 32)]
    
    global region_list
    temp_list = sorted(df['region_txt'].unique().tolist())
    region_list = [ {'label':str(i), 'value':str(i)}  for i in temp_list]
    
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
  
  
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
  
  
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attack_type_list
    temp_list = sorted(df['attacktype1_txt'].unique().tolist())
    attack_type_list = [ {'label':str(i), 'value':str(i)}  for i in temp_list]
    
    global year_list
    year_list = sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict = { str(year) : str(year) for year in year_list}
    
    chart = {"Region":'region_txt', 
             "Country Attacked":'country_txt',
             "Terrorist Organisation":'gname', 
             "Target Nationality":'natlty1_txt', 
             "Target Type":'targtype1_txt', 
             "Type of Attack":'attacktype1_txt', 
             "Weapon Type":'weaptype1_txt'
             }
    global chart_list                            
    chart_list = [{"label":keys, "value":value} for keys, value in chart.items()]
  

def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')


def create_app_ui():
    main_layout = html.Div(
        [
            html.H1(id='main_title', children='Terrorism Analysis with Insights', 
                    style={ "color": "#2B411C",
                           "text-align": "center",
                           "text-decoration": "underline",
                           "text-shadow": "2px 2px 5px #5B7742",
                           "font-family": "Papyrus",
                           "background-color": "#A4AA88"}),
            dcc.Tabs(id="Tabs", value="Map",style={ "color": "#2B411C", "font-family": "Papyrus"}, children=[
                dcc.Tab(label="Map tool", id="Map tool",value="Map", children=[
                    dcc.Tabs(id = "subtabs", value = "WorldMap",style={ "color": "#2B411C", "font-family": "Papyrus"},children = [
                        dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                        dcc.Tab(label="India Map tool", id="India", value="IndiaMap")]),
                    html.Br(), 
                    html.Br(), 
                    dcc.Dropdown(id='month-dropdown', 
                                 options=month_list,
                                 placeholder='Select a Month',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='date-dropdown', 
                                 options=date_list,
                                 placeholder='Select a Day',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='region-dropdown', 
                                 options=region_list,
                                 placeholder='Select a Region',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='country-dropdown', 
                                 options=[{'label': 'All', 'value': 'All'}],
                                 placeholder='Select a Country',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='state-dropdown', 
                                 options=[{'label': 'All', 'value': 'All'}],
                                 placeholder='Select a State or Province',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='city-dropdown', 
                                 options=[{'label': 'All', 'value': 'All'}],
                                 placeholder='Select a City',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    dcc.Dropdown(id='attacktype-dropdown', 
                                 options=attack_type_list,
                                 placeholder='Select an Attack Type',
                                 multi=True,
                                 style={ "color": "#4C5D34"}),
                    html.H3(id='year_title', children='Select the Year(s):',
                            style={ "color": "#2B411C",
                                   "font-family": "Papyrus"}),
                    dcc.RangeSlider(id='year-slider',
                                    min=min(year_list),
                                    max=max(year_list),
                                    value=[min(year_list),max(year_list)],
                                    marks=year_dict,
                                    step=None),
                    html.Br()                    
                ]),
                dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
                    dcc.Tabs(id = "subtabs2", value = "WorldChart",style={ "color": "#2B411C", "font-family": "Papyrus"}, children = [
                        dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),
                        dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
                    html.Br(),
                    html.Br(),
                    dcc.Dropdown(id="chart-dropdown", 
                                 options = chart_list, 
                                 placeholder="Select option", 
                                 value = "region_txt",
                                 style={ "color": "#2B411C"}), 
                    html.Br(),
                    html.Hr(),
                    html.Br(),
                    
                    dcc.Input(id="search", placeholder=" Search Filter",
                              style={ "color": "#2B411C", 
                                     "font-family": "Papyrus",
                                     "margin-left": "15px"}),
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.H4(id='year_title_2', children='Select the Year(s):',
                            style={ "color": "#2B411C",
                                   "font-family": "Papyrus",
                                     "margin-left": "15px"}),
                    dcc.RangeSlider(id='year_slider2',
                                    min=min(year_list),
                                    max=max(year_list),
                                    value=[min(year_list),max(year_list)],
                                    marks=year_dict,
                                    step=None)                   
                ]),
            ]),
            dcc.Loading(dcc.Graph(id='graph-object', figure = go.Figure())),
            html.Br(),                                    
        ], 
        style= {'backgroundColor':'#A4AA88',
                   'background-image': 'url("https://5.imimg.com/data5/ES/LV/MY-1498574/camouflage-printed-fabrics-250x250.jpg")',
                   'background-repeat': 'repeat-x'}
        )
    
    return main_layout

    
@app.callback(
    dash.dependencies.Output('graph-object', 'figure'),
    [
    Input('Tabs','value'),
    Input('month-dropdown','value'),
    Input('date-dropdown','value'),
    Input('region-dropdown','value'),
    Input('country-dropdown','value'),
    Input('state-dropdown','value'),
    Input('city-dropdown','value'),
    Input('attacktype-dropdown','value'),
    Input('year-slider','value'),
    
    Input("chart-dropdown", "value"),
    Input("search", "value"),
    Input('year_slider2', 'value'),
    Input("subtabs2", "value")
    ]
    )

def update_app_ui(Tabs,month_value,date_value,region_value,country_value,state_value,city_value,attacktype_value,year_value,
                  chart_dropdown_value,search,chart_year_value,subtabs2):

    print("Data Type of tabs value = " , str(type(Tabs)))
    print("Value of tabs value = " , Tabs)
    
    fig = None
        
    if Tabs == "Map": 
        print("Data Type of month value = " , str(type(month_value)))
        print("Value of month value = " , month_value)
        
        print("Data Type of day value = " , str(type(date_value)))
        print("Value of day value = " , date_value)
        
        print("Data Type of region value = " , str(type(region_value)))
        print("Value of region value = " , region_value)
        
        print("Data Type of country value = " , str(type(country_value)))
        print("Value of country value = " , country_value)
        
        print("Data Type of state value = " , str(type(state_value)))
        print("Value of state value = " , state_value)
        
        print("Data Type of city value = " , str(type(city_value)))
        print("Value of city value = " , city_value)
        
        print("Data Type of attacktype value = " , str(type(attacktype_value)))
        print("Value of attacktype value = " , attacktype_value)
        
        print("Data Type of year value = " , str(type(year_value)))
        print("Value of year value = " , year_value)
    
        mapfigure = go.Figure()
        
        year_range = range(year_value[0], year_value[1]+1)
        new_df = df[df['iyear'].isin(year_range)]
    
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df = new_df[new_df["imonth"].isin(month_value)]
            else:
                new_df = new_df[new_df["imonth"].isin(month_value)&
                                (new_df["iday"].isin(date_value))]
        
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None :
                new_df = new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value == [] or state_value is None:
                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                    (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value == [] or city_value is None:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                        (new_df["country_txt"].isin(country_value))&
                                        (new_df["provstate"].isin(state_value))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                        (new_df["country_txt"].isin(country_value))&
                                        (new_df["provstate"].isin(state_value))&
                                        (new_df["city"].isin(city_value))]
                        
        if attacktype_value == [] or attacktype_value is None:
            pass
        else:
            new_df = new_df [new_df['attacktype1_txt'].isin(attacktype_value)] 

        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 
                                             'country_txt', 'region_txt', 'provstate', 'city', 
                                             'latitude', 'longitude', 'attacktype1_txt', 'nkill'])        
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
    
        mapfigure = px.scatter_mapbox(
                new_df,
                lat='latitude',
                lon='longitude',
                color='attacktype1_txt',
                hover_name="city", 
                hover_data=['iyear', 'imonth', 'iday', 
                            'country_txt', 'region_txt', 'provstate', 'city', 
                            'latitude', 'longitude', 'attacktype1_txt', 'nkill'],
                zoom=1)
    
        mapfigure.update_layout(
            mapbox_style='open-street-map',
            autosize=True,
            margin=dict(l=10,r=10,t=25,b=25))
        
        fig = mapfigure

    elif Tabs=="Chart":
        fig = None
        
        print("Data Type of chart value = " , str(type(chart_dropdown_value)))
        print("Value of chart value = " , chart_dropdown_value)
        
        print("Data Type of search value = " , str(type(search)))
        print("Value of search value = " , search)
        
        print("Data Type of year(chart) value = " , str(type(chart_year_value)))
        print("Value of year(chart) value = " , chart_year_value)
        
        print("Data Type of subtabs value = " , str(type(subtabs2)))
        print("Value of subtabs value = " , subtabs2)
        
        year_range_c = range(chart_year_value[0], chart_year_value[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &
                                (chart_df["country_txt"]=="India")]
            
        if chart_dropdown_value is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dropdown_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dropdown_value].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dropdown_value].value_counts().reset_index(name="count")
            
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dropdown_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
            
        fig = px.area(chart_df, x="iyear", y ="count", color = chart_dropdown_value)

    return fig


@app.callback(
    Output('date-dropdown','options'),
    [Input('month-dropdown','value')]
    )
def update_date(month):
    
    print('Data Type = ', str(type(month)))
    print('Value= ', str(month))
    
#    date_list = [ x  for x in range(1,32) ]
#    if month in [1,3,5,7,8,10,12]:
#       return [  { 'label':m, 'value':m } for m in date_list ] 
#    elif month in [4,6,9,11]:
#        return [  { 'label':m, 'value':m } for m in date_list[:-1] ] 
#    elif month == 2:
#        return [  { 'label':m, 'value':m } for m in date_list[:-2] ] 
#    else:
#        return []
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option  
    
@app.callback(
    [Output("region-dropdown", "value"),
    Output("region-dropdown", "disabled"),
    Output("country-dropdown", "value"),
    Output("country-dropdown", "disabled")],
    [Input("subtabs", "value")]
    )
def update_r(tab):
    
    print('Data Type = ', str(type(tab)))
    print('Value= ', str(tab))
    
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c
    
@app.callback(
    Output('country-dropdown','options'),
    [Input('region-dropdown','value')]
    )

def set_country_options (region_value):
    
    print('Data Type = ', str(type(region_value)))
    print('Value= ', str(region_value))
    
    option = []
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('state-dropdown','options'),
    [Input('country-dropdown','value')]
    )

def set_state_options (country_value):
    
    print('Data Type = ', str(type(country_value)))
    print('Value= ', str(country_value))
    
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dropdown','options'),
    [Input('state-dropdown','value')]
    )

def set_city_options (state_value):
    
    print('Data Type = ', str(type(state_value)))
    print('Value= ', str(state_value))
    
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]  


# -----main function-----

def main():
    
    load_data()
    open_browser()
    
    global project_name
    project_name = "Terrorism Analysis with Insights"
    
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    
    print('quit from running on server')
    app = None
    project_name = None

if __name__ == '__main__':
    main()
