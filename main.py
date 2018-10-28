from lib import *

if __name__ == '__main__':
    path = "/media/administrateur/C29EAD659EAD53291/Documents/git_projects/PyqtBaseAppGenerator/data/"
    testspath = "/media/administrateur/C29EAD659EAD53291/Documents/git_projects/PyqtBaseAppGenerator/testprojects/"
    filename = "test.pyqtappscheme"

    p = PyqtBaseAppGenerator(AppInfos(path + filename))
    p.createProject(testspath)