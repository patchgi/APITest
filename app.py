from sys import argv
import glob
import json
import requests
from urllib.parse import urljoin
from pprint import pprint
import time

def main():
    tasks = getActionTask()
    action(tasks)

def getActionTask():
    input_tasks = set(argv[1:])
    tasks =  {t.split('/')[1].split('.')[0]: t for t in glob.glob('tasks/*.json')}
    action_tasks = []
    if  "-a" in input_tasks:
        action_tasks = list(tasks.keys())
    else:
        for input_task in input_tasks:
            if input_task in list(tasks.keys()):
                action_tasks.append(input_task)
            else:
                print()
                error(f"{input_task} is not defined")



    print(f"action_task_list: {action_tasks}")
    output_tasks = {}
    for action_task_name in action_tasks:
        output_tasks[action_task_name] = tasks[action_task_name]

    return output_tasks

def action(tasks):
    for name, path in tasks.items():
        print("---")
        print(f"task_name: {name}")
        print(f"task_path: {path}")
        success_tasks = []
        faild_tasks = []
        with open(path) as f:
            task = json.loads(f.read())
            try:
                method = task["method"]
                host = task["host"]
                path = task["path"]
                params = task["params"]
                result = task["result"]
            except KeyError as e:
                error(f"{e} is not found")
            
            method = method.upper()
            url = urljoin(host, path)
            start_time = time.time()
            if method == "GET":
                res = requests.get(url, params = params)

            elif method ==  "POST":
                res = requests.post(url, params = params)
            else:
                error(f"{method} is not supported")
            end_time = time.time()
            response = res.json()
            print(f"Execution time: {end_time - start_time}s")
            if res.status_code != 500:
                success("OK")
                success_tasks.append(name)
            else:
                error("FAILD")
                error(f"status_code: {res.status_code}")
                print("Result respose:")
                print(f'{str(response)[:100]}...')
                faild_tasks.append(name)

        return success_tasks, faild_tasks

def success(message):
    print("\033[32m" + message + "\033[0m")

def error(message):
    print("\033[31m" + message + "\033[0m")
if __name__ == '__main__':
    main()