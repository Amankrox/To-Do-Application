import tornado.web
from utils.db import  add_subtask,delete_subtask, mark_task_done
from utils.jwt_utils import decode_jwt,encode_jwt
class BaseHandler(tornado.web.RequestHandler):
    async def get_current_user(self):
        token = self.request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            return decode_jwt(token)
        return None

class SubtaskHandler(BaseHandler):
   # @tornado.web.authenticated
    async def post(self):
        token = self.request.headers.get("Authorization")
        #print(token)
        if not token:
            self.set_status(403)
            self.write("you are not authorized")
        decodedToken=decode_jwt(token)
        print(decodedToken)
        user_id = decodedToken['user_id']
        if not user_id:
            self.set_status(403)
            self.write({"error": "User not authenticated"})
            return
        
        data = tornado.escape.json_decode(self.request.body)
        task_id = data.get("task_id")
        print(task_id)
        subtask_title = data.get("subtask_title")
        print(subtask_title)

        if not task_id or not subtask_title:
            self.set_status(400)
            self.write({"error": "Missing task_id or subtask_title"})
            return

        try:
            subtask_id = await add_subtask(task_id, subtask_title)
            self.write({"success": "Subtask added", "subtask_id": str(subtask_id)})
        except Exception as e:
            print(f"Error adding subtask: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

    #@tornado.web.authenticated
    async def put(self):
        token = self.request.headers.get("Authorization")
        if not token:
            self.set_status(403)
            self.write("You are not authorized")
            return
        
        try:
            decodedToken = decode_jwt(token)
            user_id = decodedToken['user_id']
            data = tornado.escape.json_decode(self.request.body)
            subtask_id = data.get("subtask_id")
            
            if not subtask_id:
                self.set_status(400)
                self.write("Subtask ID is required")
                return
            
            await mark_task_done(user_id, subtask_id)
            self.write({"success": "Subtask marked as done"})
        except Exception as e:
            self.set_status(500)
            self.write(f"Internal server error: {str(e)}")


    # @tornado.web.authenticated
    async def delete(self):
        #print('***************************')
        token = self.request.headers.get("Authorization")
        #print(token)
        if not token:
            self.set_status(403)
            self.write("you are not authorized")
        decodedToken=decode_jwt(token)
        print(decodedToken)
        user_id = decodedToken['user_id']
        
        data = tornado.escape.json_decode(self.request.body)
        subtask_id = data.get("subtask_id")

        if not subtask_id:
            self.set_status(400)
            self.write({"error": "Missing subtask_id"})
            return

        try:
            await delete_subtask(user_id, subtask_id)
            self.write({"success": "Subtask deleted"})
        except Exception as e:
            print(f"Error deleting subtask: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})
