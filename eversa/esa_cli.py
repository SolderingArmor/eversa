#!/usr/bin/env python3

import os
import argparse
import json
import shutil
from  .esa_lowlevel_util import generateRandomMnemonic

# ==============================================================================
#
parser = argparse.ArgumentParser(description="eversa CLI helps to automate building and testing Everscale/Venom smart contracts")
subparsers = parser.add_subparsers(dest='command', required=True)
#parser.add_argument("-a", "--archive", action="store_true", help="archive mode")
#parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
#parser.add_argument("-B", "--block-size", help="checksum blocksize")
#parser.add_argument("--ignore-existing", action="store_true", help="skip files that exist")
#parser.add_argument("--exclude", help="files to exclude")
#parser.add_argument("src", help="Source location")
#parser.add_argument("dest", help="Destination location")

parserInit = subparsers.add_parser('init', help="init help")
parserInit.add_argument('--force',     action='store_true', help='0000')
parserInit.add_argument('--no-sample', action='store_true', help='0000')

parserBuild = subparsers.add_parser('build', help="build help")
parserBuild.add_argument('contracts', metavar='contracts', type=str, nargs='*', help='List of contract names to build')

parserMeta = subparsers.add_parser('meta',  help="Show metadata/function list for a specific contract")
parserMeta.add_argument('contracts', metavar='contracts', type=str, nargs='+', help='List of contract names to show metadta for')

parserTest = subparsers.add_parser('test',  help="test help")

# ==============================================================================
#
def runInit(args):
    print("Initializing eversa...")
    args.force
    args.no_sample
    workDir   = os.getcwd()
    moduleDir = os.path.dirname(os.path.realpath(__file__))

    dirEmpty = (len(os.listdir(workDir)) <= 0)
    if not dirEmpty and not args.force:
        print("Error! Current directory is not empty!\nPlease use flag --force to initialize eversa anyway.")
        return

    # Create directories, ignore if they already exist
    try: 
        os.mkdir(os.path.join(workDir, "bin"))
    except OSError:
        pass
    try: 
        os.mkdir(os.path.join(workDir, "contracts"))
    except OSError:
        pass
    try: 
        os.mkdir(os.path.join(workDir, "interfaces"))
    except OSError:
        pass
    try: 
        os.mkdir(os.path.join(workDir, "tests"))
    except OSError:
        pass

    # Create config and generate random seed every time
    with open(os.path.join(moduleDir, ".config.json.example")) as jsonConfig:
        config = json.load(jsonConfig)
        for configElm in config["configs"]:
            if configElm["name"] == "local":
                configElm["phrase"] = generateRandomMnemonic()
                break
        with open(os.path.join(workDir, ".config.json"), "w") as output:
            json.dump(config, output, indent=4)

    # Copy samples if needed
    if not args.no_sample:
        shutil.copyfile(os.path.join(moduleDir, "sample", "ISample.sol"), os.path.join(workDir, "interfaces", "ISample.sol"))
        shutil.copyfile(os.path.join(moduleDir, "sample", "Sample.sol"),  os.path.join(workDir, "contracts",   "Sample.sol"))
        shutil.copyfile(os.path.join(moduleDir, "sample", "test.py"),     os.path.join(workDir, "tests",       "test.py"   ))
        shutil.copyfile(os.path.join(moduleDir, "sample", ".gitignore"),  os.path.join(workDir,                ".gitignore"))

    print("Done!")

# ==============================================================================
#
def runBuild(args):
    print("runBuild")
    if args.contracts is None:
        contractsList = []
    else: 
        contractsList = args.contracts
    
    for contract in contractsList:
        print(f"Building \"{contract}\"...")
        pass

# ==============================================================================
#
def runMeta(args):
    print("runMeta")
    for contract in args.contracts:
        pass

# ==============================================================================
#
def runTest(args):
    print("runTest")

parserInit.set_defaults(func=runInit)
parserBuild.set_defaults(func=runBuild)
parserMeta.set_defaults(func=runMeta)
parserTest.set_defaults(func=runTest)
#print(config)



# ==============================================================================
# init, init force, init with sample
# build all, build single
# show meta for contract
# test
def main():
    args = parser.parse_args()
    if args.command is None:
        pass
    else:
        args.func(args)
