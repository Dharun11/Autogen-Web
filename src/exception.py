import sys

def error_mesg_detail(error,error_detail:sys):
    _,_,exec_tb=error_detail.exc_info()
    
    ## gettig the file name
    filename=exec_tb.tb_frame.f_code.co_filename
    
    ##setting up the error message
    error_message=f"Error in {filename} at line {exec_tb.tb_lineno} with error message as {str(error)}"
    return error_message

class CustomException(Exception):
    def __init__(self,error,error_detail:sys):
        super().__init__(error)
        self.error=error_mesg_detail(error,error_detail)
        
    def __str__(self):
        return self.error