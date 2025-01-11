from flask import Flask, Response


class StreamerHTTP :
    def __init__(self,indexFile) :
        self.app = Flask(__name__)
        with open(indexFile,'r') as f:
            self.indexFile = f.read()

    def route(self, path):
        # The decorator logic that wraps the function
        def decorator(func):
            @self.app.route(path)
            def handler(*args, **kwargs):
                return func(*args, **kwargs)
            return handler
        return decorator


    @route('/')
    def index(self) :
        return self.indexFile

    @route('/video_feed')
    def vedio(self,provider) :
        return Response(provider(), mimetype='multipart/x-mixed-replace; boundary=frame')


    def run(self,portNum,provider) :
        self.vedio(provider)
        self.app.run(host='0.0.0.0',port=portNum)




