#!/usr/bin/env python3

# ==============================================================================
# 
from   tonclient.client import *
from   tonclient.types  import *

# ==============================================================================
# 
class EsaGraphQL(object):
    def __init__(self, everClient: TonClient):
        self.EVER_CLIENT = everClient

    # ======================================
    #
    def _getAccountsInternalGraphQL(self, accountIDsArray, fields: str, limit: int):

        paramsCollection = ParamsOfQueryCollection(
        collection="accounts", result=fields, limit=limit,
        filter={"id":{"in":accountIDsArray}},
        order=[OrderBy(path='id', direction=SortDirection.DESC)])

        result = self.EVER_CLIENT.net.query_collection(params=paramsCollection)
        return result.result

    def getAccountGraphQL(self, accountID, fields):

        result = self._getAccountsInternalGraphQL(accountIDsArray=[accountID], fields=fields, limit=1)
        if len(result) > 0:
            return result[0]
        else:
            return None

    # ======================================
    #
    def getMessageGraphQL(self, messageID, fields):

        paramsCollection = ParamsOfQueryCollection(
            collection="messages", result=fields, limit=1,
            filter={"id":{"eq":messageID}}
        )

        result = self.EVER_CLIENT.net.query_collection(params=paramsCollection)
        if len(result.result) > 0:
            return result.result[0]
        else:
            return None

    # ======================================
    #
    def getTransactionFromMessageGraphQL(self, messageID, fields):

        paramsCollection = ParamsOfQueryCollection(
            collection="transactions", result=fields, limit=1,
            filter={"in_msg":{"eq":messageID}}
        )

        result = self.EVER_CLIENT.net.query_collection(params=paramsCollection)
        if len(result.result) > 0:
            return result.result[0]
        else:
            return None

# ==============================================================================
# 
