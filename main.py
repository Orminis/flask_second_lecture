from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is ORM which can be used in Flask
from flask_restful import Resource, Api  # Rest for Flask

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:123456@localhost:5432/store"  # configuration of the app object with PostgreSQL

db = SQLAlchemy(app)  # connection of the flask app object with the ORM
api = Api(app)  #


class BookModel(db.Model):  # model of book for the SQL database table
    __tablename__ = "books"  # name of the table in the SQL

    pk = db.Column(db.Integer, primary_key=True)  # Primary key Column
    title = db.Column(db.String(255), nullable=False)  # Column for the book's name    # db.String
    author = db.Column(db.String(255), nullable=False)  # Column for the author's name

    def __repr__(self):
        return f"<{self.pl}> {self.title} from {self.author}"

    def as_dict(self):  # връща обекта като речник за да може да се превърне в json (няма да се наложи да го ползваме
                        # този метод след като почнем да ползваме схеми.)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Books(Resource):
    def get(self):
        books = [b.as_dict() for b in BookModel.query.all()]  # Освен да създава може и да търси в таблици
        return {"books": books}

    def post(self):
        data = request.get_json()
        book = BookModel(**data)  # същото но с повече писане BookModel(title=data.get('title'), author=data.get('author'))
        db.session.add(book)    # добавяме заявката в базата данни
        db.session.comit()      # записваме добавката в базатада данни
        return "ok"


# comanda koqto se prawi samo predi da uchim migracii
# db.create_all()

api.add_resource(Books, "/books/")

if __name__ == '__main__':
    app.run(debug=True)
