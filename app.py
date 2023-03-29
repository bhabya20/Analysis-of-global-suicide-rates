from dash import dash, dcc, html, Input, Output,dash_table
import dash_bootstrap_components as dbc
import pandas as pd 
import altair as alt 

# alt.data_transformers.enable('data_server')
suicide = pd.read_csv(r'../data/master.csv')
## suicide = pd.read_csv('data/master.csv')
suicide = suicide[suicide["year"]> 2005 ][:8000]

def get_data(country_selected):

    # suicide = pd.read_csv("data/master.csv")
    if not country_selected : 
        return suicide
    else :
        df = suicide[suicide['country']==country_selected]
        return df 


def get_age(country): 
    df = get_data(country)
    data = pd.DataFrame(df.groupby(["year","age"])['suicides/100k pop'].mean().round(2))
    data = data.reset_index()
    data['year']  = pd.to_datetime(data['year'], format='%Y')
    if not country :
        title_graph = "The suicide rate by age Worldwide"
    else : 
         title_graph = "The suicide rate by age in " +  country
    chart_graph = alt.Chart(data,width = 700, height = 350, title =title_graph).mark_line(point=True).encode(
    x=alt.X('year(year):T' , axis=alt.Axis(grid=False)),
    y=alt.Y('suicides/100k pop', title='Suicides per 100k people'),
    tooltip=['age','suicides/100k pop'], 
    color = "age"
    )
    bar = alt.Chart(data,width = 700, height = 300).mark_bar().encode(
            x=alt.X('sum(suicides/100k pop)', title = 'Sum of Suicide per 100k'),
            y=alt.Y('age', sort = 'x', title ="Age"),
            color = 'age',
                tooltip ='sum(suicides/100k pop)'
        )
    chart = chart_graph & bar
    return chart

def get_gender(country) :
    df = get_data(country)
    data = pd.DataFrame(df.groupby(["year","sex"])['suicides/100k pop'].mean().round(2))
    data = data.reset_index()
    data['year']  = pd.to_datetime(data['year'], format='%Y')
    if not country :
        title_graph = "The suicide rate by gender Worldwide"
    else : 
         title_graph = "The suicide rate by gender in " +  country
    chart_graph = alt.Chart(data, width = 700, height = 300, title = title_graph).mark_line(point=True).encode(
    x=alt.X('year(year):T', axis=alt.Axis(grid=False) , title ='Year'),
    y=alt.Y('suicides/100k pop', title='Suicides per 100k people'),
    tooltip=['sex','suicides/100k pop'], 
    color = "sex"
    ) 
    bar = alt.Chart(data,width = 700, height = 320).mark_bar().encode(
            x=alt.X( 'sum(suicides/100k pop)' , title = 'Sum of Suicide per 100k'),
            y=alt.Y('sex',sort = 'x', title ='Gender'),
            color = 'sex',
            tooltip ='sum(suicides/100k pop)'
        )
    chart = chart_graph & bar
    return chart

def get_gdp(country) :
    df = get_data(country)
    data = pd.DataFrame(df.groupby(["year","gdp_per_capita ($)"])['suicides/100k pop'].mean().round(2))
    data = data.reset_index()
    data['year']  = pd.to_datetime(data['year'], format='%Y')
    if not country :
        title_graph = ""
    else : 
         title_graph = "The suicide rate by gdp in " +  country
    chart_graph = alt.Chart(data,width = 700, height = 400, title = title_graph).mark_line(point=True).encode(
    x=alt.X('gdp_per_capita ($)' , axis=alt.Axis(grid=False), title ='Gdp Per capita ($)'),
    y=alt.Y('suicides/100k pop', title='Suicides per 100k people '),
    tooltip=['gdp_per_capita ($)','suicides/100k pop','year(year):T'], 
    color = alt.Color("year(year):T", title = 'Year')
    )
    # bar = alt.Chart(data,width = 600, height = 400).mark_bar().encode(
    #         x='sum(suicides/100k pop)',
    #         y=alt.Y('year', sort = 'x'),
    #         color = 'year',
    #          tooltip ='sum(suicides/100k pop)'
    #     )
    chart = chart_graph #& bar
    return chart

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div([
            
            dbc.Row([
      dbc.Col([
            # dbc.Jumbotron(dbc.Container(html.H1('Layout demo', className='display-3'), fluid=True), fluid=True),
            html.H1('Suicide Rate Analysis',
                style={
                    'backgroundColor': 'black',
                    'padding': 20,
                    'color': 'white',
                    #'margin-top': 20,
                    #'margin-bottom': 20,
                    'margin-left':15,
                    'text-align': 'center',
                    'font-size': '36px',
                    'border-radius': 1
                    })],width = 12)]),
         dbc.Row([ 
         dbc.Col([
            html.H5('Global Options'),
            html.Br(),
            
            # dcc.RadioItems(id = 'selection', options =['gender', 'age', "no"], inline = False),
             html.Br(),
            dcc.Dropdown(id = 'country', options = [{'label': col, 'value': col} for col in suicide['country'].unique()],
                          placeholder="Select a country"),
            html.Br(),
            dcc.Dropdown(id = 'group', placeholder="Select a grouping "),
           
            html.Br(),
        
            ],
            md=2,
            style={
                'background-color': '#e6e6e6',
                'padding': 20,
                'border-radius': 3,
                'margin-left':30
                }),
    
            dbc.Col([html.Br(),html.Iframe(
            id='Plot',
            style={ 'width': '90%', 'height': '500px'})])
            ])
            
            ])


@app.callback(
    Output('group', 'options'),
    [Input('country', 'value')]
)
def update_date_dropdown(country):
    if not country : 
        return [{'label': i, 'value': i} for i in ['gender', 'age']]
    else : 
        return [{'label': i, 'value': i} for i in ['gender', 'age','gdp']]
@app.callback(Output('Plot', 'srcDoc'), 
              Input('group', 'value'), 
              Input('country','value'))

def plot_altair(grouped, country):
    ## code for group by , by age and gender 
    df = get_data(country)
    if grouped =='gender' :
        chart =get_gender(country)
    elif grouped =='age' :
        chart =get_age(country)
    elif grouped =='gdp' and   country:
        chart = get_gdp(country)
    else :
        data = pd.DataFrame(df.groupby("year")['suicides/100k pop'].mean().round(2))
        data = data.reset_index()
        data['year']  = pd.to_datetime(data['year'], format='%Y')
        if not country :
            title_graph = "The suicide rate  Worldwide"
        else : 
             title_graph = "The suicide rate  in " +  country
            
        chart = alt.Chart(data, width = 500, height = 350, title =title_graph).mark_line(point=True).encode(
        x=alt.X('year(year):T' , axis=alt.Axis(grid=False), title ='Year'),
        y=alt.Y('suicides/100k pop', title='Suicides per 100k person ', scale=alt.Scale(zero=False)),
        tooltip='suicides/100k pop')

        if not country :  
            data = pd.DataFrame(df.groupby("country")['suicides/100k pop'].mean().round(2).sort_values(ascending=False)[:10])
            data = data.reset_index()
            # data['year']  = pd.to_datetime(data['year'], format='%Y')
            bar = alt.Chart(data,width = 600, height = 400, title = "countries with highest suicide rate (top ten) ").mark_bar().encode(
            x='sum(suicides/100k pop)',
            y=alt.Y('country', sort = 'x'),
            color = alt.Color('country', legend =None),
            tooltip ='sum(suicides/100k pop)'
                )
            chart = chart & bar

        
        
    


    return chart.to_html()

server = app.server
app.title = 'Suicide Rate Analysis'
if __name__ == '__main__':
    app.run_server(debug=True) 
