# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve, f1_score



campaigns = pd.read_csv('../data/1-community_campaigns.csv',index_col=0)


Cs = [];
Ss = [];

for i in range(1,201):
  
  # Read CSV file
  df = pd.read_csv('../data/campaign'+'{0:0=4d}'.format(i)+'.csv',index_col=0)
  
  # Use date to create a datetime_index
  df['Datetime'] = pd.to_datetime(df['date'])
  df = df.set_index('Datetime')
  
  # Remove unnecesary "date" and "supporter name" columns
  # and add column with backer count and
  df = df.drop(['date','supporter name'], axis=1)
  df['backers'] = 1

  # Resamnple dataframe by day to get daily transacion data
  df = df.resample('D').sum()
  df['day_number'] = range(1,1+len(df))


  # Add columns with cummulative sums of pledges and number
  # of backers
  df['cumsum_pledges'] = df['pledge'].cumsum()
  df['cumsum_backers'] = df['backers'].cumsum()
    
  # Normalizations
  df['norm_time'] = df['day_number']/(1+campaigns.iloc[i-1]['duration'])
  df['norm_capital'] = df['cumsum_pledges']/campaigns.iloc[i-1]['Goal']
  
  t = df['norm_time'].tolist()
  m = df['norm_capital'].tolist()

  # Add point (t,M) = (0,0)
  t.insert(0,0)
  m.insert(0,0)

  # Resampled time series
  ts = np.linspace(0,1,29)
  ms = np.interp(ts,t,m)
  state = 1 if ms[-1]>=1 else 0
  
  Cs.append(ms)
  Ss.append(state)



X_train, X_test, y_train, y_test = train_test_split(Cs, Ss, stratify=Ss, test_size=0.2, random_state=42)


error = []

# Calculating error for K values between 1 and 100
for i in range(1, 100):  
  knn = KNeighborsClassifier(n_neighbors=i,weights='distance')
  knn.fit(X_train, y_train)
  pred_i = knn.predict(X_test)
  error.append(np.mean(pred_i != y_test))

plt.figure(figsize=(12, 6))  
plt.plot(range(1, 100), error, color='red', linestyle='dashed', marker='o',  
     markerfacecolor='blue', markersize=10)
plt.title('Error Rate K Value');
plt.xlabel('K Value');
plt.ylabel('Mean Error');
best_k = 1+error.index(min(error))



kNN = KNeighborsClassifier(n_neighbors=best_k,weights='distance')
kNN.fit(X_train, y_train);

y_pred = kNN.predict(X_test)

 
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print('Used',best_k,'Neighbors')
print('Accuracy of kNN classifier on test set: {:.2f}'.format(kNN.score(X_test, y_test)))
print('F1 score of kNN classifier on test set: {:.2f}'.format(f1_score(y_test,y_pred)))




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server



colors = {
  'background': '#111111',
  'text': '#7FDBFF'
}


app.layout = html.Div([
  html.H1('Crowdfunding-Prophet',
  style={'textAlign':'center', 'color': colors['text']}
  ),

  html.Div(children='Select a Campaign'),
  
  
  dcc.Dropdown(
    id='campaigns-dropdown-menu',
    style={'width': '48%','text-align':'center'},
    options=[{'label': i, 'value': i} for i in campaigns['URL']],
    placeholder='Select a Campaign'
  ),
  
  html.Div([
  dcc.Graph(id='time-series-plot')],
  style={'display': 'inline-block', 'width': '48%','text-align':'center'})
  
],
style={'backgroundColor': colors['background']})


def create_time_series(df):
  return {
    'data': [go.Scatter(
      x=df['day_number'],
      y=df['cumsum_pledges'],
      mode='lines+markers'
    )],
    'layout': {
      'height': 450,
      'widht' : 450,
      'margin': {'l': 40, 'b': 40, 'r': 10, 't': 10},
      'annotations': [{
        'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
        'xref': 'paper', 'yref': 'paper', 'showarrow': False,
        'align': 'center', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
        'text': 'Time Series data'
      }],
      'yaxis': {'type': 'linear', 'title': 'Capital'},
      'xaxis': {'showgrid': False, 'title': 'day number'}
    }
  }




@app.callback(
  dash.dependencies.Output('time-series-plot', 'figure'),
  [dash.dependencies.Input('campaigns-dropdown-menu', 'value')])
def update_graph(url):
  campaign_idx = 1+campaigns[campaigns['URL'] == url].index.values.astype(int)[0]
  df = pd.read_csv('../data/campaign'+'{0:0=4d}'.format(campaign_idx)+'.csv',index_col=0)
  
  df['Datetime'] = pd.to_datetime(df['date'])
  df = df.set_index('Datetime')

  # Remove unnecesary "date" and "supporter name" columns
  # and add column with backer count and
  df = df.drop(['date','supporter name'], axis=1)
  df['backers'] = 1

  # Resamnple dataframe by day to get daily transacion data
  df = df.resample('D').sum()
  df['day_number'] = range(1,1+len(df))

  # Add columns with cummulative sums of pledges and number
  # of backers
  df['cumsum_pledges'] = df['pledge'].cumsum()
  df['cumsum_backers'] = df['backers'].cumsum()

  # Normalizations
  df['norm_time'] = df['day_number']/(1+campaigns.iloc[5-1]['duration'])
  df['norm_capital'] = df['cumsum_pledges']/campaigns.iloc[5-1]['Goal']
  df = df[['day_number','norm_time','pledge','cumsum_pledges','norm_capital','backers','cumsum_backers']]


  return create_time_series(df)


if __name__ == '__main__':
  app.run_server(debug=True)