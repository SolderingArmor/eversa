#!/usr/bin/env python3

# ==============================================================================
# 
import json
from   tonclient.client import *
from   tonclient.types  import *

# ==============================================================================
# 
class EsaConfig(object):
    def __init__(self, target: str):
        self.EVERDEV       = ""
        self.SOURCE_DIR    = ""
        self.BIN_DIR       = ""
        self.VERBOSE       = False
        self.NAME          = ""
        self.ENDPOINTS     = [""]
        self.WORKCHAIN     = 0
        self.GIVER         = ""
        self.GIVER_ENABLED = False
        self.PHRASE        = ""

        # TODO: check if config exists and give a graceful error throw

        with open('.config.json') as jsonConfig:
            config = json.load(jsonConfig)

            # Project-wide config
            self.EVERDEV       = config["everdev"]
            self.SOURCE_DIR    = config["source_dir"]
            self.BIN_DIR       = config["bin_dir"]
            self.VERBOSE       = config["verbose"]
            self.GIVER_ENABLED = target in config["giver_enabled"]

            # Target-wide config
            for configElm in config["configs"]:
                if configElm["name"] == target:
                    self.NAME       = configElm["name"]
                    self.ENDPOINTS  = configElm["endpoints"]
                    self.WORKCHAIN  = configElm["workchain"]
                    self.GIVER      = configElm["giver"]
                    self.PHRASE     = configElm["phrase"]
                    return
            raise BaseException(f"Invalid configuration target: {target}!\nPlease use valid configuration name from .config.json!")

# ==============================================================================
# 
