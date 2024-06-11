import tornado.web
import bcrypt
from utils.db import get_user_by_identifier, create_user, delete_user, get_database
from utils.hash import hash_password, check_password
from utils.validators import validate_name, validate_phone, validate_email, validate_password
from utils.jwt_utils import encode_jwt, decode_jwt
from handlers.helper import allow_cors


class BaseHandler(tornado.web.RequestHandler):
    @allow_cors
    def get_current_user(self):
        token = self.request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            return decode_jwt(token)
        
        if self.request.method=="OPTIONS":
            self.request.set_headers("Access-Control-Allow-Origin")

        return None
    


class RegisterHandler(BaseHandler):
    @allow_cors
    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            name = data.get("name")
            phone = data.get("phone")
            email = data.get("email")
            password = data.get("password")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write({"error": "Missing required arguments"})
            return
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid JSON format"})
            return

        if not (validate_name(name) and validate_phone(phone) and validate_email(email) and validate_password(password)):
            self.set_status(400)
            self.write({"error": "Invalid input"})
            return
        
        user_by_email = await get_user_by_identifier(email)
        if user_by_email:
            self.set_status(400)
            self.write({"error": "User already exists with this email"})
            return
        
        user_by_phone = await get_user_by_identifier(phone)
        if user_by_phone:
            self.set_status(400)
            self.write({"error": "User already exists with this phone"})
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = await get_database()
        await db.users.insert_one({"name": name, "phone_number": phone, "email": email, "password": hashed_password})
        self.write({"message": "User registered successfully"})

class LoginHandler(BaseHandler):
    @allow_cors
    def get(self):
        self.render("index.html")

    
       


    async def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
            identifier = data.get("identifier")  # can be phone or email
            password = data.get("password")
            # print(password)
            # print("********")
        except tornado.web.MissingArgumentError:
            self.set_status(400)
            self.write({"error": "Missing required arguments"})
            return
        except ValueError:
            self.set_status(400)
            self.write({"error": "Invalid JSON format"})
            return

        user = await get_user_by_identifier(identifier)
        # print("user detail at line 91 ",user)

        if not user:
            self.set_status(401)
            self.write({"error": "User not found"})
            return
        #print(password)
        if check_password(password, user["password"]):
            token = encode_jwt({"user_id": str(user["_id"])})
            self.write({"success": "Login successful", "token": token})
        else:
            self.set_status(401)
            self.write({"error": "Invalid password GALT PASWORD"})

class LogoutHandler(BaseHandler):
    @allow_cors
    def post(self):
        self.clear_cookie("user")
        self.write({"success": "Logout successful"})

class DeleteAccountHandler(BaseHandler):
    @allow_cors
   # @tornado.web.authenticated
    def post(self):
        email_id = self.get_current_user().decode()
        if delete_user(email_id):
            self.clear_cookie("user")
            self.write({"success": "User deleted"})
        else:
            self.write({"error": "User not found"})
