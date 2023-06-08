#!/usr/bin/env python3

# ==============================================================================
# 
import os
from   pathlib           import Path
from   tonclient.client  import *
from   tonclient.types   import *
from  .esa_config        import EsaConfig
from  .esa_lowlevel_bc   import callFunction
from  .esa_contract      import *

# ==============================================================================
# 
class EverSa(object):
    def __init__(self, target: str = "local"):
        self.CONFIG      = EsaConfig(target)
        self.EVERCLIENT  = self.getEverClient()
        self.MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.WORK_DIR    = os.getcwd()
    
    def Log(self, *args):
        if self.CONFIG.VERBOSE:
            print(*args)

    def getSigner(self, childIndex: int=0, hardened=True):
        """
        Generates `Signer` using seed phrase from `.config` file.
        If Mnemonic is invalid an exception will be raised.

        Function argumnents:

        :param `childIndex`: Child index (see BIP-0032).
        :param `hardened`: Indicates the derivation of hardened/not-hardened key (see BIP-0032).
        """
        return generateSignerFromMnemonic(phrase=self.CONFIG.PHRASE, childIndex=childIndex, hardened=hardened)

    def findArtifact(self, name: str, ext: str):
        """
        Finds a binary artifact (file), searching in "bin" folder and library installation folder
        (for standard default artifacts like giver or multisig).

        Function argumnents:

        :param `name`: File name without extension.
        :param `ext`: File extension, use "tvc" or "abi.json".
        """
        files = list(Path(os.path.join(self.MODULE_PATH, "bin")).glob(f"**/{name}.{ext}"))
        if len(files) == 0:
            files = list(Path(os.path.join(self.WORK_DIR, "bin")).glob(f"**/{name}.{ext}"))
        return files[0] if len(files) > 0 else None

    # ========================================
    #
    def GetContract(self, contractName: str, **kwargs) -> EsaContract:
        """
        Creates a class of contract with name `contractName`. All keyword-arguments (**kwargs) 
        received by this function will be propagated as keyword-arguments to `esaUpdateInitData`.

        `esaUpdateInitData` additionally accepts the following arguments:

        :param `initialPubkey`: Initial Public Key that will be injected into contract code when InitData is generated.
                Used in such contracts as `SafeMultisig` or `SetcodeMultisig`. Default value is `ZERO_PUBKEY`.
        :param `signer`: Default `Signer` that will be used for External calls and contract deploy. Default value is `None`
                which means Signer will be randomly generated.
        """

        abiPath = self.findArtifact(contractName, "abi.json")
        tvcPath = self.findArtifact(contractName, "tvc")
        if abiPath is not None:
            contract = EsaContract(everClient=self.EVERCLIENT, abiPath=abiPath, tvcPath=tvcPath)
            contract.generateFunctionsFromAbi()
            try:
                contract.esaUpdateInitData(**kwargs)
            except TypeError as te:
                toFind = "required positional argument"
                if toFind in str(te):
                    print("")
                    print("Error! Not all InitData fields were provided!")
                    print(f"Please provide the following fields to GetContract(\"{contractName}\", ...):", str(te)[str(te).find(toFind)+len(toFind)+2:])
                    print("If you want to know more about InitData (stateInit), please, refer to https://github.com/tonlabs/TON-Solidity-Compiler/blob/master/API.md#deploy-via-new")
                    print("")
                toFind = "unexpected keyword argument"
                if toFind in str(te):
                    print("")
                    print("Error! Fields other than InitData were provided!")
                    print(f"Please remove the following fields from GetContract(\"{contractName}\", ...):", str(te)[str(te).find(toFind)+len(toFind)+2:])
                    print("If you want to know more about InitData (stateInit), please, refer to https://github.com/tonlabs/TON-Solidity-Compiler/blob/master/API.md#deploy-via-new")
                    print("")
                raise te

            return contract
        return None
    
    def getEverClient(self):
        return TonClient(config=ClientConfig(network=NetworkConfig(endpoints=self.CONFIG.ENDPOINTS), abi=AbiConfig(workchain=self.CONFIG.WORKCHAIN)))

    def Airdrop(self, contractAddress: str, value: int):
        """
        Top-up or fund or give native coin to a contract using Giver (currently works for local node only).
        """
        self.Log(f"EverSa.Airdrop(contractAddress: {contractAddress}, value: {value})")
        abiPath = self.findArtifact("local_giver", "abi.json")
        return callFunction(self.EVERCLIENT, abiPath, self.CONFIG.GIVER, "sendGrams", {"dest":contractAddress,"amount":value}, Signer.NoSigner())
