#!/usr/bin/env python3

import os
import sys
import argparse
import json
import shutil
import imp
import traceback
from   io import StringIO 
from   inspect import getmodule, getmembers, isfunction, signature
from  .esa_lowlevel_util import generateRandomMnemonic, generateRandomSigner, saveSigner
from  .eversa import eversa

# ==============================================================================
#
parser = argparse.ArgumentParser(description="eversa CLI helps to automate building and testing Everscale/Venom smart contracts")
subparsers = parser.add_subparsers(dest='command', required=True)

parserInit = subparsers.add_parser('init', help="Initialize empty project with samples in current directory")
parserInit.add_argument('--force',     action='store_true', help='Firse initialization even if directory is not empty')
parserInit.add_argument('--no-sample', action='store_true', help='Do not copy any sample files')

parserBuild = subparsers.add_parser('build', help="TODO")
parserBuild.add_argument('contracts', metavar='contracts', type=str, nargs='*', help='List of contract names to build')

parserMeta = subparsers.add_parser('meta',  help="Show metadata/function list for a specific contract")
parserMeta.add_argument('contracts', metavar='contracts', type=str, nargs='+', help='List of contract names to show metadta for')

parserTest = subparsers.add_parser('test',  help="Run test script to test the contracts")
parserTest.add_argument('environment', metavar='environment', type=str, nargs=1, help='Test environment (use a name from .config.json file), for example `local`')

parserSeed = subparsers.add_parser('new-seed', help="Create a random seed phrase with an option to save it to file")
parserSeed.add_argument('output', metavar='output', type=str, nargs='*', help='File name to save seed to')

parserKeys = subparsers.add_parser('new-keys',  help="Create a random private/public keypair with an option to save it to file")
parserKeys.add_argument('output', metavar='output', type=str, nargs='*', help='File name to save keys to')

# ==============================================================================
#
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

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
# TODO: make search case-insensitive
def runMeta(args):
    esa = eversa()
    print(f"Showing all functions for contracts:")
    for contractName in args.contracts:
        print(f"")
        print(f"\"{contractName}\":")
        contract = esa.GetContract(contractName)
        for (name, func) in getmembers(contract, isfunction):
            if name == "esaUpdateInitData":
                continue
            if name == "deploy":
                name = "constructor"
            print(f"    {name}{signature(func)}")

# ==============================================================================
#
def getLibraryFunctions():
    functionList = []
    for (name, _func) in getmembers(sys.modules["eversa"], isfunction):
        functionList.append(name)
    return functionList

def getPyFilesList(dir: str):
    result = []
    for file in os.listdir(dir):
        # check only text files
        if file.endswith('.py'):
            result.append(file)
    return result

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio # free up some memory
        sys.stdout = self._stdout

def runTest(args):
    # 1. parse environment for eversa to run tests in
    esa = eversa(args.environment[0])

    # Force blockchain errors to raise exceptions
    esa.CONFIG.RAISE = True

    # 2. List all .py files in test directory
    pyTestFiles = getPyFilesList(os.path.join(esa.WORK_DIR, "tests"))
    pyToRun     = {}

    # 3. Import each file as a separate module
    for testFile in pyTestFiles:
        pyToRun[testFile] = []
        module = imp.load_source(f"esaTest_{testFile}", os.path.join(esa.WORK_DIR, "tests", testFile))
        pyToRun[testFile] = []

        functionsInEversa = getLibraryFunctions()

        for (name, _func) in getmembers(module, isfunction):
            if name in functionsInEversa:
                continue
            pyToRun[testFile].append(getattr(module, name))

    numModules  = 0
    numTestsOK  = 0
    numTestsNOK = 0
    for module in pyToRun:
        numModules += 1
        for function in pyToRun[module]:
            print(f"{bcolors.OKBLUE}Running {module}:{function.__name__}{bcolors.ENDC}:")
            try:
                with Capturing() as output:
                    function(esa)
                print(f"    {bcolors.OKGREEN}✓ OK{bcolors.ENDC}")
                numTestsOK += 1
            except BaseException as e:
                numTestsNOK += 1
                print(f"    {bcolors.FAIL}✗ ERROR!\n    {module}:{function.__name__} output:{bcolors.ENDC}\n")
                for line in output:
                    print(line)
                traceback.print_tb(e.__traceback__)
    print(f"\n{bcolors.OKBLUE}SUMMARY:{bcolors.ENDC} Files: {numModules}; {bcolors.OKGREEN}Tests OK: {numTestsOK}{bcolors.ENDC}; {bcolors.FAIL}Tests FAIL: {numTestsNOK}{bcolors.ENDC}")

# ==============================================================================
#
def runSeed(args):
    if len(args.output) == 0:
        phrase = generateRandomMnemonic()
        print(phrase)
        return
    else: 
        fileList = args.output
        for file in fileList:
            print(f"Saving random seed phrase to \"{file}\"...")
            phrase = generateRandomMnemonic()
            with open(file, "w") as f:
                f.write(phrase)

# ==============================================================================
#
def runKeys(args):
    if len(args.output) == 0:
        signer = generateRandomSigner()
        print(signer.keys.dict)
        return
    else: 
        fileList = args.output
        for file in fileList:
            print(f"Saving random keys to \"{file}\"...")
            signer = generateRandomSigner()
            saveSigner(file, signer)

# ==============================================================================
#
parserInit.set_defaults(func=runInit)
parserBuild.set_defaults(func=runBuild)
parserMeta.set_defaults(func=runMeta)
parserTest.set_defaults(func=runTest)
parserSeed.set_defaults(func=runSeed)
parserKeys.set_defaults(func=runKeys)

# ==============================================================================
# 
def main():
    args = parser.parse_args()
    if args.command is None:
        pass
    else:
        args.func(args)
