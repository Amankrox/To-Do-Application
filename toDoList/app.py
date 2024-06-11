import tornado.ioloop
import tornado.web
import json
import os
from bson import ObjectId
from handlers.auth import RegisterHandler, LoginHandler, LogoutHandler, DeleteAccountHandler
from handlers.todo import TodoListHandler, TaskHandler
from handlers.subtask import SubtaskHandler
from handlers.testing import TestHandler

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

# Set custom JSON encoder
tornado.escape.json_encode = lambda value: json.dumps(value, cls=JSONEncoder)

def make_app():
    return tornado.web.Application([
        (r"/register", RegisterHandler),
        (r"/", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/delete_account", DeleteAccountHandler),
        (r"/todo_list", TodoListHandler),
        (r"/task", TaskHandler),
        (r"/subtask", SubtaskHandler),
        (r"/testing",TestHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./todoListfrontend", "default_filename": "index.html"}),
    ],
    cookie_secret="YOUR_SECRET_KEY",
    template_path=os.path.join(os.path.dirname(__file__), "todoListfrontend"),
    login_url="/login",
    debug=True  # Enable debugging mode
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
