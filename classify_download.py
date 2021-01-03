import json
import requests
import os.path

from fuzzywuzzy import fuzz


with open('bibdata_results.json') as file:

	for line in file:
		# if 'A1061816' in line:


			data = json.loads(line)


			if 'regnum-new' in data:
				idd = data['regnum-new']
			else:
				idd = data['regnum']


			if os.path.isfile('classify/'+idd):
				print('skipp',idd)
				continue


			# print(data['bibData'])

			data['filteredBibData'] = []

			# if len(data['bibData']) > 1:

			for bd in data['bibData']:

				if len(bd['primary_contributor']) == 0:
					continue 


				data['title'] = data['title'].replace('...','')
				data['title'] = data['title'].replace('…','')

				bd['title'] = bd['title'].replace('...','')
				bd['title'] = bd['title'].replace('…','')


				title_same = fuzz.ratio(data['title'], bd['title'])
				bd_aurthor = bd['primary_contributor'][0]['label'].replace(' [from old catalog]','')
				author = data['author'].split('.,')[0]

			

				total_score = fuzz.ratio(data['title'], bd['title']) + fuzz.ratio(author, bd_aurthor)
				# print(total_score)

				if total_score > 100:
					bd['filterScore'] = total_score
					data['filteredBibData'].append(bd)


						# print(data['title'], bd['title'])
						# print(author, bd_aurthor)
						# print(total_score)
						# print('-----')


					# if fuzz.ratio(data['title'], bd['title']) < 75:



					# 	print(data['title'], bd['title'])
					# 	print(fuzz.ratio(data['title'], bd['title']))


			best = None
			score = 0
			hasOclc = False
			for bd in data['filteredBibData']:

				if len(bd['oclc']) > 0:
					hasOclc = True
				if bd['filterScore'] > score:
					best = bd

			if not hasOclc and best != None:

				title = best['title']
				author = best['primary_contributor'][0]['label'].replace(' [from old catalog]','')


				# if os.path.isfile('classify/'+idd):
				# 	# print('skip')
				# 	continue


				print(title, author,idd)

				# http://classify.oclc.org/classify2/Classify?author=Sampson%2C%20Blanche%20D.&title=The%20crystal%20loom%2C
				payload = {'author':author[0:49], 'title':title[0:49]}
				response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
				# print(response.text)

				with open('classify/'+idd, 'w') as out:
					out.write(response.text)

			elif hasOclc and best != None:

				if len(best['oclc'])==0:
					continue

				o = best['oclc'][0]
				o = o.strip()
				o = o.replace('ocm','').replace('ocn','').replace('on','')

				if o == '':
					continue

				if os.path.isfile('classify/'+o):
					print('skipp oclc',o)
					continue
				else:
					
		

					payload = {'oclc':o}
					response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
					with open('classify/'+o, 'w') as out:
						out.write(response.text)


					# print(o)
					# print(best)




			# possible_oclc = []
			# for o in data['bibDataAll']['oclc']:

			# 	o = o.strip()
			# 	o = o.replace('ocm','').replace('ocn','').replace('on','')

			# 	if o == '':
			# 		continue

			# 	if  o.isdigit():

			# 		possible_oclc.append(o)

			# if len(possible_oclc) > 0:

			# 	pass
			# 	# for o in possible_oclc:


			# 	# 	if not os.path.isfile('classify/'+o):
			# 	# 		print(o)

			# 	# 		response = requests.get('http://classify.oclc.org/classify2/Classify?oclc='+o)
			# 	# 		with open('classify/'+o, 'w') as out:
			# 	# 			out.write(response.text)
			# 	# 	else:
			# 	# 		print('skip',o)
			# else:

			# 	if len(data['bibDataAll']['title']) > 2:

			# 		print(data['title'])	
			# 		print(data['bibDataAll'])
			# 		print()

				#  [from old catalog]