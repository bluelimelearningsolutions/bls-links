# Minimal Flask APP Structure

from flask import Flask,render_template,request, redirect, url_for,flash,abort,session,jsonify
import json
import os.path


app = Flask(__name__)
app.secret_key = 'abrakadabra@#247'

@app.route('/')
def home():
    return render_template('home.html',codes=session.keys()) # displays session

@app.route('/your-url', methods=['GET','POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('home'))

        urls[request.form['code']] = {'url':request.form['url']}
        with open('urls.json','w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True  # TO  save user session input
            # You can display the saved session on the home page
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))

@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url']) 

    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# creating API AND IMPORT jsonify

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))

# To access the API : homepage/api ( This will list all short codes yoo have created)
