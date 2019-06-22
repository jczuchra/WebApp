from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import statistics

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

class Formdata(db.Model):
    __tablename__ = 'formdata'
    id = db.Column(db.Integer, primary_key=True)
    dodano = db.Column(db.DateTime, default=datetime.now)
    imie = db.Column(db.String, nullable=False)
    wiek = db.Column(db.String)
    rodzaj = db.Column(db.String)
    czestosc = db.Column(db.String)
    kwota = db.Column(db.String)
    like = db.Column(db.String)
    wystroj = db.Column(db.String)
    typ = db.Column(db.String)
    wyglad = db.Column(db.Integer)

    def __init__(self, imie, wiek, rodzaj, czestosc, kwota, like, wystroj, typ, wyglad):
        self.imie = imie
        self.wiek = wiek
        self.rodzaj = rodzaj
        self.czestosc = czestosc
        self.kwota = kwota
        self.like = like
        self.wystroj = wystroj
        self.typ = typ
        self.wyglad = wyglad

db.create_all()


@app.route('/')
def home():
    return render_template('home.html')

# Do zrobienia:
@app.route('/poll')
def poll():
    return render_template('poll.html')

@app.route('/thx', methods = ['POST']) #Panel z podziękowaniem w stylu "Dzięki za wypełnienie ankiety, Ania/Ola/Paweł itp
def thx():
    imie = request.form['imie']
    wiek = request.form['wiek']
    rodzaj = request.form['rodzaj']
    czestosc = request.form['czestosc']
    kwota = request.form['kwota']
    like = request.form['like']
    wystroj = request.form['wystroj']
    typ = request.form['typ']
    wyglad = request.form['wyglad']
    print(request.form['fileToUpload'])

    fd=Formdata(imie, wiek, rodzaj, czestosc, kwota, like, wystroj, typ, wyglad)
    db.session.add(fd)
    db.session.commit()

    return render_template('thx.html')

#do zrobienia
@app.route('/dane')   #<- widok z którego można się wybrać do surowych lub obrobionych danych
def dane():
    return render_template('dane.html')

#do zrobienia
@app.route('/raw')
def raw():
    fd = db.session.query(Formdata).all()
    return render_template('raw.html', formdata=fd)

#do zrobienia
@app.route('/processed')
def processed():

    fastfood = db.session.query(Formdata).filter_by(rodzaj = "szybkie typu fastfood").count()
    dobrajakosc = db.session.query(Formdata).filter_by(rodzaj = "wazne, aby bylo z dobrej jakosci skladnikow").count()
    domowe = db.session.query(Formdata).filter_by(rodzaj = "domowe, czesto wybieram bary mleczne").count()
    orientalne = db.session.query(Formdata).filter_by(rodzaj = "lubie probowac czegos nowego, np. kuchnia orientalna").count()
    rodzaj=[['szybkie typu fastfood', fastfood], ['wazne, aby bylo z dobrej jakosci skladnikow', dobrajakosc], ['domowe, czesto wybieram bary mleczne', domowe], ['lubie probowac czegos nowego, np. kuchnia orientalna', orientalne]]

    czesto = db.session.query(Formdata).filter_by(czestosc="bardzo czesto").count()
    czasami = db.session.query(Formdata).filter_by(czestosc="czasami").count()
    sporadycznie = db.session.query(Formdata).filter_by(czestosc="sporadycznie").count()
    nigdy = db.session.query(Formdata).filter_by(czestosc="prawie nigdy").count()
    czestosc = [['bardzo czesto', czesto], ['czasami', czasami],
              ['sporadycznie', sporadycznie],
              ['prawie nigdy', nigdy]]

    czesto = db.session.query(Formdata).filter_by(kwota="10-25zl").count()
    czasami = db.session.query(Formdata).filter_by(kwota="25-40zl").count()
    sporadycznie = db.session.query(Formdata).filter_by(kwota="powyzej 40 zl").count()
    kwota = [['10-25zl', czesto], ['25-40zl', czasami],
                ['powyzej 40 zl', sporadycznie]]

    tak = db.session.query(Formdata).filter_by(like="Tak").count()
    nie = db.session.query(Formdata).filter_by(like="Nie").count()
    like = [['Tak', tak], ['nie', nie]]

    tak = db.session.query(Formdata).filter_by(wystroj="Tak").count()
    nie = db.session.query(Formdata).filter_by(wystroj="Nie").count()
    wystroj= [['Tak', tak], ['nie', nie]]

    duzy = db.session.query(Formdata).filter_by(typ="z duzym wyborem dan w karcie").count()
    kilka = db.session.query(Formdata).filter_by(typ="z kilkoma pozycjami w karciel").count()
    jeden = db.session.query(Formdata).filter_by(typ="z jednym okreslonym typem posilku, np. kebab, pizza").count()
    typ = [['z duzym wyborem dan w karcie', duzy], ['z kilkoma pozycjami w karciel', czasami],
             ['z jednym okreslonym typem posilku, np. kebab, pizza', sporadycznie]]

    jeden = db.session.query(Formdata).filter_by(wyglad="1").count()
    dwa = db.session.query(Formdata).filter_by(wyglad="2").count()
    trzy = db.session.query(Formdata).filter_by(wyglad="3").count()
    cztery = db.session.query(Formdata).filter_by(wyglad="4").count()
    piec = db.session.query(Formdata).filter_by(wyglad="5").count()
    wyglad = [['1', jeden], ['2', dwa],
             ['3', trzy], ['4', cztery], ['5', piec]]

    class Dane:
        def __init__(self, rodzaj, czestosc, kwota, like, wystroj, typ, wyglad):
            self.rodzaj = rodzaj
            self.czestosc = czestosc
            self.kwota = kwota
            self.like = like
            self.wystroj = wystroj
            self.typ = typ
            self.wyglad = wyglad

    readyData = Dane(rodzaj, czestosc, kwota, like, wystroj, typ, wyglad)
    return render_template('processed.html', data=readyData)


if __name__ == "__main__":
    app.debug = True
    app.run()