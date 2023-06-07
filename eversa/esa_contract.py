#!/usr/bin/env python3

# ==============================================================================
# 
from   tonclient.client  import *
from   tonclient.types   import *
from   datetime          import datetime
from   pprint            import pprint
from  .esa_lowlevel_util import *
from  .esa_lowlevel_bc   import *
from  .esa_constants     import *
from  .esa_graphql       import *
from   makefun           import create_function
from   inspect           import getmodule

# ==============================================================================
#
class EsaCallable(object):
    """
    Generic wrapper class for callable functions.
    
    All contracts in eversa are of `EsaContract` class with dynamically added functions. Each function is contract
    function from Solidity/ABI. The main problem in ABI about functions is that there is no way to 
    distinct pure functions from views and from functions that can modify the state. If you don't have access
    to source code you need to either just know or try to call the function to see what it does. `EsaCallable` 
    is a wrapper that allows to call any function either externally, from Multisig (including `submitToMultisig` 
    if Multisig has 2+ signers) or run it locally. If you are using `EsaContract` class to access the contract 
    (as you really should), `EsaContract` will fill all `EsaCallable` parameters for you, all you will need to 
    do is use the correct way to call the function.
    """
    def __init__(self, everClient: TonClient, contractClass, abiPath: str, tvcPath: str, contractAddress: str, functionName, functionParams):
        self.EVERCLIENT  = everClient
        self.ABI         = abiPath
        self.TVC         = tvcPath
        self.ADDRESS     = contractAddress
        self.CONTRACT    = contractClass
        self.FUNC_NAME   = functionName
        self.FUNC_PARAMS = functionParams

    def callExternal(self, signer: Signer = None, waitForTransaction: bool = True):
        if signer is None:
            if hasattr(self, "CONTRACT"):
                signer = self.CONTRACT.SIGNER
            else:
                print("")
                print("Error! No SIGNER in EsaCallable.callExternal(...)!")
                print(f"Please provide a valid signer!")
                print("")
                raise

        result = callFunction(everClient=self.EVERCLIENT, abiPath=self.ABI, contractAddress=self.ADDRESS, functionName=self.FUNC_NAME, functionParams=self.FUNC_PARAMS, signer=signer, waitForTransaction=waitForTransaction)
        return result

    def sendFromMultisig(self, msig, value: int = DIME, bounce: bool = True, flags: int = 1):
        messageBoc = prepareMessageBoc(abiPath=self.ABI, functionName=self.FUNC_NAME, functionParams=self.FUNC_PARAMS)
        result     = msig.sendTransaction(dest=self.ADDRESS, value=value, bounce=bounce, flags=flags, payload=messageBoc)
        return result

    def submitToMultisig(self, msig, value: int = DIME, bounce: bool = True, allBalance: bool = False):
        messageBoc = prepareMessageBoc(abiPath=self.ABI, functionName=self.FUNC_NAME, functionParams=self.FUNC_PARAMS)
        result     = msig.submitTransaction(dest=self.ADDRESS, value=value, bounce=bounce, allBalance=allBalance, payload=messageBoc)
        return result

    def run(self):
        """
        Run function locally without signing and/or modifying the state.
        """
        boc = self.CONTRACT.getBOC()
        result = runFunctionLocal(everClient=self.EVERCLIENT, boc=boc, abiPath=self.ABI, contractAddress=self.ADDRESS, functionName=self.FUNC_NAME, functionParams=self.FUNC_PARAMS)
        return result

# ==============================================================================
#
class EsaContractGenerator(object):
    """
    Generic class to generate functions dynamically from ABI.

    For internal use only, use it only if you know what you are doing.
    """
    def __init__(self):
        pass

    # ========================================
    # Generic dynamic function implementation
    def _genericCallableFunction(self, f, **kwargs) -> EsaCallable:
        callable = EsaCallable(everClient=self.EVERCLIENT, contractClass=self, abiPath=self.ABI, tvcPath=self.TVC, contractAddress=self.ADDRESS, functionName=f.__name__, functionParams=kwargs)
        return callable
    
    # ========================================
    #
    def _genericDeployFunction(self, f, **kwargs):
        self.CONSTRUCTOR = kwargs
        result = deployContract(everClient=self.EVERCLIENT, abiPath=self.ABI, tvcPath=self.TVC, constructorInput=self.CONSTRUCTOR, initialData=self.INITDATA, signer=self.SIGNER, initialPubkey=self.INITIAL_PUBKEY)
        return result

    # ========================================
    #
    def _genericUpdateInitDataFunction(self, f, **kwargs):
        signer        = kwargs["signer"]
        initialPubkey = kwargs["initialPubkey"]
        del kwargs["signer"]
        del kwargs["initialPubkey"]

        if signer is not None:
            self.SIGNER = signer
        self.INITDATA       = kwargs
        self.INITIAL_PUBKEY = initialPubkey
        self.ADDRESS        = getAddress(abiPath=self.ABI, tvcPath=self.TVC, signer=self.SIGNER, initialPubkey=self.INITIAL_PUBKEY, initialData=self.INITDATA)

    # ========================================
    #
    def _getFunctionSignature(self, functionAbi, functionName=None, fieldsToJoin=None):
        if functionName is None:
            functionName = functionAbi["name"]
        arguments = []
        for input in functionAbi["inputs"]:
            arguments.append(input["name"])

        if fieldsToJoin is not None:
            arguments.append(fieldsToJoin)
        return f"{functionName}({','.join(arguments)})"

    # ========================================
    #
    def generateFunctionsFromAbi(self):
        with open(self.ABI) as abiContents:
            abiConfig = json.load(abiContents)

            # 1. genetate "updateInitData" with initdata and initialPubkey params
            #
            initDataFields = []
            for field in abiConfig["data"]:
                initDataFields.append(field["name"])
            
            initDataParams = ""
            if len(initDataFields) > 0:
                initDataParams =  f"{','.join(initDataFields)},initialPubkey:str=ZERO_PUBKEY,signer:Signer=None"
            else:
                initDataParams = "initialPubkey:str=ZERO_PUBKEY,signer:Signer=None"
            setattr(
                self, 
                "updateInitData", 
                create_function(f"updateInitData({initDataParams})", 
                                self._genericUpdateInitDataFunction, inject_as_first_arg=True)
            )

            # 2. all other functions are generated to retrun EsaCallable because we don't know if it is getter or caller, main idea is to supply params and the body will be the same
            #
            for function in abiConfig["functions"]:
                if function["name"] == "constructor":
                    # 1. "deploy" is a renamed constructor
                    setattr(
                        self, 
                        "deploy", 
                        create_function(self._getFunctionSignature(functionAbi=function, functionName="deploy"), 
                                        self._genericDeployFunction, inject_as_first_arg=True)
                    )
                else:
                    setattr(
                        self, 
                        function["name"], 
                        create_function(self._getFunctionSignature(functionAbi=function), 
                                        self._genericCallableFunction, inject_as_first_arg=True)
                    )

# ==============================================================================
#
class EsaContract(EsaContractGenerator):
    """
    Generic contract class.
    """
    def __init__(self, everClient: TonClient, abiPath: str, tvcPath: str, signer: Signer = None, initialPubkey: str = ZERO_PUBKEY, address: str = None):
        self.SIGNER         = signer if signer is not None else generateRandomSigner()
        self.EVERCLIENT     = everClient
        self.GRAPHQL        = EsaGraphQL(everClient=everClient)
        self.BOC            = None
        self.ABI            = abiPath
        self.TVC            = tvcPath
        self.CONSTRUCTOR    = {} if not hasattr(self, "CONSTRUCTOR") else self.CONSTRUCTOR
        self.INITDATA       = {} if not hasattr(self, "INITDATA")    else self.INITDATA
        self.INITIAL_PUBKEY = initialPubkey
        self.ADDRESS        = address

    def getBOC(self, forceUpdate: bool = False):
        if forceUpdate or self.BOC is None:
            result = self.GRAPHQL.getAccountGraphQL(accountID=self.ADDRESS, fields="boc")
            if result is None or result["boc"] is None:
                self.BOC = None
            else:
                self.BOC = result["boc"]
        return self.BOC

    def getBalance(self, showInEvers=False):
        result = self.GRAPHQL.getAccountGraphQL(accountID=self.ADDRESS, fields="balance(format:DEC)")
        balance = int(result["balance"]) if result is not None else 0
        return balance / EVER if showInEvers else balance

    def getAccType(self):
        """
        Gets Account type from blockchain. Possible values:

        `0` - uninit.
        `1` - active.
        `2` - frozen.
        `3` - nonExist.
        """
        result = self.GRAPHQL.getAccountGraphQL(accountID=self.ADDRESS, fields="acc_type")
        return int(result["acc_type"]) if result is not None else 0

# ==============================================================================
#
