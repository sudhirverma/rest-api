from flask_sqlalchemy import SQLAlchemy


# What this does is it create this SQLAlchemy object from the flask SQLAlchemy extension, and we can
# then go and link it to our Flask app.
db = SQLAlchemy() 