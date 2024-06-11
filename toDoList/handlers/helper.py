import functools
from tornado.web import RequestHandler
#this is for allowing accerss to origin
def allow_cors(func):
    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
        if self.request.method == "OPTIONS":
            self.set_status(204)
            self.finish()
            return
        return await func(self, *args, **kwargs)
    return wrapper

class BaseHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")

    def options(self):
        self.set_status(204)
        self.finish()
