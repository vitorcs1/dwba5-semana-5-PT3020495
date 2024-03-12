from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators=[DataRequired()])
    lastname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    college = StringField('Informe a sua Instituição de ensino:', validators=[DataRequired()])
    discipline = SelectField('Informe a sua disciplina:', choices=[('DSWA5'), ('DWBA4'), ('Gestão de projetos')])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['lastname'] = form.lastname.data
        session['college'] = form.college.data
        session['discipline'] = form.discipline.data
        session['userIp'] = request.headers.get("host")
        session['appHost'] = request.headers.get("Referer")
        return redirect(url_for('index'))
    return render_template('index.html',
                           form=form,
                           name=session.get('name'),
                           lastname=session.get('lastname'),
                           college=session.get('college'),
                           discipline=session.get('discipline'),
                           userIp=session.get('userIp'),
                           appHost=session.get('appHost'),
                           current_time=datetime.utcnow())
