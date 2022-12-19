# Flask
+ [Flask-2.0](https://flask.palletsprojects.com/en/2.0.x/)
+ [github-flask](https://github.com/pallets/flask/)
+ 
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

# Flask-RESTPlus vs Flask-RESTX
+ [flask-restplus](https://flask-restplus.readthedocs.io/en/stable/index.html)
+ [flask-restx](https://flask-restx.readthedocs.io/en/latest/)
+ Tác giả `@noirbizarre` của Flask-RESTPlus không thấy hổ trợ ae sử dụng nữa nên nhóm Flask-RESTX tạo một nhánh mới để tiếp tục phát triển hổ trợ ae.
  
+ Concept:
  + `Resource` : giving you easy access to multiple HTTP methods just by defining methods on your resource(get, put, post,..)
  + `Namespace` : organize your Flask-RESTPlus app , same pattern as Flask’s `blueprint`. The main idea is to split your app into reusable namespaces.

# Blueprints 
+ https://flask.palletsprojects.com/en/2.2.x/blueprints/
+ https://flask-restx.readthedocs.io/en/latest/scaling.html#use-with-blueprints
+ Blueprints can greatly simplify how large applications work 
+ Using a blueprint will allow you to mount your API on any url prefix and/or subdomain in you application
+ Không dùng theo hướng dẫn, lỗi