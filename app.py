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
def add_task():
    data = request.json
    
    new_tasks = []
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
        new_tasks.append(new_task)

    with open("tasks.json", "w") as j:
        json.dump(all_tasks, j)
    return {"tasks": new_tasks}, 201




    
    

