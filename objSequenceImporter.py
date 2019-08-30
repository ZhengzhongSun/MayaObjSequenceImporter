# Orignial from https://mayapy.wordpress.com/2011/12/19/obj-sequence-importer-for-maya/
# Modified by Zhengzhong Sun

import maya.cmds as cmds

current_scene=cmds.ls(assemblies=True)

def selectDir():
	basicFilter = "*.obj"
	filename=cmds.fileDialog2(fileMode=4,ds=1, caption="Select Sequence",fileFilter=basicFilter)
	uniToStr=str(filename)
	global objList
	filePath=uniToStr.split("'")
	search=".obj"
	objList=[mesh for mesh in filePath if search in mesh]
	cmds.textScrollList(path, edit=True, append=objList)

def importer():
	objList.sort()
	for each in objList:
		loaded=cmds.file(each,i=True,dns=True)
	cmds.deleteUI('objwindow',window=True)
	getMeshes()

def loadWin():
	if cmds.window('objwindow',exists=True):
		cmds.deleteUI('objwindow',window=True)
	win=cmds.window('objwindow',title="Load Obj sequence",widthHeight=(250,450))
	cmds.columnLayout()
	cmds.text('Path to files')
	global path
	path=cmds.textScrollList(w=250)
	browseButton=cmds.button(label='browse',w=250,c='selectDir()')
	importButton=cmds.button(label='import',w=250,c='importer()')
	cmds.showWindow(win)

def getMeshes():
	newScene=cmds.ls(assemblies=True)
	meshList=[mesh for mesh in newScene if mesh not in current_scene]
	cmds.group(meshList,n="OBJ_GROUP")
	for i in range(len(meshList)):
		cmds.setKeyframe(meshList[i],attribute='visibility',value=0,t=0)
		cmds.setKeyframe(meshList[i],attribute='visibility',value=1,t=i+1)
		cmds.setKeyframe(meshList[i],attribute='visibility',value=0,t=i+2)

loadWin()
