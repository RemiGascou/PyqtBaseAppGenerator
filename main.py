#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PyqtBaseAppGenerator -> Main

Author: Remi GASCOU
Last edited: October 2018
"""

from lib import *

if __name__ == '__main__':
    path = "D:\\Projets GIT\\#Python Projects - GIT\\PyqtBaseAppGenerator/data/"
    testspath = "D:\\Projets GIT\\#Python Projects - GIT\\PyqtBaseAppGenerator/testprojects/"
    filename = "test" + ".pyqtappscheme"
    if filename.endswith(".pyqtappscheme"):
        a = AppInfos(path + filename)
        p = PyqtBaseAppGenerator(a)
        p.createProject(testspath)
