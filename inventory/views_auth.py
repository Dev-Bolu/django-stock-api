# inventory/views_auth.py
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import UserRegisterSerializer





# -----------------------------
# REGISTER VIEW
# -----------------------------
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get("username")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": f"Username '{username}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the user
        response = super().create(request, *args, **kwargs)

        # Generate or get the user's token
        user = User.objects.get(username=username)
        token, _ = Token.objects.get_or_create(user=user)

        # Return success response
        return Response(
            {
                "message": f"✅ Registration successful for '{username}'.",
                "token": token.key
            },
            status=status.HTTP_201_CREATED
        )


# -----------------------------
# LOGIN VIEW
# -----------------------------
class CustomAuthToken(ObtainAuthToken):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


# -----------------------------
# LOGOUT VIEW
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    token = getattr(request.user, 'auth_token', None)
    if token:
        token.delete()
    return Response({"message": "Successfully logged out"})

# -----------------------------
# Browser-based authentication
# -----------------------------

def user_login_view(request):
    """
    Renders a login form for browser users.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # 👈 redirects to 'home' after login
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "inventory/login.html")



def user_register_view(request):
    """
    Handles simple registration form.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, "Registration successful!")
        return redirect('home')

    return render(request, "inventory/register.html")


def user_logout_view(request):
    """
    Logs out the user and redirects to login page.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')



@login_required
def home_view(request):
    return render(request, "inventory/home.html")
