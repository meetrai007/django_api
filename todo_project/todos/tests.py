from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import ToDo


class TodoApiTests(APITestCase):

    def setUp(self):
        self.todo_list_url = reverse('todos_list')
        self.create_user_url = reverse('create_user')
        self.login_url = reverse('login_user')



    def test_get_todo_list(self):
        """
        Ensure we can retrieve the ToDo list
        """
        
        # Send GET request to the API
        response = self.client.get("/api/todos/")
        
        # Assert the response status is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert the ToDo list was returned in the response
        self.assertEqual(len(response.data), 0)
        
        # Assert the ToDo list is empty in the database
        self.assertEqual(ToDo.objects.count(), 0)



    def test_create_todo(self):
        """
        Ensure we can create a new ToDo item
        """
        # Send POST request to the API
        response = self.client.post("/api/todos/", {"title": "New ToDo", "description": "Description", "completed": False})
        
        # Assert the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert the ToDo item was created in the database
        todo = ToDo.objects.get(title="New ToDo")
        self.assertEqual(todo.title, "New ToDo")
        self.assertEqual(todo.description, "Description")
        self.assertFalse(todo.completed)



    def create_user(self):
        # Send POST request to the API
        response = self.client.post(self.create_user_url, {"username": "meet2", "password": "meet2"})
        
        # Assert the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    # def test_get_token(self):
    #     # Send POST request to obtain token
    #     response = self.client.post(self.login_url, {
    #         "username": "meet",
    #         "password": "meet"
    #     })
        
    #     # Print the response data to debug
    #     # print(response.data)

    #     # Assert the response status is 200 OK
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_login(self):
        # Test login with correct credentials
        response = self.client.post(self.login_url, {'username': 'meet', 'password': 'meet'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


    def test_invalid_login(self):
        # Test login with incorrect password
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)