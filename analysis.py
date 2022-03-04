import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly
from datetime import date
import datetime as dt


today = date.today()
print("load data from csv")
data = pd.read_csv('all_data.csv')
df = pd.DataFrame(data)
df_power = df.loc[df.data_name =='SITE_SM_solarInstPower']
df_power['timestamp'] = pd.to_datetime(df_power['timestamp'])

#filter for anomalies (negs)
df_power.dropna()
anomalies = df_power[(df_power[['signals']] < 0).all(1)]
print('Anomalies from {} to {}'.format(df_power['timestamp'].head().values[0], df_power['timestamp'].tail().values[0]))
print(anomalies)
print('Number of total anomalies:{}'.format(len(anomalies)))

# plot anomalies
fig = go.Figure()
for s in anomalies.site.unique():
    plot_df = anomalies[anomalies.site == s]
    fig.add_trace(go.Scatter(x=plot_df['timestamp'], y=plot_df['signals'], name=s,
                              mode='markers'))
fig.update_layout(legend_title_text='Sites', yaxis=dict(title_text="Watt"),xaxis=dict(title_text="Timestamp"), title='Anomalies from {} to {}'.format(df_power['timestamp'].head().values[0], df_power['timestamp'].tail().values[0]))

plotly.offline.plot(fig, filename=str(today) + '_SummaryAnomalies.html')


# plot all
condition = (df_power['signals'] < 0)
df_power['Anomaly'] = np.where(condition, 'Yes', 'No')
for s in anomalies.site.unique():
    plot_site = df_power[df_power.site == s]
    fig2 = px.scatter(x=plot_site['timestamp'], y=plot_site['signals'], color=plot_site['Anomaly'])
    fig2.update_layout(legend_title_text='Anomaly', yaxis=dict(title_text="Watt"),xaxis=dict(title_text="Timestamp"), title='Historical solar production from {} to {} for {}'.format(df_power['timestamp'].head().values[0], df_power['timestamp'].tail().values[0], s))
    plotly.offline.plot(fig2, filename=str(s) + '_SolarProd.html')

# count anomalies in site
fig3 = go.Figure()
for i in anomalies.site.unique():
    plot_anomaly = anomalies[anomalies.site == i]
    fig3.add_trace(go.Bar(x=plot_anomaly['site'], y=plot_anomaly.count(),name=i))
fig3.update_layout(legend_title_text='Sites', yaxis=dict(title_text="Count"),xaxis=dict(title_text="Site"), title='Count of Anomalies from {} to {}'.format(df_power['timestamp'].head().values[0], df_power['timestamp'].tail().values[0]))

plotly.offline.plot(fig3, filename=str(today) + '_AnomalyCount.html')
