import tornado.web
from utils.db import get_todo_list,delete_todo_list,getuser_id,mark_todo_list_done,update_todo_list_title,create_todo_list, add_task, add_subtask, modify_task,delete_subtask, mark_task_done,delete_task ,mark_list_done
#from utils.db import todo_collection
from utils.jwt_utils import decode_jwt,encode_jwt
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        token = self.request.headers.get("Authorization")
        if token:
            token = token.replace("Bearer ", "")
            data_token= decode_jwt(token)
           # print(data_token)
            return data_token
        return None
class TodoListHandler(BaseHandler):
    #@tornado.web.authenticated
    async def get(self):
        token = self.request.headers.get("Authorization")
        #print(token)
        if not token:
            self.set_status(403)
            self.write("you are not authorized")
        decodedToken=decode_jwt(token)
        #clprint(decodedToken)
        user_id = decodedToken['user_id']
        if not user_id:
            self.set_status(403)
            self.write({"error": "User not authenticated"})
            return
        try:
           todo_list = await get_todo_list(user_id)
           #print(f"Fetching to_do_list: {todo_list}")
           self.write({"todo_list": todo_list})
        except Exception as e:
           # print(f"Error fetching  to do list:{e}")
            self.set_status(500)
            self.write({"error":"Internal server error"})           
        

   # @tornado.web.authenticated
    async def post(self):
        token = self.request.headers.get("Authorization")
        #print(token)
        if not token:
            self.set_status(403)
            self.write("you are not authorized")
        decodedToken=decode_jwt(token)
        #print(decodedToken)
        user_id = decodedToken['user_id']
        if not user_id:
            self.set_status(403)
            self.write({"error": "User not authenticated"})
            return

        data = tornado.escape.json_decode(self.request.body)
        
        title = data.get("title")
        print("this is my title",title)
        await create_todo_list(user_id, title)
        self.write({"success": "Todo list created"})
    
    #@tornado.web.authenticated
    async def put(self):
        token = self.request.headers.get("Authorization")
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
        list_id = data.get("list_id")
        print(list_id)
        new_title = data.get("new_title")
        print(new_title)

        if not list_id or not new_title:
            print("hekkooooo")
            self.set_status(400)
            self.write({"error": "Missing list_id or new_title"})
            return

        try:
            print("hekkooooo")
            result = await update_todo_list_title(user_id,list_id, new_title)
            if result:
                self.write({"success": "Todo list title updated"})
            else:
                self.set_status(404)
                self.write({"error": "Todo list not found or no change in title"})
        except Exception as e:
            print(f"Error updating todo list title: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

    #@tornado.web.authenticated
    async def delete(self):
        print("this is my self.request.method",self.request.method)
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

        # data = tornado.escape.json_decode(self.request.body)
        list_id = self.get_arguments("list_id")[0]
        print("my list is is",list_id)

        if not list_id:
            self.set_status(400)
            self.write({"error": "Missing list_id"})
            return

        try:
            result = await delete_todo_list(user_id, list_id)
            if result:
                self.write({"success": "Todo list deleted"})
            else:
                self.set_status(404)
                self.write({"error": "Todo list not found"})
        except Exception as e:
            print(f"Error deleting todo list: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

   # @tornado.web.authenticated
    async def patch(self):
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

        #data = tornado.escape.json_decode(self.request.body)
        list_id = self.get_arguments("list_id")[0]

        if not list_id:
            self.set_status(400)
            self.write({"error": "Missing list_id"})
            return

        try:
            result = await mark_todo_list_done(list_id)
            if result:
                self.write({"success": "Todo list and all tasks marked as done"})
            else:
                self.set_status(404)
                self.write({"error": "Todo list not found or no change in status"})
        except Exception as e:
            print(f"Error marking todo list as done: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

class TaskHandler(BaseHandler):
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
        #user_idQ=
        #get user id using tite_id(task) and match it for authorization
        
        data = tornado.escape.json_decode(self.request.body)
        list_id = data.get("list_id")
        task_title = data.get("task_title")

        if not list_id or not task_title:
            self.set_status(400)
            self.write({"error": "Missing list_id or task_title"})
            return
        print(await getuser_id(list_id))
        # checking user id is same or not
        userIdQ=await getuser_id(list_id)
        
        # print("this is checkimg")
        # print(userIdQ,user_id)
        userIdQ = str(userIdQ)
        print("*********************",userIdQ == user_id)


        if (userIdQ != user_id):
            print(userIdQ,user_id)
            self.set_status(403) 
            self.write({"error":"you are not authorized"})  

            return
            
        try:
            print("inside task")
            task_id = await add_task(list_id, task_title)
            self.write({"success": "Task added", "task_id": str(task_id)})
        except Exception as e:
            print(f"Error adding task: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

    #@tornado.web.authenticated
    async def put(self):
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
        print(data.get("new_title"))
        task_id = data.get("task_id")
        new_title = data.get("new_title")
        
                
        
        if not task_id:
            self.set_status(400)
            self.write({"error": "Missing task_id or new_title"})
            return
        if not new_title:
            self.set_status(400)
            self.write({"error": " new_title"})
            return


        try:
            result = await modify_task(task_id, new_title)
            if result:
                self.write({"success": "Task modified"})
            else:
                self.write({"error": "Task not found or no change in title"})
        except Exception as e:
            print(f"Error modifying task: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})

    
    #@tornado.web.authenticated
    async def delete(self):
        #print("Hitting this functiuon")
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

        if not task_id:
            self.set_status(400)
            self.write({"error": "Missing task_id"})
            return

        try:
            await delete_task(user_id, task_id)
            self.write({"success": "Task deleted"})
        except Exception as e:
            print(f"Error deleting task: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})
    
    async def patch(self):
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
        #list marking
        data = tornado.escape.json_decode(self.request.body)
        title_id = data.get("title_id")

        if not title_id:
            self.set_status(400)
            self.write({"error": "Missing title_id"})
            return

        try:
            result = await mark_list_done(title_id)
            if result:
                self.write({"success": "list and all tasks marked as done"})
            else:
                self.set_status(404)
                self.write({"error": "list not found or no change in status"})
        except Exception as e:
            print(f"Error marking  list as done: {e}")
            self.set_status(500)
            self.write({"error": "Internal server error"})
        


