#雑用を行うクラス
#多分staticに呼び出すのが正だと思うが、時間があったら直します。

import pathlib
import os

class Util:
    def __init__(self):
        envTxt = "..\env.txt"
        p_rel = pathlib.Path(envTxt)
        self.prop = {}
        txt = open(p_rel.resolve(), "r", encoding="utf-8")
        readline = txt.readlines()
        for line in readline:
            if(line.strip() == ""):
                continue
            
            if(line[0:1] == "#"):
                continue

            self.prop[line.split("=")[0]] = line.split("=")[1].strip()


#    @staticmethod
    def readProp(key):
        return prop[key]
    
    def getWorkDir(self):
        return self.prop["workDir"]
