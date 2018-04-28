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

import cmd
import sys
from QueryDBPedia import QueryDBPedia
from DependencyKeyGen import DependencyKeyGen
from NERWrapper import NERWrapper

class QuestionAnswer(cmd.Cmd):
	
    	def __init__(self):
		cmd.Cmd.__init__(self)
		self.qdb = QueryDBPedia()
		self.dpKG = DependencyKeyGen()
		self.NERW = NERWrapper()
		self.prompt = "QAInteractive: "

	def do_ans(self, question):
		try:
			key1,key2=self.dpKG.getKey(question)
			print key1
			print key2
			print self.qdb.getAnswer(key1,key2)
		except:
			print ("Something have gone wrong!! Try again")		
			print sys.exc_info()[0]

	def do_ner(self, question):
		try:
			key1,key2=self.NERW.getKey(question)
			print key1
			print key2
			if not len(key1)<2:
				print self.qdb.getAnswer(key1,key2)
			else:
				print "Unable to extract Resource name"
		except:
			print ("Something have gone wrong!! Try again")
			print sys.exc_info()[0]


	def default(self,question):
		try:
			key1,key2=self.dpKG.getKey(question)
			print key1
			print key2
			if key1!='unknown':
				print self.qdb.getAnswer(key1,key2)
			else:
				print "Unable to extract Resource name"
		except:
			print ("Something have gone wrong!! Try again")
			print sys.exc_info()[0]

	    
	def do_EOF(self, line):
		return True

	def do_exit(self,line):
		exit()

if __name__ == '__main__':
	QuestionAnswer().cmdloop()
