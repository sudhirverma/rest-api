from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    
    store = db.relationship("StoreModel", back_populates="tags")
    # this is the secondary table that we've defined here as a table name.
    # SQLAlchemy will know that it has to go through this secondary table in order 
    # to find what items this tag is related to. 
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
