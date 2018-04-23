
# coding: utf-8

# In[1]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from citipy import citipy
import openweathermapy as owm
import datetime
import seaborn as sns
now = datetime.datetime.now()


# # CLEANING AND MERGING DATA
# 
# 

# In[2]:


#load CSV

Country_Dictionary = "Resources/dictionary.csv"
summercsv = "Resources/summer.csv"
wintercsv = "Resources/winter.csv"
winterHostcsv = "Resources/winter_hosts.xlsx"
summerHostcsv = "Resources/summer_hosts.xlsx"


summer_pd = pd.read_csv(summercsv, low_memory=False)
winter_pd = pd.read_csv(wintercsv, low_memory = False)
dict_pd = pd.read_csv(Country_Dictionary, low_memory = False)
win_host = pd.read_excel(winterHostcsv)
sum_host = pd.read_excel(summerHostcsv)

#change column name of Country on summer/winter DF
summer_pd = summer_pd.rename(columns={"Country":"Code"})
winter_pd = winter_pd.rename(columns={"Country":"Code"})

#Change URS TO RUS

summer_pd["Code"] = summer_pd["Code"].replace("URS", "RUS") 
winter_pd["Code"] = winter_pd["Code"].replace("URS", "RUS") 
#summer_pd["Country"].unique()


#MERGE DATAFRAMES ON COUNTRY CODE
summer_merge = pd.merge(summer_pd, dict_pd, on="Code")
winter_merge = pd.merge(winter_pd, dict_pd, on="Code")

#MERGE DATAFRAMES TO INCLUDE HOST COUNTRY on YEAR
summer_merge = pd.merge(summer_merge, sum_host, on="Year")
winter_merge = pd.merge(winter_merge, win_host, on="Year")


#winter_merge.head(-100)

#winter_merge.head(5)


# # BY COUNTRY

# ### Summer Games by Country

# In[5]:


#PIE CHART FOR BY COUNTRY WINS, TOP 5 in each summer

#winter_pd["Athlete"].value_counts().head(5).index.tolist()

#print(winter_merge["Country"].value_counts().head())
sum_oly_pie = summer_merge["Country"].value_counts().head(10).values.tolist()
sum_oly_lab = summer_merge["Country"].value_counts().head(10).index.tolist()

explode = (0.25,0,0,0,0,0,0,0,0,0)
plt.axis("equal")

plt.pie(sum_oly_pie, explode=explode, labels=sum_oly_lab, autopct="%1.1f%%", shadow=True, startangle=140)
plt.title("Summer Olympic Winners By Country")
plt.xlabel("Country")
plt.savefig("Sum_Oly_wins_byCountry.png")
plt.show()


# ### Winter Games by Country

# In[7]:


#PIE CHART FOR BY COUNTRY WINS, TOP 5 in each WINTER

#winter_pd["Athlete"].value_counts().head(5).index.tolist()

#print(winter_merge["Country"].value_counts().head())
win_oly_pie = winter_merge["Country"].value_counts().head(10).values.tolist()
win_oly_lab = winter_merge["Country"].value_counts().head(10).index.tolist()

explode = (0,0.25,0,0,0,0,0,0,0,0)
plt.axis("equal")

plt.pie(win_oly_pie, explode=explode, labels=win_oly_lab, autopct="%1.1f%%", shadow=True, startangle=100)
plt.title("Winter Olympic Winners By Country")
plt.xlabel("Country")
plt.savefig("Win_Oly_wins_byCountry.png")
plt.show()


# # Patterns by Sex

# ### Summer Common Winners by Sex

# In[8]:


#MEN VS WOMEN STUFF


men_summer = summer_merge.loc[summer_merge["Gender"] == "Men"]
women_summer = summer_merge.loc[summer_merge["Gender"] == "Women"]

men_winter = winter_merge.loc[winter_merge["Gender"] == "Men"]
women_winter = winter_merge.loc[winter_merge["Gender"] == "Women"]

#MEN
Men_Sum_byCountry = men_summer["Country"].value_counts()
Men_Win_byCountry = men_winter["Country"].value_counts()

#Women

Women_Sum_byCountry = women_summer["Country"].value_counts()
Women_Win_byCountry = women_winter["Country"].value_counts()

#Total Medal Winning men - 20512  // Total Medal Winning Women - 7279
#Men_Sum_byCountry.sum()

#Men_Sum_byCountry


Women_Sum_byCountry.head(20)
#Men_Sum_byCountry.head(25)

#SUMMER CHART MENS/WOMENS
n = 11
sum_women = (1377,932,308,142,135,91,389,245,493,263,537)
sum_men = (3208,1885,1412,1254,1161,953,916,834,696,525,270)
x_axis = np.arange(n)
width = 0.4

bar1 = plt.bar(x_axis, sum_men, width, color = 'C0')
bar2 = plt.bar(x_axis, sum_women, width, color = 'C3')
plt.xticks(x_axis, ('United States','Russia','United Kingdom', 'France', 'Italy', 'Sweden', 'Germany', 'Hungary','Australia', 'Japan','China'),rotation=45)
plt.legend((bar1[0], bar2[0]), ('Men', 'Women'))
plt.xlabel("Summer Olympics Winners by Sex")

plt.show()


# ### Winter Common Winners by Sex

# In[9]:


#WINTER MEN/WOMEN

#Women_Win_byCountry.head(20)
Men_Win_byCountry.head(25)

n=12

win_women = (243,215,239,98,106,106,71,75,157,61,55,43)
win_men = (410,488,386,359,328,327,214,205,203,131,97,79)
x_axis = np.arange(n)
width = 0.4

bar1 = plt.bar(x_axis, win_men, width, color = 'C0')
bar2 = plt.bar(x_axis, win_women, width, color = 'C3')
plt.xticks(x_axis, ('United States', 'Russia', 'Canada','Norway','Finland','Sweden','Switzerland','Austria','Germany','Italy','France','Netherlands'),rotation=45)
plt.legend((bar1[0], bar2[0]), ('Men', 'Women'))
plt.xlabel("Winter Olympics Winners by Sex")
plt.show()


# # Most Decorated Athletes (all medals)
# 

# ### Winter

# In[10]:


winter_athletes = winter_pd["Athlete"].value_counts().head(5).values.tolist()

x_axis = np.arange(5)
plt.bar(x_axis, winter_athletes, align="edge", color='C9')
tick_locations = [value+0.4 for value in x_axis]


plt.xticks(tick_locations, winter_pd["Athlete"].value_counts().head(5).index.tolist(), rotation=45)

plt.xlim(-0.25, len(x_axis))
plt.title("Most Decorated Winter Athletes")
plt.ylabel("Number of Olympic Medals(GS&B)")
plt.xlabel("Winter Athlete")
plt.show()


# ### Summer 

# In[11]:


summer_athletes = summer_pd["Athlete"].value_counts().head(5).values.tolist()

x_axis = np.arange(5)
plt.bar(x_axis, summer_athletes, align="edge", color='C2')
tick_locations = [value+0.4 for value in x_axis]

plt.xticks(tick_locations, summer_pd["Athlete"].value_counts().head(5).index.tolist(),rotation=45)

plt.xlim(-0.25, len(x_axis))
plt.title("Most Decorated Summer Athletes")
plt.ylabel("Number of Olympic Medals(GS&B)")
plt.xlabel("Summer Athlete")
plt.show()


# # GDP by Capita's Effect on Olympic Wins

# In[12]:


#GDP PER CAPITA BY WINS GRAPH
#INCLUDE BOTH WINTER AND SUMMER DATA

GDP_win = winter_merge["Country"].value_counts()
GDP_sum = summer_merge["Country"].value_counts()

test = pd.DataFrame(GDP_win)
test.reset_index(inplace=True)

test = test.rename(columns={"Country":"Wins","index":"Country"})
GDP_win1 = pd.merge(dict_pd, test, on="Country")

GDP_win1.head()


test2 = pd.DataFrame(GDP_sum)
test2.reset_index(inplace=True)
test2=test2.rename(columns={"Country":"Wins","index":"Country"})

GDP_sum1 = pd.merge(dict_pd, test2, on="Country")

w_medals = GDP_win1["Wins"] 
w_GDP = GDP_win1["GDP per Capita"]

s_medals = GDP_sum1["Wins"] 
s_GDP = GDP_sum1["GDP per Capita"]

bub_w = plt.scatter(w_medals, w_GDP, c='C0', label="Winter Events", alpha=0.85, edgecolor="black")
bub_s = plt.scatter(s_medals, s_GDP, c='C8', label="Summer Events", alpha=0.85, edgecolor="black")

legend = plt.legend(handles=[bub_w,bub_s])

plt.title("Wins by GDP per Capita")
plt.xlabel("Olympic Medals Won")
plt.ylabel("GDP per Capita")

plt.show()


# # Most Celebrated Athletes (Gold Only)

# In[82]:





# # Quantifying Home Team Advantage

# In[13]:


#making smaller datasets where host=country[ALL MEDALS]


#ALL MEDAL WINNERS, HOST = WINNER COUNTRY
Host_All_Summer = summer_merge.loc[summer_merge["Country"] == summer_merge["Host"]]
Host_All_Winter = winter_merge.loc[winter_merge["Country"] == winter_merge["Host"]]

#GOLD MEDAL WINNERS, HOST = WINNER COUNTRY
Host_Gold_Summer = Host_All_Summer.loc[Host_All_Summer["Medal"] == "Gold"]
Host_Gold_Winter = Host_All_Winter.loc[Host_All_Winter["Medal"]=="Gold"]

#ALL MEDAL WINNERS, host NOT winner Country
Not_Host_All_Summer = summer_merge.loc[summer_merge["Country"] != summer_merge["Host"]]
Not_Host_All_Winter = winter_merge.loc[winter_merge["Country"] != winter_merge["Host"]]

Not_Host_Gold_Summer = Not_Host_All_Summer.loc[Not_Host_All_Summer["Medal"] == "Gold"]
Not_Host_Gold_Winter = Not_Host_All_Winter.loc[Not_Host_All_Winter["Medal"]=="Gold"]


Not_Host_Gold_Winter.head(-5)


# In[14]:


# Create API key and preferred units
api_key = "7f565398c1a0ab6b2dde537d78e10dc8"
# Setting the units to imperial to get Fahrenheit reading
settings = {"units": "imperial", "appid": api_key}


# # WINTER DATAFRAME

# In[15]:


# Get data for each country in winter dataframe
winter_weather_data = []

url="https://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&units=imperial&q="

print("\nCollecting Country Information\n")
#Search OpenWeatherMap and store the response into winter_weather_data if response is found
for index,row in win_host.iterrows():  
    print("\nProcessing record %s|%s,%s"%((index+1),row["Host City"], row["Host"]))
    try:
        response = owm.get_current("%s,%s"%(row["Host City"],row["Host"]), **settings)
        print("\n"+url+"%s,%s"%(row["Host City"],row["Host"]))
        # Appending the response to the weather_Data
        winter_weather_data.append(response)
    except:
        print("\nCountry Not Found\n")

print("\n-----------------------------\nInformation Collection Complete\n-----------------------------")


# In[16]:


# Create object to to form the weather data table
summary = ["name","dt","coord.lat", "coord.lon","main.temp_max","main.humidity","wind.speed","clouds.all"]

# Create a Pandas DataFrame with the results
data = [response(*summary) for response in winter_weather_data]
column_names = ["Host City","Date","Latitude", "Longitude","Temperature","Humidity","Wind speed","Cloudliness"]
winter_weather_data = pd.DataFrame(data, columns=column_names)

winter_weather_data.head()


# # SUMMER DATAFRAME

# In[17]:


# Get data for each country in summer dataframe
summer_weather_data = []

url="https://api.openweathermap.org/data/2.5/weather?appid=" + api_key + "&units=imperial&q="

print("\nCollecting Country Information\n")
#Search OpenWeatherMap and store the response into winter_weather_data if response is found
for index,row in sum_host.iterrows():  
    print("\nProcessing record %s|%s,%s"%((index+1),row["Host City"], row["Host"]))
    try:
        response = owm.get_current("%s,%s"%(row["Host City"],row["Host"]), **settings)
        print("\n"+url+"%s,%s"%(row["Host City"],row["Host"]))
        # Appending the response to the weather_Data
        summer_weather_data.append(response)
    except:
        print("\nCountry Not Found\n")

print("\n-----------------------------\nInformation Collection Complete\n-----------------------------")


# In[18]:


# Create object to to form the weather data table
summary1 = ["name","dt","coord.lat", "coord.lon","main.temp_max","main.humidity","wind.speed","clouds.all"]

# Create a Pandas DataFrame with the results
data = [response(*summary1) for response in summer_weather_data]
column_names = ["Host City","Date","Latitude", "Longitude","Temperature","Humidity","Wind speed","Cloudliness"]
summer_weather_data = pd.DataFrame(data, columns=column_names)

summer_weather_data.head()


# # Create Weather Charts

# In[19]:


#merge summer and winter dataframes to create chart
summer_weather_merge = pd.merge(summer_merge, summer_weather_data, on="Host City")
winter_weather_merge = pd.merge(winter_merge, winter_weather_data, on="Host City")

summer_weather_merge.head(10)


# In[20]:


#find values for summer medal count and latitude
summer_bubble_plot_df1 = summer_weather_merge.groupby(["Country", "Population"],as_index=True).count()["Medal"].to_frame().reset_index()
summer_bubble_plot_df2 = summer_weather_merge.groupby(["Country", "Population"],as_index=True).mean()["Latitude"].to_frame().reset_index()
summer_bubble_plot_df = pd.merge(summer_bubble_plot_df1,summer_bubble_plot_df2,
                                on=["Country", "Population"])
summer_bubble_plot_df.head(10)



# In[21]:


#create country medal count vs. latitude scatter plot for summer games
size = 5
sns.lmplot(x="Latitude", y="Medal", data=summer_bubble_plot_df,
          fit_reg=False, legend_out=False,
          size=5,scatter_kws={"s": size, 'linewidths':1, 'edgecolor':'black'})
plt.grid(linestyle="dotted")
plt.xlim(-20,55)
plt.ylim(0,5000)
plt.title("Summer Olympic Medals vs. Latitude", fontsize=15)
plt.xlabel("Lattitude")
plt.ylabel("Total Medal Count per Country")

plt.show()


# In[22]:


#find values for summer medal count and latitude
winter_bubble_plot_df1 = winter_weather_merge.groupby(["Country", "Population"],as_index=True).count()["Medal"].to_frame().reset_index()
winter_bubble_plot_df2 = winter_weather_merge.groupby(["Country", "Population"],as_index=True).mean()["Latitude"].to_frame().reset_index()
winter_bubble_plot_df = pd.merge(winter_bubble_plot_df1,winter_bubble_plot_df2,
                                on=["Country", "Population"])
winter_bubble_plot_df.head(10)


# In[23]:


#create country medal count vs. latitude scatter plot for winter games
size = 5
sns.lmplot(x="Latitude", y="Medal", data=winter_bubble_plot_df,
          fit_reg=False, legend_out=False,
          size=5,scatter_kws={"s": size, 'linewidths':1, 'edgecolor':'black'})
plt.grid(linestyle="dotted")
plt.xlim(30,55)
plt.ylim(0,1000)
plt.title("Winter Olympic Medals vs. Climate", fontsize=15)
plt.xlabel("Lattitude")
plt.ylabel("Total Medal Count per Country")

plt.show()


# # Host Medals Won

# In[24]:


#HOST VS NOT HOST

#ALL MEDAL WINNERS, HOST = WINNER COUNTRY
Host_All_Summer = summer_merge.loc[summer_merge["Country"] == summer_merge["Host"]]
Host_All_Winter = winter_merge.loc[winter_merge["Country"] == winter_merge["Host"]]

#ALL MEDAL WINNERS, host NOT winner Country
Not_Host_All_Summer = summer_merge.loc[summer_merge["Country"] != summer_merge["Host"]]
Not_Host_All_Winter = winter_merge.loc[winter_merge["Country"] != winter_merge["Host"]]


# In[25]:


#Pie Chart for Summer Host Wins - Top 10

#print(winter_merge["Country"].value_counts().head())
summer_host_pie = Host_All_Summer["Country"].value_counts().head(10).values.tolist()
summer_host_lab = Host_All_Summer["Country"].value_counts().head(10).index.tolist()

explode = (0.25,0,0,0,0,0,0,0,0,0,)
plt.axis("equal")

plt.pie(summer_host_pie, explode=explode, labels=summer_host_lab, autopct="%1.1f%%", shadow=True, startangle=100)
plt.title("Summer Olympic Host Medals")
#plt.savefig("Win_Oly_wins_byCountry.png")
plt.show()


# In[26]:


#Pie Chart for Summer Not Host Wins - Top 10

#print(winter_merge["Country"].value_counts().head())
not_summer_host_pie = Not_Host_All_Summer["Country"].value_counts().head(10).values.tolist()
not_summer_host_lab = Not_Host_All_Summer["Country"].value_counts().head(10).index.tolist()

explode = (0.25,0,0,0,0,0,0,0,0,0)
plt.axis("equal")

plt.pie(not_summer_host_pie, explode=explode, labels=not_summer_host_lab, autopct="%1.1f%%", shadow=True, startangle=100)
plt.title("Summer Olympic Medals (Non-Host)")
#plt.savefig("Win_Oly_wins_byCountry.png")
plt.show()


# In[27]:


#Pie Chart for Winter Host Wins - Top 10

#print(winter_merge["Country"].value_counts().head())
winter_host_pie = Host_All_Winter["Country"].value_counts().head(10).values.tolist()
winter_host_lab = Host_All_Winter["Country"].value_counts().head(10).index.tolist()

explode = (0.25,0,0,0,0,0,0,0,0,0)
plt.axis("equal")

plt.pie(winter_host_pie, explode=explode, labels=winter_host_lab, autopct="%1.1f%%", shadow=True, startangle=100)
plt.title("Winter Olympic Host Medals")
#plt.savefig("Win_Oly_wins_byCountry.png")
plt.show()


# In[28]:


#Pie Chart for Winter Not Host Wins - Top 10

#print(winter_merge["Country"].value_counts().head())
not_winter_host_pie = Not_Host_All_Winter["Country"].value_counts().head(10).values.tolist()
not_winter_host_lab = Not_Host_All_Winter["Country"].value_counts().head(10).index.tolist()

explode = (0.25,0,0,0,0,0,0,0,0,0)
plt.axis("equal")

plt.pie(not_winter_host_pie, explode=explode, labels=not_winter_host_lab, autopct="%1.1f%%", shadow=True, startangle=100)
plt.title("Winter Olympic Medals (Non-Host)")
#plt.savefig("Win_Oly_wins_byCountry.png")
plt.show()

