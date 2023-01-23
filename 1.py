from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from bs4 import BeautifulSoup
import requests

answer = 0

app = Flask(__name__)

@app.route("/")
def about():
    return render_template('about.html')

@app.route("/home")
def home():
    return render_template('home.html', answer=0)

@app.route("/answer", methods=['POST'])
def result():
    
    streamers = ["s1mple","buster","n3koglai","bratishkinoff","evelone192"]
    new = str((request.form.get('streamer')))
    new = new.lower()
    if new in streamers:
        return render_template('home.html', answer="входит")
    streamers.append(new)
    url = "https://streaminside.ru/streamers/" + streamers[-1]
    req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    bs = BeautifulSoup(req.text, 'lxml')
    exists = bs.findChildren('strong', {'class': 'd-block text-gray-dark'}) 

    if str(exists) in f'[<strong class="d-block text-gray-dark">Пользователь с ником "{streamers[-1]}" не найден!</strong>]':
        return render_template('home.html', answer="нет на сайте")

    
    
    else:

        if bs.find('p' , {'class': 'mb-0 p-1 pr-2 pl-2 nowrap socialHeaderTwitch'}):
            folowers = []
            for i in streamers:
                url = "https://streaminside.ru/streamers/" + i
                req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                bs = BeautifulSoup(req.text, 'lxml')

                twitch = bs.find('p' , {'class': 'mb-0 p-1 pr-2 pl-2 nowrap socialHeaderTwitch'})       
                fcounter = twitch.find('a', {'class': 'socialHeaderCounter'})
                fcounter = int((fcounter.find(text=True, recursive=False)).replace(',',''))
                folowers.append(fcounter)
        else:
            return render_template('home.html', answer = "не твич")
        print (streamers)
        print(folowers)
        fig, ax = plt.subplots()
        ax.bar(streamers, folowers)
        plt.ylabel("Количество фоловеров")
        fig.set_figwidth(15)    #  ширина Figure
        fig.set_figheight(6)    #  высота Figure

        buf = BytesIO()
        fig.savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode('ascii')

        return render_template('result.html', streamer=streamers, folowers=folowers, data=data)




if __name__ == '__main__':
    app.run(debug=True, port= 8000)