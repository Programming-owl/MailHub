from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import psycopg2

# Create your views here.
class user:
    def __init__(self):
        self.tt = 0
    
    def get_id(self, request):
        return request.session['id']
    
    def get_login(self, request):
        return request.session['login']

class DB:
    def __init__(self):
        self.conn = psycopg2.connect("postgres://mail_user:7jMZvwmYRF1Tp7RnPP3kFKRzBGjgg0Pr@dpg-ce4uq8p4reb0n5m70ke0-a.oregon-postgres.render.com/mail")
        self.cursor = self.conn.cursor()

    def table_exists(self, name):
        try:
            self.cursor.execute(f"SELECT * FROM {name}")
            return True
        
        except:
            self.__init__()
            return False

    def login_free(self, login):
        if (not self.table_exists('users')):
            self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, login text, password text)")
            self.conn.commit()

            return True
        
        self.cursor.execute("SELECT login FROM users")
        f = self.cursor.fetchall()

        for i in f:
            if login in i:
                return False
        
        return True

    def new_account(self, request, login, password):
        if (not self.login_free(login)):
            return 'Такой логин уже существует'

        self.cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        self.conn.commit()

        self.cursor.execute("SELECT id FROM users WHERE login=%s", (login, ))
        id = self.cursor.fetchone()[0]

        request.session['login'] = login
        request.session['id'] = id
        
        return "ok"
    
    def login(self, request, login, password):
        if (self.login_free(login)):
            return "Неверный логин"
        
        self.cursor.execute("SELECT * FROM users WHERE login=%s", (login,))
        f = self.cursor.fetchall()[0]

        user_id = f[0]
        user_password = f[2]

        if (user_password == password):
            request.session['login'] = login
            request.session['id'] = user_id

            return 'ok'
        
        return 'Неверный пароль'

    def send_message(self, login, theme, message, from_user):
        if (not self.table_exists('messages')):
            self.cursor.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, from_user text, to_user text, theme text, message text, read_status text)")
            self.conn.commit()

        if (from_user == login):
            return "Не надо"

        self.cursor.execute("INSERT INTO messages (from_user, to_user, theme, message, read_status) VALUES (%s,%s,%s,%s,%s)", (from_user, login, theme, message, '0'))
        self.conn.commit()

        return 'ok'

    def get_messages(self, login):
        if (not self.table_exists("messages")):
            return None
        
        self.cursor.execute("SELECT * FROM messages WHERE to_user=%s", (login, ))
        f = self.cursor.fetchall()

        ans = []
        _list = []

        for i in f:
            _list.append(int(i[0]))
        
        _list.sort()

        for j in _list:
            for i in f:
                if (i[0] == j):
                    ans.append({'id':int(i[0]), 'from':i[1], 'theme':i[3], 'message':i[4], 'read_status':int(i[5])})

        return ans
    
    def get_message(self, m_id, login):
        if (not self.table_exists("messages")):
            return None
        
        self.cursor.execute("SELECT * FROM messages WHERE to_user=%s and id=%s", (login, m_id))
        f = self.cursor.fetchone()

        if (f == None):
            self.cursor.execute("SELECT * FROM messages WHERE from_user=%s and id=%s", (login, m_id))
            f = self.cursor.fetchone()

            if (f == None):
                return None

            return {"id":f[0], "from":f[1], 'theme':f[3], 'message':f[4]}
        
        self.cursor.execute("UPDATE messages set read_status=1 WHERE to_user=%s and id=%s", (login, m_id))
        self.conn.commit()  
        
        return {"id":f[0], "from":f[1], 'theme':f[3], 'message':f[4]}

    def get_my_messages(self, login):
        if (not self.table_exists('messages')):
            return None
        
        self.cursor.execute("SELECT * FROM messages WHERE from_user=%s", (login, ))
        f = self.cursor.fetchall()

        if (f == None):
            return None

        ans = []
        _list = []

        for i in f:
            _list.append(int(i[0]))
        
        _list.sort()

        for j in _list:
            for i in f:
                if (i[0] == j):
                    ans.append({'id':int(i[0]), 'to':i[2], 'theme':i[3], 'message':i[4]})

        return ans


def login_requered(f):
    def main(request, **kwargs):
        if (request.session['id'] == None):
            return HttpResponseRedirect("/login")

        return f(request, **kwargs)
    
    return main

global db
db = DB()

global USER
USER = user()

#!------ autenfication functions

def login(request):
    return render(request, 'index.html')

def login_post(request):
    login = request.GET['login']
    password = request.GET['password']

    status = db.login(request, login, password)

    return JsonResponse({'status':status})

def signup(request):
    return render(request, 'signup.html')

def signin_post(request):
    login = request.GET['login']
    password = request.GET['password']

    status = db.new_account(request, login, password)

    return JsonResponse({'status':status})

#!---- homepage
@login_requered
def home(request):
    return render(request, 'homepage.html')


@login_requered
def new_message(request):
    

    return render(request, 'new_message.html')

@login_requered
def send(request):
    login = request.GET['to']
    theme = request.GET['theme']
    message = request.GET['message'].replace("<br>", "\n")

    if (db.login_free(login)):
        return JsonResponse({'status':"Пользователь не найден"})

    status = db.send_message(login, theme, message, request.session['login'])

    return JsonResponse({'status':status})


@login_requered
def show_messages(request):
    _db = DB()
    messages = _db.get_messages(request.session['login'])

    if (messages != None):
        messages = messages[::-1]

    else:
        messages = "None"

    return JsonResponse({'ans':messages})

@login_requered
def message(request, m_id):
    print(m_id)

    s = db.get_message(m_id, request.session['login'])

    return render(request, 'message.html', {"id":s['id'], 'from':s['from'], "theme":s['theme'], 'message':s['message']})

@login_requered
def sent(request):
    return render(request, 'my_messages.html')

def get_sent(request):
    my_messages = db.get_my_messages(request.session['login'])

    if (my_messages == None):
        ans = "None"
    else:
        my_messages = my_messages[::-1]
    
    return JsonResponse({"ans":my_messages})

def logout(request):
    request.session['login'] = None
    request.session['id'] = None

    return HttpResponseRedirect('/login')