from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy is ORM which can be used in Flask
from flask_restful import Resource, Api  # Rest for Flask
from decouple import config
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}@' \
                                        f'localhost:{config("DB_PORT")}/{config("DB_NAME")}'  # configuration of the app object with PostgreSQL

db = SQLAlchemy(app)  # connection of the flask app object with the ORM
api = Api(app)  #
migrate = Migrate(app, db)


class BookModel(db.Model):  # model of book for the SQL database table
    __tablename__ = "books"  # name of the table in the SQL

    pk = db.Column(db.Integer, primary_key=True)  # Primary key Column
    title = db.Column(db.String(255), nullable=False)  # Column for the book's name    # db.String
    author = db.Column(db.String(255), nullable=False)  # Column for the author's name
    reader_pk = db.Column(db.Integer, db.ForeignKey("readers.pk"))  # one-to-many relationship Foreign key to
    # Reader table pk. readers.pk is the name of the table and the name of the column
    reader = db.relationship("ReaderModel") # орм-а прави join/връзка с класа ReaderModel И ни връща
    # читателя който седи на reader_pk за книгата
    # BookModel.query.all()[0].reader


    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):  # връща обекта като речник за да може да се превърне в json (няма да се наложи да го ползваме
        # този метод след като почнем да ползваме схеми.)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReaderModel(db.Model):
    __tablename__ = "readers"

    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    books = db.relationship("BookModel", backref="book", lazy='dynamic')
    # lazy='dynamic' - relationship-a се изпълнява само когато се извиква
    # za debug ReaderModel.query.all()[0].books = връща всички книги които са закачени към читателя

    def __repr__(self):
        return f"<{self.pk}> {self.first_name} {self.last_name}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AuthorModel(db.Model):
    __tablename__ = "author"

    pk = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    nationality = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<{self.pk}> {self.first_name} {self.last_name}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Books(Resource):
    def get(self):
        books = BookModel.query.all()
        books_data = [b.as_dict() for b in books]  # Освен да създава може и да търси в таблици
        return {"books": books_data}  # Обръщаме всички книги като речник чрез метода as_dict
        # и връщаме речник с вложения речник от предния ред

    def post(self):
        data = request.get_json()
        book = BookModel(
            **data)  # същото но с повече писане BookModel(title=data.get('title'), author=data.get('author'))
        db.session.add(book)  # добавяме заявката в базата данни
        db.session.commit()  # записваме добавката в базатада данни
        return book.as_dict()


# TODO
# class Reader(Resource):
#     pass

# команда която ползваме само преди да вземем миграции
# db.create_all()

api.add_resource(Books, "/books/")

if __name__ == '__main__':
    app.run(debug=True)
