from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

import pickle

def stressed(sa):
    """
    Returns from string with capital letter that mean stress to string of '0' and '1'

    """
    fuld = []
    wovels = set(['а', 'о', 'у', 'е', 'и', 'э', 'ю', 'ы', 'я', 'ё', 'Ё', 'А', 'О', 'У', 'Е', 'И', 'Э', 'Ы', 'Ю', 'Я', '0'])
    print("введите  пожалуйста ударения слова", sa)
    ful1 = input()
    for kk in ful1:
        if kk in wovels:
            if kk.lower() == kk:
                fuld.append(0)
            else:
                fuld.append(1)
    f1 = open('itoggg.txt', 'a')
    dol = str(fuld)
    f1.write('\n' + sa + ' >>> ' + dol)
    f1.close()
    dd[sa] = dol
    return dol

def makeclear():
    """
    Delete punctuation marks and capital letters in text

    """
    MM = []
    С = []
    gum = open('output.txt')  # Text of verse from file.txt.
    for line in gum.readlines():  # Read verse line by line.
        line = line.rstrip()
        line = line.lower()
        line = line.replace(',', '')
        line = line.replace('.', '')
        line = line.replace('?', '')
        line = line.replace('!', '')
        line = line.replace('-', '')
        line = line.replace(':', '')
        line = line.replace(';', '')
        C = line.split()
        MM.append(C)
    gum.close()
    return MM

def read(s1):
    n = s1
    f = open('output.txt', 'w')
    f.write(n)
    f.close()

def read_2():
    f3 = open('dictionary_pro_rasmer.txt', 'r')
    dwd = [line.strip().split(' >>> ') for line in f3]
    f3.close()
    return dwd

def make_dict():
    dd = {}  # Dictionary of stresses in words.
    words = {}
    f1 = open('itoggg.txt', 'r')  # Read dictionary from file.txt.
    lines = f1.readlines()
    for line in lines:
        words = line.split(">>>")
        words[0] = words[0].replace(' ', '')
        words[1] = eval(words[1])
        asd = words[0]
        dd[asd] = words[1]
    f1.close()
    return dd

def make_array_3(MM):
    M = []
    ful = [[], [], [], [], [], []]
    for z in MM:  # Reading of line.
        for sa in z:  # Reading of words in line.
            if sa in dd:
                zz = dd.get(sa, ful)
            elif not (sa in dd):
                zz = stressed(sa)
            M.append(zz)
    return M

def make_array_2(M):
    strof = []
    for xx in M:
        for jj in xx:
            strof.append(jj)
    strof = ''.join(map(str, strof))
    strof = strof.replace('[', '')
    strof = strof.replace(']', '')
    strof = strof.replace(' ', '')
    strof = strof.replace(',', '')
    return strof

def make_better_2(strof):
    if (len(strof) % 2 == 1):
        strof += '0'
    return strof

def make_better_3(strof):
    if (len(strof) % 3 == 1):
        strof += '00'
    elif(len(strof) % 3 == 2):
        strof += '0'
    return strof

def make_array_4(dwd):
    ans = []
    for i in range(len(dwd)):
        ans.append(dwd[i][1])
    return ans

def make_array_5(answ, ka, kab):
    ans = []

    for i in range(len(answ)):
        if (i < 2):
            ans.append(answ[i] / ka)
        else:
            ans.append(answ[i] / kab)
    return ans

def prosody(ddd, dd_1):
    max_1 = float(-1.98)
    string = 'not specified'
    for i in range(len(ddd)):
        if (ddd[i] > max_1 and ddd[i] > 0.6):
            max_1 = ddd[i]
            string = dd_1[i]
    return string

def answering(s1):
    read(s1)
    MM = makeclear()
    M = make_array_3(MM)
    dwd = read_2()
    dd_1 = make_array_4(dwd)
    answ = [0] * len(dd_1)
    kab = 0
    ka = 0
    d = dict(dwd)
    strof = make_array_2(M)
    strof = make_better_2(strof)
    s = (strof[ka: ka + 2])
    while(ka + 1 <= len(strof)):
        if (s in d):
            answ[dd_1.index(d[s])] += 1
        elif(s == "00"):
            for j in range(2):
                answ[j] += 1
        ka += 2
        s = (strof[ka:ka + 2])
    strof = make_better_3(strof)
    s = (strof[kab:kab + 3])
    while kab + 2 < (len(strof) - 1):
        if (s in d):
            answ[dd_1.index(d[s])] += 1
        elif (s == "000"):
            for j in range(2, len(dwd)):
                answ[d[dd_1[j]]] += 1
        kab += 3
        s = (strof[kab:kab + 3])

    kab /= 3
    ka /= 2
    ddd = make_array_5(answ, ka, kab)
    return prosody(ddd, dd_1)

dd = make_dict()  # Dictionary of stresses in words.

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    entries = []
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        flash(answering(request.form['username']))
        return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()