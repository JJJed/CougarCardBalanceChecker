from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, VerificationForm, ApproveForm, SetMaxForm
from methods import *
import mysqlmethods
from flask_httpauth import HTTPBasicAuth
import mysql.connector


app = Flask(__name__, static_url_path='/static')
application = app
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


auth = HTTPBasicAuth()

# Define a dictionary of valid usernames and passwords
users = {
    "jed": os.environ.get("APPROVAL_PASSWORD"),
}


# Verify the username and password
@auth.verify_password
def verify_password(username, password):
    return users.get(username) == password


# Example User class (replace it with your actual User model)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect("/balance")
    else:
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # If the user is already logged in, redirect to the balance page
    if current_user.is_authenticated:
        return redirect("/balance")

    form = LoginForm()
    if form.is_submitted():
        user_id = form.user_id.data
        try:
            if mysqlmethods.is_verified(user_id):
                user = User(user_id)
                login_user(user)
                return redirect("/balance")
            else:
                flash('Invalid user ID. Please try again.', 'error')
        except mysql.connector.errors.OperationalError:
            mysqlmethods.re_init()
            flash("Database error. Please try again later.", 'error')
    return render_template("login.html", form=form)


@app.route("/balance", methods=["GET"])
@login_required
def balance():
    user_id = current_user.id
    caf_bal = get_balance(user_id, 2)
    den_bal = get_balance(user_id, 1)
    try:
        name = mysqlmethods.name_from_id(user_id)
    except mysql.connector.errors.OperationalError:
        mysqlmethods.re_init()
        return redirect("/balance")
    user_id = int(user_id)
    return render_template("balance.html", caf_bal=caf_bal, den_bal=den_bal, name=name, user_id=user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    mysqlmethods.check_day()
    form = VerificationForm()
    max_requests = mysqlmethods.get_max()[0]
    requests_today = mysqlmethods.get_daily()[0]
    if form.is_submitted():
        if requests_today < max_requests:
            name = form.name.data
            email = form.email.data
            send_emails(name, email)
            mysqlmethods.increase_daily()
            return redirect("/login")
        else:
            flash('Maximum daily verification slot limit reached. Please try again tomorrow.', 'error')
    return render_template("verify.html", form=form, max_requests=max_requests, requests_today=requests_today)


@app.route("/approve", methods=["GET", "POST"])
@auth.login_required
def approve():
    form = ApproveForm()
    if form.is_submitted():
        user_id = form.user_id.data
        name = form.name.data
        email = form.email.data
        try:
            mysqlmethods.approve(user_id, name, email)
            flash("Success!", "success")
        except mysql.connector.errors.OperationalError:
            mysqlmethods.re_init()
            return redirect("/approve")
        send_approval_email(user_id, email, name)
        return redirect("/approve")
    return render_template("approve.html", form=form)


@app.route("/setmax", methods=["GET", "POST"])
@auth.login_required
def setmax():
    form = SetMaxForm()
    if form.is_submitted():
        max = form.max.data
        try:
            mysqlmethods.set_max(max)
            flash("Success!", "success")
        except mysql.connector.errors.OperationalError:
            mysqlmethods.re_init()
            return redirect("/setmax")
        return redirect("/setmax")
    return render_template("setmax.html", form=form)


if __name__ == '__main__':
    app.run()
