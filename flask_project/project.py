import json
from flask import Flask
from flask import url_for, render_template, request, redirect

search_request = []
def get_results_json():
    results = open('results.csv', 'r', encoding='utf-16')
    respondent = 1
    data_dic = {}
    for line in results:
        dic = {}
        result_arr = line.split('\t')
        dic['пол'] = result_arr[0]
        dic['возраст'] = result_arr[1]
        dic['город'] = result_arr[2]
        dic['почта'] = result_arr[3]
        
        question1 = {}        
        question1['вопрос 1'] = result_arr[4]
        question1['вопрос 2'] = result_arr[5]
        question1['вопрос 3'] = result_arr[6]
        question1['вопрос 4'] = result_arr[7]
        question1['вопрос 5'] = result_arr[8]
        question1['вопрос 6'] = result_arr[9]
        question1['вопрос 7'] = result_arr[10]
        question1['вопрос 8'] = result_arr[11]
        
        dic['вопросы про Машу'] = question1
        
        question2 = {}
        question2['вопрос 1'] = result_arr[12]
        question2['вопрос 2'] = result_arr[13]
        question2['вопрос 3'] = result_arr[14]
        question2['вопрос 4'] = result_arr[15]
        question2['вопрос 5'] = result_arr[16]
        question2['вопрос 6'] = result_arr[17]
        question2['вопрос 7'] = result_arr[18]
        question2['вопрос 8'] = result_arr[19].strip('\n')
        
        dic['вопросы про правильность предложений'] = question2
        data_dic['респондент ' + str(respondent)] = dic
        respondent += 1   	

    json_string = json.dumps(data_dic, ensure_ascii=False, separators=(',', ':'), indent=4, sort_keys=True)
    results.close()
    return json_string

def frequency_array(words):
    freq_arr = []
    for word in words:
        tf = 'f'
        if freq_arr != []:
            for pair in freq_arr:
                if pair[0] == word:
                    pair[1] += 1
                    tf = 't'
            if tf != 't':
                freq_arr.append([word, 1])
        else:
            freq_arr.append([word, 1])
    return freq_arr

def making_freqarr():
    file = open('results.csv', 'r', encoding='utf-16')
    data = file.read()
    arr = data.split('\n')

    arr2 = []
    for respondent in arr:
        respondent1 = respondent.split('\t')
        arr2.append(respondent1)

    n = 4
    questions_array = []
    while n<20:
        array = []
        for element in arr2:
            array.append(element[n])
        questions_array.append(array)
        n+=1

    freqarr = []
    for element in questions_array:
        a = frequency_array(element)
        freqarr.append(a)
        
    return freqarr

def making_stats_arr(freqarr):
    j = 0
    options1 = ['маша пришла', 'маша не пришла', 'так сказать нельзя', 'затрудняюсь с ответом']
    options2 = ['1. ужасно', '2. плохо', '3. средне', '4. нормально', '5. отлично']

    for elem in freqarr:
        if j<8:
            not_answered = list(options1)
            for answer in elem:
                not_answered.remove(answer[0])
            for na in not_answered:
                elem.append([na, 0])
            j += 1
        else:
            not_answered = list(options2)
            for answer in elem:
                not_answered.remove(answer[0])
            for na in not_answered:
                elem.append([na, 0])
            
        
    file = open('questions.txt', 'r', encoding='utf-8')
    questions_txt = file.read()
    questions = questions_txt.split('\n')

    n = 0
    full_arr = []
    for element in questions:
        freqarr[n].sort(key=lambda i: -i[1])
        full_arr.append([element, freqarr[n]])
        n += 1

    return full_arr

def making_freqarr_search(sex, age_min, age_max, city):
    file = open('results.csv', 'r', encoding='utf-16')
    data = file.read()
    arr = data.split('\n')

    arr2 = []
    for respondent in arr:
        respondent1 = respondent.split('\t')
        arr2.append(respondent1)

    arr3 = []
    for respondent in arr2:
        if sex == 'любой' or sex == respondent[0]:
            if age_min == 'любой' or int(age_min) <= int(respondent[1]):
                if age_max == 'любой' or int(age_max) >= int(respondent[1]):
                    if city == 'любой' or city == respondent[2]:
                        arr3.append(respondent)                                                                                                        
    n = 4
    questions_array = []
    while n<20:
        array = []
        for element in arr3:
            array.append(element[n])
        questions_array.append(array)
        n+=1

    freqarr = []
    for element in questions_array:
        a = frequency_array(element)
        freqarr.append(a)
        
    return freqarr


app = Flask(__name__)

@app.route('/')
def home():
    adress = 'results.csv'
    if request.args:
        if 'sex' in request.args:
            sex = request.args['sex']
            age = request.args['age']
            city = request.args['city']
            city = city.lower()
            try:
                email = request.args['email']
            except:
                email = 'none'
            text = open(adress, 'a', encoding='utf-16')
            text.write('\n' + sex + '\t')
            text.write(age + '\t')
            text.write(city + '\t')
            text.write(email + '\t')
            text.close()
        if 'q1' in request.args:
            q1 = request.args['q1']
            q2 = request.args['q2']
            q3 = request.args['q3']
            q4 = request.args['q4']
            q5 = request.args['q5']
            q6 = request.args['q6']
            q7 = request.args['q7']
            q8 = request.args['q8']
            text = open(adress, 'a', encoding='utf-16')
            text.write(q1 + '\t')
            text.write(q2 + '\t')
            text.write(q3 + '\t')
            text.write(q4 + '\t')
            text.write(q5 + '\t')
            text.write(q6 + '\t')
            text.write(q7 + '\t')
            text.write(q8 + '\t')
            text.close()
            
            return render_template('home_part_3.html')
        if 'menu1' in request.args:
            menu1 = request.args['menu1']
            menu2 = request.args['menu2']
            menu3 = request.args['menu3']
            menu4 = request.args['menu4']
            menu5 = request.args['menu5']
            menu6 = request.args['menu6']
            menu7 = request.args['menu7']
            menu8 = request.args['menu8']
            text = open(adress, 'a', encoding='utf-16')
            text.write(menu1 + '\t')
            text.write(menu2 + '\t')
            text.write(menu3 + '\t')
            text.write(menu4 + '\t')
            text.write(menu5 + '\t')
            text.write(menu6 + '\t')
            text.write(menu7 + '\t')
            text.write(menu8)
            text.close()
            return redirect(url_for('finish'))
        return render_template ('home_part_2.html')
    return render_template ('home_part_1.html')

@app.route('/finish')
def finish():
    links = {'СТАТИСТИКА': url_for('stats'), 'JSON': url_for('json_page'), 'ПОИСК': url_for('search'),}
    return render_template ('finish.html', links=links)

@app.route('/stats')
def stats():
    questions = making_stats_arr(making_freqarr())    
    return render_template('stats.html', questions=questions)

@app.route('/json')
def json_page():
    json_string = get_results_json()
    return render_template('json.html', json=json_string)

@app.route('/search')
def search():
    if request.args:
        try:
            sex = request.args['sex']
        except:
            sex = 'любой'
            
        if request.args['age_min'] != '':
            age_min = request.args['age_min']
        else:
            age_min = 'любой'

        if request.args['age_max'] != '':
            age_max = request.args['age_max']
        else:
            age_max = 'любой'

        if request.args['city'] != '':
            city = request.args['city'].lower()
        else:
            city = 'любой'

        global search_request                                                                                                         
        search_request = [sex, age_min, age_max, city]
        
        return redirect(url_for('results'))
    return render_template('search.html')

@app.route('/results')
def results():
    global search_request
    questions = making_stats_arr(making_freqarr_search(search_request[0], search_request[1], search_request[2], search_request[3]))
    sex = search_request[0]
    age_min = search_request[1]
    age_max = search_request[2]
    city = search_request[3]
    return render_template('results.html', questions=questions, sex=sex, age_min=age_min, age_max=age_max, city=city)

if __name__ == '__main__':
    app.run()
