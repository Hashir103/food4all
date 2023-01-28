# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_googlemaps import GoogleMaps

# create the application object
app = Flask(__name__)

# config
app.secret_key = 'HashirRyanYash'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyBWkQvoVZn9ObPO_f_lUxOqSqMjK69q9RE"

# Initialize the extension
GoogleMaps(app)

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# use decorators to link the function to a url
@app.route('/info')
def json():
    return render_template('info.json')

@app.route('/')
def home():
    return render_template('index.html')  # render a template
    # return "Hello, World!"  # return a string

@app.route('/consumers')
def consumers():
    return render_template('consumer.html')  # render a template
    # return "Hello, World!"  # return a string

@app.route('/donate')
@login_required
def welcome():
    return render_template('donate.html')  # render a template

# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'business' or request.form['password'] != 'owner':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('home'))


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)