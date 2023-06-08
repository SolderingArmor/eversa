#!/usr/bin/env python3

# ==============================================================================
# 
from eversa import *

# ==============================================================================
# EVERSA INIT
# ==============================================================================
# 
# eversa main class
esa = EverSa()

# ==============================================================================
# SIGNERS
# ==============================================================================
#
# Generate random mnemonic and get Signer from it
phrase  = generateRandomMnemonic()
signer1 = generateSignerFromMnemonic(phrase=phrase, childIndex=1)

# Generate Signer from mnemonic from `.config.json`
signer2 = esa.getSigner(childIndex=7)

# Generate completely random Signer
signer3 = generateRandomSigner()

# Save and load Signer to/from JSON file
saveSigner(filename="signer3.json", signer=signer3)
signer4 = loadSigner(filename="signer3.json")

# ==============================================================================
# CONTRACTS
# ==============================================================================
#
# Dynamically create `SetcodeMultisig` contract class
msig1 = esa.GetContract("SetcodeMultisig", signer=signer1, initialPubkey=signer1.keys.public)
esa.Airdrop(msig1.ADDRESS, EVER)
print(f"Multisig 1 address: {msig1.ADDRESS}")
print(f"Multisig 1 balance: {msig1.getBalance(showInEvers=True)}")

# Specify contract constructor params in `deploy` function and print results
result = msig1.deploy(owners=[f"0x{signer1.keys.public}"], reqConfirms=1)
print(result["result"], result["exception"])
