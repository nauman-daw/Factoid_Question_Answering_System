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

class DependencyTAG:
	def __init__(self,typeRel,govName,govIdx,depName,depIdx):
		self.typeRel = typeRel
		self.govMap={}
		self.depMap={}
		self.gov=govName
		self.dep=depName
		self.govMap[govName] = govIdx
		self.depMap[depName] = depIdx

	def __str__(self):
		govKey = self.gov
		depKey = self.dep
		return self.typeRel + " " + govKey + " " + self.govMap[govKey] + " " + depKey + " " + self.depMap[depKey]
