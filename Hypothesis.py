import pandas as pd
import numpy as np
# import netCDF4
# from netCDF4 import Dataset
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from scipy import stats
from countrygroups import EUROPEAN_UNION
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.power import TTestIndPower


def calc_lat(lat):
    if lat>0:
        index = 2160 - lat * 2160/90
    elif lat ==0:
        index = 2160
    else:
        index = 2160 + lat * 2160 / 90
    return int(index)

def calc_long(long):
    if long > 0:
        index = 4320 + long * 4320 / 180
    elif long == 0:
        index = 4320
    else:
        index = 2160 - long * 2160 / 90
    return int(index)

def zad1():
    df_deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
    df_recovery = pd.read_csv('time_series_covid19_recovered_global.csv')
    df_confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')

    # Check if country show deaths
    df_temp = df_deaths.drop(columns=['Lat', 'Long'])
    df_temp['Total_deaths'] = df_temp.sum(axis=1)
    df_temp = df_temp.loc[df_temp['Total_deaths'] > 0]
    df_temp = df_temp.loc[df_temp['Country/Region'] != 'Canada'] # Remove due to diffrence in provinces in dateframes
    df_temp = df_temp.loc[df_temp['Country/Region'] != 'MS Zaandam'] # Remove cause it is ship
    df_temp = df_temp.loc[df_temp['Country/Region'] != 'Diamond Princess'] # Remove cause it is ship
    df_temp = df_temp['Country/Region'].tolist()

    df_deaths['Check'] = df_deaths['Country/Region'].isin(df_temp)
    df_deaths = df_deaths.loc[df_deaths['Check'] == True]

    df_recovery['Check'] = df_recovery['Country/Region'].isin(df_temp)
    df_recovery = df_recovery.loc[df_recovery['Check'] == True]

    df_confirmed['Check'] = df_confirmed['Country/Region'].isin(df_temp)
    df_confirmed = df_confirmed.loc[df_confirmed['Check'] == True]

    df_deaths = df_deaths.reset_index()
    df_deaths = df_deaths.drop(columns=['index'])

    df_recovery = df_recovery.reset_index()
    df_recovery = df_recovery.drop(columns=['index'])

    df_confirmed = df_confirmed.reset_index()
    df_confirmed = df_confirmed.drop(columns=['index'])

    df_temp = df_recovery.drop(columns=['Lat', 'Long', 'Check'])
    df_temp['Total_recovery'] = df_temp.sum(axis=1)
    df_recovery['Total_recovery'] = df_temp['Total_recovery']

    loop_1 = df_recovery.index.tolist()
    loop_2 = df_temp.columns.tolist()
    loop_2 = loop_2[2:-1]

    days=[]
    df_temp_1=df_confirmed.copy()
    df_temp_death=df_deaths.copy()

    for i in loop_1:
        recovery = df_recovery.loc[i,'Total_recovery']
        if recovery == 0:
            for j,day in enumerate(loop_2):
                days.append(day)
                if len(days)>14:
                    df_recovery.loc[i,day] = df_temp_1.loc[i,days[j-14]] - df_temp_death.loc[i,day]
            days = []

    df_temp_1 = df_confirmed.copy()
    df_temp_2 = df_recovery.copy()
    df_temp_death=df_deaths.copy()

    df_active = df_confirmed.copy()
    for i in loop_1:
        for j, day in enumerate(loop_2):
            df_active.loc[i, day] = df_temp_1.loc[i, day] - df_temp_2.loc[i,day] - df_temp_death.loc[i, day]
    df_recovery.to_csv('lol')

    df_mortality = df_deaths.copy()
    df_mortality = df_mortality.loc[:,['Province/State','Country/Region']]

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    df_temp_1 = df_deaths.copy()
    df_temp_1 = df_temp_1.drop(columns=['Province/State','Country/Region','Lat', 'Long', 'Check'])
    df_temp_2 = df_recovery.copy()
    df_temp_2 = df_temp_2.drop(columns=['Province/State', 'Country/Region', 'Lat', 'Long', 'Check'])

    loop_1 = df_temp_1.index.tolist()
    loop_2 = df_temp_1.columns.tolist()

    prev_mon = 1
    temp_1 = 0
    temp_2 = 0
    for i,index in enumerate(loop_1):
        for j, date in enumerate(loop_2):
            mon = date[:2]
            year = date[-2:]
            if mon[1] == '/':
                mon = mon[:1]
            if mon == prev_mon:
                temp_1 = temp_1 + df_temp_1.loc[index,date]
                temp_2 = temp_2 + df_temp_2.loc[index,date]
            else:
                month = months[int(mon)-1]
                time = month + ' ' + year
                if temp_2 == 0:
                    df_mortality.loc[index, time] = 0
                else:
                    df_mortality.loc[index,time] = temp_1/temp_2
                temp_1 = 0
                temp_2 = 0
            prev_mon = mon

    return df_active,df_deaths,df_confirmed,df_mortality

def zad1_2(df_active):
    df_active = df_active.drop(columns=['Lat', 'Long', 'Check'])
    df_active_temp = df_active.copy()
    df_M = df_active.copy()

    loop_1 = df_M.index.tolist()
    loop_2 = df_M.columns.tolist()
    loop_2 = loop_2[2:-1]
    days = []

    for i, index in enumerate(loop_1):
        for j,day in enumerate(loop_2):
            days.append(day)
            temp = 0
            if j>6:
                for k in range(6):
                    temp = temp + df_active_temp.loc[index, days[len(days)-1-k]]
            df_M.loc[index, day] = temp
    df_R = df_M.copy()
    loop_1 = df_R.index.tolist()
    loop_2 = df_R.columns.tolist()
    loop_2 = loop_2[2:]
    days = []
    for i, index in enumerate(loop_1):
        for j, day in enumerate(loop_2):
            days.append(day)
            temp = 0
            if j > 6:
                if df_M.loc[index, days[len(days) - 5 ]] ==0:
                    temp = 0
                else:
                    temp = df_M.loc[index, day]/df_M.loc[index, days[len(days) - 5 ]]
                df_R.loc[index, day] = temp
    return df_R

def zad2(df_active):
    df_weather = df_active
    df_weather_max = df_weather.loc[:,['Province/State','Country/Region','Lat','Long']]
    df_weather_min = df_weather.loc[:,['Province/State','Country/Region','Lat','Long']]
    df_weather_mean = df_weather.loc[:,['Province/State','Country/Region','Lat','Long']]

    weather_max = Dataset('./data/TerraClimate_tmax_2018.nc')
    weather_min = Dataset('./data/TerraClimate_tmin_2018.nc')

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    for i, month in enumerate(months):
        df_weather_max[month] = 0
        df_weather_min[month] = 0
        df_weather_mean[month] = 0
    loop_1 = df_weather_max.index.tolist()
    for i,index in enumerate(loop_1):
        for j,month in enumerate(months):
            lat = df_weather.loc[index,'Lat']
            long = df_weather.loc[index,'Long']
            max = weather_max['tmax'][j,calc_lat(lat),calc_long(long)]
            min = weather_min['tmin'][j,calc_lat(lat),calc_long(long)]
            mean = (max + min)/2
            df_weather_max.loc[index,month] = max
            df_weather_min.loc[index,month] = min
            df_weather_mean.loc[index, month] = mean
    return df_weather_mean
def zad3_1(df_R,df_weather_mean):
    loop_1 = df_R.index.tolist()
    loop_2 = df_R.columns.tolist()

    loop_2 = loop_2[2:]
    df_RN = df_R.copy()
    for i,index in enumerate(loop_1):
        max = df_R.max(axis=1)
        max = int(max[i])
        for j,day in enumerate(loop_2):
            if max == 0:
                df_RN.loc[index, day] = 0
            else:
                df_RN.loc[index,day] = df_R.loc[index,day] / max

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    vec_0,vec_10,vec_20,vec_30,vec_40 =[],[],[],[],[]
    for i, index in enumerate(loop_1):
        for j,day in enumerate(loop_2):
            mon = day[:2]
            if mon[1] == '/':
                mon = mon[:1]
            mon = int(mon) - 1
            temperature = df_weather_mean.loc[index,months[mon]]
            if temperature < 0:
                vec_0.append(df_RN.loc[index,day])
            elif temperature < 10:
                vec_10.append(df_RN.loc[index, day])
            elif temperature < 20:
                vec_20.append(df_RN.loc[index, day])
            elif temperature < 30:
                vec_30.append(df_RN.loc[index, day])
            elif temperature < 40:
                vec_40.append(df_RN.loc[index, day])

def zad3_chi2(df_deaths,df_confirmed):
    df_deaths['Check'] = df_deaths['Country/Region'].isin(EUROPEAN_UNION.names)
    df_deaths = df_deaths.loc[df_deaths['Check'] == True]

    df_confirmed['Check'] = df_confirmed['Country/Region'].isin(EUROPEAN_UNION.names)
    df_confirmed = df_confirmed.loc[df_confirmed['Check'] == True]

    df_temp = df_confirmed.loc[:,['Province/State','Country/Region','Lat','Long']]
    df_deaths = df_deaths.drop(columns=['Province/State','Country/Region','Lat', 'Long', 'Check'])
    df_confirmed = df_confirmed.drop(columns=['Province/State','Country/Region','Lat', 'Long', 'Check'])

    df_deaths['sum_deaths'] = df_deaths.sum(axis=1)
    df_confirmed['sum_confirmed'] = df_confirmed.sum(axis=1)
    df_confirmed.to_csv('conf3')

    df_temp['ratio'] = df_deaths['sum_deaths']/df_confirmed['sum_confirmed']
    df_deaths.to_csv('deaths')

    print(df_temp)

    list = df_temp['ratio'].tolist()

    obs = np.array(list)  # wartość obserwowana
    ox = [1/len(list)]*len(list)
    exp = np.array(ox) * np.sum(obs)  # oczekiwana liczba wystąpień (suma musi być taka jak dla obs)
    chi2, p = chisquare(obs, exp)
    print(chi2)
    print(p)

def zad3_anova(df_mortality):
    df_mortality['Check'] = df_mortality['Country/Region'].isin(EUROPEAN_UNION.names)
    df_mortality = df_mortality.loc[df_mortality['Check'] == True]
    df_mortality.to_csv('deaths')

    temp = []
    loop_1 = df_mortality.columns.tolist()
    loop_1 = loop_1[3:-1]
    for i,index in enumerate(loop_1):
        tempy_temp = df_mortality[index].tolist()
        temp.append(tempy_temp)
    pts = 1000
    np.random.seed(28041990)
    x = np.concatenate(temp)
    k2, p = stats.normaltest(x)
    alpha = 1e-3
    print("p = {:g}".format(p))

    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")

    arr = np.array(temp)
    arr = np.transpose(arr)
    print(arr.shape)

    f_value, p_value = f_oneway(arr[0],arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8],arr[9],arr[10],
                                arr[11],arr[12],arr[13],arr[14],arr[15],arr[16],arr[17],arr[18],arr[19],arr[20],arr[21],
                                arr[22],arr[24],arr[25],arr[25],arr[26],arr[27],arr[28],arr[29],arr[30],arr[31],arr[32],
                                arr[33],arr[34],arr[35],arr[36],arr[37],arr[38],arr[39],arr[40],arr[41],arr[42],arr[43])
    print(f'F-stat: {f_value}, p-val: {p_value}')

    print(pairwise_tukeyhsd(np.concatenate([arr[0],arr[1],arr[2]]),
                            np.concatenate([['arr[0]'] * len(arr[0]), ['arr[1]'] * len(arr[1]), ['arr[2]'] * len(arr[2])])))

    a = arr[0]
    b = arr[2]

    a_mean = np.mean(a)
    b_mean = np.mean(b)

    a_std = np.std(a)
    b_std = np.std(a)

    effect = (a_mean - b_mean)/((a_std + b_std)/2)
    analysis = TTestIndPower()
    result = analysis.solve_power(effect, power=None, nobs1=len(a), ratio=1.0, alpha=alpha)
    print(result)


def main():
    df_active,df_deaths,df_confirmed,df_mortality = zad1()
    # df_R = zad1_2(df_active)
    # df_weather_mean = zad2(df_active)
    # zad3_1(df_R,df_weather_mean)
    zad3_chi2(df_deaths,df_confirmed)
    # zad3_anova(df_mortality)


main()
