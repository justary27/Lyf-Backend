from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from services.firebase.auth import FirebaseAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from enums.response_type import ResponseType
from handlers.pagination_handler import LyfPaginator

from .models import Todo
from .enums import TodoMessages
from .serializers import TodoSerializer


class TodoViews:

    @staticmethod
    @api_view(["GET", "PUT", "POST", "PATCH", "DELETE"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])    
    def todo_list(request: Request, user_id: str):

        match request.method:
            case "GET":
                return TodoViews.get_all_todos(request, user_id)
            case "POST":
                return TodoViews.create_todo(request, user_id)
            case _:
                return Response(
                    ResponseType.INVALID_REQUEST.value.get_data(),
                    status.HTTP_405_METHOD_NOT_ALLOWED
                )

    @staticmethod
    @api_view(["GET", "PUT", "POST", "PATCH", "DELETE"])
    @authentication_classes([FirebaseAuthentication])
    @permission_classes([IsAuthenticated])
    def todo_detail(request: Request, user_id: str, todo_id: str):

        if Todo.objects.check_if_todo_exists(todo_id):
            
            match request.method:
                case "GET":
                    return TodoViews.get_todo(request, user_id, todo_id)
                case "PUT":
                    return TodoViews.update_todo(request, user_id, todo_id)
                case "PATCH":
                    return TodoViews.update_todo(request, user_id, todo_id)
                case "DELETE":
                    return TodoViews.delete_todo(request, user_id, todo_id)
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
    def get_all_todos(request: Request, user_id: str):

        todos = Todo.objects.get_user_todos(user_id)

        serialized_todos = TodoSerializer(todos, many=True)

        return LyfPaginator(request).get_paginated_response(
            serialized_todos.data
        )

    @staticmethod
    def create_todo(request: Request, user_id: str):
        data = request.data

        data["created_by"] = user_id

        todo_serializer = TodoSerializer(data)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(
                ResponseType.ok_request(TodoMessages.T_CREATE_SUCCESS.value).get_data(), 
                status.HTTP_200_OK
            )
        else:
            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_todo(request: Request, user_id: str, todo_id: str):

        todo = Todo.objects.get_todo_by_id(todo_id)
        
        serialized_todo = TodoSerializer(todo)

        return Response(
            ResponseType.ok_request(TodoMessages.SUCCESS.value, serialized_todo.data).get_data(), 
            status.HTTP_200_OK
        )

    @staticmethod
    def update_todo(request: Request, user_id: str, todo_id: str):
        data = request.data

        data["created_by"] = user_id
        data["id"] = todo_id

        todo = Todo.objects.get_todo_by_id(todo_id)
        todo_serializer = TodoSerializer(todo, data=data, partial=True)

        if todo_serializer.is_valid():
            todo_serializer.save()
            return Response(
                ResponseType.ok_request(TodoMessages.T_UPDATE_SUCCESS.value).get_data(), 
                status.HTTP_200_OK
            ) 
        else:
            return Response(
                ResponseType.BAD_REQUEST.value.get_data(),
                status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def delete_todo(request: Request, user_id: str, todo_id: str):
        todo = Todo.objects.get_todo_by_id(todo_id)

        todo.delete()

        return Response(
            ResponseType.ok_request(TodoMessages.T_DELETE_SUCCESS.value).get_data(),
            status.HTTP_200_OK
        )
