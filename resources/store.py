import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models import StoreModel
from db import db
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        #it's going to turn the dictionary into keyword arguments
        store = StoreModel(**store_data)

        try:
            # when we add to the session that is going to put it in a place where 
            # it's not written into the database file, but it will be written to 
            # the database file when we commit.
            db.session.add(store)
            # And that's what committing does is actually saving to disk.
            db.session.commit()
        except IntegrityError:
            # integrity error, which SQLAlchemy raises when we try to insert something into the database, but that
            # woud cause an inconsistency in the data. It would violate one of the constraints we've set 
            # And if you remember in StoreModel we've got the name to be unique. So it could be that when we try to 
            # insert a store that already exits, this raises an integrity error, and we would that abort with  a 500 
            # and respond with a message
            abort(
                400,
                message="A store with that name already exits."
            )
        except SQLAlchemyError:
            abort(500, "An error occurred whilte inserting the item.")

        return store

