from locust import HttpUser, TaskSet, task, between
from locust.user.wait_time import constant_throughput

count = 0
max_count = 1000


class CFunction(TaskSet):
	wait_time = between(0.1, 0.2)

	# def __init__(self):
	# 	super().__init__()
	# 	self.count = 0

	# @task(3)
	# def view_items(self):
	# 	for item_id in range(10):
	# 		self.client.get(f"/item?id={item_id}", name="/item")
	# 		time.sleep(1)

	@task(5)
	def scenario_invoke_func1(self):
		global count
		somedata = {
			"vargs": {"a":1000}
			}
		count += 1
		with self.client.post("/actions/func1/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	# @task(5)
	# def scenario_invoke_func2(self):
	# 	global count
	# 	somedata = {
	# 		"vargs": {"a":100}
	# 		}
	# 	count += 1
	# 	with self.client.post("/actions/func2/invoke", json=somedata) as resp:
	# 		assert resp.status_code == 200

	# @task(5)
	# def scenario_invoke_func3(self):
	# 	global count
	# 	somedata = {
	# 		"vargs": {"a":1}
	# 		}
	# 	count += 1
	# 	with self.client.post("/actions/func3/invoke", json=somedata) as resp:
	# 		assert resp.status_code == 200

	@task(5)
	def scenario_invoke_ping(self):
		with self.client.get("/ping", catch_response=True) as response:
			assert response.text != "pong"

	# def on_start(self):
	# 	with self.client.get("/ping", catch_response=True) as response:
	# 		if response.text != "pong":
	# 			response.success()
	# 		elif response.elapsed.total_seconds() > 0.5:
	# 			response.failure("Request took too long")
	
	# @task
	def halt(self):
		global count
		if count > max_count:
			self.user.environment.runner.quit()
		# else:
		#     raise RescheduleTaskImmediately()


class CNativeFunction(TaskSet):
	wait_time = between(0.1, 0.2)

	@task(5)
	def scenario_invoke_func1(self):
		global count
		somedata = {
			"vargs": {"a":1000}
			}
		count += 1
		with self.client.post("/actions/func4/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	@task(5)
	def scenario_invoke_ping(self):
		with self.client.get("/ping", catch_response=True) as response:
			assert response.text != "pong"


class Mix(TaskSet):
	wait_time = between(0.1, 0.1)

	@task(10)
	def scenario_invoke_func_c(self):
		global count
		somedata = {
			"vargs": {"a":50000}
			}
		count += 1
		with self.client.post("/actions/func_c/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	@task(10)
	def scenario_invoke_func_native(self):
		global count
		somedata = {
			"vargs": {"a":50000}
			}
		count += 1
		with self.client.post("/actions/func_native/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	@task(5)
	def scenario_invoke_ping(self):
		with self.client.get("/ping", catch_response=True) as response:
			assert response.text != "pong"


class FibTest(TaskSet):
	wait_time = between(10, 10)

	@task(10)
	def scenario_invoke_fib_cn(self):
		somedata = {
			"vargs": {"a":48}
			}
		with self.client.post("/actions/fib_cn/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	@task(10)
	def scenario_invoke_fib_c(self):
		somedata = {
			"vargs": {"a":48}
			}
		with self.client.post("/actions/fib_c/invoke", json=somedata) as resp:
			assert resp.status_code == 200

	@task(5)
	def scenario_invoke_ping(self):
		with self.client.get("/ping", catch_response=True) as response:
			assert response.text != "pong"



class QuickstartUser(HttpUser):
	tasks = [FibTest]
    # wait_time = wait_time_func
