from django.urls import path
from . import views
from ninja import NinjaAPI
from .views import user_router  # import the router

# from .views import ToDoViewSet
# from .views import TodosView, TodoDetail

# router = DefaultRouter()
# router.register(r'todos', ToDoViewSet)


urlpatterns = [
    # Path for Todo Detail view
    path('todos/<int:pk>/', views.TodoDetail.as_view(), name="todo_detail"),
    
    # Path for List and Create Todo view
    path('todos/', views.TodosView.as_view(), name="todos_list"),

    # Path for user login (You can modify this as per your implementation)
    path('create-user/', views.CreateUserView.as_view(), name="create_user"),
    
    # Path for user login
    path('login-user/', views.LoginAPIView.as_view(), name="login_user"),
]
