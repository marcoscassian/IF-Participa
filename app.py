from flask import Flask, render_template
from models import criar_tabelas

app = Flask(__name__)

criar_tabelas()

@app.route('/')
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
