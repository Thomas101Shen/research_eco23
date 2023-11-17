import pandas as pd

def main():
	from0508num()
	from0813nonum()
	timeline()
	# FCS()

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

	# second["c22a"]=second["_2008_2013_c22a"]
	# second = second.rename(columns={"_2008_2013_c22a":"c22a"})

	with pd.io.stata.StataReader("./data_files/raw_data/Turkey_2008_2013_2019.dta") as dta:
	    value_labels = dta.value_labels()

	turkey08 = pd.read_stata("./data_files/raw_data/Turkey-2008--full-data-.dta", convert_categoricals=False)

	# for col in df:
	#     if col in value_labels:
	#         turkey08[col].replace(value_labels[col], inplace=True)

	turkey08 = turkey08[turkey08["idstd"].isin(second["idstd"].tolist())]
	# print(second.head()["c22a"])
	turkey08.to_csv("./data_files/stage_1/firms2008.csv") # a3x

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
	data=data[data["panel"]=="2005 and 2008"]
	data.to_csv("./data_files/stage_1/prepanel.csv")

def FCS():
	rd1=pd.read_stata("./data_files/raw_data/Turkey-2009-FCS-full-data-.dta")
	rd2=pd.read_stata("./data_files/raw_data/Turkey-2010-FCS-full data-.dta")
	rd3=pd.read_stata("./data_files/raw_data/Turkey-2010-FCS w3-full data-.dta")

	# print(rd1.head()["c6"])
	# rd1.to_csv("./data_files/stage_1/rd1.csv")

	full_FCS_data=pd.concat([rd1, rd2, rd3], axis=0)
	full_FCS_data.to_csv("./data_files/stage_1/full_FCS_data.csv")

def timeline():
	pre=pd.read_csv("./data_files/stage_1/prepanel.csv")
	# post=pd.read_csv("./data_files/stage_1/panel.csv")
	post=pd.read_csv("./data_files/stage_1/t2013.csv")
	timeline=pd.concat([pre,post], axis=0)
	timeline.to_csv("./data_files/stage_1/timeline.csv")



if __name__ == '__main__':
	main()