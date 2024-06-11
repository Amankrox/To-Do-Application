from tornado import *
import tornado.web
from utils.jwt_utils import decode_jwt,encode_jwt
class TestHandler(tornado.web.RequestHandler):
    async def get(self):
        token=self.request.headers.get("Authorization")
        print(token)
        decodedToken=decode_jwt(token)
        print('DECODE TOKEN : ',decodedToken)
        print(decodedToken['user_id'])
        

