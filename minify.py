#!/usr/bin/env python

# This class is used to minify JS and CSS files. 
# @author Nitesh Morajkar

import getopt, sys, string, re, os

#{{ Prints Usage of this script
def Usage():
	print """Usage python filename [options...]
Options:
-f --fileStack : Js and css files(comma separated) with absolute path eg: /home/demo/st.js,/home/demo/ss.css
-o --outputDir : Output directory where files are to be stored
-h --help      : Display help contents\n"""
	sys.exit(1)
#}}	

#{{ Gets command line arguments
class GetArguments:

    def __init__(self, args):
        self.args = args

    def GetArgs(self):
        try:
            self.options, remainder = getopt.getopt(self.args, 'f:o:h', ['fileStack=', 'outputDir=', 'help'])
            #print self.options
            return self.parseArgs()
        except getopt.GetoptError:
            Usage()

    def parseArgs(self):
		for opt, arg in self.options:
			if opt in ('-f', '--fileStack'):
				fileStack = arg
			elif opt in ('-o', '--outputDir'):
				outputDir = arg
			elif opt in ('-h', '--help'):
				Usage()

		return {'fileStack': fileStack, 'outputDir': outputDir}
#}}

#{{ Validates command line arguments
class ValidateArguments:

	def __init__(self, argsList):
		self.argsList = argsList

	def validateArgs(self):
		list = self.argsList
		if list['fileStack'] == '' or list['outputDir'] == '':
			return 0
		return 1
	
	#{{ Validates file names
	def validateFiles(self, fileList):
		for files in fileList:
			files = string.strip(files)
			if files != '':
				if re.match('([A-Za-z0-9.-_/:])+\.(js|css)$', files) == None:
					print "Invalid filename '" + files + "'"
					sys.exit(1)
			if self.checkFileExists(files) == 0:
				print "Invalid file path '"+ files + "'"
				sys.exit(1)
		return 1
	#}}
	
	#{{ Checks if file exists
	def checkFileExists(self, fileName):
		return os.path.isfile(fileName)
	#}}
	
	#{{ Checks if directory exists
	def checkDirExists(self):
		return os.path.exists(self.argsList['outputDir'])
	#}}
#}}

#{{ Minifies JS and CSS scripts
class Minify:
	def __init__(self, filesList, outputDir):
		self.filesList = filesList
		self.outputDir = outputDir
		self.yuiCompressorPath = "/home/yuicompressor-2.4.7.jar"
	
	#{{ Compress JS and CSS files
	def compress(self, fileName):
		print "Minifying " + fileName + "...\n"
		jsCssFlag = self.getJsCssFlag(fileName)
		file = self.getFileName(fileName)
		cmd = "java -jar \"" + self.yuiCompressorPath + "\" \"" + fileName + "\" --type \"" + jsCssFlag + "\" -o \"" + self.outputDir + "/" + file + "\""
		#print cmd + "\n"
		#sys.exit()
		op = os.popen(cmd)
		print "Minified " + fileName + "\n"
		
	def getJsCssFlag(self, fileName):
		if re.search('([A-Za-z0-9.-_/:])+\.js$', fileName):
			return "js"
		elif re.search('([A-Za-z0-9.-_/:])+\.css$', fileName):
			return 'css'
	
	#{{ triggers Compress
	def minify(self):
		for files in self.filesList:
			self.compress(string.strip(files))
	#}}
	
	def getFileName(self, file):
		startIndex = file.rfind("\\")
		length = len(file)
		if startIndex != -1:
			return file[startIndex:length]
		else:
			return file
#}}

argv = sys.argv[1:]
getArgsObj = GetArguments(argv)
ArgumentList = getArgsObj.GetArgs()

validateArgsObj = ValidateArguments(ArgumentList)

if validateArgsObj.validateArgs():
    filesList = string.split(ArgumentList['fileStack'], ',')
    if validateArgsObj.validateFiles(filesList):
		minifyObj = Minify(filesList, ArgumentList['outputDir'])
		minifyObj.minify()
    else:
        print Usage()
else:
    Usage()
