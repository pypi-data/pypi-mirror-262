#File type: extension <Function> set
#By Junxiang H., 2023/06/30
#wacmk.com/cn Tech. Supp.

import os,re
#return Filesdir/Filename.type
def GetFiles(filedir=os.getcwd(),filetype=""):
	'''
	for root, dirs,files in os.walk(filedir,topdown=False):
		for file in files:
			if file.endswith(filetype):
				result+=(os.path.join(root,file),)
	'''
	i=0
	files=os.listdir(filedir)
	result=[]
	while True:
		file=f"data.{i if i >999 else f'0{i}' if i>99 else f'00{i}' if i>9 else f'000{i}'}.{filetype}"
		if file in files:
			result.append(os.path.join(filedir,file))
			i+=1
		else:
			break
	return result

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("Testing Function:", GetFiles)
	print("Testing Result:", GetFiles(filetype="py"))