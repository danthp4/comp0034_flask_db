from flask import render_template, Blueprint, request, flash, redirect, url_for

from app.main.forms import SignupForm

# bp_main = Blueprint('main', __name__, template_folder='templates', static_folder='static')
bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def index():
    return render_template('index.html')


@bp_main.route('/signup/', methods=['POST', 'GET'])
def signup():
    signup_form = SignupForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        flash('Signup requested for {}'.format(signup_form.name.data))
        # Code to add the student to the database goes here
        return redirect(url_for('main.index'))
    return render_template('signup.html', form=signup_form)
