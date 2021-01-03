import csv
import shutil
import requests
import os

dupe_check = {}
no_oclc = []
unique = []
with open('/Users/m/data/hathi_full_20210101_pd.txt') as infile:
	reader = csv.reader(infile, delimiter="\t",quoting=csv.QUOTE_NONE)
	for l in reader:
		if l[7] != '':
			if l[7] not in dupe_check:
				dupe_check[l[7]] = True
				unique.append(l)


		else:
			no_oclc.append(l)
			unique.append(l)

print(len(unique))
print(len(no_oclc))

count = 0
for r in unique:

	htid = r[0].replace(':','').replace('/','')
	url = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={htid};width=400"

	if os.path.isfile('/Users/m/data/hathi_1925_pd_metadata/'+htid):
		print('skipp ',htid)
		continue
	count+=1
	print(count,'/',len(unique))
	if r[7] != '':
		
		o = r[7].split(',')[0]

		payload = {'oclc':o}
		response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
		with open('/Users/m/data/hathi_1925_pd_metadata/'+htid, 'w') as out:
			out.write(response.text)



	else:

		author = r[25]
		title = r[11]
		payload = {'author':author[0:49], 'title':title[0:49]}
		response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
		with open('/Users/m/data/hathi_1925_pd_metadata/'+htid, 'w') as out:
			out.write(response.text)
