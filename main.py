from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from wsgi_app.logmodule import getLogger
from gevent.pywsgi import WSGIServer
import os
import QA.QA_System as QA


# It creates a class called App that inherits from Flask.
class App(Flask):
    def __init__(self) -> None:
        Flask.__init__(self, __name__, static_url_path='', static_folder='wsgi_app/static/', template_folder='wsgi_app/templates/')
        self.config['TEMPLATES_AUTO_RELOAD'] = True
        self.wsgiServer = WSGIServer(('', 4999), self)
        self.ip = "0.0.0.0"
        self.port = 4999
        print(f"Current working directory: {os.path.abspath(os.path.dirname(__file__))}")
        self.logger = getLogger(__name__, os.path.abspath(os.path.dirname(__file__)) + '/wsgi_app/logs/app.log', maxBytes=1024 * 100)
        self.http_server = WSGIServer((self.ip, self.port), self, log=self.logger)
        self.routes = {
            "/": (self.index, ["GET", "POST"]),
            "/index.html": (self.index, ["GET", "POST"]),
        }

    def getStudiengaenge(self) -> list:
        """
        It returns a list of all the files in a directory
        
        Returns:
          A list of all the files in the directory.
        """
        path = f'{os.getcwd()}/txt'
        sg = (os.listdir(path))
        sg.remove('1. all txt')
        return sg
               
    def index(self) -> str:
        """
        It takes a question and a studiengang (study program) as input and returns an answer
        
        Returns:
          The answer to your question.
        """
        if request.method == "GET":
            return render_template("index.html", studiengaenge=self.getStudiengaenge())
        elif request.method == "POST":
            self.logger.debug(request.form)
            sg = request.form.get('studiengang', default=None)
            q = request.form.get('question', default=None)
            if q is not None and sg is not None:
                answer = QA.pipe(q, sg)
                return jsonify(answer)
            return jsonify({"answer": "Insufficient data"})

    def run(self) -> None:
        """
        It takes a dictionary of routes and methods, and then creates a route for each key in the
        dictionary, using the value of the key as the function to be called when the route is hit
        """
        for key in self.routes.keys():
            self.route(key, methods=self.routes[key][1])(self.routes[key][0])
        self.http_server.serve_forever()


if __name__ == "__main__":
    app = App()
    app.run()