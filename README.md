## eversa

**eversa is a toolkit for Everscale/Venom smart contract development and testing written in Python.**

eversa consists of a library and CLI.

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

esa = EverSa()

signer = esa.getSigner(7)
surf   = esa.GetContract("Surf", signer=signer, initialPubkey=signer.keys.public)
esa.Airdrop(surf.ADDRESS, EVER)
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
