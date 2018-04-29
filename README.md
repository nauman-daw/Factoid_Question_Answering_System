# Factoid Question Answering System
This system is based on knowledge based factoid question-answering. It has 2 modules; Question Analysis and Answer extraction. Question Analysis is performed by rule based approach. Stanford's dependency parser is used to obtain the property to be searched. Further, Google's deep Word2Vec model was used to obtain semantically close property to be searched in the knowledge base.
- This version of the system is in interative mode. However, the mode can easily be changed as per the requirement.

# Prerequisites
- Python 2.7, NumPy
- Google's Word2Vec model
- Stanford's NER, Parser and POS-tagger
- Need to keep all above in the current directory

# Usage
```
$ python QAInteractive.py
```
# Authors
Nauman Dawalatabad, Krishnaraj, and Jom Kuriakose

# License
Licensed under the Apache License, Version 2.0. Please see license.md file
