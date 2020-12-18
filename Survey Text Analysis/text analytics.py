import operator
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import csv
import xlrd
from xlutils.copy import copy
import re

tokenizer = RegexpTokenizer(r'\w+')

wb = xlrd.open_workbook('survey_data.xls')
ws = wb.sheet_by_name('Sheet1')

# Generate writable copy of the workbook
cwb = copy(wb)

# Sheet to write to within the writable copy
s = cwb.get_sheet(0)



'''
# Loop through each row of the worksheet
for i in range(1787):

	#print(i)
	# Grabs value of cell and writes to variable cell
	cell = ws.cell_value(i+1, 7)
	#print(cell)

	# Remove carriage returns and replace with a space
	text = str(cell).replace('\n', ' ')

	# Remove everything EXCEPT upper and lower case alphabets
	text = re.sub(r'([^a-zA-Z ]+?)', '', text)
	#print(text)

	text = text.lower()

	# Create a set of stop words
	stop_words = set(stopwords.words('english'))

	# Tokenize the words in variable text
	tokens = tokenizer.tokenize(text)
	#print(tokens)

	filtered_sentence = [] 

	# Remove stopwords from text 
	for w in tokens: 
	    if w not in stop_words: 
	    	filtered_sentence.append(w) 
	    	
	#print(filtered_sentence)

	# Create filtered text string: 
	filtered_string = ' '.join(filtered_sentence)
	#print(filtered_string)

	# Perform word count and rank:
	wc = {}
	for t in filtered_sentence:
		count = 0
		if t != "patient" and t != "cannabis" and t != "medical" and t != "marijuana":
			for j in range(len(filtered_sentence)):
				if t == filtered_sentence[j]:
					count += 1

			wc[t] = count

	# Print word count (wc) dictionary
	#print(wc)

	# Sort dictionary elements in descending order
	sorted_wc = sorted(wc.items(), key=operator.itemgetter(1), reverse=True)
	#print(sorted_wc)

	# Store keywords (only) for d3 hover textbox: 
	keywords = []
	for k in sorted_wc:
		keywords.append(k[0])

	#print(keywords)
	
	# Save the changed workbook to a file
	#s = cwb.get_sheet(0)
	#s.write(i+1, 29, keywords)
	s.write(i+1, 29, ' '.join(keywords))
	#s.write(18, 3, filtered_string)
'''
	if ws.cell_value(i+2, 0) == ws.cell_value(i+1, 0):
		#s.write(i+1, 30, "Yay!!!" + " Jennifer, we found a duplicate on the next row!")
		#print(ws.cell_value(rnum+1, 29))
		#print(type(ws.cell_value(rnum+2, 29)))
		s.write(i+1, 30, ws.cell_value(rnum+2, 29) + ws.cell_value(rnum+1, 29))
	else:
		#print(str(ws.cell_value(rnum+1, 29)))
		s.write(i+1, 30, "This is a unique value!")
'''

cwb.save('research.xls')

# Recall: Ultimately want to create a same topic? column


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3

for x in range(1786):
	print(x)

	numRD = int(ws.cell_value(x+1, 28))

	if ws.cell_value(x+2, 0) == ws.cell_value(x+1, 0):
		#s.write(i+1, 30, "Yay!!!" + " Jennifer, we found a duplicate on the next row!")
		#print(ws.cell_value(rnum+1, 29))
		#print(type(ws.cell_value(rnum+2, 29)))

		if numRD == 5:
			l1 = (ws.cell_value(x+1, 29)).split(' ')
			l2 = (ws.cell_value(x+2, 29)).split(' ')
			l3 = (ws.cell_value(x+3, 29)).split(' ')
			l4 = (ws.cell_value(x+4, 29)).split(' ')
			l5 = (ws.cell_value(x+5, 29)).split(' ')


			# Find the intersection of the lists
			intersect = list(set(l1) & set(l2) & set(l3) & set(l4) & set(l5))

			# Write to the cell
			s.write(x+1, 30, str(len(intersect)))

			if intersect == 0:
				s.write(x+1, 31, "N")
			else:
				s.write(x+1, 31, "Y")

		if numRD == 4:
			l1 = (ws.cell_value(x+1, 29)).split(' ')
			l2 = (ws.cell_value(x+2, 29)).split(' ')
			l3 = (ws.cell_value(x+3, 29)).split(' ')
			l4 = (ws.cell_value(x+4, 29)).split(' ')


			# Find the intersection of the lists
			intersect = list(set(l1) & set(l2) & set(l3) & set(l4))

			# Write to the cell
			s.write(x+1, 30, str(len(intersect)))

			if intersect == 0:
				s.write(x+1, 31, "N")
			else:
				s.write(x+1, 31, "Y")

		if numRD == 3:
			l1 = (ws.cell_value(x+1, 29)).split(' ')
			l2 = (ws.cell_value(x+2, 29)).split(' ')
			l3 = (ws.cell_value(x+3, 29)).split(' ')


			# Find the intersection of the lists
			intersect = list(set(l1) & set(l2) & set(l3))

			# Write to the cell
			s.write(x+1, 30, str(len(intersect)))

			if intersect == 0:
				s.write(x+1, 31, "N")
			else:
				s.write(x+1, 31, "Y")

		elif numRD == 2:
			l1 = (ws.cell_value(x+1, 29)).split(' ')
			l2 = (ws.cell_value(x+2, 29)).split(' ')


			# Find the intersection of the lists
			intersect = intersection(l1,l2)
			#print(intersect)
			#s.write(x+1, 30, ''.join(intersect))

			#numRD = int(ws.cell_value(x+1, 28))

			#for fb in range(numRD):
			s.write(x+1, 30, str(len(intersect)))

			if intersect == 0:
				s.write(x+1, 31, "N")
			else:
				s.write(x+1, 31, "Y")
	else:
		# Write to the cell
		s.write(x+1, 30, str(0))
		s.write(x+1, 31, "N")

cwb.save('research.xls')
