from locust import HttpUser, task, between

class Products(HttpUser):
    wait_time = between(1, 3)  # Adjust wait time between requests

    @task
    def my_task(self):
        self.client.get("http://127.0.0.1:8000/api/products/")  # Example API endpoint
