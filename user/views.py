from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from enums.response_type import ResponseType

from services.firebase.auth import FirebaseAuthentication

from .models import LyfUser
from .enums import LyfUserMessages
from .serializers import LyfUserSerializer


class LyfUserViews:

    @staticmethod
    @api_view(["POST"])
    def signup(request: Request):

        token = request.headers.get('Authorization')

        if not token:
            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )
        else:
            uid = FirebaseAuthentication.fire_id(token)

            data = request.data

            data['id'] = uid

            user_serializer = LyfUserSerializer(data)

            if user_serializer.is_valid():
                user_serializer.save()

                return Response(
                    ResponseType.ok_request(LyfUserMessages.U_CREATE_SUCCESS.value).get_data(),
                    status.HTTP_201_CREATED
                )

            else:
                return Response(
                    ResponseType.BAD_REQUEST.value.get_data(),
                    status.HTTP_400_BAD_REQUEST
                )

    @staticmethod
    @api_view(["POST"])
    def login(request: Request):
        print(request.data)
        token = request.headers.get('Authorization')

        if not token:
            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )
        else:
            uid = FirebaseAuthentication.fire_id(token)

            if LyfUser.objects.check_if_user_exists(uid):

                user = LyfUser.objects.get_user_by_id(uid)

                serialized_user = LyfUserSerializer(user)

                return Response(
                    ResponseType.ok_request(LyfUserMessages.SUCCESS.value, serialized_user.data).get_data(),
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    ResponseType.DOES_NOT_EXIST.value.get_data(),
                    status.HTTP_200_OK
                )

    # @api_view(["PUT"])
    # @permission_classes([IsAuthenticated])
    # def update_account(request, user_id):
    #     data = request.data

    #     try:
    #         entry = LyfUser.objects.update(
    #             email=data['email'],
    #             username=data['username'],
    #         )
    #     except Exception as e:
    #         return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)

    # @api_view(["PUT"])
    # @authentication_classes([FirebaseAuthentication])
    # @permission_classes([IsAuthenticated])
    # def deactivate_account(request, user_id):
    #     if LyfUser.objects.check_if_user_exists(user_id):
    #         user = LyfUser.objects.get_user_by_id(user_id)
    #         user.is_active = False
    #         try:
    #             user.save(update_fields=['is_active'])
    #             return Response("Account deactivated successfully!")
    #
    #         except Exception as e:
    #             return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    @api_view(["DELETE"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def delete_account(request: Request, user_id: str):

        if LyfUser.objects.check_if_user_exists(user_id):
            user = LyfUser.objects.get_user_by_id(user_id)

            user.delete()
            return Response(
                ResponseType.ok_request(LyfUserMessages.U_DELETE_SUCCESS.value).get_data(),
                status.HTTP_200_OK
            )

        else:
            return Response(
                ResponseType.DOES_NOT_EXIST.value.get_data(),
                status.HTTP_404_NOT_FOUND
            )
