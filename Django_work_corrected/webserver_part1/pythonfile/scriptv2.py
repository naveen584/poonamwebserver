
import csv
max_=0
max_index=0
to_be_include=[]
def filemake(x):
	out=open("search_result.faa", "a")
	f = open("search.faa", "r")

	a=f.readline()

	while(a):
		if a.startswith(">"+x):

			out.write(a)
			startpont=True	
			a=f.readline()
			break		

		a=f.readline()
	while (a):
		# print (a)
		if a.startswith(">"):
			break
		else:
			out.write(a)
		a=f.readline()
	f.close()
	out.close()
	# print(count)
with open("all_data1.csv", 'r', encoding='utf-8', newline='\n') as csv_in_file:
		r = csv.reader(csv_in_file, quoting=csv.QUOTE_ALL)
		previous_=None
		previous_row=None
		count=0
		for i in r:
			current=float(i[0])
			previous_row=i[2]
			count+=1
			if previous_ :
				if ((abs(float(i[0]))-previous_)/float(i[0]) > float(max_)):
					max_=abs(float(i[0])-previous_)/float(i[0])
					max_index=count
			previous_=current
print(max_index)
with open("all_data1.csv", 'r', encoding='utf-8', newline='\n') as csv_in_file:
		r = csv.reader(csv_in_file, quoting=csv.QUOTE_ALL)
		index=0
		for i in r:
			if(index!=0 and index <max_index):
				to_be_include.append(i[2])
			index+=1
# print(to_be_include)
for i in to_be_include:
	filemake(i)
