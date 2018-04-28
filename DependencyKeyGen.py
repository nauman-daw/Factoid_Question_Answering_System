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
import string
from POSTag import POSTag
from DependencyTAG import DependencyTAG
from DParserWrapper import DParserWrapper
import sys


class DependencyKeyGen:
	def __init__(self):
		self.dPW=DParserWrapper()

	def getKey(self,question):
		key1 ='unknown'
		key2 ='unknown'
		posList,dependList = self.dPW.getParse(question)
		Types = ''
		typeList=[]
		wrd1=[]
		wrd2=[]
		tmp=[]
		
		questionWords = []
		listOfList = []
		a_list = []
		for i in range(0,len(dependList)):
			dependency = dependList[i]
			rel = dependency.typeRel
			gov = dependency.gov # gov is first element
			dep = dependency.dep # dep is second element
			if  'nmod' in rel: # making it generic
				rel = 'nmod'

			typeList.append(rel)
			wrd1.append(gov)
			wrd2.append(dep)

			a_list = [rel , gov , dep]
			listOfList.append( (list(a_list), a_list[0]) )	 # NOT needed 
			print( a_list  )


		c_amod = typeList.count('amod')
		c_compound = typeList.count('compound')


		question = question.lower() # making it lower only after PARSING
		questionWords = list(question)
		

		if "nmod" in typeList or c_amod > 1  or c_compound > 1: # or "nmod:in" in typeList or "nmod:of" in typeList or "nmod:at" in typeList:
			if "nmod" in typeList:
				key1= wrd2[typeList.index('nmod')]  	#dependList[typeList.index('nmod:of')].gov
				key2= wrd1[typeList.index('nmod')] 	#dependList[typeList.index('nmod:of')].dep

			#print ("RESOURCE: " +key1, "PROP: "+key2)
			#flag = 0 # flag is to track if it has TWO ADJECTIVEs


			if 'amod' in typeList : # If key 2 ADJECTIVE (It cannot be NOUN)
				key2 = wrd2[typeList.index('amod')] + ' ' + wrd1[typeList.index('amod')]	

				if c_amod > 1 : # Highly unlikely

					print ('2 Ajective Modifiers found!')
					if 'nsubj' in typeList:
						wrdAtNsubj = wrd2[typeList.index('nsubj')]
				
					else:	
						if 'nsubjpass' in typeList:
							wrdAtNsubj = wrd2[typeList.index('nsubjpass')]
						else:
							wrdAtNsubj = 'unknown'	
			
					if wrdAtNsubj == 'unknown':  ## If Subject is Absent in the Question
						print ('Subject and passive subject are NOT present in Question!')
						key1 = 'unknown'
						key2 = 'unknown'

	
					indices = [i for i, x in enumerate(typeList) if x == 'amod' ] 
					print (indices)				

					for j in indices:
						if wrd1[j] == wrdAtNsubj:
							key2 = wrd2[j] + ' ' + wrd1[j]
						else:
							key1 = wrd2[j] + ' ' + wrd1[j]
		
					print (key1, key2)		
			

			if 'compound' in typeList : # this can b mostly NOUN PART 
				key1 = wrd2[typeList.index('compound')] + ' ' + wrd1[typeList.index('compound')] # Assuming it is KEY1 => Resource		

				if c_compound > 1: #   small case united states <<>>
	
					print('2  Compound words found!')	
					if 'nsubj' in typeList:
						wrdAtNsubj = wrd2[typeList.index('nsubj')] # this may NOT always be the case
					else:
						if 'nmod' in typeList:
							wrdAtNsubj = wrd2[typeList.index('nmod')]
						else:
							if 'root' in typeList:
								wrdAtNsubj =  wrd2[typeList.index('root')]
							else:
								wrdAtNsubj = 'unknown' 
				
					indices = [i for i, x in enumerate(typeList) if x == 'compound' ]    
					print (indices)                          
					for j in indices:
					        if wrd1[j] == wrdAtNsubj:
					                key2 = wrd2[j] + ' ' + wrd1[j]
					        else:
					                key1 = wrd2[j] + ' ' + wrd1[j]


		else:
			if 'nsubj' in typeList:
				key1 = wrd2[typeList.index('nsubj')]
				key2 = 'description'
			if 'advmod' in typeList:
				key2 = wrd1[typeList.index('advmod')]

			if 'nsubjpass' in typeList :
				if 'nsubj' not in typeList: # for boundary checks
		                        key1 = wrd2[typeList.index('nsubjpass')]
		                        key2 = wrd1[typeList.index('nsubjpass')] # 'description'
					print (key1, key2)


			if 'amod' in typeList: # If key 2 ADJECTIVE (It cannot be NOUN)
				key2 = wrd2[typeList.index('amod')] + ' ' + wrd1[typeList.index('amod')]

			if 'compound' in typeList: # this can b both either KEY1 or KEY2
				key1 = wrd2[typeList.index('compound')] + ' ' + wrd1[typeList.index('compound')] # Assuming it is KEY1 => Resource  


			if question.split()[0].lower() == 'where':
				key2 =  key2 + ' place'
			else:
				if question.split()[0].lower() == 'when':
					key2 =  key2 + ' date'
				if question.split()[0].lower() == 'who':
                                        key2 = 'occupation'
				if question.split()[0].lower() == 'what':
					key2 = 'abstract'
				if question.split()[0].lower() == 'how':
                                        key2 = 'abstract'


			if 'located' in questionWords or 'situated' in questionWords:
				key2 = 'location'

		#print ('\nKEY1 (Resource) ==> ' + key1)
		#print ('KEY2 (Property) ==> ' + key2)
		#print('\n')

		return key1,key2

		''' PARSE TREE (NOT REQUIRED)
		WORD=[]
		POS =[]
		for posItem in posList:
			pos = posItem.pos
			word = posItem.word
			POS.append(pos)
			WORD.append(word)
			#print word,pos
		'''

	

if __name__ == '__main__':
	LIST=sys.argv[1]
	dpKG = DependencyKeyGen()
	with open(LIST) as f:
		for line in f:
			key1,key2=dpKG.getKey(line)
			print ('\nIN MAIN KEY1 (Resource) ==> ' + key1)
	                print ('IN MAIN KEY2 (Property) ==> ' + key2)
        	        print('\n')





