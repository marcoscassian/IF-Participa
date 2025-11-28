from flask import Flask, render_template
from models import criar_tabelas
from auth.routes import auth_bp 

app = Flask(__name__)
app.secret_key = "CHAVE_ULTRA_SECRETA"

app.register_blueprint(auth_bp)

criar_tabelas()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
