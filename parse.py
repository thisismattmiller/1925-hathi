import csv
with open('/Users/m/data/hathi_full_20210101_pd.txt','w') as outfile:

	with open('/Users/m/data/hathi_full_20210101.txt') as infile:
		reader = csv.reader(infile, delimiter="\t",quoting=csv.QUOTE_NONE)
		for l in reader:

			if '1925' in l[16] and l[15] == '0' and 'pd' in l[2] and '2021' in l[14]:
				outfile.write("\t".join(l)+'\n')

