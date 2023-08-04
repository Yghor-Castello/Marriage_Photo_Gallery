from rest_framework import status
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model, authenticate, login
from .serializers import UsuarioSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = response.data.get('refresh')
        if refresh_token:
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        return response


class LoginUsuarioView(APIView):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            try:
                AccessToken(token=access_token).check_exp()
            except TokenError:
                return Response({'detail': 'Expired access token'}, status=status.HTTP_401_UNAUTHORIZED)

            login(request, user)
            serializer = CustomTokenObtainPairSerializer(data={'refresh': str(refresh), 'access': str(access_token)})
            serializer.is_valid()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Incorrect email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):

    permission_classes = [IsAdminUser]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response_data = serializer.data
            response_data['access'] = access_token
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditUserView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):

        try:
            if request.user != request.user:
                raise exceptions.PermissionDenied('User not authorized to edit')

            serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                raise exceptions.ValidationError(serializer.errors)

        except exceptions.PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

        except exceptions.ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EditPasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        senha_atual = request.data.get('password')
        nova_senha = request.data.get('new_password')
        confirmar_senha = request.data.get('confirm_new_password')

        if not user.check_password(senha_atual):
            return Response({'detail': 'Incorrect current password'}, status=status.HTTP_400_BAD_REQUEST)

        if nova_senha != confirmar_senha:
            return Response({'detail': 'New password and confirmation do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(nova_senha)
        user.save()
        return Response({'detail': 'Password changed successfully'})
    

class LogoutUsuarioView(APIView):

    def post(self, request, *args, **kwargs):
        if 'refresh_token' in request.COOKIES:
            response = Response({'detail': 'Logout successful!'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            return response
        else:
            return Response({'error': 'You are already logged out.'}, status=status.HTTP_400_BAD_REQUEST)
