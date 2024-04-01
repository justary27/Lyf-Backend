import io
import threading

from rest_framework import status
from django.http import FileResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.firebase.auth import FirebaseAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from enums.response_type import ResponseType
from handlers.pagination_handler import LyfPaginator
from services.firebase.store import FirebaseStore
from services.reportlab.entry_exports import EntryPDFGen

from .models import DiaryEntry
from .utils import EntryTxtGen
from .enums import DiaryMessage
from .serializers import DiaryEntrySerializer


class DiaryViews:
    entry_text_generator = EntryTxtGen()
    entry_pdf_generator = EntryPDFGen(
        font_data={
            "ABZee": "ABeeZee-Regular.ttf",
            "Ubuntu": "Ubuntu-Regular.ttf",
            "Caveat": "Caveat-Regular.ttf"
        }
    )

    @staticmethod
    @api_view(["GET", "PUT", "POST", "PATCH", "DELETE"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def diary_list(request: Request, user_id: str):

        match request.method:
            case "GET":
                return DiaryViews.get_diary(request, user_id)
            case "POST":
                return DiaryViews.create_entry(request, user_id)
            case _:
                return Response(
                    ResponseType.INVALID_REQUEST.value.get_data(),
                    status.HTTP_405_METHOD_NOT_ALLOWED
                )

    @staticmethod
    @api_view(["GET", "PUT", "POST", "PATCH", "DELETE"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def diary_detail(request: Request, user_id: str, entry_id: str):

        if DiaryEntry.objects.check_if_entry_exists(entry_id):

            match request.method:
                case "GET":
                    return DiaryViews.get_entry(request, user_id, entry_id)
                case "PUT":
                    return DiaryViews.update_entry(request, user_id, entry_id)
                case "PATCH":
                    return DiaryViews.update_entry(request, user_id, entry_id)
                case "DELETE":
                    return DiaryViews.delete_entry(request, user_id, entry_id)
                case _:
                    return Response(
                        ResponseType.INVALID_REQUEST.value.get_data(),
                        status.HTTP_405_METHOD_NOT_ALLOWED
                    )
        else:
            return Response(
                ResponseType.DOES_NOT_EXIST.value.get_data(),
                status.HTTP_404_NOT_FOUND
            )

    @staticmethod
    def get_diary(request: Request, user_id: str):
        """
        Get the list of all the DiaryEntry(s) of a LyfUser.
        """
        entries = DiaryEntry.objects.get_user_entries(user_id)

        serialized_entries = DiaryEntrySerializer(entries, many=True)

        return LyfPaginator(request).get_paginated_response(
            serialized_entries.data,
        )

    @staticmethod
    @api_view(["GET"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def get_diary_as_txt(request: Request, user_id: str):
        diary = DiaryEntry.objects.get_user_entries(user_id)

        file_buffer = io.BytesIO()
        file_buffer = DiaryViews.entry_text_generator.generate_diary(diary, file_buffer)
        file_buffer.seek(0)

        return FileResponse(file_buffer, as_attachment=True, filename=f"{request.user}_diary.txt")

    @staticmethod
    @api_view(["GET"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def get_diary_as_pdf(request: Request, user_id: str):
        diary = DiaryEntry.objects.get_user_entries(user_id)

        file_buffer = io.BytesIO()
        file_buffer = DiaryViews.entry_pdf_generator.generate_diary(
            diary=diary, file_buffer=file_buffer
        )
        file_buffer.seek(0)

        return FileResponse(file_buffer, as_attachment=True, filename=f"{request.user}_diary.pdf")

    @staticmethod
    def create_entry(request: Request, user_id: str):
        # if request.method == 'POST':
        #     image = request.FILES.get('image')

        #     if not image:
        #         return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        #     # Create an InMemoryUploadedFile from the received image
            

        #     # Create a separate thread for uploading to Firebase and updating the model
        #     upload_thread = threading.Thread(target=FirebaseStore.upload_and_get_download_url, args=('/testing', image))
        #     upload_thread.start()

        #     return Response({'message': 'Image received and processing started'}, status=status.HTTP_202_ACCEPTED)

        # return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        data = request.data

        entry_serializer = DiaryEntrySerializer(data=data)

        if entry_serializer.is_valid():
            entry_serializer.save()

            return Response(
                ResponseType.ok_request(DiaryMessage.E_CREATE_SUCCESS.value).get_data(),
                status.HTTP_201_CREATED
            )
        else:

            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_entry(request: Request, user_id: str, entry_id: str):
        entry = DiaryEntry.objects.get_entry_by_id(entry_id)

        serialized_entry = DiaryEntrySerializer(entry)

        return Response(
            ResponseType.ok_request(DiaryMessage.SUCCESS.value, serialized_entry.data).get_data(),
            status.HTTP_200_OK
        )

    @staticmethod
    @api_view(["GET"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def get_entry_as_txt(request: Request, user_id: str, entry_id: str):
        entry = DiaryEntry.objects.get_entry_by_id(entry_id)

        file_buffer = io.BytesIO()
        file_buffer = DiaryViews.entry_text_generator.generate_entry(entry, file_buffer)
        file_buffer.seek(0)

        return FileResponse(file_buffer, as_attachment=True, filename=f"{entry.title}.txt")

    @staticmethod
    @api_view(["GET"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def get_entry_as_pdf(request: Request, user_id: str, entry_id: str):
        entry = DiaryEntry.objects.get_entry_by_id(entry_id)

        file_buffer = io.BytesIO()
        file_buffer = DiaryViews.entry_pdf_generator.generate_entry(
            entry=entry, file_buffer=file_buffer
        )
        file_buffer.seek(0)

        return FileResponse(file_buffer, as_attachment=True, filename=f"{entry.title}.pdf")

    @staticmethod
    def update_entry(request: Request, user_id: str, entry_id: str, **kwargs):
        data = request.data

        data["created_by"] = user_id
        data["id"] = entry_id

        entry = DiaryEntry.objects.get_entry_by_id(entry_id)
        entry_serializer = DiaryEntrySerializer(entry, data, partial=True)

        if entry_serializer.is_valid():
            entry_serializer.save()
            return Response(
                ResponseType.ok_request(DiaryMessage.E_UPDATE_SUCCESS.value).get_data(),
                status.HTTP_200_OK
            )
        else:
            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def delete_entry(request: Request, user_id: str, entry_id: str):
        entry = DiaryEntry.objects.get_entry_by_id(entry_id)

        entry.delete()

        return Response(
            ResponseType.ok_request(DiaryMessage.E_DELETE_SUCCESS.value).get_data(),
            status.HTTP_200_OK
        )
