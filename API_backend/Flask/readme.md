# Flask
+ [Flask-2.0](https://flask.palletsprojects.com/en/2.0.x/)
+ Example
    ```python
    from flask import Flask
    
    app = Flask(__name__)
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    ```
+ Concept:
  + `Flask` class. An instance of this class will be our WSGI application.
  + `__name__`: the name of the application’s module or package
  + `route()` decorator to tell Flask what URL should trigger our function
  + The function returns the message we want to display in the user’s browser. The default content type is HTML.

# Flask-RESTPlus
+ [flask-restplus-quickstart](https://flask-restplus.readthedocs.io/en/stable/quickstart.html#quickstart)
+ [flask-restplus-scaling](https://flask-restplus.readthedocs.io/en/stable/scaling.html)
+ Minimal example:
  ```python
  from flask import Flask
  from flask_restplus import Resource, Api
  
  app = Flask(__name__)
  api = Api(app)
  
  @api.route('/hello')
  class HelloWorld(Resource):
      def get(self):
          return {'hello': 'world'}
  
  if __name__ == '__main__':
      app.run(debug=True)
  ```
  
+ Concept:
  + `Resource` : giving you easy access to multiple HTTP methods just by defining methods on your resource(get, put, post,..)
  + `Namespace` : organize your Flask-RESTPlus app , same pattern as Flask’s `blueprint`. The main idea is to split your app into reusable namespaces.