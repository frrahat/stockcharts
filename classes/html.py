#!/usr/bin/python
import os

class html:

	def __init__(self, name):
		# Need to initilize the file pointer here in order to avoid the problem with appending. If we use the same filepointer here it will be automatically initialized here

		self.name = name
		self.createDirectory("Results")


	def  getHeader(self, header):
		 print("Adding Header")
		 header=self.openFile("html/header.txt")
		 print("Opening the file...")
		 target = open ("Results/xeg.html", 'w')
		 print(header)
		 target.writelines(header)
		 target.write('powerpork...............')
		 target.writelines(['\n \n And a fifth', 'And also a sixth.'])
		 
		 target.write( '<img src="images/sunset.gif" height="100%" width="100%">')



		 print("Creating the footer")
		 footer = self.openFile("html/footer.txt") 

		 target.writelines(footer)
		 target.close()

	def addImageToHtmlBody(self,image ):
		print("Adding the image to body")
	
	def addBody(self, NameOfImage):
		print("Adding the content of the body")

	def addGraph(self, image, tab):
		print("Testing addgraph")

	def createDirectory(self, directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except Exception as e:
			raise e
		
	def deleteFiles(self, subFolderName):
		print("Testing addgraph")

	def createFile(self,subFolderName, FileName):
		print("Testing addgraph")

	def addPrice(self, pricearray):
		print("Testing addgraph")
	

	def openFile(self, filelocationAnaName):
		# open a file and return the content of the file 
		try:
			print("Opening the", filelocationAnaName)
			file = open(filelocationAnaName)
			fileContent=file.read()
			file.close()
			return fileContent
		except IOError: 
		   print("Error: File does not appear to exist.")
		return 0 


	def addTab(self, Ticker):
		print("Testing addgraph")






