#!/usr/bin/env python
# coding: utf-8

# ## Dashboard for SpaceX

# In[2]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Input,Output,callback,dcc,html, Dash


# In[3]:


spaceX_df=pd.read_csv("spacex_launch_dash.csv")


# In[4]:


spaceX_df.drop('Unnamed: 0',axis=1,inplace=True)


# In[5]:


Launch_site=spaceX_df['Launch Site'].unique()
options=[]
options=[{'label':a,'value':a} for a in Launch_site]
options.append({'label':'ALL sites','value':'ALL'})

options


# In[19]:


external_stylesheets_ = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# from dash import external_stylesheets
app=Dash(__name__,external_stylesheets=external_stylesheets_)


app.layout=html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign':'center','color':'#000500','font-size':'40px'}),
                             html.Div(dcc.Dropdown(id='all_site_dropdown',options=options,value='ALL',placeholder='Launch Site',searchable=True,style={'width':'50%','border-radius':'10px'})),
html.Div(dcc.Graph(id='pie_chart')),
html.Div([html.P('Payload Mass (kg):',style={'color':'white'}),dcc.RangeSlider(id='payload_slider',
                min=0, max=10000, step=10,
                marks={0: {'label':'0','style':{'color':'blue'}},10000: {'label':'10000','style':{'color':'green'}}},
                value=[spaceX_df['Payload Mass (kg)'].min(),spaceX_df['Payload Mass (kg)'].max() ],tooltip={'placement':'bottom',"always_visible":True})
          
          
          
          ,html.Br()]),
                              
html.Div(dcc.Graph(id='success_payload_scatter_chart')),
                             
                             
                             ])
                             
                             


# In[20]:


# Function decorator to specify function input and output
@app.callback(Output(component_id='pie_chart', component_property='figure'),
              Input(component_id='all_site_dropdown', component_property='value'))
# pie_=spacex_df[]
def get_pie_chart(entered_site):
    filtered_df = spaceX_df
    if entered_site == 'ALL':
        fig = px.pie(spaceX_df,names='Launch Site', values='class',title=f'Success Ratio of {entered_site}')
        return fig
    else:
        
        __=spaceX_df[spaceX_df['Launch Site']==entered_site].groupby(['Launch Site','class']).size().reset_index(name='counts')
        fig=px.pie(__,names='class', values='counts',hover_name='Launch Site',title=f'Failed and Success Rate of {entered_site}')
        return fig

@app.callback(Output(component_id='success_payload_scatter_chart',component_property='figure'),
  [Input(component_id='payload_slider', component_property='value'),Input(component_id='all_site_dropdown',component_property='value')])
def payloader_slide(mass,entered_site):
    # rate=type(mass)
    # for a in mass:
    #     return mass[0],mass[1]
    if entered_site=='ALL':
        payL=spaceX_df[(spaceX_df['class']==1) & (spaceX_df['Payload Mass (kg)'] >= mass[0]) & (spaceX_df['Payload Mass (kg)']<= mass[1])]
        fig=px.scatter(payL,x='Payload Mass (kg)',y='Launch Site',color='Booster Version Category',size='Payload Mass (kg)', title='ScatterPlot of All Successful PayLoad Mass')
        return fig
    else:
        payL=spaceX_df[(spaceX_df['class']==1) & (spaceX_df['Payload Mass (kg)'] >= mass[0]) & (spaceX_df['Payload Mass (kg)']<= mass[1])&(spaceX_df['Launch Site']==entered_site)]
        fig=px.scatter(payL,x='Payload Mass (kg)',y='Launch Site', color='Booster Version Category',size='Payload Mass (kg)', title=f'ScatterPlot  of successful {entered_site} PayLoad Mass')
        return fig

        # return the outcomes piechart for a selected site
if __name__=='__main__':
    app.run_server(port=8081,host= '127.0.0.4',debug=True)


# In[13]:


get_ipython().run_cell_magic('html', '', 'From the Dashboard above, it can be deducted that:\n<ol>\n<li><b>KSC LC-39A</b> has the highest amount of <i>succesful lauches<i> amasing up to <b>42%</b> of the succesful launches </li>\n<li><b>CCAFS SLC-40</b> has the lowest amount of </>successful launches</i> with just <b>13%</b> </li>\n<li>The <i>highest launch success rate</i> happend with <b>VAFB SLC-4E</b> having <b>9600 kg</b> Payload Mass </li>\n<li>The <i>lowest launch success rate</i> happend with <b>CCAFS SLC-40</b> having <b>362 kg</b> Payload Mass </li>\n<li><b>The F9 Booster Version</b> with the highest success rate is <b>FT</b></li>\n</ol>\n<style>\n b{\n     font-weight:1500;\n},\nli{\n    background-color:lightblue;\n    font-family:verdana;\n}\n</style>\n')


# In[ ]:




