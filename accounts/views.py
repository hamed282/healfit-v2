from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, AddressModel
from .serializers import UserRegisterSerializer, UserLoginSerializer, ChangePasswordSerializer, UserAddressSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
import urllib.parse
from django.conf import settings
import requests


class UserRegisterView(APIView):

    @staticmethod
    def post(request):
        """
        parameters:
        1. first_name
        2. last_name
        3. email
        4. phone_number
        5. trn_number
        6. company_name
        7. password
        """
        form = request.data
        ser_data = UserRegisterSerializer(data=form)
        if ser_data.is_valid():
            if not User.objects.filter(email=form['email']).exists():
                User.objects.create_user(first_name=form['first_name'],
                                         last_name=form['last_name'],
                                         email=form['email'],
                                         phone_number=form['phone_number'],
                                         trn_number=form['trn_number'],
                                         company_name=form['company_name'],
                                         password=form['password']),
                try:
                    user = authenticate(email=form['email'], password=form['password'])
                    if user is not None:
                        user = get_object_or_404(User, email=form['email'])
                        if user.is_active:
                            token_access = AccessToken.for_user(user)
                            token_refresh = RefreshToken.for_user(user)
                            return Response(data={'access': str(token_access), 'refresh': str(token_refresh)},
                                            status=status.HTTP_200_OK)
                        return Response(data='user is not active', status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response(data='user invalid', status=status.HTTP_400_BAD_REQUEST)
                except:
                    return Response(data={'message': 'Authenticate Error.'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'message': 'user with this Email already exists.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):

    @staticmethod
    def post(request):
        """
        parameters:
        1. email
        2. password
        """
        form = request.data
        ser_data = UserLoginSerializer(data=form)
        if ser_data.is_valid():
            try:
                user = authenticate(email=form['email'], password=form['password'])
                if user is not None:
                    user = get_object_or_404(User, email=form['email'])
                    if user.is_active:
                        token_access = AccessToken.for_user(user)
                        token_refresh = RefreshToken.for_user(user)
                        return Response(data={'access': str(token_access), 'refresh': str(token_refresh)},
                                        status=status.HTTP_200_OK)
                    return Response(data='user is not active', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data='user invalid', status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response(data={'message': 'Authenticate Error.'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(data=ser_data.errors, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """
        parameters:
        1. old_password
        2. new_password
        """
        ser_data = ChangePasswordSerializer(data=request.data)
        if ser_data.is_valid():
            user = request.user
            if user.check_password(ser_data.data.get('old_password')):
                user.set_password(ser_data.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        """
        parameters:
        1. refresh_token

        sample: {"refresh_token": "dsade3ewqdwxr44354x4rxexrre"}
        """
        try:
            refresh_token = request.data["refresh_token"]

            token = RefreshToken(refresh_token)
            print(token)
            token.blacklist()
            return Response(data='Logout successfully', status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = AddressModel.objects.filter(user=request.user)
        ser_addresses = UserAddressSerializer(instance=addresses, many=True)
        return Response(data=ser_addresses.data)

    def post(self, request):
        """
        parameters:
        {
            address
            additional_information
            emirats
            city
            country
            phone_number
        }
        """
        form = request.data
        ser_address = UserAddressSerializer(data=form)
        if ser_address.is_valid():
            address = AddressModel.objects.create(user=request.user,
                                                  address=form['address'],
                                                  additional_information=form['additional_information'],
                                                  emirats=form['emirats'],
                                                  city=form['city'],
                                                  country=form['country'],
                                                  phone_number=form['phone_number'])
            # address.save()
            return Response(data={'massage': 'Address added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=ser_address.errors, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        address_id = self.request.query_params.get('address_id', None)
        address = get_object_or_404(AddressModel, id=address_id)
        if address.user.id == request.user.id:
            form = request.data

            ser_address = UserAddressSerializer(instance=address, data=form, partial=True)
            if ser_address.is_valid():
                ser_address.save()
                return Response(data=ser_address.data, status=status.HTTP_200_OK)
            return Response(data=ser_address.errors, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        address_id = self.request.query_params.get('address_id', None)
        address = get_object_or_404(AddressModel, id=address_id)
        if address_id is not None:
            if address.user.id == request.user.id:

                address = AddressModel.objects.get(id=address_id)
                address.delete()
                return Response(data={'massage': 'address deleted'}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(APIView):

    def post(self, request):

        code = request.data.get('code')
        decoded_code = urllib.parse.unquote(code)
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': decoded_code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        access_token = token_json.get('access_token')
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_params = {'access_token': access_token}
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        if 'error' in user_info:
            return Response({'message': user_info['error']['message'], 'status': user_info['error']['status']},
                            status=status.HTTP_401_UNAUTHORIZED)

        email = user_info.get('email')
        name = user_info.get('name')

        user, created = User.objects.get_or_create(email=email)
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(tokens, status=status.HTTP_200_OK)
