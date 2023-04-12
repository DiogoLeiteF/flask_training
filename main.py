from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)




# class HelloWorld(Resource):
#     def get(self, name, test):
#         return {"data": name, "test": test}


# names = {
#     'tim':{'age': 19, 'gender': 'male'},
#     'ana':{'age':25, 'gender': 'femnale'},
#     }

# class HelloWorld(Resource):
#     def get(self, name):
#         return names[name]

video_put_args = reqparse.RequestParser()
video_put_args.add_argument('name', type=str, help='Name of the video', required = True)
video_put_args.add_argument('views', type=int, help='Views of the video', required = True)
video_put_args.add_argument('likes', type=int, help='Likes of the video', required = True)


videos={}

def abort_if_vid_id_doesent_exist(video_id):
    if video_id not in videos:
        abort(404, message="video id not valid")

def abort_if_video_exist(video_id):
    if video_id in videos:
        abort(409, "video already exitsts..")


class Video(Resource):
    def get(self, video_id):
        abort_if_vid_id_doesent_exist(video_id)
        return videos[video_id]
    

    def put(self, video_id):
        # print(request.form['likes'])
        abort_if_video_exist(video_id)
        args = video_put_args.parse_args()
        videos[video_id]= args
        return videos[video_id], 201

    def delete(self, video_id):
        abort_if_vid_id_doesent_exist(video_id)
        del videos[video_id]
        return '', 204 # deleted successefully

# register the resource
# api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__  == '__main__':
    app.run(debug=True)
