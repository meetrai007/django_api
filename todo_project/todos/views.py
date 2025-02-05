from .schama import LoginSchema
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics, permissions
from .models import ToDo
from .serializers import ToDoSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny



class TodosView(generics.ListCreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Token protection

    @swagger_auto_schema(
        operation_description="Get the list of Todos",
        responses={200: ToDoSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token (e.g. 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        Get a list of ToDos
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new Todo item",
        request_body=ToDoSerializer,
        responses={201: ToDoSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token (e.g. 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new ToDo item
        """
        return super().post(request, *args, **kwargs)


class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific Todo item.
    """
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get, update, or delete a specific Todo item",
        responses={200: ToDoSerializer},
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication (e.g., 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific Todo item",
        request_body=ToDoSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication (e.g., 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: ToDoSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific Todo item",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token for authentication (e.g., 'Bearer <your_token>')",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={204: "No content, deleted successfully"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer},
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new user with a hashed password
        """
        user_data = request.data
        password = user_data.get("password")

        # Ensure password is set securely
        if not password:
            return Response({"error": "Password is required"}, status=400)

        # Save the user with hashed password
        serializer = self.get_serializer(data=user_data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)  # Hash the password
            user.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



class LoginAPIView(APIView):
    """
    API endpoint for user login using JWT authentication.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login user and get JWT tokens",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={
            200: "JWT tokens",
            401: "Invalid username or password"
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                # User is active, allow login
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful!'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not staff'}, status=status.HTTP_401_UNAUTHORIZED)     
        else:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)




from ninja import Router
from pydantic import BaseModel
from ninja.security import HttpBearer

# Create a new Router instance
user_router = Router()

# Define a response schema for user
class UserResponse(BaseModel):
    username: str
    email: str

# Define authentication logic using HttpBearer
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # Custom authentication logic here
        # This is a simple check where the token is "valid_token"
        if token == "valid_token":
            return True
        return None

# Define the route to list users
@user_router.get("/list")  # Using the AuthBearer for authentication  auth=AuthBearer()
def list_users(request):
    # List of users can be fetched from the database, but for now, it is hardcoded.
    return {"status": "success", "users": ["Alice", "Bob"]}

# Define the route to create a user
@user_router.post("/create", response=UserResponse)
@swagger_auto_schema(
    operation_description="Create a new user with a hashed password.",
    responses={201: UserResponse},
    request_body=UserResponse,
)
def create_user(request):
    # Here, you would typically save the user to the database and return the response
    return {"username": "new_user", "email": "new_user@example.com"}

# To mount the user router, add the following in your main api file
# from ninja import NinjaAPI
# api = NinjaAPI()

# api.add_router("/user", user_router)  # Mount the router to the "/user" endpoint

