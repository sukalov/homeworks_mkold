import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

def citiesplot(cities):

    citiesc = []
    citiesp = []
    for eleme in cities[1]:
        city = []
        city.append(eleme)
        city.append(average(cities[1][eleme]))
        citiesc.append(city)

    for elem in cities[0]:
        city2 = []
        city2.append(elem)
        city2.append(average(cities[0][elem]))
        citiesp.append(city2)
        
    citydic = {}

    n = -1
    for element in citiesp:
        n += 1
        citydic[n] = element[0]
        element[0] = n
        
    for el in citiesc:
        if el[0] not in citydic.values():
            n += 1
            citydic[n] = el[0]
            el[0] = n
        else:
            for key in citydic:
                if citydic[key]==el[0]:
                    el[0] = key
    
           
    plt.scatter([a[0] for a in citiesp], [i[1] for i in citiesp], c='r', label='длина поста')
    plt.scatter([a[0] for a in citiesc], [i[1] for i in citiesc], c='b', label='длина комментария')
    plt.xticks(range(len(citydic)), [citydic[n] for n in citydic], rotation='vertical')   
    plt.legend()
    plt.show()       

def average(arr):
    s = 0
    for elem in arr:
        s += elem
    try:
        return s / len(arr)
    except:
        return 0


cities = [{'Moscow': [6, 9, 17, 16, 9, 37, 0, 3, 32, 112, 70, 4]}, {'Praha': [5], 'Moscow': [25, 14, 17, 14, 8, 3, 9, 4, 3, 1, 4, 7, 5, 4, 15, 5, 5, 9, 8, 2, 8, 10, 9, 5, 9, 3, 8, 5, 4, 2, 1, 1, 1, 1, 1, 2, 7, 19, 4, 6, 1, 2, 2, 2, 4, 4, 7, 1, 4, 4, 4, 5, 4, 4, 4, 4, 6, 1, 5, 4, 4, 7, 6, 7, 7, 8, 2, 1, 4, 6, 2, 7, 2, 8, 4, 4, 4, 7, 5, 2, 6, 5, 4, 1, 4, 9, 10, 15, 13, 4, 11, 3, 4, 5, 4, 4, 2, 3, 3, 3, 4, 1, 10, 5, 3, 5, 3, 3, 2, 3, 3, 4, 3], 'Grodno': [7], 'Parizhskaya Kommuna': [4, 8, 5], 'Chelyabinsk': [4], 'Ryazan': [2], 'Noginsk': [12, 23], 'Izhevsk': [6], 'Kyiv': [7], 'Elektrostal': [6, 6], 'Saint Petersburg': [5, 7, 2], 'Taman': [3, 5, 2], 'Tambov': [8]}]


citiesplot(cities)
