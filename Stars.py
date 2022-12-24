import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def parse(x):
    return [i.strip() for i in x.split(',') if i != '']

def data_sep(x):
    y = []
    for i in range(0, len(x)):
        y.append(x[i][0])
    del y[0]
    return y

def calculate_HHD(x):
    year = []
    month = []
    day = []
    hours = []
    minutes = []
    seconds = []
    for i in range(0, len(x)):
        a = float(x[i]) + 2432044
        b = (4 * a + 3) // 146097
        c = a - (146097 * b // 4)
        d = (4 * c + 3) // 1461
        e = c - (1461 * d // 4)
        m = (5 * e + 2) // 153
        day_i = e - (153 * m + 2) // 5 + 1
        month_i = m + 3 - (2 * m) // 10
        year_i = 100 * b + d - 4800 + (m // 10)
        month_i = int(month_i)
        year_i = int(year_i)
        hour_i = (day_i - int(day_i)) * 24
        min_i = (hour_i - int(hour_i)) * 60
        sec_i = int((min_i - int(min_i)) * 60)
        day_i = int(day_i)
        hour_i = int(hour_i)
        min_i = int(min_i)
        day.append(day_i)
        month.append(month_i)
        year.append(year_i)
        hours.append(hour_i)
        minutes.append(min_i)
        seconds.append(sec_i)
    return [list(i) for i in zip(day, month, year, hours, minutes, seconds)]

def create_data(x, n):
    new_data = []
    for k in range(0, len(x)):
        for i in range(0, len(x)):
            if i == n + 4 * k:
                new_data.append(x[i])
    return new_data


file = open("TASK_2.dat", "r")
data = file.read().split("\n")
data_0 = []
for line in data:
    data = line.split('  ')
    for line in data:
        data = line.strip()
        data = [data]
        data_0.append(data)
while [''] in data_0:
    data_0.remove([''])
#print(data_0)
data_1 = create_data(data_0, 0)
data_2 = create_data(data_0, 1)
data_3 = create_data(data_0, 2)
data_4 = create_data(data_0, 3)
AllObjects = data_sep(data_1)
AllHJDs = data_sep(data_2)
AllFilters = data_sep(data_3)
AllMagnitudes = data_sep(data_4)
Objects = list(set(AllObjects))
Filters = list(set(AllFilters))
date = calculate_HHD(AllHJDs)
date = pd.DataFrame(date)
date['HHD'] = date[0].astype(str) + '.' + date[1].astype(str) + '.' + date[2].astype(str) + ' ' + date[3].astype(str) + ':' + date[4].astype(str) + ':' + date[5].astype(str)
AllHHDs = date['HHD'].tolist()
#print(AllHHDs)
for i in range(0, len(Filters)):
    for k in range(0, len(Objects)):
        Filter_i_k = []
        Objects_i_k = []
        HJD_i_k = []
        HHD_i_k = []
        Magnitude_i_k = []
        for j in range(0, len(AllFilters)):
            if AllFilters[j] == Filters[i] and AllObjects[j] == Objects[k]:
                Filter_i_k.append(AllFilters[j])
                Objects_i_k.append(AllObjects[j])
                HJD_i_k.append(AllHJDs[j])
                HHD_i_k.append(AllHHDs[j])
                Magnitude_i_k.append(AllMagnitudes[j])
        if Objects_i_k != []:
            df_i_k = pd.DataFrame(list(zip(Objects_i_k, HJD_i_k, HHD_i_k, Filter_i_k, Magnitude_i_k)), columns=['Object', 'HDJ 24...', 'HHD', 'Filter', 'Magnitude'])
            df_i_k = df_i_k.sort_values(by='HDJ 24...')
            #print(df_i_k)
            df_i_k.to_csv('txt.csv', mode='a', header=False, index=False)
with open('txt.csv', 'r') as file:
    read_data = [line.strip() for line in file.readlines()]
    read_data = [parse(x) for x in read_data if x != '']
DATA = pd.DataFrame(read_data, columns=['Object', 'HDJ 24...', 'HHD', 'Filter', 'Magnitude'])


print('Объекты, которые наблюдались:', '   '.join(Objects))
name = input('Введите название объекта чтобы узнать, в каком фильтре он наблюдался: ')
filter = []
for i in range(0, len(AllObjects)):
    if AllObjects[i] == name:
        filter.append(AllFilters[i])
print('Filters:', '   '.join(list(set(filter))))
print('Введите название объекта и фильтры, данные в которых нужны.')
name_object = input('Object: ')
name_filter = input('Filters: ')
name_filter = [f for f in name_filter if f]
name_filter = ''.join(name_filter).split()
loc_object = DATA.loc[DATA['Object'] == f"{name_object}"]
for i in name_filter:
    Graph = loc_object.loc[loc_object['Filter'] == f"{i}"]
    if i.isupper() == True:
        Graph.to_csv(f'{name}_{i}.csv', mode='w', header=['Object', 'HDJ 24...', 'HHD', 'Filter', 'Magnitude'], index=False, sep=('\t'))
    else:
        Graph.to_csv(f'{i}_{name}.csv', mode='w', header=['Object', 'HDJ 24...', 'HHD', 'Filter', 'Magnitude'], index=False, sep=('\t'))
    fig = plt.figure()
    ax = plt.subplot()
    ax.set_title(f'{i}_{name}', color='red')
    ax.set_xlabel('HDJ 24...')
    ax.set_ylabel('Magnitude')
    ax.xaxis.set_major_locator(ticker.LinearLocator(10))
    ax.yaxis.set_major_locator(ticker.LinearLocator(10))
    X = [float(i) for i in Graph.iloc[:, 1]]
    Y = [float(i) for i in Graph.iloc[:, 4]]
    ax.scatter(X, Y, color='black')
plt.show()
