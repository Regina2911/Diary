#Импорт
from flask import Flask, render_template, request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Задаем секретный ключ для работы session
app.secret_key = 'my_top_secret_123'
#Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)
#Создание таблицы

class Card(db.Model):
    #Создание полей
    #id
    id = db.Column(db.Integer, primary_key=True)
    #Заголовок
    title = db.Column(db.String(100), nullable=False)
    #Описание
    subtitle = db.Column(db.String(300), nullable=False)
    #Текст
    text = db.Column(db.Text, nullable=False)
    #email владельца карточки
    user_email = db.Column(db.String(100), nullable=False)

    #Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Задание №1. Создать таблицу User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String(70), nullable=False)




#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        user = User.query.filter_by(email=form_login).first()
        if not user:
            return render_template("login.html", error="Неверный логин или пароль")
        if user.password != form_password:
            return render_template("login.html", error="Неверный логин или пароль")

        session["user_email"] = user.email
        return redirect("/index")
    
    else:
        return render_template('login.html')





@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('registration.html', error="Такой пользователь уже существует")
        if len(password) < 8:
            return render_template('registration.html', error="Праоль должен содержать более 8 символов")
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        #Задание №3. Реализовать запись пользователей
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    #Задание №4. Сделай, чтобы пользователь видел тольуо свои карточки
    email = session["user_email"]
    if not email:
        return redirect('/')
    cards = Card.query.filter_by(user_email=email).order_by(Card.id).all()
    return render_template('index.html', cards=cards)

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    email = session["user_email"]
    if not email:
        return redirect('/')
    card = Card.query.filter_by(user_email=email, id=id).first()


    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        email = session["user_email"]
        if not email:
            return redirect('/')
        
        #Задание №4. Сделай, чтобы создание карточки происходило от имени пользователя
        card = Card(title=title, subtitle=subtitle, text=text, user_email = email)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.app_context().push()
    db.create_all()
    app.run(debug=True)
