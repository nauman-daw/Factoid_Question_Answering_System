'''
   Copyright 2017 Indian Institute of Technology Madras
   (Authors: Nauman Dawalatabad, Krishnaraj, Jom Kuriakose)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import os
from POSTag import POSTag
from DParserWrapper import DParserWrapper
class NERWrapper:
	outFile = "tmp/ner.txt"
	tmpFile = "tmp/nertmp.txt"
	cmdPath = "stanford-ner-2015-12-09/ner.sh"
	cachedStopWords = []
	nerList = []
	posList = []
	def __init__(self):
		self.dPW=DParserWrapper()
		with open('./Conf/stop-word') as stopWds:
			for word in stopWds.readlines():
				tmp = word.strip().upper()
				if len(tmp)>0:
					self.cachedStopWords.append(tmp)

	def removestopwords(self,text):
		return ' '.join([word for word in text.split() if word.upper() not in self.cachedStopWords])

	
	def getNER(self,sentence):
		self.listTags = []
		self.nerList = []
		fout = open(self.outFile,"w")
		fout.write(sentence)
		fout.close()
		os.system(self.cmdPath + " "+ self.outFile + ">" + self.tmpFile)
		idx=1
		with open(self.tmpFile) as inpFile:
			for wordLabel in inpFile.readline().strip().split(' '):
				tmp = wordLabel.split('/')
				word = tmp[0]
				label = tmp[1]
				tmpPOS = POSTag(str(idx),label,word)
				self.nerList.append(tmpPOS)
				self.listTags.append(label)
				idx=idx+1
		self.posList,self.dependList = self.dPW.getParse(sentence)
		#for pos in self.posList:
		#	print pos
		return self.nerList

	def getDistinctTags(self):
		return self.listTags

	def getWordByTag(self, tags):
		retList = []
		for tag in tags:
			for pos in self.nerList: 
				if pos.pos==tag:
					if tag=='O': 
						if pos.word.upper() not in self.cachedStopWords:
							retList.append(pos)
					else:
						retList.append(pos)
		return retList

	def getKey(self,sentence):
		self.getNER(sentence)
		tmpresourcetags = set(self.getDistinctTags())-set(['O'])
		if len(tmpresourcetags)==0:
			return [],[]
		tagOrder =['PERSON','ORGANIZATION' ,'LOCATION']

		resourcetags = []
		for  tag in tagOrder:
			if tag in tmpresourcetags:
				resourcetags.append(tag)
				break

		resources =  self.getWordByTag(resourcetags)
		predicates = self.getWordByTag(['O'])
		resourceRet =''
		self.resourceList =[]
		self.predicateList =[]
		for resourcetag in resourcetags:
			tmpResource =''
			tmpresourcetag = []
			tmpresourcetag.append(resourcetag)
			for resource in  self.getWordByTag(tmpresourcetag):
				tmpResource = tmpResource + ' ' + resource.word
			self.resourceList.append(tmpResource.strip())
			
		for predicate in predicates:
			self.predicateList.append(predicate.word)

		return self.resourceList[0],' '.join(self.predicateList).strip()



if __name__ == '__main__':
	#questions = ["capital of United States of America","who is Sachin Tendulkar","I bank on you"]
	fin = open("tmpQues")
	questions=fin.readlines()
	for question in questions:
		NERW = NERWrapper()
		nerList = NERW.getNER(question)
		for pos in nerList:
			print pos
		predicateList,resourceList = NERW.getResourcePredicateList()
		print "Resource:"
		print resourceList
		print "Predicate:"
		print predicateList
		raw_input('a')
		
