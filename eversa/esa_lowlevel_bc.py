#!/usr/bin/env python3

# ==============================================================================
# 
from  tonclient.client  import *
from  tonclient.types   import *
from .esa_lowlevel_util import *
from .esa_constants     import *
from .esa_return_values import EsaReturnValue
from .esa_graphql       import EsaGraphQL

# ==============================================================================
# 
def getAddress(abiPath, tvcPath, signer, initialPubkey, initialData):

    everClient = TonClient(config=ClientConfig())
    (abi, tvc) = getAbiTvc(abiPath, tvcPath)
    deploySet  = DeploySet(tvc=tvc, initial_pubkey=initialPubkey, initial_data=initialData)

    params     = ParamsOfEncodeMessage(abi=abi, signer=signer, deploy_set=deploySet)
    encoded    = everClient.abi.encode_message(params=params)
    return encoded.address

# ==============================================================================
#
def getAddressZeroPubkey(abiPath, tvcPath, initialData):

    keys   = KeyPair(ZERO_PUBKEY, ZERO_PUBKEY)
    signer = Signer.Keys(keys)
    return getAddress(abiPath, tvcPath, signer, ZERO_PUBKEY, initialData)

# ==============================================================================
#
def prepareMessageBoc(abiPath, functionName, functionParams):

    everClient = TonClient(config=ClientConfig())
    callSet    = CallSet(function_name=functionName, input=functionParams)
    params     = ParamsOfEncodeMessageBody(abi=getAbi(abiPath), signer=Signer.NoSigner(), is_internal=True, call_set=callSet)
    encoded    = everClient.abi.encode_message_body(params=params)
    return encoded.body

# ==============================================================================
# 
def deployContract(everClient: TonClient, abiPath, tvcPath, constructorInput, initialData, signer, initialPubkey):

    try:
        (abi, tvc)    = getAbiTvc(abiPath, tvcPath)
        callSet       = CallSet(function_name='constructor', input=constructorInput)
        deploySet     = DeploySet(tvc=tvc, initial_pubkey=initialPubkey, initial_data=initialData)
        params        = ParamsOfEncodeMessage(abi=abi, signer=signer, call_set=callSet, deploy_set=deploySet)
        encoded       = everClient.abi.encode_message(params=params)

        messageParams = ParamsOfSendMessage(message=encoded.message, send_events=False, abi=abi)
        messageResult = everClient.processing.send_message(params=messageParams)
        waitParams    = ParamsOfWaitForTransaction(message=encoded.message, shard_block_id=messageResult.shard_block_id, send_events=False, abi=abi)
        result        = everClient.processing.wait_for_transaction(params=waitParams)

        return EsaReturnValue(everResult=result)

    except TonException as e:
        print(e.client_error.message)
        return EsaReturnValue(everException=e)

# ==============================================================================
#
def runFunctionLocal(everClient: TonClient, boc: str, abiPath: str, contractAddress: str, functionName: str, functionParams):

    try:
        abi          = getAbi(abiPath)
        callSet      = CallSet(function_name=functionName, input=functionParams)
        params       = ParamsOfEncodeMessage(abi=abi, address=contractAddress, signer=Signer.NoSigner(), call_set=callSet)
        encoded      = everClient.abi.encode_message(params=params)

        paramsRun    = ParamsOfRunTvm(message=encoded.message, account=boc, abi=abi)
        result       = everClient.tvm.run_tvm(params=paramsRun)

        paramsDecode = ParamsOfDecodeMessage(abi=abi, message=result.out_messages[0])
        decoded      = everClient.abi.decode_message(params=paramsDecode)

        if len(decoded.value) == 1 and list(decoded.value.keys())[0] == "value0":
            result = decoded.value["value0"]
        else:
            result = decoded.value

        return result
    
    except TonException as e:
        print(e.client_error.message)
        return EsaReturnValue(everException=e)

def runFunction(everClient: TonClient, graphQL: EsaGraphQL, abiPath, contractAddress, functionName, functionParams):

    result = graphQL.getAccountGraphQL(contractAddress, "boc")
    if result is None:
        return None
    if result["boc"] is None:
        return None

    return (runFunctionLocal(everClient=everClient, boc=result["boc"], abiPath=abiPath, contractAddress=contractAddress, functionName=functionName, functionParams=functionParams))

# ==============================================================================
#
def callFunction(everClient: TonClient, abiPath, contractAddress, functionName, functionParams, signer, waitForTransaction: bool = True):

    try:
        abi           = getAbi(abiPath)
        callSet       = CallSet(function_name=functionName, input=functionParams)
        params        = ParamsOfEncodeMessage(abi=abi, address=contractAddress, signer=signer, call_set=callSet)
        encoded       = everClient.abi.encode_message(params=params)

        messageParams = ParamsOfSendMessage(message=encoded.message, send_events=False, abi=abi)
        messageResult = everClient.processing.send_message(params=messageParams)

        if waitForTransaction:
            waitParams = ParamsOfWaitForTransaction(message=encoded.message, shard_block_id=messageResult.shard_block_id, send_events=False, abi=abi)
            result     = everClient.processing.wait_for_transaction(params=waitParams)
        else:
            result = None

        return EsaReturnValue(everResult=result)

    except TonException as e:
        print(e.client_error.message)
        return EsaReturnValue(everException=e)

# ==============================================================================
#
