from flask import Flask, render_template, request, redirect, url_for
import db
from db import insert_data, query

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        type = request.form.get('form_type')
        if type == 'input_form':
            name = request.form.get('name', 'Unknown')
            age = request.form.get('age', 100)
            return f'Name: {name}\nAge: {age}'

        elif type == 'fetch_data_form':
            return redirect(url_for('display'))






@app.route('/display', methods=['GET', 'POST'])
def display():
    results = query()
    print(f'Rows::: {results}')
    return render_template('display.html', results=results)




if __name__ == '__main__':
    app.run(debug=True)




