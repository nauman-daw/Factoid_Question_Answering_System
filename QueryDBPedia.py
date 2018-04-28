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

#!/usr/bin/python

########################################################################################
# Code to query DBpedia using Resource and Property words
########################################################################################

# import sys
from SPARQLWrapper import SPARQLWrapper, JSON # query DBpedia
import gensim # word2vec
import urllib2 # Catch HTTP Error

########################################################################################
# Class: QueryDBPedia
########################################################################################

class QueryDBPedia:

	def __init__(self):
		self.printFlag = False
		print "Loading Word2Vec Model..."
		self.model = gensim.models.Word2Vec.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

########################################################################################
# Code to query DBpedia using SPARQL query
########################################################################################

	def getDataQuery(self,theQuery):
		#sparql = SPARQLWrapper("http://wikidata.dbpedia.org/sparql")
		#sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setReturnFormat(JSON)
		sparql.setQuery(theQuery)
		try:
			queryResult = sparql.query().convert()
			return queryResult
		except urllib2.HTTPError as err:
			if err.code == 502:
				print "HTTP Error 502: Bad Gateway: Server under maintainance"
			else:
				raise
	        	
	def getDataQueryLive(self,theQuery):
		#sparql = SPARQLWrapper("http://wikidata.dbpedia.org/sparql")
		sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
		#sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setReturnFormat(JSON)
		sparql.setQuery(theQuery)
		try:
			queryResult = sparql.query().convert()
			return queryResult
		except urllib2.HTTPError as err:
			if err.code == 502:
				print "HTTP Error 502: Bad Gateway: Server under maintainance"
			else:
				raise

########################################################################################
# Code to retrieve DBpedia resource link from Resource word
########################################################################################

	def getResourceLink(self,resourceWord):
		query1 = """SELECT ?s WHERE {{?s rdfs:label \""""+ resourceWord +"""\"@en ;a owl:Thing .}UNION{?altName rdfs:label \""""+ resourceWord +"""\"@en ;dbo:wikiPageRedirects ?s .}}"""
		liveFlag = 0
		resourceSTR = self.getDataQuery(query1)
		if self.printFlag == True:
			print resourceSTR
		if resourceSTR["results"]["bindings"] == []:
			liveFlag = 1
			resourceSTR = self.getDataQueryLive(query1)
		if resourceSTR["results"]["bindings"] == []:
			print "Couldn't retrieve Resource link"
		else:
			resourceLink = []
			for resourceJSON in resourceSTR["results"]["bindings"]:
				resourceLink.append(resourceJSON["s"]["value"])
			if len(resourceLink) > 1:
				print "More than one resource selected. Have to find some method to select between these"
				for index in range(len(resourceLink)):
					print resourceLink[index]
				print "For now, returning the first resource"
				return resourceLink[0], liveFlag
			else:
				return resourceLink[0], liveFlag

########################################################################################
# Code to split at capitals
########################################################################################

	def split_on_uppercase(self, string, keep_contiguous=True):
		try:
			pos = []
			for i, e in enumerate(string):
				if e.isupper() and (not keep_contiguous or i and string[i-1].islower() or len(string) > (i + 1) and string[i + 1].islower()):
					pos.append(i)
			if pos[0]:
				pos.insert(0, 0)
			i = -1
			parts = [string[pos[i]: pos[i + 1]] for (i, p) in enumerate(pos[:-1])]
			parts.append(string[pos[i + 1]:])
			return parts
		except IndexError:
			return [string]

########################################################################################
# Similarity measuring using word2vec
########################################################################################

	def word2vecSim(self,Phrase1,Phrase2):
		try:
			Phrase1Together = ''.join(Phrase1.split(' ')).lower()
			Phrase2Together = ''.join(self.split_on_uppercase(Phrase2)).lower()
			try:
				similarityTogether = self.model.similarity(Phrase1Together, Phrase2Together)
			except KeyError:
				if self.printFlag == True:
					print "Not Found! Together " + Phrase2
				similarityTogether = 0
			Phrase1List = Phrase1.split(' ')
			Phrase2List = self.split_on_uppercase(Phrase2)
			similaritySeparate = 0
			for i in range(len(Phrase1List)):
				scoreList = []
				for j in range(len(Phrase2List)):
					sim = self.model.similarity(Phrase1List[i].lower(), Phrase2List[j].lower())
					scoreList.append(sim)
				similaritySeparate = similaritySeparate + max(scoreList)
			if similaritySeparate > similarityTogether:
				return similaritySeparate
			else:
				return similarityTogether
		except KeyError:
			if self.printFlag == True:
				print "Not Found! Separate " + Phrase2
			return 0

########################################################################################
# Code to retrieve DBpedia matching propery link from Resource link and Property Word
########################################################################################

	def getPropertyLink(self,resourceLink,propertyWord,liveFlag):
		matchProperty = []
		matchPropertyP = []
		matchPropertyO = []
		abstractFlag = 0
		query2 = """select distinct ?p where {<"""+resourceLink+"""> ?p ?o}"""
		propertyListSTR = self.getDataQuery(query2)
		if self.printFlag == True:
			print propertyListSTR
		propertyListSTRLive = self.getDataQueryLive(query2)
		if self.printFlag == True:
			print propertyListSTRLive
		# propertySimVal = sys.maxint
		propertyPSimVal = 0
		propertyOSimVal = 0
		for propertyListJSON in propertyListSTR["results"]["bindings"]:
			propertyLink = (propertyListJSON["p"]["value"])
			if propertyLink.split("/")[-1].lower() == 'abstract':
				abstractFlag = 1
				abstractLink = propertyLink
			if self.printFlag == True:
				print propertyLink
			propertySimTemp = 0
			if propertyLink.split("/")[-2] == "property" and self.split_on_uppercase(propertyLink.split("/")[-1])[0] != 'wiki':
				if len(propertyWord.split(' ')) > 1 :
					propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
				else:
					try:
						propertySimTemp = self.model.similarity(propertyWord.lower(), propertyLink.split("/")[-1].lower())
					except KeyError:
						propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
						if self.printFlag == True:
							print "Not Found! " + propertyLink.split("/")[-1]
				if self.printFlag == True:
					print propertyLink.split("/")[-1] + " : " + str(propertySimTemp)
				if propertySimTemp > propertyPSimVal:
					propertyPSimVal = propertySimTemp
					matchPropertyP = propertyLink
					matchLiveFlagP = 0
			if propertyLink.split("/")[-2] == "ontology" and self.split_on_uppercase(propertyLink.split("/")[-1])[0] != 'wiki':
				if len(propertyWord.split(' ')) > 1:
					propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
				else:
					try:
						propertySimTemp = self.model.similarity(propertyWord.lower(), propertyLink.split("/")[-1].lower())
					except KeyError:
						propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
						if self.printFlag == True:
							print "Not Found! " + propertyLink.split("/")[-1]
				if self.printFlag == True:
					print propertyLink.split("/")[-1] + " : " + str(propertySimTemp)
				if propertySimTemp > propertyOSimVal:
					propertyOSimVal = propertySimTemp
					matchPropertyO = propertyLink
					matchLiveFlagO = 0
		for propertyListJSON in propertyListSTRLive["results"]["bindings"]:
			propertyLink = (propertyListJSON["p"]["value"])
			if propertyLink.split("/")[-1].lower() == 'abstract':
				abstractFlag = 1
				abstractLink = propertyLink
			if self.printFlag == True:
				print propertyLink
			propertySimTemp = 0
			if propertyLink.split("/")[-2] == "property" and self.split_on_uppercase(propertyLink.split("/")[-1])[0] != 'wiki':
				if len(propertyWord.split(' ')) > 1:
					propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
				else:
					try:
						propertySimTemp = self.model.similarity(propertyWord.lower(), propertyLink.split("/")[-1].lower())
					except KeyError:
						propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
						if self.printFlag == True:
							print "Not Found! " + propertyLink.split("/")[-1]
				if self.printFlag == True:
					print propertyLink.split("/")[-1] + " : " + str(propertySimTemp)
				if propertySimTemp > propertyPSimVal:
					propertyPSimVal = propertySimTemp
					matchPropertyP = propertyLink
					matchLiveFlagP = 1
			if propertyLink.split("/")[-2] == "ontology" and self.split_on_uppercase(propertyLink.split("/")[-1])[0] != 'wiki':
				if len(propertyWord.split(' ')) > 1:
					propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
				else:
					try:
						propertySimTemp = self.model.similarity(propertyWord.lower(), propertyLink.split("/")[-1].lower())
					except KeyError:
						propertySimTemp = self.word2vecSim(propertyWord, propertyLink.split("/")[-1])
						if self.printFlag == True:
							print "Not Found! " + propertyLink.split("/")[-1]
				if self.printFlag == True:
					print propertyLink.split("/")[-1] + " : " + str(propertySimTemp)
				if propertySimTemp > propertyOSimVal:
					propertyOSimVal = propertySimTemp
					matchPropertyO = propertyLink
					matchLiveFlagO = 1
		if propertyPSimVal > propertyOSimVal:
			propertySimVal = propertyPSimVal
			matchProperty = matchPropertyP
			matchLiveFlag = matchLiveFlagP
		else:
			propertySimVal = propertyOSimVal
			matchProperty = matchPropertyO
			matchLiveFlag = matchLiveFlagO
		print "Property similarity value: "+str(propertySimVal)
		if matchProperty == []:
			print "Code not able to find any matching Property for Resourse "+resourceLink
			if abstractFlag == 0:
				print "Abstract not found. Not returning any property"
			else:
				matchProperty = abstractLink
				print "Returning abstract as the matching property"
		return matchProperty, matchLiveFlag

########################################################################################
# Code to retrieve query answer from Resource link and Propery link
########################################################################################

	def getQueryAnswer(self,resourceLink,matchProperty,matchLiveFlag):
		query3 = """select distinct ?o where {<"""+resourceLink+"""> <"""+matchProperty+"""> ?o. FILTER langMatches(lang(?c),'en')}"""
		if matchLiveFlag == 0:
			queryAnswerSTR = self.getDataQuery(query3)
		else:
			queryAnswerSTR = self.getDataQueryLive(query3)
		if self.printFlag == True:
			print queryAnswerSTR
		queryAnswer = []
		if queryAnswerSTR["results"]["bindings"] == []:
			query3 = """select distinct ?o where {<"""+resourceLink+"""> <"""+matchProperty+"""> ?o}"""
			if matchLiveFlag == 0:
				queryAnswerSTR = self.getDataQuery(query3)
			else:
				queryAnswerSTR = self.getDataQueryLive(query3)
			if self.printFlag == True:
				print queryAnswerSTR
		for queryAnswerJSON in queryAnswerSTR["results"]["bindings"]:
			queryAnswer.append(queryAnswerJSON["o"]["value"])	
		return queryAnswer

########################################################################################
# Wrapper code to get answer from Resource word and Property word
########################################################################################

	def getAnswer(self,resourceWord,propertyWord):
		resourceLink, liveFlag = self.getResourceLink(resourceWord)
		print "DBpedia Resource Link: "+resourceLink
		matchProperty, matchLiveFlag = self.getPropertyLink(resourceLink,propertyWord, liveFlag)
		if matchProperty == []:
			print "Not able to any retrive matching property"
			return "Couldn't retrieve any queryAnswer"
		else:
			print "DBpedia Property Link: "+matchProperty
			queryAnswer = self.getQueryAnswer(resourceLink,matchProperty,matchLiveFlag)
			print "Answer/s"
			for i in range(len(queryAnswer)):
				print queryAnswer[i].split("/")[-1]
				# print queryAnswer[i]

########################################################################################
# The main function
########################################################################################

if __name__ == "__main__":
	qdb = QueryDBPedia()
	qdb.getAnswer('Earth','satellite')
