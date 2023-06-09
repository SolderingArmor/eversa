## eversa

**eversa is a toolkit for Everscale/Venom smart contract development and testing written in Python.**

eversa consists of a library and CLI.

## WIP Disclaimer

This project is currently work in progress, like alpha version, some features may be broken or missing!

Library part should fully work (best of my knowledge), Solidity contract sample is still missing, `eversa build` is still missing, `eversa test` is still missing.

But fear not! You can already do `eversa init` and use the library!

## Requirements

To build contracts you need `everdev` utility with `solc` compiler and `tvm-linker` installed. Please refer to https://github.com/tonlabs/everdev or simply run:

```
> npm i -g everdev
> everdev sol update
```

To locally test contracts you need `docker` and `tonlabs/local-node`. 

For `docker` installation refer to https://docs.docker.com/engine/install.

For `tonlabs/local-node` installation refer to https://hub.docker.com/r/tonlabs/local-node or simply run:

```
> docker run -d --name local-node -e USER_AGREEMENT=yes -p80:80 tonlabs/local-node
```

## Installation

```
> pip install eversa
```

## eversa

### Features

TODO

One of the main features is `eversa.getContract(...)` function. It dynamically builds python Object class with all contract functions from ABI.

`eversa` comes with pre-built Multisig contracts that are always ready for use. After `init` you can use the following Multisig wallets without any hassle or preparation:

```
esa    = eversa()
signer = generateRandomSigner()
setc  = esa.GetContract("SetcodeMultisig",   signer=signer, initialPubkey=signer.keys.public)
safe  = esa.GetContract("SafeMultisig",      signer=signer, initialPubkey=signer.keys.public)
surf  = esa.GetContract("Surf",              signer=signer, initialPubkey=signer.keys.public)
high  = esa.GetContract("HighloadSinglesig", signer=signer, initialPubkey=signer.keys.public)
```

Want some contract in pre-built directory? Hop in to [Telegram](https://t.me/eversa_main)!

## CLI

To run a cli type the following in console:

```
> eversa
```

To see full command description simply run:

```
> eversa -h
> eversa init -h
> eversa build -h
> eversa meta -h
> eversa test -h
> eversa new-seed -h
> eversa new-keys -h
``` 

### Commands

-   **init**
    - Initializes empty project with sample contract, sample test script and configuration file.
-   **build**
    - Builds single or all contracts and puts artifacts in thrget folder set in configuration file.
-   **meta**
    - Prints list of contract functions with all arguments. Static code parsers won't pick up contract's dynamic functions and reading ABI can be... frustrating.
-   **test**
    - Wraps and runs test scripts.
-   **new-seed**
    - Creates a random seed phrase with an option to save it to file.
-   **new-keys**
    - Creates a random private/public keypair with an option to save it to file.

## Configuration

`eversa` is designed to be configurable. You can configure `eversa` using a file called `.config.json` in the root of your project.

To create a basic, extendable `.config.json` file run:
```
> eversa init
``` 

This command will create a standard `.config.json` file, please note that seed phrase for `local` target is randomly generated every time you run `init` for security purposes, but be sure to generate all your non-test seed phrases manually and keep them safe! `init` also creates `.gitignore` file that won't let you accidentally commit your `.config.json` to GitHub repo.

## Quick Start

To ensure that everything works you can simply run the following commands in an empty directory:
```
> eversa init
> eversa build 
> eversa test
``` 

## Code examples

You can open `tests/tests.py` code file (after you run `init`) to see hands-on examples of `eversa` toolkit.

The following is a complete example of importing `eversa`, initializing toolkit, instantiating `Surf` wallet, deploying it, running getters and `sendTransaction`:

```
from eversa import *

esa = eversa()

signer = esa.getSigner(7)
surf   = esa.GetContract("Surf", signer=signer, initialPubkey=signer.keys.public)
esa.airdrop(surf.ADDRESS, EVER)
surf.deploy(owners=[f"0x{signer.keys.public}"], reqConfirms=1)

print(f"Surf address: {surf.ADDRESS}")
print(f"Surf balance: {surf.getBalance(True)}")

custodians = surf.getCustodians().run()
print(f"Surf custodians: {custodians}")

result = surf.sendTransaction(dest=ZeroAddress(), value=DIME*2, bounce=False, flags=1, payload=ZERO_PAYLOAD).callExternal()
print(result["result"], result["exception"])
```

## Useful Links

Get list of endpoints:
https://docs.evercloud.dev/products/evercloud/networks-endpoints

Register Everscale app:
https://dashboard.evercloud.dev/

## Getting Help

First, see if the answer to your question can be found in this readme or in the comments to the relevant Python code.

If the answer is not there:

-   Ask in [Telegram](https://t.me/eversa_main) to get help, or
-   Open a [discussion](https://github.com/SolderingArmor/eversa/discussions/new) with your question, or
-   Open an issue with [the bug](https://github.com/SolderingArmor/eversa/issues/new)

If you want to contribute, or follow along with contributor discussion, you can use our [main telegram](https://t.me/eversa_main) to chat with us about the development of `eversa`!

## Acknowledgements

TODO

## Roadmap

Something that needs to be done at some point to make life of users easier.

* Merge Exception and result not to have dictionary as return value.
* Add message tracing to library.
* Choose compiler version while building (and cache compiler binaries)
* Define function variables types in meta (as close to Solidity as possible)
* Write best practices writing tests for reusable and clean environments
* Tests should support sets of rules to ignore specific errors for example

## Changelog

v.0.5.0
* Tests now work. Tests fail only if blockchain exception was received or manual exception was raised. Otherwise test will be considered OK.
* Removed `EsaException`, because `EsaReturnValue` now keeps both result and exception.

v.0.4.0

* Added `giver_enabled` in `.config.json` file.
* Added running `eversa test` for all test files in `tests` folder, currently WIP.
* Updated test sample.
* `filename` -> `keysFile` in `saveSigner()` to be consistent in naming.

v.0.3.0:

* Changed `EverSa` class name to `eversa` to be consistent in naming.

v.0.2.0:

* Added `new-seed` to cli to easily generate and save random seed phrases;
* Added `new-keys` to cli to easily generate and save random keypairs;
* Added `getContractCode` to `eversa` to get code from tvc for contracts;
* Renamed `Airdrop` to `airdrop` in `eversa` to be consistent in naming.
