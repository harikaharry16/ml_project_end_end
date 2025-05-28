import sys
from logger import logger  # ✅ Import the logger you configured



def error_message_detail(error,error_detail:sys):
    # getting where error is getting 
    _,_,exc_tb = error_detail.exc_info()
    # how to get file name from exc_tb
    file_name = exc_tb.tb_frame.f_code.co_filename
    # to format error message
    error_message = "Error occured in file name [{0}] in line number [{1}] error is [{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

class customException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message



# if __name__ == "__main__":
#     try:
#         a=1/0
#     except Exception as e:
#         logger.info("Divide by zero error")
#         raise customException(e,sys)