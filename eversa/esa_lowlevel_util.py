#!/usr/bin/env python3

# ==============================================================================
# 
import base64
from   tonclient.client import *
from   tonclient.types  import *
from   datetime         import datetime
from  .esa_constants    import ZERO_PUBKEY

# ==============================================================================
# 
def getAbi(abiPath):
    abi = Abi.from_path(path=abiPath)
    return abi

def getTvc(tvcPath):
    fp  = open(tvcPath, 'rb')
    tvc = base64.b64encode(fp.read()).decode()
    fp.close()
    return tvc

def getAbiTvc(abiPath, tvcPath):
    return (getAbi(abiPath), getTvc(tvcPath))

def getCodeFromTvc(tvcPath):
    everClient    = TonClient(config=ClientConfig())
    tvc           = getTvc(tvcPath)
    tvcCodeParams = ParamsOfGetCodeFromTvc(tvc=tvc)
    tvcCodeResult = everClient.boc.get_code_from_tvc(params=tvcCodeParams).code
    return tvcCodeResult

# ==============================================================================
#
def stringToHex(inputString):
    return str(inputString).encode('utf-8').hex()

def hexToString(inputHex):
    return bytearray.fromhex(inputHex).decode()

# ==============================================================================
#
def getNowTimestamp():
    dt = datetime.now()
    unixtime = round(dt.timestamp())
    return unixtime

# ==============================================================================
#
def generateRandomMnemonic() -> str:
    crypto = TonClient(config=ClientConfig()).crypto
    phrase = crypto.mnemonic_from_random(params=ParamsOfMnemonicFromRandom()).phrase
    return phrase

def generateRandomSigner() -> Signer:
    keypair = TonClient(config=ClientConfig()).crypto.generate_random_sign_keys()
    signer  = Signer.Keys(keys=keypair)
    return signer

def generateSignerFromMnemonic(phrase: str, childIndex: int=0, hardened=True) -> Signer:
    try:
        crypto  = TonClient(config=ClientConfig()).crypto
        xprv    = crypto.hdkey_xprv_from_mnemonic(params=ParamsOfHDKeyXPrvFromMnemonic(phrase=phrase)).xprv
        hdkey   = crypto.hdkey_derive_from_xprv(params=ParamsOfHDKeyDeriveFromXPrv(xprv=xprv, child_index=childIndex, hardened=hardened)).xprv
        keypair = KeyPair(
            secret=crypto.hdkey_secret_from_xprv(params=ParamsOfHDKeySecretFromXPrv(xprv=hdkey)).secret, 
            public=crypto.hdkey_public_from_xprv(params=ParamsOfHDKeyPublicFromXPrv(xprv=hdkey)).public
        )
        signer = Signer.Keys(keys=keypair)
        return signer
    except:
        raise "Invalid Mnemonic!"

def saveSigner(filename: str, signer: Signer = generateRandomSigner()):
    signer.keys.dump(filename, False)

def loadSigner(keysFile=None) -> Signer:
    if keysFile is None:
        signer = Signer.External(ZERO_PUBKEY)
    else:
        signer = Signer.Keys(KeyPair.load(keysFile, False))
    return signer


# ==============================================================================
#
