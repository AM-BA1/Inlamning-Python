from flask import Flask, render_template, request
import json
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

with open("tasks.json", "r") as j:
    all_tasks = json.load(j)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return all_tasks

@app.route("/tasks", methods=["POST"])
def task_add():
    data = request.json
    
    for item in data:
        description = item.get("description")
        category = item.get("category")

        last_task = all_tasks[-1]
        last_id = last_task["id"]
        id_auto = last_id + 1

        new_task = {
            "id": id_auto,
            "description": description,
            "category": category,
            "status": "pending"
        }
        all_tasks.append(new_task)
    with open("tasks.json", "w") as j:
        json.dump(all_tasks, j)
    return new_task, 201

@app.route("/tasks/<int:id>", methods=["GET"])
def task_get(id):
    for task in all_tasks:
        if task["id"] == id:
            return task, 200

@app.route("/tasks/<int:id>", methods=["DELETE"])
def task_delete(id):
    for i, task in enumerate(all_tasks):
        if task["id"] == id:
            all_tasks.pop(i)
            with open("tasks.json", "w") as j:
                json.dump(all_tasks, j)
            return f"The task with id:{id} has been deleted!", 201
    return f"The task with id:{id} was not found!", 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def task_update(id):
    data = request.json
    for item in data:
        description = item.get("description")
        category = item.get("category")

    for task in all_tasks:
        if task["id"] == id:
            task.update({f"id": id, "description": description, "category": category, "status": "pending"})
            with open("tasks.json", "w") as j:
                json.dump(all_tasks, j)
            return task, 200
    return f"The task with id:{id} was not found!", 404     

@app.route("/tasks/<int:id>/complete", methods=["PUT"])
def task_complete(id):
    for task in all_tasks:
        if task["id"] == id:
            task.update({"status": "complete"})
            with open("tasks.json", "w") as j:
                json.dump(all_tasks, j)
            return task, 200
    return f"The task with id:{id} was not found!", 404

@app.route("/tasks/categories", methods=["GET"])
def categories_all():
    all_cat = []
    for task in all_tasks:
        category = task.get("category")
        if category not in all_cat:
            all_cat.append(category)
    return all_cat

@app.route("/tasks/categories/<category_input>", methods=["GET"])
def category_tasks(category_input):
    cat_tasks = []
    for task in all_tasks:
        if task["category"] == category_input:
            cat_tasks.append(task)
    return cat_tasks, 200

@app.route("/")
def index():  
    return render_template("index.html", title="Tasks", tasks=all_tasks), 200

             
            





        





    
    

