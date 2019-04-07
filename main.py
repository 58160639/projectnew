from flask import Flask, render_template, request, jsonify
import mysql.connector
import re
import deepcut
app = Flask(__name__)

key_words = [
    ['ใคร', 'แสดง', 'หนัง', 'เรื่อง'],
    ['กำกับ', 'หนัง', 'เรื่อง', 'ใคร'],
    ['เข้า', 'ฉาย', 'วัน', 'ไหน'],
    ['vote'],
    ['ภาษา'],
    ['บริษัท'],
    ['เรื่อง', 'ย่อ'],
    ['บ้าง', 'แสดง', 'อะไร'],
    ['กำกับ', 'อะไร', 'บ้าง'],
    ['หนัง', 'แนว', 'ไหน'],
    ['ระยะ', 'เวลา']
]

def connectDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="moviedb"
    )
    return mydb

def check_words(words):
    score = []
    for key in key_words:
        score_rec = 0
        for word in words:
            if word in key:
                score_rec += 1
        percent = (score_rec / len(key)) * 100
        score.append(percent)
    print(score)
    if max(score) != 0:
        return score.index(max(score))
    else:
        return -1

def query(index, words):
    print('index ' + str(index))
    mydb = connectDB()
    mycursor = mydb.cursor()
    querystr = None
    result = []
    if index == 0:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title, cast.castname, cast.gender, cast.the_character FROM movie INNER JOIN movie_has_cast on movie_has_cast.movie_idmovie = movie.idmovie INNER JOIN cast on movie_has_cast.cast_idcast = cast.idcast where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'name': v[1], 'gender': v[2], 'charactor': v[3]} for v in myresult]
    if index == 1:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title, crew.crewname, crew.gender FROM movie INNER JOIN movie_has_crew on movie_has_crew.movie_idmovie = movie.idmovie INNER JOIN crew on movie_has_crew.crew_idcrew = crew.idcrew where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'name': v[1], 'gender': v[2]} for v in myresult]
    if index == 2:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title, movie.release_date FROM movie where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'release_date': v[1]} for v in myresult]
    if index == 3:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title, movie.vote FROM movie where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'vote': v[1]} for v in myresult]
    if index == 4:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title, movie.language FROM movie where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'language': v[1]} for v in myresult]
    if index == 5:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT production_companies.name FROM production_companies INNER JOIN movie_has_production_companies on movie_has_production_companies.production_companies_idproduction_companies = production_companies.idproduction INNER JOIN movie on movie.idmovie = movie_has_production_companies.movie_idmovie WHERE movie.title ='" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'name': v[0]} for v in myresult]
    if index == 6:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT overview FROM movie WHERE movie.title ='" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'overview': v[0]} for v in myresult]
    if index == 7:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title FROM cast INNER JOIN movie_has_cast ON movie_has_cast.cast_idcast = cast.idcast INNER JOIN movie on movie.idmovie = movie_has_cast.movie_idmovie WHERE cast.castname = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'title': v[0]} for v in myresult]
    if index == 8:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.title FROM crew INNER JOIN movie_has_crew ON crew.idcrew = movie_has_crew.crew_idcrew INNER JOIN movie ON movie.idmovie = movie_has_crew.crew_idcrew WHERE crew.crewname = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'title': v[0]} for v in myresult]
    if index == 9:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT genres.Movie_genres FROM movie INNER JOIN movie_has_genres on movie_has_genres.movie_idmovie = movie.idmovie INNER JOIN genres on genres.idgenres = movie_has_genres.genres_idgenres WHERE movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'genres': v[0]} for v in myresult]
    if index == 10:
        result = re.search("'(.*)'", words).group(1)
        querystr = "SELECT movie.runtime FROM movie where movie.title = '" + result + "'"
        print(querystr)
        mycursor.execute(querystr)
        myresult = mycursor.fetchall()
        result = [{'runtime': v[0]} for v in myresult]
    return result

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    data = request.args.get('data')
    words = deepcut.tokenize(data)
    store_word = []
    for word in words:
        if word not in store_word:
            if word != ' ':
                store_word.append(word)
    print(store_word)
    index = check_words(store_word)
    if index != -1:
        res = query(index, data)
    else:
        res = []
    url = None
    if len(res) > 0:
        if index == 0:
            url = 'result.html'
        if index == 1:
            url = 'result1.html'
        if index == 2:
            url = 'result2.html'
        if index == 3:
            url = 'result3.html'
        if index == 4:
            url = 'result4.html'
        if index == 5:
            url = 'result5.html'
        if index == 6:
            url = 'result6.html'
        if index == 7:
            url = 'result7.html'
        if index == 8:
            url = 'result8.html'
        if index == 9:
            url = 'result9.html'
        if index == 10:
            url = 'result10.html'
        return render_template(url, res=res)
    else:
        return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
