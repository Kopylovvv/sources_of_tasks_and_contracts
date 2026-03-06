from src.sources import *
from src.validation import validate_task_source



def run():
    api = APITaskSource()
    file = FileTaskSource("tests/tasks.json")
    gen = RandomTaskSource()

    if validate_task_source(api):
        api_tasks = api.get_tasks()
        print(api_tasks)

    if validate_task_source(gen):
        gen_tasks = gen.get_tasks()
        print(gen_tasks)

    if validate_task_source(file):
        file_tasks = file.get_tasks()
        print(file_tasks)


if __name__ == "__main__":
    run()