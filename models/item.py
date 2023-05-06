from sqlalchemy import ForeignKey
from db import db

# inherit from db.Model
# This now becomes a mapping between a row in a table to a Python class and therefore Python object
class ItemModel(db.Model):
    # this is gonna tell SQLAlchemy that we wanna create or use a table
    #  called items for this class and all the object of this class
    __tablename__ = "items"

    # This is how we define a column that will be part of this items table.
    # And this is gonna be an integer column and it's the primary key of the table
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=False, nullable=False)

    description = db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    # Now that we've got the store_id here, we can tell SQLAlchemy, which will 
    # then tell our SQL database that the store_id is a foreign key
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)


    # grab me a store object, or a store model object. That has this store ID.

    # SQLAlchemy knows that the stores table is used by the StoreModel class.
    # So when we have a store ID that is using the stores table, we can then define 
    # a relationship with the StoreModel class, and it will automatically populate 
    # the store variable with a StoreModel object, whose ID matches that of the foreign key.
    store = db.relationship("StoreModel", back_populates="items")

    # we cannot create an ItemModel until you've created the store that it will be associated


    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")