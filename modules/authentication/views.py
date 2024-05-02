import traceback
from datetime import timedelta

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from modules.authentication.models import User, UserDevice, Tenant
from modules.authentication.serializers import UserSerializer
from utils import global_defs

# def get_access_token(user):
#     application = list(Application.objects.filter(user=user))[-1]
#     token = generate_token()
#     refresh_token = generate_token()
#     expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
#     scope = "read write"
#     acces_token = AccessToken.objects.create(
#         user=user, application=application, expires=expires, token=token, scope=scope
#     )
#
#     RefreshToken.objects.create(
#         user=user,
#         application=application,
#         token=refresh_token,
#         access_token=acces_token,
#     )
#
#     token_json = {
#         "access_token": acces_token.token,
#         "expires_in": oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
#         "refresh_token": acces_token.refresh_token.token,
#         "scope": acces_token.scope,
#         "client_id": application.client_id,
#         "client_secret": application.client_secret,
#         "encrypted_id": _e.encrypt(user.pk)
#     }
#
#     user.last_login = now()
#     user.save()
#
#     return token_json

# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=400)


class UserLoginView(APIView):
    def post(self, request):
        data = request.data

        # serializer = UserSerializer(data=request.data)
        if User.objects.filter(email=data['email']).exists():
            user = User.objects.get(email=data['email'])
            refresh = RefreshToken.for_user(user)
            refresh.set_exp(lifetime=timedelta(days=30))
            access_token = refresh.access_token

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(access_token),
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(global_defs.response_data(message="User doesn't exist"), status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(GenericAPIView):
    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'error': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.set_exp(lifetime=timedelta(days=30))
            access_token = refresh_token.access_token

            return Response(
                {
                    'refresh': str(refresh_token),
                    'access': str(access_token),
                }, status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({'error': 'Invalid refresh token. ', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Login_User_ViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    # throttle_classes = (UserRateThrottle,)

    @swagger_auto_schema(responses={200: UserSerializer})
    def create(self, request):
        try:
            request_user = request.user
            data = request.data
            user_json = UserSerializer(request_user).data

            # Guarda el dispositivo en el caso que exista
            fb_token = data.get("user_firebase_token")
            if fb_token is not None:
                inst_token = UserDevice.objects.filter(fb_token=fb_token)
                # Si el dispositivo existe se actualiza el usuario
                if inst_token.exists():
                    inst_userdevice = UserDevice.objects.get(fb_token=fb_token)
                    inst_userdevice.user_id = request.user.pk
                    inst_userdevice.save()
                else:
                    inst_userdevice = UserDevice()
                    inst_userdevice.user_id = request.user.pk
                    inst_userdevice.fb_token = fb_token
                    inst_userdevice.save()

            # Company asociated for Admins and SuperAdmins Users
            # try:
            #     company = Tenant.objects.get(id=request_user.company_key_id)
            #     company_json = CompanySerializer(company).data
            # except Tenant.DoesNotExist:
            #     company_json = None

            # Company asociated to car in citizens

            # recupera las opciones del menu del usuario logeado
            # options = User_Option.objects.filter(user_id=request.user.pk, menu__parent_id__isnull=True).order_by(
            #     'menu__order')
            options_menu_json = []
            # for option in options:
            #     if option.menu.state == 1:
            #         options_menu_json.append(option.menu.to_dict())

            response_json = {
                # "token": get_access_token(request_user),
                "user": user_json,
                # "company": company_json,
                # "car": car_json,
                # "car_company": car_company_json,
                # "contact_card": contact_card_json,
                "menu_options": options_menu_json,
                # "menu_options": menu_hierarchy,
            }
            return Response(response_json)
        except Exception as e:
            traceback.print_exc()
            return Response(global_defs.response_data('Error: ' + str(e)), status=status.HTTP_400_BAD_REQUEST)
