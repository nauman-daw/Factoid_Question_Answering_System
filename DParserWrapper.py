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
import xml.etree.ElementTree as ET
from POSTag import POSTag
from DependencyTAG import DependencyTAG

class DParserWrapper:
	outFile = "tmp/question.txt"
	cmdPath = "./stanford-parser-full-2015-12-09/lexparser_xml.sh"
	def __init__(self):
		a=1

	def getParse(self,question):
		posList = []
		dependList = []
		fout = open(self.outFile,"w")
		fout.write(question)
		fout.close()
		os.system(self.cmdPath + " "+ self.outFile)
		tree = ET.parse(self.outFile +'.stp')
		root = tree.getroot()
		for words in root.iter('words'):
			for word in words.iter('word'):
				idx = word.attrib['ind']
				pos = word.attrib['pos']
				wordText = word.text
				tmpPOS = POSTag(idx,pos,wordText)
				posList.append(tmpPOS)
		for dependencies in root.iter('dependencies'): 
			for dep in dependencies.iter('dep'):
				typeRel = dep.attrib['type']
				for governor in dep.iter('governor'):
					govIdx = governor.attrib['idx']
					govName =  governor.text
				for dependent in dep.iter('dependent'):
					depIdx = dependent.attrib['idx']
					depName =  dependent.text
				dependList.append(DependencyTAG(typeRel,govName,govIdx,depName,depIdx))
		return posList,dependList
			

		
		
if __name__ == '__main__':
	question = "what is the capital of USA"
	question = question.lower()
	dPW=DParserWrapper()
	posList,dependList = dPW.getParse(question)
	for pos in posList:
		print pos
	for dep in dependList:
		print dep
