from enum import Enum


class DiaryMessage(Enum):
    
    SUCCESS = "Success!"
    E_CREATE_SUCCESS = "Entry created successfully!"
    E_UPDATE_SUCCESS = "Entry updated successfully!"
    E_DELETE_SUCCESS = "Entry deleted successfully!"
