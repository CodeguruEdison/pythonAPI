
from typing import List
import uuid
from flask import jsonify, request
from flask.views import MethodView;
from flask_smorest import Blueprint,abort
from db import db
from schemas import PlainTagSchema, StoreSchema, TagSchema
from models import TagModel,StoreModel
from sqlalchemy.exc import SQLAlchemyError,IntegrityError


blp = Blueprint("tags",__name__,description="Operation on tags")

@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id:int):
        store:StoreSchema =StoreModel.query.get_or_404(store_id)
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)
        
        print(tag)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag

    
@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id:int):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
