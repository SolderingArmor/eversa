## eversa

**eversa is a toolkit for Everscale/Venom smart contract development and testing written in Python.**

eversa consists of a library and CLI.

## Installation

```
> pip install eversa
```

## eversa

### Features

TODO

## CLI

### Features

-   **init**
    - TODO
-   **build**
    - TODO
-   **meta**
    - TODO
-   **test**
    - TODO

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

TODO

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
