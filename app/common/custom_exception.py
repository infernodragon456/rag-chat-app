import sys

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: Exception = None):
        self.error_message = self.get_detailed_error_message(error_message, error_detail)
        super().__init__(error_message)

    
    @staticmethod
    def get_detailed_error_message(error_message, error_detail) -> str:
        _, _, exc_tb = sys.exc_info()
        line_number = exc_tb.tb_frame.f_lineno if exc_tb.tb_frame else "<unknown line>"
        file_name = exc_tb.tb_frame.f_code.co_filename if exc_tb.tb_frame else "<unknown file>"
        error_message = f"{error_message}, File Name: [{file_name}] at line number: [{line_number}] error: [{error_detail}]"
        return error_message

    def __str__(self):
        return self.error_message




