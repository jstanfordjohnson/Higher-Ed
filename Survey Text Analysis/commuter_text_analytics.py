import operator
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import csv
import xlrd
from xlutils.copy import copy
import re

import nltk
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures

wb = xlrd.open_workbook('commuter_survey.xls')
ws = wb.sheet_by_name('Sheet1')

# Generate writable copy of the workbook
cwb = copy(wb)

# Sheet to write to within the writable copy
s = cwb.get_sheet(0)


# Grabs value of worksheet cell and writes to variable cell
# Cell reference is 1 minus row number
# Also change encoding of special characters
cell = ws.cell_value(128, 0)
cell = cell.replace("‚Äô", "'")
#print(cell)

# Remove carriage returns and replace with a space
text = str(cell).replace('\n', ' ')
#print(text)


# Remove everything EXCEPT upper and lower case alphabets
text = re.sub(r'([^a-zA-Z ]+?)', '', text)

text = text.lower()
print(text)



tokenizer = RegexpTokenizer(r'\w+')

# Create a set of stop words
stop_words = set(stopwords.words('english'))

# Tokenize the words in variable text
# Output is a list
tokens = tokenizer.tokenize(text)
print(tokens)

filtered_sentence = [] 

# Remove stopwords from text 
for w in tokens: 
	   if w not in stop_words: 
	    filtered_sentence.append(w) 
	    	
print(filtered_sentence)

##########################################
#Collocate Cloud

from collections import defaultdict

bi_dict = defaultdict(int)
bg_measures = BigramAssocMeasures()

for i in range(127):
	cell = ws.cell_value(i+1, 0)
	cell = cell.replace("‚Äô", "'")

	text = str(cell).replace('\n', ' ')
	text = re.sub(r'([^a-zA-Z ]+?)', '', text)
	text = text.lower()

	#for text in reasmes:
	words = nltk.word_tokenize(text)
	bi_finder = BigramCollocationFinder.from_words(words)
	bi_collocs = bi_finder.nbest(bg_measures.likelihood_ratio, 10)
	#print("bi_collocs", bi_collocs)
	#print(bi_dict)
	for colloc in bi_collocs:
		bi_dict[colloc] += 1

#print(bi_dict)
# Create a list of tuples sorted by index 1 i.e. value field     
listofTuples = sorted(bi_dict.items() , reverse=True, key=lambda x: x[1])
 
# Iterate over the sorted sequence
#for elem in listofTuples :
    #print(elem[0] , " ::" , elem[1] )  
