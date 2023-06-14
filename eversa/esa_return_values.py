#!/usr/bin/env python3

# ==============================================================================
# 
from tonclient.client import TonException
from tonclient.types  import ResultOfProcessMessage

# ==============================================================================
# 
class EsaReturnValue(object):
    """
    Return value from any blockchain call and Exception (if exists).

    `EsaReturnValue` has the following local variables:

    :var `RESULT`: Raw native `ResultOfProcessMessage` from `ton-client-py`.
    :var `EXCEPTION`: Raw native `TonException` from `ton-client-py`.
    :var `ERROR_CODE`: `TonException.client_error.code` if any.
    :var `ERROR_DESC`: `TonException.client_error.data["description"]` if any.
    :var `ERROR_MSG`: `TonException.client_error.message` if any.
    :var `TXN_ID`: `TonException.client_error.data["transaction_id"]` if any.
    """
    # ======================================
    #
    def __init__(self, everResult: ResultOfProcessMessage = None, everException: TonException = None):
        self.RESULT     = None
        self.EXCEPTION  = None
        self.ERROR_CODE = 0
        self.ERROR_DESC = None
        self.ERROR_MSG  = None
        self.TXN_ID     = None

        if everResult is not None:
            self.SetResult(everResult)
        if everException is not None:
            self.SetException(everException)

    # ======================================
    #
    def SetResult(self, everResult: ResultOfProcessMessage):
        self.RESULT = everResult
        # TODO: parse result

    # ======================================
    #
    def SetException(self, everException: TonException):
        self.EXCEPTION = everException
        self.ERROR_CODE = self.EXCEPTION.client_error.code
        self.ERROR_MSG  = self.EXCEPTION.client_error.message
        
        result = self.EXCEPTION.client_error.data
        if "description" in result:
            self.ERROR_DESC = result["description"]
        if "transaction_id" in result:
            self.TXN_ID = result["transaction_id"]

    # ======================================
    #
    def __str__(self):
        #if self.RESULT is None:
        #    return f'RESULT None'
        #else:
            if self.ERROR_CODE == 0:
                return f'RESULT OK'
            else:
                return f'RESULT ERROR\nError Code: {self.ERROR_CODE}\nError Message: {self.ERROR_MSG}\nError Description: {self.ERROR_DESC}\nTransaction ID: {self.TXN_ID}'

# ==============================================================================
# 
