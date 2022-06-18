from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:123456@localhost:5432/store"
db = SQLAlchemy(app)











if __name__ == '__main__':
    app.run(debug=True)
