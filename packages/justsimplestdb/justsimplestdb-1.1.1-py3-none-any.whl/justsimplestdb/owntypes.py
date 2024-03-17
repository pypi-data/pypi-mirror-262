from os.path import exists as is_file_exists
from os.path import abspath
class FileName(str):
    """Type for file names."""
    def __init__(self, given_string: str) -> None:
        super().__init__(given_string)
        
class StructurisedListLikeDBObject(list):
    """Type for database-like list."""
    def __init__(self, given_list: list):
        super().__init__(given_list)   

class KeysError(Exception):
    def __init__(self, message: str):
        """Keys exception"""
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return ("\n\nKeysError: " + self.message)

class StructurisedLikeDBerror(Exception):
    def __init__(self, message: str):
        """StructurisedLikeDB exception"""
        self.message = message
        super().__init__(self.message)
    def __str__(self) -> str:
        return ("\n\nStructurisedLikeDB Error: " + self.message)

class DatabaseObject(dict):
    pass

class IdError(Exception):
    def __init__(self, message: object) -> None:
        "Exceptions for every id problem."
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return (f"\n\nIdError: {self.message}")

class DatabaseObjectExistence(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return (f"\n\nDatabaseObjectExistence: {self.message}")
    
class JustSimplestDBAccessDenied(Exception):
    def __init__(self, message: str) -> None:
        '''JustSimplestDBDenied exception'''
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return (f"\n\nJustSimplestDBAccessDenied: {self.message} Access Denied.")
    
class UnknownFileExtension(Exception):
    def __init__(self, message: str) -> None:
        '''UnknownFile exception'''
        self.message = message
        super().__init__(message)
    def __str__(self) -> str:
        return (f"\n\nUnkownFile: {self.message}")

class WrongSeparator(Exception):
    def __init__(self, message: str):
        "Exception dedicated to wrong separator exceptions."
        self.message = message
        super().__init__(message)
    
    def __str__(self) -> str:
        return (f"\n\nWrongSeparator: {self.message}")
# Author data: 
# 01001010 01100001 01101011 01110101 01100010 00100000 01000001 01101100 01100101 01101011 01110011 01100001 01101110 01100100 01100101 01110010 00100000 01001101 01101001 01100011 01101000 01100001 01101100 01110011 01101011 01101001 00100000 00100010 01001101 00110001 01100011 01101000 00110100 01101100 00110101 01101011 00110001 00100010