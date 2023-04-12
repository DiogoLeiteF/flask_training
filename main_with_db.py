from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self) -> str:
        return f"Video(name = {self.name}, views = {self.views}, likes = {self.likes})"


with app.app_context():
    db.create_all()


video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required = True)
video_put_args.add_argument('views', type=int, help='Views of the video', required = True)
video_put_args.add_argument('likes', type=int, help='Likes of the video', required = True)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video')
video_update_args.add_argument('views', type=int, help='Views of the video')
video_update_args.add_argument('likes', type=int, help='Likes of the video')



resouce_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views' : fields.Integer,
    'likes': fields.Integer,
}


class Video(Resource):
    @marshal_with(resouce_fields) #convert the query object in the serialized specified in the "resource_fields"
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video not found...")
        return result
    

    @marshal_with(resouce_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")

        video = VideoModel(id = video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201


    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video not found...")
        db.session.delete(result)
        db.session.commit()
        return '', 204 # deleted successefully
    

    @marshal_with(resouce_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video not found...")

        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']

        # db.session.add(result)  # not required 
        db.session.commit()

        return result



# register the resource
# api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__  == '__main__':
    app.run(debug=True)
