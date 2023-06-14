#!/usr/bin/env python3

# ==============================================================================
# 
from eversa import *

# ==============================================================================
# SIGNERS
# ==============================================================================
def testSigners(esa: eversa):
    #
    # Generate random mnemonic and get Signer from it
    phrase  = generateRandomMnemonic()
    signer1 = generateSignerFromMnemonic(phrase=phrase, childIndex=1)

    # Generate Signer from mnemonic from `.config.json`
    signer2 = esa.getSigner(childIndex=7)

    # Generate completely random Signer
    signer3 = generateRandomSigner()

    # Save and load Signer to/from JSON file
    saveSigner(keysFile="signer3.json", signer=signer3)
    signer4 = loadSigner(keysFile="signer3.json")

# ==============================================================================
# CONTRACTS
# ==============================================================================
def testContracts(esa: eversa):
    #
    # Generate completely random Signer
    signer = generateRandomSigner()
    #
    # Dynamically create `SetcodeMultisig` contract class
    msig1 = esa.GetContract("SetcodeMultisig", signer=signer, initialPubkey=signer.keys.public)
    esa.airdrop(msig1.ADDRESS, EVER)
    print(f"Multisig 1 address: {msig1.ADDRESS}")
    print(f"Multisig 1 balance: {msig1.getBalance(showInEvers=True)}")

    # Specify contract constructor params in `deploy` function and print results
    result = msig1.deploy(owners=[f"0x{signer.keys.public}"], reqConfirms=1)
    print(result)

# ==============================================================================
# RUNNING MANUALLY
# ==============================================================================
# Keep this part if you want to manually run the tests without `eversa test` wrapper
#
if __name__ == "__main__":
    esa = eversa()
    testSigners(esa)
    testContracts(esa)
