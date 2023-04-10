from flask import Flask, request
from flask_restful import Api, Resource, reqparse

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

videos={}

class Video(Resource):
    def get(self, video_id):
        return videos[video_id]
    

    def put(self, video_id):
        # print(request.form['likes'])
        return {}



# register the resource
# api.add_resource(HelloWorld, "/helloworld/<string:name>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__  == '__main__':
    app.run(debug=True)
