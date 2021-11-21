import os
import discord
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import kaggle
import tempfile
os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

kaggle.api.authenticate()
kaggle.api.dataset_download_files('novel-corona-virus-2019-dataset', path='sudalairajkumar/novel-corona-virus-2019-dataset', unzip=True)

client = discord.Client()

USdata = pd.DataFrame(pd.read_csv(r'time_series_covid_19_confirmed_US.csv'))
globalData = pd.DataFrame(pd.read_csv(r'time_series_covid_19_confirmed.csv'))
mainData = pd.DataFrame(pd.read_csv(r'covid_19_data.csv'))
with open('CovidFact.txt', 'r') as myfile:
  factData = myfile.readlines()

xData = np.array(USdata.columns.tolist()[20:])
xDataGlobalCompare = np.array(globalData.columns.tolist()[5:])


def visualize(state):
  yData = np.array([])
  for dates in xData:
     yData = np.append(yData, USdata.loc[USdata['Province_State'] == state, dates].sum())
  plt.plot(xData, yData, 'r')
  plt.xlabel=('Time Passed')
  plt.ylabel=('Confirmed COVID-19 Cases')
  plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
  plt.title('Confirmed COVID-19 cases in '+ state +' over Time')
  return plt.savefig("US_visualize.png")


def compare_world(location1, location2):
  yData1 = np.array([])
  yData2 = np.array([])
  for dates in xDataGlobalCompare:
    yData1 = np.append(yData1, globalData.loc[globalData['Country/Region'] == location1, dates].sum())
    yData2 = np.append(yData2, globalData.loc[globalData['Country/Region'] == location2, dates].sum())
  

  plt.plot(xDataGlobalCompare, np.log(yData1+1), 'r')
  plt.plot(xDataGlobalCompare, np.log(yData2+1), 'b')
  plt.xlabel=('Time Passed')
  plt.ylabel=('Confirmed COVID-19 Cases')
  plt.title('Comparative Graph of COVID-19 cases in '+ location1 +' vs ' + location2+' over Time')

  plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
  plt.savefig("global_compare.png")
  response1 = location1 + ": "+ str(np.sum(yData1)) 
  response2 = location2 + ": " + str(np.sum(yData2))
  return response1, response2

def compare_US(state1, state2):
  yData1 = np.array([])
  yData2 = np.array([])
  for dates in xData:
    yData1 = np.append(yData1, USdata.loc[USdata['Province_State'] == state1, dates].sum())
    yData2 = np.append(yData2, USdata.loc[USdata['Province_State'] == state2, dates].sum())
  

  plt.plot(xData, np.log(yData1+1), 'r')
  plt.plot(xData, np.log(yData2+1), 'b')
  plt.xlabel=('Time Passed')
  plt.ylabel=('Confirmed COVID-19 Cases')
  plt.tick_params(axis = "x", which = "both", bottom = False, top = False)
  plt.title('Comparative Graph of COVID-19 cases in '+ state1 +' vs ' + state2 +' over Time')
  plt.savefig("US_compare.png")
  
  response1 = state1 + ": "+ str(np.sum(yData1)) 
  response2 = state2 + ": " + str(np.sum(yData2))
  return response1, response2

def get_fact():
  return factData[random.randint(0, len(factData))]

@client.event
async def on_ready():
  print("okay let's go, I'm {0.user}".format(client), "btw :D")

@client.event

# while factors:
#   if msg.author == client.user:
#     return
#   if msg.content.startswith("$plot"):
#     factor1 = factor[0]
#     factor2 = factor[1]
#     sng.pairplot(data, x_values = [factor1, factor2], y_values = ['covid cases'])
#     plt.savefig("factors_pairplot.png")
#     msg.channel.send(file = discord.File("factors_pairplot.png"))
#     os.remove("factors_pairplot.png")
#     factors = False
#   else:
#     factor = []
#     factor.append(msg.content)


async def on_message(msg):
  if msg.author == client.user:
    return

  if msg.content.startswith("$hello"):
    await msg.channel.send("Hi, this is Defne's Bot. They wrote this for Dataverse's Datathon! Enjoy :D")
  if msg.content.startswith('$visualize'):
    state = msg.content.split('$visualize ', 1)[1]
    visualize(state)
    await msg.channel.send(file=discord.File('US_visualize.png'))
    os.remove('US_visualize.png')
  
  if msg.content.startswith('$compareUS'):
    state1 = ''.join(msg.content.split()[1])
    state2 = ''.join(msg.content.split()[2])
    await msg.channel.send(compare_US(state1, state2))
    await msg.channel.send(file=discord.File("US_compare.png"))
    os.remove('US_compare.png')
  
  if msg.content.startswith('$compare'):
    location1 = ''.join(msg.content.split()[1])
    location2 = ''.join(msg.content.split()[2])
    await msg.channel.send(compare_world(location1, location2))
    await msg.channel.send(file=discord.File("global_compare.png"))
    os.remove('global_compare.png')
  
  # if msg.content.startswith('$correlation'):
  #   factors = True
  #   msg.channel.send("You've chosen to compare two factors! Here are your options: "+ blabla +" message $plot to plot a comparative graph.") THIS WILL BE COMPLETED ONCE I FIND THE DATASET

  if msg.content.startswith('$fact'):
    await msg.channel.send(get_fact())


my_secret = os.environ['TOKEN']
client.run(my_secret)
