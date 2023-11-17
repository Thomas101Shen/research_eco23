import pandas as pd


def main():
	digit2013()
	digit2008_05()

def digit2013():
	beeps=pd.read_csv("./data_files/stage_1/t2013.csv", index_col=[0])

	beeps["c22a"]=beeps["c22a"].replace("Don't know")
	beeps["c22b"]=beeps["c22b"].replace("Refused")

	beeps=beeps[(beeps["c22a"]=="Yes") | (beeps["c22a"]=="No")]
	beeps=beeps[(beeps["c22b"]=="Yes") | (beeps["c22b"]=="No")]

	beeps["c22a"]=beeps["c22a"].replace("Yes", 1)
	beeps["c22a"]=beeps["c22a"].replace("No", 0)

	beeps["c22b"]=beeps["c22b"].replace("Yes", 1)
	beeps["c22b"]=beeps["c22b"].replace("No", 0)

	beeps["digitization"]=beeps["c22a"]+beeps["c22b"]

	beeps.to_csv("./data_files/digit/t2013digit.csv")

def digit2008_05():
	prepanel=pd.read_csv("./data_files/stage_1/prepanel.csv", index_col=[0])

	tdz=['gebze', 'ankara', 'izmir', 'istanbul',
		'eskisehir', 'kocaeli', 'konya', 'antayla',
		'trabzon', 'kayseri', 'adana', 'erzurum', 'isparta',
		'mersin', 'bursa', 'gaziantep', 'denizli', 'elazig',
		'sivas', 'edirne', 'diyarbakir']

	# prepanel["a3x"]=prepanel["city1f"]
	prepanel["a3x"]=prepanel["a3x"].replace(18, "Istanbul")
	beeps=prepanel[prepanel["year"]==2008]

	# panel08=pd.read_csv("./data_files/stage_1/firms2008.csv")

	print("_______ number of firms in 2008 from prepanel")
	print(len(beeps["idstd"].tolist()))

	# Neglecting 89 firms from 2008 to 2013
	# print(len([idstd for idstd in panel08["idstd"].tolist() if idstd not in beeps["idstd"].tolist()]))

	# Create another dataframe with same digitization stuff as 2008 but with firms from panel
	# [idstd for idstd in panel08["idstd"].tolist() if idstd not in beeps["idstd"].tolist()]
	# firms08 = [idstd for idstd in panel08["idstd"].tolist() if idstd not in beeps["idstd"].tolist()]
	# panel08=panel08[panel08["idstd"].isin(firms08)]

	int_nos=prepanel["interview_no"].tolist()
	for no in int_nos:
		idstd08=prepanel.loc[(prepanel["interview_no"]==no) & (prepanel["year"]==2008), "idstd"].iat[0]
		prepanel.loc[(prepanel["interview_no"]==no)&(prepanel["year"]==2005), "idstd"]=idstd08
	first=prepanel[prepanel["year"]==2005]

	# print(len(beeps["idstd"].tolist())) # need to modify the c22a in panel08 in order for firms to carry over
	beeps=beeps[(beeps["c22a"]=="Yes") | (beeps["c22a"]=="No")]
	beeps=beeps[(beeps["c22b"]=="Yes") | (beeps["c22b"]=="No")]

	# beeps=pd.concat([beeps, panel08], axis=0)
	# print(len(beeps["idstd"].tolist()))

	beeps["c22a"]=beeps["c22a"].replace("Yes", 1)
	beeps["c22a"]=beeps["c22a"].replace("No", 0)
	# beeps["c22a"]=beeps["c22a"].replace(2, 0)

	beeps["c22b"]=beeps["c22b"].replace("Yes", 1)
	beeps["c22b"]=beeps["c22b"].replace("No", 0)
	# beeps["c22b"]=beeps["c22b"].replace(2, 0)

	# Implementing tdzs into the calculation of digitization

	# tdz={"Gebze": 427, "Ankara": 5753, "Izmir": 220, "Istanbul":566 , "Eskisehir":75, "Kocaeli", "Konya", "Antayla"
	# 		, "Trabzon", "Kayseri", "Adana", "Erzurum", "Isparta", "Mersin",
	# 		"Bursa", "Gaziantep", "Denizli", "Elazig": 1, "Sivas", "Edirne", "Diyarbakir"}
	# tdz={"gebze": 2, "ankara": 5, "izmir": 1, "istanbul": 3, "eskisehir": 1, "kocaeli": 3, "konya": 1, "antayla": 1
	# 		, "trabzon": 1, "kayseri": 1, "adana": 1, "erzurum": 1, "isparta": 1, "mersin": 1,
	# 		"bursa": 1, "gaziantep": 1, "denizli": 1, "elazig": 1, "sivas": 1, "edirne": 1, "diyarbakir": 1}


	beeps["a3x"]=beeps["a3x"].str.lower()
	beeps.rename(columns={"c22a":"E-mail", "c22b": "website", "a3x": "city"}, inplace=True)

	tdzfirms=beeps[beeps["city"].isin(tdz)]
	print("Firms in tdzs 2008: ",len(tdzfirms["idstd"].tolist()))

	nontdzfirms=beeps[-beeps["idstd"].isin(tdz)]
	print("Firms not in tdzs 2008: ", len(nontdzfirms["idstd"].tolist()))

	tdz05=['gebze', 'ankara', 'izmir', 'istanbul',
		'eskisehir', 'kocaeli', 'konya', 'antayla',
		'trabzon', 'kayseri', 'adana', 'erzurum', 'isparta',
		'mersin', 'bursa']

	beeps.to_csv("./data_files/digit/t2008digit.csv")

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

	# Happens here too
	# first["digitization"]=first["q39a"]+first["q39b"]
	# first["city1f"]=first["city1f"].str.lower()
	# for index, row in first.iterrows():
	# 	city = row["city1f"]
	# 	if city in tdz.keys():
	# 		first.at[index, "digitization"]=tdz[city]*(row["q39a"]+row["q39b"]) + row["q39a"]+row["q39b"]
	# first.to_csv("./data_files/digit/t2005digit.csv")

	# regions_w_tdz=[]
	# regions_wout_tdz=[]
	# for index, row in beeps.iterrows():
	# 	city = row["a3x"]
	# 	if city in tdz.keys():
	# 		beeps.at[index, "digitization"]=tdz[city]*(row["c22a"]+row["c22b"]) + row["c22a"]+row["c22b"]
	# 		regions_w_tdz.append(row["a2"])
	# 	else: regions_wout_tdz.append(row["a2"])

	# regions_w_tdz=set(regions_w_tdz)
	# print(len(set(regions_wout_tdz)))
	# regions_wout_tdz=set([region for region in regions_wout_tdz if region not in regions_w_tdz])
	# print(len(regions_wout_tdz))

	# areas=[region for region in beeps["a2"].tolist() if  ]
	# use city1f to set digit
	# Set tdz based on city, than print cities where tdz==0
	# set city = region and print regions where tdz==0
	# Remove all regions where tdz==1 from list of regions where tdz==0
	# See if number of output are the same

if __name__ == '__main__':
	main()