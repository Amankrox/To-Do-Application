from pymongo import MongoClient
from bson.objectid import ObjectId
import motor.motor_tornado


client = motor.motor_tornado.MotorClient("mongodb://localhost:27017/")
db =client["todolist"]
users_collection = db["users"]
todo_collection = db["todos"]

async def get_database():
    print(get_database)
    return db
async def getuser_id(list_id):
    userIdQ = await todo_collection.aggregate([
        {
            '$match': {
                '_id': ObjectId(list_id)
            }
        },
        {
            '$project': {
                'user_id': 1,
                '_id': 0
            }
        }
    ]).to_list(length=1)
    print("my useridQ",userIdQ)
    
    # Convert the cursor to a list and get the first document
   # userIdDoc = await userIdQ.to_list(length=1)
    
    # If the list is not empty, return the 'user_id'
    if userIdQ:
        return userIdQ[0].get('user_id')
    else:
        return None

async def get_user_by_identifier(identifier):
    
    user = await users_collection.find_one({"$or": [{"phone": identifier}, {"email": identifier}]})
    return user

async def create_user(name, phone, email, hashed_password):
       # Check if a user with the provided email or phone already exists
    existing_user = await db.users_collection.find_one({"$or": [{"phone": phone}, {"email": email}]})
    if existing_user:
       return None  # User already exists, return None to indicate failure
    return await db.users_collection.insert_one({"name": name, "phone": phone, "email": email, "password": hashed_password})

async def delete_user(user_id):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count > 0

async def get_todo_list(user_id):
    user_id_object = ObjectId(user_id)
    cursor = todo_collection.find({"user_id": user_id_object})
    todo_list = await cursor.to_list(length=None)
    print(todo_list) 
    print('55555')    
    return todo_list
    # Retrieve the todo list from the database
   # todo_list = db.todo_lists.find({"user_id": ObjectId(user_id)})
    #todo_list = db.todos.find({"user_id": ObjectId(user_id_object)})
    
    # Convert ObjectId to string
    # def convert_objectid(obj):
    #     if isinstance(obj, ObjectId):
    #         return str(obj)
    #     if isinstance(obj, list):
    #         return [convert_objectid(item) for item in obj]
    #     if isinstance(obj, dict):
    #         return {key: convert_objectid(value) for key, value in obj.items()}
    #     return obj

    # return [convert_objectid(item) for item in todo_list]
   # return list(todo_collection.find({"user_id": ObjectId(user_id)}))

async def create_todo_list(user_id, title):
    await todo_collection.insert_one({"user_id": ObjectId(user_id), "title": title, "tasks": []})

async def update_todo_list_title(user_id,list_id, new_title):
    result = await todo_collection.update_one(
        {"_id": ObjectId(list_id),"user_id":(ObjectId(user_id))},
        {"$set": {"title": new_title}}
    )
    return result.modified_count > 0

async def delete_todo_list(user_id, list_id):
    result = await todo_collection.delete_one(
        {"_id": ObjectId(list_id), "user_id": ObjectId(user_id)}
    )
    return result.deleted_count > 0

async def mark_todo_list_done( list_id):
    result = await todo_collection.update_one(
        {"_id": ObjectId(list_id)},
        {"$set": {"tasks.$[].subtasks.$[].done": True, "tasks.$[].done": True, "done": True}}
    )
    return result.modified_count > 0

async def add_task(list_id, task_title):
    task_id = ObjectId()
    result = await todo_collection.update_one(
        {"_id": ObjectId(list_id)},
        {"$push": {"tasks": {"_id": task_id, "title": task_title, "subtasks": []}}}
    )
    print(f"Task added: {result.modified_count} document(s) modified, task_id={task_id}")
    return task_id
    #todo_collection.update_one(
     #   {"_id": ObjectId(list_id), "user_id": ObjectId(user_id)},
      #  {"$push": {"tasks": {"title": task_title, "subtasks": []}}}
    #)
async def modify_task(task_id, new_title):
    print(task_id)
    print(new_title)
    result = await todo_collection.update_one(
        {"tasks._id": ObjectId(task_id)},
        {"$set": {"tasks.$.title": new_title}}
    )
    return result.modified_count > 0

async def mark_list_done(task_id):
    result = await todo_collection.update_one(
        {"tasks._id": ObjectId(task_id)},
        {
            "$set": {
                "tasks.$[task].done": True,
                "tasks.$[task].subtasks.$[subtask].done": True
            }
        },
        array_filters=[
            {"task._id": ObjectId(task_id)},
            {"subtask.done": {"$exists": True}}
        ]
    )
    return result.modified_count > 0

async def delete_task(user_id, task_id):
    print(f"delete_task called with user_id: {user_id}, task_id: {task_id}")
    try:
        query = {"tasks._id": ObjectId(task_id), "user_id": ObjectId(user_id)}
        update = {"$pull": {"tasks": {"_id": ObjectId(task_id)}}}
        print(f"Query: {query}")  # Debugging line to check the query
        print(f"Update: {update}")  # Debugging line to check the update
        result = await todo_collection.update_one(query, update)
        print(f"Deleted count: {result.modified_count}")
        if result.modified_count > 0:
            print("Task successfully deleted")
        else:
            print("No matching task found or task was not deleted")
    except Exception as e:
        print(f"Error deleting task: {e}")


async def add_subtask(task_id, subtask_title):
    #print("i ma in sub task handerr to add sub task")
    subtask_id = ObjectId()
    result = await todo_collection.update_one(
        {"tasks._id": ObjectId(task_id)},
        {"$push": {"tasks.$.subtasks": {"_id":subtask_id,"title": subtask_title, "done": False}}}
    )
    print(f"Subtask added: {result.modified_count} document(s) modified, subtask_id={subtask_id}")
    return subtask_id

async def delete_subtask(user_id, subtask_id):
    result = await todo_collection.delete_one({"tasks._id": ObjectId(subtask_id)})
    return result.deleted_count > 0

#def modify_task(task_id, new_title):
    # Find the todo document containing the task with the specified task_id
   ## print(task_id)
   # todo_collection.update_one(
   #     {"tasks._id": ObjectId(task_id)},
   #     {"$set": {"tasks.$.title": new_title}}
   # )


async def mark_task_done(user_id, subtask_id):
    print(f"Marking subtask as done for user_id: {user_id}, subtask_id: {subtask_id}")

    result = await todo_collection.update_one(
        {
            "user_id": ObjectId(user_id),
            "tasks.subtasks._id": ObjectId(subtask_id),
            "tasks.subtasks.done": {"$ne": True}
        },
        {
            "$set": {"tasks.$[].subtasks.$[subtask].done": True}
        },
        array_filters=[{"subtask._id": ObjectId(subtask_id)}]
    )
    
    if result.modified_count == 0:
        raise ValueError("Subtask not found or already marked as done")
    #await todo_collection.update_one(
        #{"tasks.subtasks._id": ObjectId(subtask_id), "user_id": ObjectId(user_id)},
        #{"$set": {"tasks.$.subtasks.$.done": True}},
        #array_filters=[{"subtask._id": ObjectId(subtask_id)}]
        
        
    #)
