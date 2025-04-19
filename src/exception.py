import sys
from src.logger import logging

def error_detail_info(error, error_detail:sys):
    exc_tb= error_detail.exc_info()[2]

    file_name= exc_tb.tb_frame.f_code.co_filename
    lineno= exc_tb.tb_lineno

    error_message = "There was an error in the python script [{0}], line number [{1}], error message[{2}]".format(file_name, lineno, str(error))
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_detail_info(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
