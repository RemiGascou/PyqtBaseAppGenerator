#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PyqtBaseAppGenerator -> PBAGenerator

Author: Remi GASCOU
Last edited: October 2018
"""

"""
Syntax : python main.py
"""

import os,sys
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

class PyqtBaseAppGenerator(object):
    """docstring for PyqtBaseAppGenerator."""
    def __init__(self, appinfos:AppInfos):
        super(PyqtBaseAppGenerator, self).__init__()
        self.appinfos   = appinfos
        self.path       = ""
        self.verbose    = False

    def createProject(self, path, verbose=False):
        self.path       = path
        self.verbose    = verbose
        if not os.path.exists(self.path + self.appinfos.get_appname()):
            self.path = self.path + self.appinfos.get_appname()
            os.mkdir(self.path)
        else :
            k = 0
            while os.path.exists(self.path + self.appinfos.get_appname() + "_" + str(k)): k+=1
            self.path = self.path + self.appinfos.get_appname() + "_" + str(k)
            os.mkdir(self.path)

        os.mkdir(self.path + "/lib")
        f = open(self.path + "/lib/" + "__init__.py", 'w')
        f.write("""# -*- coding: utf-8 -*-\n\nfrom lib."""+ self.appinfos.get_mainappname() + """ import *\nfrom lib.ui import *\nfrom lib.core import *\n""")
        f.close()

        os.mkdir(self.path + "/lib" + "/meta")

        os.mkdir(self.path + "/lib" + "/ui")
        f = open(self.path + "/lib/ui/" + "__init__.py", 'w')
        f.write("""# -*- coding: utf-8 -*-\n\nfrom lib.ui.widgets import *\nfrom lib.ui.windows import *\n""")
        f.close()

        os.mkdir(self.path + "/lib" + "/ui" + "/widgets")
        f = open(self.path + "/lib/ui/widgets/" + "__init__.py", 'w')
        f.write("""# -*- coding: utf-8 -*-\n\n""")
        f.close()

        os.mkdir(self.path + "/lib" + "/ui" + "/windows")
        f = open(self.path + "/lib/ui/windows/" + "__init__.py", 'w')
        f.write("""# -*- coding: utf-8 -*-\n\n""")
        f.close()

        os.mkdir(self.path + "/lib" + "/core")
        f = open(self.path + "/lib/core/" + "__init__.py", 'w')
        f.write("""# -*- coding: utf-8 -*-\n\n__all__ = [\n\t'""" + self.appinfos.get_mainappname()+"Infos" + """'\n]\n\n""")
        f.close()

        # Gen files
        self._genMain()
        self._genAppClass()
        self._genAppInfos()

    def _genMain(self):
        mainfile = """# -*- coding: utf-8 -*-\n\nimport os, sys\n\nfrom PyQt5.QtWidgets import *\nfrom PyQt5.QtGui import *\nfrom PyQt5.QtCore import *\n\nfrom lib import *\n\n"""
        mainfile += """if __name__ == \"\"\"__main__\"\"\":\n\tapp = QApplication(sys.argv)\n\tex = """ + self.appinfos.get_appname() + """()\n\tsys.exit(app.exec_())\n"""
        f = open(self.path + "/main.py", 'w')
        f.write(mainfile)
        f.close()

    def _genAppInfos(self):
        _fileAppInfos = """# -*- coding: utf-8 -*-\n\ndef get_name():\n\treturn '""" + self.appinfos.get_appname() + """'\n\n\ndef get_version():\n\treturn get_version_name() + " " + get_version_tag()\n\ndef get_version_tag():\n\treturn "v.0.0.1"\n\ndef get_version_name():\n\treturn "Alpha"\n\ndef get_credits():\n\treturn u'\\u00A9' + ' """ + self.appinfos.get_author() + """'"""
        f = open(self.path + "/lib/core/" + self.appinfos.get_mainappname() + "Infos.py", 'w')
        f.write(_fileAppInfos)
        f.close()

    def _genAppClass(self):
        if self.verbose == True:
            print("Creating" + "/lib/" + self.appinfos.get_mainappname() + ".py")

        appclass = self.appinfos.gen_header(self.appinfos.get_mainappname()) + "\n"

        _classInit = """class """ + self.appinfos.get_mainappname() + """(QMainWindow):\n\t\"\"\"docstring for """ + self.appinfos.get_mainappname() + """.\"\"\"\n\tdef __init__(self, parent=None):\n\t\tsuper(""" + self.appinfos.get_mainappname() + """, self).__init__()\n\t\tself.title        = """ + self.appinfos.get_mainappname() + """Infos.get_name() + " - " + """ + self.appinfos.get_mainappname() + """Infos.get_version_tag()\n\t\tself.margin_left  = 200\n\t\tself.margin_top   = 200\n\t\tself.width        = 800\n\t\tself.height       = 600\n\t\tself._initUI()\n\n"""
        appclass += _classInit

        #_initUI
        _initUI = """\tdef _initUI(self):\n\t\tself.setWindowTitle(self.title)\n\t\t#self.setWindowIcon(QIcon('lib/meta/ico.png'))\n\t\tself.setGeometry(self.margin_left, self.margin_top, self.width, self.height)\n\t\tself.setFixedSize(self.size())\n\t\tself.setAttribute(Qt.WA_DeleteOnClose)\n\t\tself._initMenus()\n\t\tself.show()\n\n"""
        appclass += _initUI

        if len (self.appinfos.menus) != 0:
            #_initMenus
            _initMenus = """\tdef _initMenus(self):\n\t\tmainMenu = self.menuBar()\n"""
            _windowsHandlers = """# *------------------------------Windows Handlers----------------------------- *\n\n"""

            for menu in self.appinfos.menus:
                _initMenus += """\t\tmenu""" + menu[0] + """  = mainMenu.addMenu(\'""" + menu[0] + """\')\n"""
            for actionbutton in self.appinfos.menus[0][1]:
                self._genWindow(actionbutton.replace(" ", "").lower())
                _initMenus += """\t\t""" + actionbutton.replace(" ", "").lower() + """Button = QAction(\'""" + actionbutton + """\', self)\n"""
                _initMenus += """\t\t""" + actionbutton.replace(" ", "").lower() + """Button.triggered.connect(self.start_""" + actionbutton.replace(" ", "").lower() + """Window)\n"""
                _initMenus += """\t\tmenu""" + self.appinfos.menus[0][0] + """.addAction(""" + actionbutton.replace(" ", "").lower() + """Button)\n"""
                _windowsHandlers += """\tdef start_""" + actionbutton.replace(" ", "").lower() + """Window(self):\n\t\tself.w""" + actionbutton.replace(" ", "").lower() + """Window = """ + actionbutton.replace(" ", "").lower() + """Window()\n\t\tself.w""" + actionbutton.replace(" ", "").lower() + """Window.show()\n\n"""
            _initMenus += """\t\tmenu""" + self.appinfos.menus[0][0] + """.addSeparator()\n\t\texitButton = QAction('Exit', self)\n\t\texitButton.setShortcut('Ctrl+Q')\n\t\texitButton.setStatusTip('Exit application')\n\t\texitButton.triggered.connect(self.close)\n\t\tmenu""" + self.appinfos.menus[0][0] + """.addAction(exitButton)\n\n"""

            for menu in self.appinfos.menus[1:]:
                for submenu in menu[1]:
                    self._genWindow(submenu.replace(" ", "").lower())
                    _initMenus += """\t\t""" + submenu.replace(" ", "").lower() + """Button = QAction(\'""" + actionbutton + """\', self)\n"""
                    _initMenus += """\t\t""" + submenu.replace(" ", "").lower() + """Button.triggered.connect(self.start_""" + submenu.replace(" ", "").lower() + """Window)\n"""
                    _initMenus += """\t\tmenu""" + menu[0] + """.addAction(""" + submenu.replace(" ", "").lower() + """Button)\n"""
                    _windowsHandlers += """\tdef start_""" + submenu.replace(" ", "").lower() + """Window(self):\n\t\tself.w""" + submenu.replace(" ", "").lower() + """Window = """ + submenu.replace(" ", "").lower() + """Window()\n\t\tself.w""" + submenu.replace(" ", "").lower() + """Window.show()\n\n"""
                _initMenus += """\n"""

            appclass += _initMenus
            appclass += _windowsHandlers

        appclass += """\n\nif __name__ == '__main__':\n\tapp = QApplication(sys.argv)\n\tex = """ + self.appinfos.get_mainappname() + """()\n\tsys.exit(app.exec_())\n"""

        f = open(self.path + "/lib/" + self.appinfos.get_mainappname() + ".py", 'w')
        f.write(appclass)
        f.close()

    def _genWindow(self, windowname):
        if not windowname.endswith("Window"): windowname = windowname + "Window"

        if self.verbose == True: print("Creating" + "/lib/ui/windows/" + windowname + ".py") #verbose

        #Append import to __init__
        f = open(self.path + "/lib/ui/windows/" + "__init__.py", 'a')
        f.write("""from lib.ui.windows.""" + windowname + """ import *\n""")
        f.close()

        _windowData = self.appinfos.gen_header(windowname) + "\n"

        _windowData += """class """ + windowname + """(QWidget):\n\tdef __init__(self, parent=None):\n\t\tsuper(""" + windowname + """, self).__init__()\n\t\tself.title = '""" + windowname + """'\n\t\tself.marginleft = 0\n\t\tself.margintop  = 0\n\t\tself.width      = 300\n\t\tself.height     = 200\n\t\tself._initUI()\n\t\tself.show()\n\n"""
        _windowData += """\tdef _initUI(self):\n\t\tself.setWindowTitle(self.title)\n\t\tself.setAttribute(Qt.WA_DeleteOnClose)  #Kill application on close\n\t\tself.setGeometry(self.marginleft, self.margintop, self.width, self.height)\n\t\tself.label = QLabel("<b>" + """ + self.appinfos.get_mainappname() + """Infos.get_name() + " " + """ + self.appinfos.get_mainappname() + """Infos.get_version() + " </b><br><br>" + """ + self.appinfos.get_mainappname() + """Infos.get_credits(), self)\n\t\tself.label.setAlignment(Qt.AlignCenter)\n\t\tself.layout = QGridLayout()\n\t\tself.layout.addWidget(self.label, 0, 0)\n\t\tself.setLayout(self.layout)\n\n"""
        _windowData += """\n\nif __name__ == '__main__':\n\tapp = QApplication(sys.argv)\n\tex = """ + windowname + """()\n\tsys.exit(app.exec_())\n"""

        f = open(self.path + "/lib/ui/windows/" + windowname + ".py", 'w')
        f.write(_windowData)
        f.close()


if __name__ == '__main__':
    ext     = ".pyqtappscheme"
    if len(sys.argv) != 3:
        _help = """ PyqtBaseAppGenerator v1.0.1 :\n\n"""
        _help += """       Supported files are *""" + ext + """\n\n"""
        _help += """       Usage : python3  main.py  path/to/filename""" + ext + """  path/to/projects/directory/\n"""
        print(_help)
    else:
        pathtofilename = sys.argv[1]
        pathtoexport   = sys.argv[2]
        print("\npathtofilename = ",pathtofilename)
        print("pathtoexport   = ",pathtoexport,"\n")
        if pathtofilename.endswith(ext):
            a = AppInfos(pathtofilename)
            p = PyqtBaseAppGenerator(a)
            p.createProject(pathtoexport, verbose=True)
        else :
            print("Unsupported file. Supported files are *" + ext)
