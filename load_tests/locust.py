from locust import HttpUser, task, between


class AuthTestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def login(self):
        response = self.client.post("/api/auth/", data={
            "username": "testuser",
            "password": "testpassword"
        })
        if response.status_code == 200:
            print("Успешная аутентификация")
        else:
            print("Ошибка аутентификации", response.status_code)

# Запустить тест можно командой:
# locust -f этот_файл.py --host=http://127.0.0.1:8000
