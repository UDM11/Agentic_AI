from queue import Queue
import time
import random

# message queues
researcher_to_planner = Queue()
planner_to_researcher = Queue()


# researcher agent
class Researcher:
    def __init__(self, name):
        self.name = name

    def gather_data(self):
        data_items = ["Data A", "Data B", "Data C", "Data D"]
        for data in data_items:
            print(f"{self.name}: Gathered -> {data}")
            researcher_to_planner.put(data)
            time.sleep(random.uniform(0.5, 1.5))


# planner agent
class Planner:
    def __init__(self, name):
        self.name = name

    def plan_tasks(self):
        while True:
            if not researcher_to_planner.empty():
                data = researcher_to_planner.get()
                print(f"{self.name}: Received -> {data}")
                next_steps = f"Plan created using '{data}"
                print(f"{self.name}: Sending next steps -> {next_steps}")
                planner_to_researcher.put(next_steps)
            else:
                time.sleep(0.5)


# initialize agents
researcher = Researcher("Researcher Agent")
planner = Planner("Planner Agent")

 
# start planner in a background thread to continuously listen
import threading
planner_thread = threading.Thread(target = planner.plan_tasks, daemon = True)
planner_thread.start()


# start researcher
researcher.gather_data()


# main looop to receive planner responses
while not planner_to_researcher.empty() or planner_thread.is_alive():
    if not planner_to_researcher.empty():
        response = planner_to_researcher.get()
        print(f"{researcher.name}: Received instructions -> {response}")

    else:
        time.sleep(0.5)