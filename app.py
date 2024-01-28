from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    jsonify,
)
from flask_login import login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap5
from extensions import db, login_manager, csrf
from models import User, Emoji
from forms import RegistrationForm, LoginForm
import os

# define base directory of app
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Configure CSRF protection
csrf.init_app(app)

Bootstrap5(app)


# User authentication and authorization
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_table():
    # db.drop_all()
    # db.create_all()
    print("database created")


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "error")
    return render_template("form.html", form=form, title="Login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("form.html", form=form, title="Register")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout successfully.", "success")
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("view-emoji.html")


@app.route("/saved-emojis")
@login_required
def display_saved_emojis():
    emojis = current_user.emojis
    print(emojis)
    return render_template("saved-emojis.html", emojis=emojis)


@app.route("/save-emoji", methods=["POST"])
@csrf.exempt
def save_emoji():
    emoji_data = request.get_json()

    new_emoji = Emoji(
        name=emoji_data.get("name"),
        category=emoji_data.get("category"),
        group=emoji_data.get("group"),
        html_code=emoji_data.get("htmlCode")[
            0
        ],  # Assuming you only want the first HTML code
        unicode=emoji_data.get("unicode")[
            0
        ],  # Assuming you only want the first Unicode
        user_id=emoji_data.get("userId"),
    )

    db.session.add(new_emoji)
    db.session.commit()

    return jsonify({"message": "Emoji saved successfully"}), 200


@app.route("/update-emoji/<int:emoji_id>", methods=["PUT"])
@csrf.exempt
def update_emoji(emoji_id):
    emoji = Emoji.query.get(emoji_id)
    if emoji:
        data = request.get_json()
        emoji.name = data.get("name", emoji.name)
        db.session.commit()
        return jsonify({"message": "Emoji updated successfully"}), 200
    else:
        return jsonify({"error": "Emoji not found"}), 404


@app.route("/delete-emoji/<int:emoji_id>", methods=["DELETE"])
@csrf.exempt
def delete_emoji(emoji_id):
    emoji = Emoji.query.get(emoji_id)

    if emoji:
        db.session.delete(emoji)
        db.session.commit()
        return jsonify({"message": "Emoji deleted successfully"}), 200
    else:
        return jsonify({"error": "Emoji not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
