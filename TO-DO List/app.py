from flask import Flask, render_template, url_for, redirect, request, abort, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {}
todos = {}
roles = {}

roles = {
    'admin':'admin',
    'manager':'manager',
    'user':'user',
    'guest':'guest'
}

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
@app.context_processor
def inject_roles():
    return dict(roles=roles)


@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

class User(UserMixin):
    def __init__(self, id, username, password, role='user'):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        if username.data in [user.username for user in users.values()]:
            raise ValidationError('That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = next((user for user in users.values() if user.username == form.username.data), None)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            # Pass error message to the login page
            return render_template('login.html', form=form, error='Invalid username or password. You can register here if you don\'t have an account.')
    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = request.args.get('error')
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_id = len(users) + 1
        # Create an admin user for demonstration
        if len(users) == 0:  # Create admin only if it's the first user
            admin_user = User(id=1, username='admin', password=bcrypt.generate_password_hash('admin').decode('utf-8'), role='admin')
            users[1] = admin_user
            new_user = User(id=user_id, username=form.username.data, password=hashed_password, role='user')
            users[user_id] = new_user
            todos[user_id] = []
        return redirect(url_for('login'))
    return render_template('register.html', form=form, error=error)

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    if request.method == 'POST':
        task_content = request.form['task']
        if current_user.id not in todos:
            todos[current_user.id] = []
        todos[current_user.id].append({"task": task_content, "done": False})
        return redirect(url_for('dashboard'))
    
    user_tasks = todos.get(current_user.id, [])
    return render_template('todo.html', tasks=user_tasks)
@app.route("/index")
@login_required
def index():
    user_todos = todos.get(current_user.id, [])
    return render_template("index.html", todos=user_todos)

@app.route("/add", methods=["POST"])
@login_required
def add():
    todo = request.form["todo"]
    todos[current_user.id].append({"task": todo, "done": False})
    return redirect(url_for("index"))

@app.route("/edit/<int:index>", methods=["GET", "POST"])
@login_required
def edit(index):
    user_todos = todos.get(current_user.id, [])
    if index < len(user_todos):
        todo = user_todos[index]
        if request.method == "POST":
            todo['task'] = request.form.get('todo')
            return redirect(url_for("index"))
        else:
            return render_template("edit.html", todo=todo, index=index)
    return redirect(url_for("index"))

@app.route("/check/<int:index>")
@login_required
def check(index):
    user_todos = todos.get(current_user.id, [])
    if index < len(user_todos):
        todo = user_todos[index]
        todo['done'] = not todo['done']
    return redirect(url_for("index"))

@app.route('/delete/<int:index>')
@login_required
def delete(index):
    user_todos = todos.get(current_user.id, [])
    if index < len(user_todos):
        del user_todos[index]
    return redirect(url_for("index"))

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

if __name__ == "__main__":
    app.run(debug=True)
 