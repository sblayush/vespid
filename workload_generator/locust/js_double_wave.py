import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape
from locust.user.wait_time import constant_throughput

class T1(TaskSet):

	@task()
	def scenario_invoke_jsn(self):
		somedata = {
			"vargs": {"string": "Hello"}
			}
		with self.client.post("/actions/jsn/invoke", json=somedata) as resp:
			# assert resp.status_code == 200
			assert resp.json()['result'] == '"SGVsbG8="'


class WebsiteUser(HttpUser):
    wait_time = constant(0.25)
    tasks = [T1]


class DoubleWave(LoadTestShape):
    """
    A shape to imitate some specific user behavior. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3
    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 50
    peak_one_users = 250
    peak_two_users = 150
    time_limit = 300

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = (
                (self.peak_one_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 5) ** 2)
                + (self.peak_two_users - self.min_users)
                * math.e ** -(((run_time / (self.time_limit / 10 * 2 / 3)) - 10) ** 2)
                + self.min_users
            )
            return (round(user_count), round(user_count))
        else:
            return None