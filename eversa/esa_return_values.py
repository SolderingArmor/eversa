#!/usr/bin/env python3

# ==============================================================================
# 
from tonclient.client import TonException
from tonclient.types  import ResultOfProcessMessage

# ==============================================================================
# 
class EsaException(object):
    """
    Exception from any blockchain call.
    
    `EsaReturnValue` has the following local variables:

    :var `EXCEPTION`: Raw native `TonException` from `ton-client-py`.
    :var `ERROR_CODE`: `TonException.client_error.code` if any.
    :var `ERROR_DESC`: `TonException.client_error.data["description"]` if any.
    :var `ERROR_MSG`: `TonException.client_error.message` if any.
    :var `TXN_ID`: `TonException.client_error.data["transaction_id"]` if any.
    """
    # ======================================
    #
    def __init__(self, everException: TonException = None):
        self.EXCEPTION  = None
        self.ERROR_CODE = 0
        self.ERROR_DESC = None
        self.ERROR_MSG  = None
        self.TXN_ID     = None
        if everException is not None:
            self.SetException(everException)

    # ======================================
    #
    def SetException(self, everException: TonException):
        self.EXCEPTION = everException

        result = self.EXCEPTION.client_error.data
        self.ERROR_CODE = self.EXCEPTION.client_error.code
        self.ERROR_MSG = self.EXCEPTION.client_error.message
        
        if "description" in result:
            self.ERROR_DESC = result["description"]
        if "transaction_id" in result:
            self.TXN_ID = result["transaction_id"]

    # ======================================
    #
    def __str__(self):
        return f'Error Code: {self.ERROR_CODE}\nError Message: {self.ERROR_MSG}\nError Description: {self.ERROR_DESC}\nTransaction ID: {self.TXN_ID}'

# ==============================================================================
# 
class EsaReturnValue(object):
    """
    Return value from any blockchain call.

    `EsaReturnValue` has the following local variables:

    :var `RESULT`: Raw native `ResultOfProcessMessage` from `ton-client-py`.
    """
    # ======================================
    #
    def __init__(self, everResult: ResultOfProcessMessage = None):
        self.RESULT = None
        if everResult is not None:
            self.SetResult(everResult)

    # ======================================
    #
    def SetResult(self, everResult: ResultOfProcessMessage):
        self.RESULT = everResult
        # TODO: parse result

    # ======================================
    #
    def __str__(self):
        if self.RESULT is None:
            return f'RESULT None'
        else:
            return f'RESULT OK\nTransaction: {self.RESULT.transaction}\nOut Messages: {self.RESULT.out_messages}\nDecoded Output: {self.RESULT.decoded.output}'

# ==============================================================================
# 
