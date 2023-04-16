import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        #It retrieves the item from the database using the item's primary key.
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        db.session.delete(item)
        db.session.commit()

        return {"message": "Item deleted"}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        print("sdfjkhfdkhfkljsdfkljskljsdfkljklsdfjklsfjklsdfjklsdfjklsdfjkldfjklfjdkljdfkljsdfkljfl")
        #it's going to turn the dictionary into keyword arguments
        item = ItemModel(**item_data)

        try:
            # when we add to the session that is going to put it in a place where 
            # it's not written into the database file, but it will be written to 
            # the database file when we commit.
            db.session.add(item)
            # And that's what committing does is actually saving to disk.
            db.session.commit()
        except SQLAlchemyError:
            abort(500, "An error occurred whilte inserting the item.")

        return item

