import pandas as pd


def main():
	digit2013()
	digit2008_05()

def digit2013():
	# Due to the abscence of a city column here we will add city when consolidating data
	beeps=pd.read_csv("./data_files/stage_1/t2013.csv", index_col=[0])

	beeps["tdz"]=0

	beeps["c22a"]=beeps["c22a"].replace("Don't know")
	beeps["c22b"]=beeps["c22b"].replace("Refused")

	beeps=beeps[(beeps["c22a"]=="Yes") | (beeps["c22a"]=="No")]
	beeps=beeps[(beeps["c22b"]=="Yes") | (beeps["c22b"]=="No")]

	beeps["c22a"]=beeps["c22a"].replace("Yes", 1)
	beeps["c22a"]=beeps["c22a"].replace("No", 0)

	beeps["c22b"]=beeps["c22b"].replace("Yes", 1)
	beeps["c22b"]=beeps["c22b"].replace("No", 0)

	beeps.rename(columns={"c22a": "E-mail", "c22b": "website"}, inplace=True)
	beeps.to_csv("./data_files/digit/t2013digit.csv")

def digit2008_05():
	prepanel=pd.read_csv("./data_files/stage_1/prepanel.csv", index_col=[0])

	tdz=['gebze', 'ankara', 'izmir', 'istanbul',
		'eskisehir', 'kocaeli', 'konya', 'antayla',
		'trabzon', 'kayseri', 'adana', 'erzurum', 'isparta',
		'mersin', 'bursa', 'gaziantep', 'denizli', 'elazig',
		'sivas', 'edirne', 'diyarbakir']

	prepanel["a3x"]=prepanel["a3x"].replace(18, "Istanbul")
	beeps=prepanel[prepanel["year"]==2008]

	print("_______ number of firms in 2008 from prepanel")
	print(len(beeps["idstd"].tolist()))

	int_nos=prepanel["interview_no"].tolist()
	for no in int_nos:
		idstd08=prepanel.loc[(prepanel["interview_no"]==no) & (prepanel["year"]==2008), "idstd"].iat[0]
		prepanel.loc[(prepanel["interview_no"]==no)&(prepanel["year"]==2005), "idstd"]=idstd08
	first=prepanel[prepanel["year"]==2005]

	beeps=beeps[(beeps["c22a"]=="Yes") | (beeps["c22a"]=="No")]
	beeps=beeps[(beeps["c22b"]=="Yes") | (beeps["c22b"]=="No")]

	beeps["c22a"]=beeps["c22a"].replace("Yes", 1)
	beeps["c22a"]=beeps["c22a"].replace("No", 0)

	beeps["c22b"]=beeps["c22b"].replace("Yes", 1)
	beeps["c22b"]=beeps["c22b"].replace("No", 0)

	beeps["tdz"]=0
	beeps["a3x"]=beeps["a3x"].str.lower()
	beeps.rename(columns={"c22a":"E-mail", "c22b": "website", "a3x": "city"}, inplace=True)

	tdzfirms=beeps[beeps["city"].isin(tdz)]
	print("Firms in tdzs 2008: ",len(tdzfirms["idstd"].tolist()))

	nontdzfirms=beeps[-beeps["idstd"].isin(tdz)]
	print("Firms not in tdzs 2008: ", len(nontdzfirms["idstd"].tolist()))

	beepstdz=beeps.loc[beeps["city"].isin(tdz)]
	beepstdz.loc[:,"tdz"]=1
	beepsnontdz=beeps.loc[~beeps["city"].isin(tdz)]

	beeps=pd.concat([beepstdz, beepsnontdz], axis=0)
	beeps["city"].replace(18, "istanbul", inplace=True)

	# print(beeps.head())
	beeps.to_csv("./data_files/digit/t2008digit.csv")

	tdz05=['gebze', 'ankara', 'izmir', 'istanbul',
		'eskisehir', 'kocaeli', 'konya', 'antayla',
		'trabzon', 'kayseri', 'adana', 'erzurum', 'isparta',
		'mersin', 'bursa']

	first["q39a"]=first["q39a"].replace(2,0)
	first["q39b"]=first["q39b"].replace(2,0)

	first.rename(columns={"q39a": "E-mail", "q39b": "website", "city1f" : "city"}, inplace=True)

	first["city"]=first["city"].str.lower()
	tdz2005=first[first["city"].isin(tdz05)]
	nontdz2005=first[-first["city"].isin(tdz05)]

	tdz05_ls=tdz2005["idstd"].tolist()
	nontdz2005_ls=nontdz2005["idstd"].tolist()
	print(f"tdz firms in 2005: {len(tdz05_ls)}")
	print(f"non tdz firms in 2005: {len(nontdz2005_ls)}")

	tdz2005.loc[:,'tdz']=1
	nontdz2005.loc[:,'tdz']=0
	first=pd.concat([tdz2005,nontdz2005], axis=0)
	# firsttdz=first.loc[first["city"].isin(tdz)]
	# firsttdz.loc[:,"tdz"]=1
	# firstnontdz=first.loc[~first["city"].isin(tdz)]
	# first=pd.concat([firsttdz, firstnontdz], axis=0)
	first.to_csv("./data_files/digit/t2005digit.csv")

if __name__ == '__main__':
	main()