from flask import Flask, render_template, redirect
from flask_restful import Api, Resource
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from forms.user import RegisterForm, LoginForm
from data.users import User

app = Flask(__name__)
db_session.global_init("db/users_data.db")
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
lessons = [
    {
        'name': 'Скачивание и установка',
        'lesson-text': '''Для начала работы с языком программирования Python,
        мы должны скачать установщик с официального сайта Python(python.org).
        Далее просто следовать простейшим шагам установки, после которых можно приступать к практике.
        Затем стоит очень важный шаг, выбор IDE для написания программ,
        этот шаг очень ответственный и его можно сравнить с выбором автомобиля,
        и для каждого это строго индивидуально. Мы не будем навязывать вам что либо
        и лишь посоветуем присмотреться к таким вариантам, как - PyCharm, VS code, Atom'''
    },
    {
        'name': 'Переменные и типы данных',
        'lesson-text': '''Если достаточно формально подходить к вопросу о типизации языка Python, 
        то можно сказать, что он относится к языкам с неявной сильной динамической типизацией.
        Неявная типизация означает, что при объявлении переменной вам не нужно указывать её тип,
        при явной – это делать необходимо. В качестве примера языков с явной типизацией можно привести Java, 
        C++. Вот как будет выглядеть объявление целочисленной переменной в Java и Python: 
        (Java) - int i = 0; (Python) - i = 0. Также в python присутствуют и другие типы данных, таких как 
        float(число с плавающей точкой), str(строка), int(целочисленный тип), boolean(логический тип), 
        None(неопределенный тип), bytes(байты). Рассмотрим как создаются объекты в памяти, их устройство, процесс 
        объявления новых переменных и работу операции присваивания. Для того, чтобы объявить и сразу инициализировать 
        переменную необходимо написать её имя, потом поставить знак равенства и значение, с которым эта переменная будет
        создана. Например строка: a = 5 объявляет переменную b и присваивает ей значение 5. Целочисленное значение 5 в 
        рамках языка Python по сути своей является объектом. Объект, в данном случае – это абстракция для представления
        данных, данные – это числа, списки, строки и т.п. При этом, под данными следует понимать как непосредственно 
        сами объекты, так и отношения между ними (об этом чуть позже). Каждый объект имеет три атрибута – это 
        идентификатор, значение и тип. Идентификатор – это уникальный признак объекта, позволяющий отличать объекты друг
        от друга, а значение – непосредственно информация, хранящаяся в памяти, которой управляет интерпретатор.'''
    },
    {
        'name': 'Условные операторы в Python',
        'lesson-text': '''В этом уроке рассмотрим оператор ветвления if. Основная цель – это дать общее представление 
        об этом операторе и на простых примерах показать базовые принципы работы с ним. Оператор ветвления if  позволяет
        выполнить определенный набор инструкций в зависимости от некоторого условия. Возможны следующие варианты 
        использования: if выражение: инструкция 1, инструкция 2... инструкция n. После оператора if записывается 
        выражение. Если это выражение истинно, то выполняются инструкции, определяемые данным оператором. Выражение 
        является истинным, если его результатом является число не равное нулю, непустой объект, либо логическое True. 
        После выражения нужно поставить двоеточие “:”. ВАЖНО: блок кода, который необходимо выполнить, в случае 
        истинности выражения, отделяется четырьмя пробелами слева! Бывают случаи, когда необходимо предусмотреть 
        альтернативный вариант выполнения программы. Т.е. при истинном условии нужно выполнить один набор инструкций, 
        при ложном – другой. Для этого используется конструкция if – else или if - elif - else.'''
    },
    {
        'name': 'Базовые циклы в Python',
        'lesson-text': '''В python присутствует 2 вида цикла - while и for. Оператор цикла while  выполняет указанный 
        набор инструкций до тех пор, пока условие цикла истинно. Истинность условия определяется также как и в 
        операторе if. Синтаксис оператора while  выглядит так: while выражение: инструкция 1, инструкция 2... 
        инструкция n. Выполняемый набор инструкций называется телом цикла. Оператор for  выполняет указанный набор 
        инструкций заданное количество раз, которое определяется количеством элементов в наборе. 
        Пример: for i in range(5): print('А'). Данная конструкция выведет букву А 5 раз построчно. Также с помощью 
        цикла for можно выполнить операции над элементами списка или пройтись по элементам строки.'''
    },
    {
        'name': 'Множества, списки, словари и т.д',
        'lesson-text': '''Список (list) – это структура данных для хранения объектов различных типов. 
        Если вы использовали другие языки программирования, то вам должно быть знакомо понятие массива. 
        Так вот, список очень похож на массив, только, как было уже сказано выше, в нем можно хранить объекты 
        различных типов. Размер списка не статичен, его можно изменять. Список по своей природе является изменяемым 
        типом данных. Про типы данных можно подробно прочитать здесь. Переменная, определяемая как список, содержит 
        ссылку на структуру в памяти, которая в свою очередь хранит ссылки на какие-либо другие объекты или 
        структуры. Cоздать список можно одним из следующих способов: a = [], a = list(), также можно наполнить 
        их данными при обьявлении. Добавление элемента в список осуществляется с помощью метода append(): 
        a = [1] -> a.append('hello') -> [1, 'hello']. Если необходимо работать с элементами списка, то обратиться к ним 
        можно по индексу (нумерация начинается с 0): a = ['a', 'b', 'c'] -> print(a[1]) -> 'c'. Также, используя 
        индексацию, можно изменять элементы списка. Далее, перейдем  множествам. Множество в python - "контейнер", 
        содержащий не повторяющиеся элементы в случайном порядке. Создаём множества: a = set(). Множества удобно 
        использовать для удаления повторяющихся элементов: words = ['hello', 'daddy', 'hello', 'mum'] -> set(words) -> 
        {'hello', 'daddy', 'mum'}. Добавляются элементы в множества с помощью метода add: {'word1', 'word2'} -> 
        a.add('word3') -> {'word1', 'word2', 'word3'}. Перейдем к последней рассматриваемой коллекции - словарь. 
        Словари (dict) – это одна из наиболее часто используемых структур данных, позволяющая хранить объекты, для 
        доступа к которым используется ключ. В этом уроке будут рассмотрены операции создания, удаления, работы со 
        словарями и их методы. Словарь (dict) представляет собой структуру данных 
        (которая ещё называется ассоциативный массив), предназначенную для хранения произвольных объектов с доступом 
        по ключу. Данные в словаре хранятся в формате ключ – значение. Если вспомнить такую структуру как список, то 
        доступ к его элементам осуществляется по индексу, который представляет собой целое неотрицательное число, причем
        мы сами, непосредственно, не участвуем в его создании (индекса). В словаре аналогом индекса является ключ, при 
        этом ответственность за его формирование ложится на программиста. Пустой словарь можно создать, 
        используя функцию dict(), либо просто указав пустые фигурные скобки: a = dict(), a = {}. Если необходимо 
        создать словарь с заранее подготовленным набором данных, то можно использовать один из перечисленных выше 
        подходов, но с перечислением групп ключ-значение: a = {'a': 1, 'b': 2, 'c': 3}. Добавление и удаление элемента
        Чтобы добавить элемент в словарь нужно указать новый ключ и значение: a['d'] = 4. Итерация по элементам словаря 
        может проводиться по ключам и/или значениям: for key, value in a: print(key, value) (данная конструкция выведет 
        последовательно и построчно ключи словаря и соответсвующие им значения).'''
    }
]


@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/install_python')
def install_python():
    return render_template("install_python.html")


@app.route("/data_type")
def data_type():
    return render_template("data_type.html")


@app.route("/conditional_operators")
def conditional_operators():
    return render_template("conditional_operators.html")


@app.route("/basic_loops")
def basic_loops():
    return render_template("basic_loops.html")


@app.route("/sets_lists_etc")
def sets_lists_etc():
    return render_template("sets_lists_etc.html")


@app.route("/API")
def API():
    return render_template("API.html")


@app.route("/first_ex")
def first_ex():
    return render_template("first_ex.html")


@app.route("/first_ex_ans")
def first_ex_ans():
    return render_template("first_ex_ans.html")

@app.route("/second_ex")
def second_ex():
    return render_template("second_ex.html")


@app.route("/second_ex_ans")
def second_ex_ans():
    return render_template("second_ex_ans.html")

@app.route("/third_ex")
def third_ex():
    return render_template("third_ex.html")

@app.route("/third_ex_ans")
def third_ex_ans():
    return render_template("third_ex_ans.html")

@app.route("/fourth_ex")
def fourth_ex():
    return render_template("fourth_ex.html")

@app.route("/fourth_ex_ans")
def fourth_ex_ans():
    return render_template("fourth_ex_ans.html")

class Quote(Resource):
    def get(self, name='default'):
        if name == 'default':
            return lessons
        for i in lessons:
            if(i["name"] == name):
                return i
        return "Quote not found", 404


api.add_resource(Quote, "/main", "/main/", "/main/<string:name>")


if __name__ == '__main__':
    app.run()
