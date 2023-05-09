from db import db

# inherit from db.Model
# This now becomes a mapping between a row in a table to a Python class and therefore Python object


class StoreModel(db.Model):
    # this is gonna tell SQLAlchemy that we wanna create or use a table
    #  called items for this class and all the object of this class
    __tablename__ = "stores"

    # This is how we define a column that will be part of this items table.
    # And this is gonna be an integer column and it's the primary key of the table
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False)

    # back_populates, SQLAlchemy knows that these are two ends of a relationship.
    # Therefore the item has a store ID, which is what link one item to one store
    # and it will know that items is the other end of that relationship and find
    # all the items that have a store ID equal to this store's ID

    # Lazy, equal dynamic just means that the items here are not going to be fetched
    # from the database until we tell it to.
    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
