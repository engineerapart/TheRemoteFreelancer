from io import StringIO
import pandas 

commit_dates = {
"993bfdf5ec4e19148d11fe16de7f48364dd0c52e":"Nov 2 2019",
"90cd77d68222726e8a0d0a76440f754d9cb69b88":"Nov 2 2019",
"2867866de9247e8c291f3aeb50735c81af519001":"Nov 6 2018",
"4aff92abd48b8540a24c5fa35ce7a9f52a4d0b98":"Nov 6 2018",
"db77bca196313f322348df176a7344265f772c92":"Aug 10 2018",
"c595c00524893858d40ecdc7a8a9ad0ea60d7a2b":"Jan 6 2018",
"eeca09b5fc937090c39d63ae0e4cfdaf4c46dd74":"Dec 12 2017",
"7d3fbb68a56a5edc37d5532b893fc19f06dcc618":"Sep 16 2017",
"ed9f37e1095f5a66a988b97b28746ae4e7acc5dc":"Sep 14 2017",
"1b75a6b82a5c45a63576addde0d9201ed97116b9":"Sep 14 2017",
"eaca0b183453262516f71f0d2533e1f91677f574":"Sep 14 2017",
"0d7f80401f7f1da9eb82c51f3fce83be325a994b":"Sep 14 2017",
"cf63e30b90829d6edb69093c13d8514c92beb5a8":"Sep 12 2017",
"548c49a6369de1f48e5596deeaf16adebcf9474a":"Sep 12 2017",
"6dcace80f214907b0c5627399583d0289be8039f":"Sep 10 2017",
"40df07c44b10d3de0df90c81d62368261ea31e9d":"Sep 10 2017",
"b4d8e363674b931dcb54b424075438fc5801778e":"Sep 10 2017",
"660191d0210347e307f52e356b9ae697c4b7f251":"Sep 10 2017",
"6a24a4c1ee905c68a36d8b2739b761b1e83af3db":"Sep 10 2017"
}

header_row = False

out_df = pandas.DataFrame()
tables = []
dates = []
i = -1

for line in open("i.txt"):
	if line.startswith("----"):
		i+=1
		tables.append("")
		dates.append("")
		dates[i] = commit_dates[line.strip("-").strip("\n")]
	else:
		tables[i] += line 

for date, table in zip(dates, tables):
	s = StringIO(table)
	s.seek(0)
	df = pandas.read_csv(s, error_bad_lines=False, warn_bad_lines=False)
	df['date'] = date
	out_df = out_df.append(df)

out_df.to_csv("i2.csv")
