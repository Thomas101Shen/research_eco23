import pandas as pd


def dig():
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

	beeps.rename(columns={"c22a": "email", "c22b": "website"}, inplace=True)
	beeps.to_csv("./data_files/digit/t2013digit.csv")

def digit2008_05():
	prepanel=pd.read_csv("./data_files/stage_1/prepanel.csv", index_col=[0])

	prepanel["a3x"]=prepanel["a3x"].replace(18, "Istanbul")
	beeps=prepanel[prepanel["year"]==2008]

	print("_______ number of firms in 2008 from prepanel")
	print(len(beeps["idstd"].tolist()))

	tdz08 ={"gebze": 2, "ankara": 5, "izmir": 1, "istanbul": 3, "eskisehir": 1, "kocaeli": 3, "konya": 1, "antayla": 1
	, "trabzon": 1, "kayseri": 1, "adana": 1, "erzurum": 1, "isparta": 1, "mersin": 1,
	"bursa": 1, "gaziantep": 1, "denizli": 1, "elazig": 1, "sivas": 1, "edirne": 1, "diyarbakir": 1}

	tdz05 ={"gebze": 2, "ankara": 3, "izmir": 1, "istanbul": 3, "eskisehir": 1,
	"kocaeli": 3, "konya": 1, "antayla": 1, "trabzon": 1, "kayseri": 1, "adana": 1,
	"erzurum": 1, "isparta": 1, "mersin": 1, "bursa": 1,}

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
	beeps.rename(columns={"c22a":"email", "c22b": "website", "a3x": "city"}, inplace=True)

	tdzfirms=beeps[beeps["city"].isin(tdz08.keys())].drop_duplicates()
	print("Firms in tdzs 2008: ",len(tdzfirms["idstd"].tolist()))

	nontdzfirms=beeps[~beeps["idstd"].isin(tdz08.keys())].drop_duplicates()
	print("Firms not in tdzs 2008: ", len(nontdzfirms["idstd"].tolist()))

	tdzfirms["tdz"]=tdzfirms["city"].apply(lambda city: tdz08[city])
	print(tdzfirms.head())

	beeps=pd.concat([tdzfirms, nontdzfirms], axis=0)
	beeps["city"].replace(18, "istanbul", inplace=True) # Why is this here?

	# print(beeps.head())
	beeps.to_csv("./data_files/digit/t2008digit.csv")

	first["q39a"]=first["q39a"].replace(2,0)
	first["q39b"]=first["q39b"].replace(2,0)

	first.rename(columns={"q39a": "email", "q39b": "website", "city1f" : "city"}, inplace=True)
	first["tdz"]=0

	first["city"]=first["city"].str.lower()
	tdz2005=first[first["city"].isin(tdz05.keys())]
	nontdz2005=first[-first["city"].isin(tdz05.keys())]

	tdz05_ls=tdz2005["idstd"].tolist()
	nontdz2005_ls=nontdz2005["idstd"].tolist()
	print(f"tdz firms in 2005: {len(tdz05_ls)}")
	print(f"non tdz firms in 2005: {len(nontdz2005_ls)}")

	tdz2005["tdz"]=tdz2005["city"].apply(lambda city: tdz05[city])
	print(tdz2005.head())
	first=pd.concat([tdz2005,nontdz2005], axis=0)
	first.to_csv("./data_files/digit/t2005digit.csv")

if __name__ == '__main__':
	dig()