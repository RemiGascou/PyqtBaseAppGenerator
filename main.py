from lib import *

if __name__ == '__main__':
    path = "D:\\Projets GIT\\#Python Projects - GIT\\PyqtBaseAppGenerator/data/"
    testspath = "D:\\Projets GIT\\#Python Projects - GIT\\PyqtBaseAppGenerator/testprojects/"
    filename = "test.pyqtappscheme"

    p = PyqtBaseAppGenerator(AppInfos(path + filename))
    p.createProject(testspath)