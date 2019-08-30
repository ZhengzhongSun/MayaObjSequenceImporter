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
	namearray = []
	for each in objList:
		loaded=cmds.file(each,i=True,dns=True)
		label1 = each.rfind("/")
		label2 = each.rfind(".")
		file_name = each[label1+1:label2]
		label0 = each[0:label1].rfind("/")
		folder_name = each[label0+1:label1]
		# use the folder name and file name to be the model name in maya
		model_name = folder_name+"_"+file_name
		print(model_name)
		cmds.select("Mesh")
		cmds.rename("{}".format(model_name))
		namearray.append("{}".format(model_name))
	getMeshes(namearray)
	
def clear():
	objList = []
	cmds.textScrollList(path, edit=True, removeAll=True)

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
	clearButton=cmds.button(label='clear',w=250,c='clear()')
	cmds.showWindow(win)

def getMeshes(namearray):
	global groupid
	newScene=cmds.ls(assemblies=True)
	meshList=namearray
	groupname = "OBJ_GROUP{}".format(groupid)
	print(meshList)
	cmds.group(meshList,n=groupname)
	
	for i in range(len(meshList)):
		cmds.setKeyframe(meshList[i],attribute='visibility',value=0,t=0)
		cmds.setKeyframe(meshList[i],attribute='visibility',value=1,t=i+1)
		cmds.setKeyframe(meshList[i],attribute='visibility',value=0,t=i+2)
		
	groupid += 1
	

groupid = 0
loadWin()
