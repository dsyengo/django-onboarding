from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        # The serializer will run the validate_email and validate_username checks here
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": RegisterSerializer(user).data,
                "message": "User created successfully. You can now login.",
            }, status=status.HTTP_201_CREATED)
        
        # If invalid, it returns the errors defined in the serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        # We accept 'username' key from frontend, but user might have typed an email
        login_input = request.data.get('username')
        password = request.data.get('password')

        if not login_input or not password:
            return Response({"error": "Please provide both username/email and password"}, status=status.HTTP_400_BAD_REQUEST)

        # --- STEP 1: Determine if input is Email or Username ---
        username_to_authenticate = login_input

        # Simple check: If it contains '@', assume it's an email
        if '@' in login_input:
            try:
                # Find the user with this email
                user_obj = User.objects.get(email=login_input)
                # Use their actual username for authentication
                username_to_authenticate = user_obj.username
            except User.DoesNotExist:
                # If no user has this email, authentication will fail below naturally
                pass

        # --- STEP 2: Verify Credentials ---
        # authenticate() always expects a 'username' keyword argument, 
        # even if we found it via email.
        user = authenticate(request, username=username_to_authenticate, password=password)

        if user is not None:
            # --- STEP 3: Generate Tokens ---
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Login successful",
                "username": user.username,
                "email": user.email, # Good to return this too
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
            
        else:
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # 1. safely get the refresh token
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 2. Instantiate and Blacklist
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"}, 
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError as e:
            # 3. Handle Invalid/Expired tokens gracefully
            # If the token is already expired or garbage, we still treat the logout as "successful" 
            # because the user's goal (to end the session) is effectively achieved.
            return Response(
                {"warning": "Token is already invalid or expired"}, 
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            # 4. Catch unexpected server errors
            return Response(
                {"error": "An unexpected error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )