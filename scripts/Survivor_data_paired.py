import pandas as pd

def from0813nonum():
	with pd.io.stata.StataReader("./data_files/raw_data/Turkey_2008_2013_2019.dta") as sr:
	    value_labels = sr.value_labels()

	df = pd.read_stata(
	    "./data_files/raw_data/Turkey_2008_2013_2019.dta",
	    convert_categoricals=False,
	)

	for col in df:
	    if col in value_labels:
	        df[col].replace(value_labels[col], inplace=True)
	df=df[(df["panel"]=="2008, 2013 and 2019") | (df["panel"]=="2008 and 2013 only")]
	# df["idstd"]=df["panelid"]
	df=df[df["year"]!=2019]
	second=df[df["year"]==2008]
	df=df[df["year"]!=2008]
	df.to_csv("./data_files/stage_1/panel.csv")

	beeps=pd.read_stata("./data_files/raw_data/Turkey-2013-full-data.dta")
	# ids=[idstd for idstd in df["idstd"].tolist()]
	beeps=beeps[beeps["idstd"].isin(df["idstd"].tolist())]
	beeps["year"]=2013

	idstd_nums=[idstd for idstd in beeps["idstd"]]
	beeps["idstd"]=pd.to_numeric(beeps["idstd"])
	for idstd in idstd_nums:
		new_id=df.loc[df["idstd"]==idstd, "panelid"].iat[0]
		beeps.loc[beeps["idstd"]==idstd, "idstd"]=new_id
	beeps.to_csv("./data_files/stage_1/t2013.csv")

def from0508num():
	data = pd.io.stata.read_stata("./data_files/raw_data/Turkey2005_2008_panel.dta")
	data=data[data["year"]==2008]
	data.to_csv("./data_files/stage_1/prepanel.csv")

def var_0813():
	# Adds variables to 13 and tdz using 08 location
	beeps=pd.read_csv("./data_files/stage_1/prepanel.csv", index_col=[0])
	panel=pd.read_csv("./data_files/stage_1/panel.csv", index_col=[0])

	beeps["a3x"]=beeps["a3x"].replace(18, "Istanbul")
	beeps.drop_duplicates(inplace=True)

	beeps.rename(columns={"a3x": "city"}, inplace=True)

	tdz13 = {"gebze": 2, "ankara": 5, "izmir": 4, "istanbul": 6, "eskisehir": 1, "kocaeli": 3, "konya": 1, "antayla": 1
	, "trabzon": 1, "kayseri": 1, "adana": 1, "erzurum": 1, "isparta": 1, "mersin": 1, "yalova": 6,
	"bursa": 1, "gaziantep": 1, "denizli": 1, "elazig": 1, "sivas": 1, "edirne": 1, "diyarbakir": 2,
	"yogzat": 3, "burdur": 2, "amasya": 2, "kirklareli": 2, "bilecik": 2, "tunceli": 2,
	"karaman": 1, "canakkale": 1, "usak": 1, "osmaniye": 1, "kirsehir": 1, "mugla": 1,
	"gumushane": 1, "bayburt": 1, "hakkari": 1, "kilis": 1}

	panel["idstd"]=panel["panelid"]
	# panel=panel[panel["year"]==2013]
	panel=panel[panel["idstd"].isin(beeps["idstd"].tolist())]
	print(len(panel["idstd"].isin(beeps["idstd"].tolist())))

	panel["tdz"]=0
	for firm in beeps["idstd"].tolist():
		city08=beeps.loc[(beeps["idstd"]==firm), "city"].iat[0]
		city08=city08.lower()
		if city08 in tdz13.keys():
			# panel.loc[(panel["idstd"]==firm), "tdz"]=tdz13[city08]
			panel.loc[(panel["idstd"]==firm), "tdz"]=1

	panel.rename(columns = {"_2008_2013_c22a": "c22a"}, inplace=True)
	print(panel.head())
	t2013 = panel[panel["idstd"].isin(beeps["idstd"].tolist())]
	print(len(t2013))

	# Total perm employees
	t2013=t2013[t2013["l1"]>0]
	t2013["l1"]=pd.to_numeric(t2013["l1"], errors='coerce').dropna()
	print(len(t2013))

	# Labor force education
	t2013=t2013[t2013["_2008_2013_ECAq69"]>0]
	t2013["lf_ed"]=pd.to_numeric(t2013["_2008_2013_ECAq69"], errors='coerce').dropna()
	print(f'labor force ed: {len(t2013)}')

	# Percent foreign owned
	# t2013=t2013[t2013["b2b"]>0]
	# t2013["b2b"]=pd.to_numeric(t2013["b2b"], errors='coerce').dropna()


	# email
	t2013["c22a"]=t2013["c22a"].replace("Yes", 1)
	t2013["c22a"]=t2013["c22a"].replace("No", 0)
	print(len(t2013))

	# website
	t2013["c22b"]=t2013["c22b"].replace("Yes", 1)
	t2013["c22b"]=t2013["c22b"].replace("No", 0)
	t2013["c22b"]=t2013["c22b"].replace(-8, 0)
	print(len(t2013))


	# Electricity
	t2013["c30a"].replace(["Don't know", "DOES NOT APPLY", "No obstacle", -9, -7], 0, inplace=True)
	t2013["c30a"].replace("Minor obstacle", 1, inplace=True)
	t2013["c30a"].replace("Moderate obstacle", 2, inplace=True)
	t2013["c30a"].replace("Major obstacle", 3, inplace=True)
	t2013["c30a"].replace("Very severe obstacle", 4, inplace=True)
	print(len(t2013))




	t2013.rename(columns={"l1": "tot_emp", "b2b": "perc_foriegn_own",
							"d2": "tot_sales", "c22a": "email",
							"c22b": "website", "c30a": "electricity",
							"k1c": "input_credit"
							}, inplace=True)

	col_ls = t2013.columns.tolist()

	t2013c=t2013.iloc[:, [col_ls.index("idstd"), col_ls.index("tot_emp"),
						col_ls.index("year"),
						# col_ls.index("tot_sales"),
						col_ls.index("email"), col_ls.index("website"),
						col_ls.index("electricity"),
						col_ls.index("input_credit"),
						col_ls.index("lf_ed"),
						# col_ls.index("perc_foriegn_own"),
						col_ls.index("tdz")]
						]
	t2013s=t2013.iloc[:, [col_ls.index("idstd"), col_ls.index("tot_emp"),
						col_ls.index("year"), col_ls.index("tot_sales"),
						col_ls.index("email"), col_ls.index("website"),
						col_ls.index("electricity"),
						col_ls.index("lf_ed"),
						# col_ls.index("input_credit"),
						# col_ls.index("perc_foriegn_own"),
						col_ls.index("tdz")]
						]

	# % inputs bought on credit
	t2013c["input_credit"]=pd.to_numeric(t2013["input_credit"], errors="coerce").dropna()
	t2013c=t2013c[t2013c["input_credit"]>0]
	print(len(t2013))

	# Total sales last year
	t2013s=t2013s[t2013s["tot_sales"]>0]
	t2013s["tot_sales"]=pd.to_numeric(t2013s["tot_sales"], errors='coerce').dropna()
	# print(len(t2013))

	t2013c.to_csv("./data_files/final_data/2013survivorscpair.csv")
	t2013s.to_csv("./data_files/final_data/2013survivorspair.csv")

def main():
	from0813nonum()
	from0508num()
	var_0813()

if __name__ == '__main__':
	main()
