#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PyqtBaseAppGenerator -> AppInfos

Author: Remi GASCOU
Last edited: October 2018
"""

import json
import datetime

class AppInfos(object):
    """docstring for AppInfos."""
    def __init__(self, path=""):
        super(AppInfos, self).__init__()
        self.appname    = "NewApp"
        self.data       = {}
        self.hasmenu    = 0
        self.menus      = []
        self.author     = "John Doe"
        if path != "":
            self.loadFromJSONFile(path)

    def get_appname (self):
        return self.appname

    def set_appname (self, appname):
        if appname != "": self.appname = appname.replace(" ", "")

    def get_hasmenu (self):
        return self.hasmenu

    def set_hasmenu (self, hasmenu):
        self.hasmenu = hasmenu

    def get_author (self):
        return self.author

    def set_author (self, author):
        self.author = author

    def add_menu(self, menuname, menuentries):
        if self.hasmenu == False:
            self.hasmenu = True
        self.menus.append([menuname, menuentries])

    def exists_menu(self, menuname):
        for e in self.menus:
            if e[0] == menuname:
                return e
            else :
                return None

    def get_mainappname(self):
        if self.appname.endswith("App"):
            return self.appname
        else :
            return self.appname + "App"

    def gen_header(self, file):
        header = """#!/usr/bin/python3\n# -*- coding: utf-8 -*-\n\n\"\"\"\n"""
        header += self.appname + """ -> """ + file + """\n\n"""
        header += """Author: """ + self.author + """\n"""
        header += """Last edited: """ + datetime.date.today().strftime("%B")[0].upper() + datetime.date.today().strftime("%B")[1:] + " " + datetime.date.today().strftime("%Y") + """\n\"\"\"\n\n"""
        header += """from PyQt5.QtWidgets import *\nfrom PyQt5.QtGui import *\nfrom PyQt5.QtCore import *\n\n"""
        header += """from lib.ui import *\nfrom lib.core import *\n"""
        return header

    def loadFromJSONFile(self,path,log = False):
        if log == True:
            print("Opening file ",path,"...")
            f = open(path,'r')
            print("Reading file ",path,"...")
            lignes  = ''.join([e for e in f.readlines() if type(e) == str])
            print("Closing file ",path,"...")
            f.close()
            print("Parsing JSON file ...")
            self.data = json.loads(lignes)
            print("Done !")
        else :
            f = open(path,'r')
            lignes = ''.join([e for e in f.readlines() if type(e) == str])
            f.close()
            self.data = json.loads(lignes)
        for menu in self.data["menus"]:
            menuname, menuentries = "", []
            menuname = self.data["menus"][menu]['menuname']
            for entry in self.data["menus"][menu]['entries']:
                menuentries.append(self.data["menus"][menu]['entries'][entry])
            self.menus.append([menuname, menuentries])



    def __str__(self):
        sdata = """appname : """ + self.appname + """\n"""
        for menu in self.menus:
            sdata += """menu : """ + menu[0] + """\n"""
            for e in menu[1]:
                sdata += " => " + e + """\n"""
        return sdata[:-1]
