import pandas as pd

def count_dpout():
	prepanel = pd.read_stata("./data_files/raw_data/Turkey2005_2008_panel.dta")
	panel = pd.read_stata("./data_files/raw_data/Turkey_2008_2013_2019.dta", convert_categoricals=False)
	rd1 = pd.read_stata("./data_files/raw_data/Turkey-2009-FCS-full-data-.dta")
	rd2 = pd.read_stata("./data_files/raw_data/Turkey-2010-FCS-full data-.dta")
	rd3 = pd.read_stata("./data_files/raw_data/Turkey-2010-FCS w3-full data-.dta")

	int_nos=prepanel[prepanel["panel"]=="2005 and 2008"]["interview_no"].tolist()
	# print(prepanel["idstd"].tolist())
	# print(prepanel.head())
	int_nos=int_nos[1:]
	# print(prepanel.loc[(prepanel["interview_no"]==int_nos[0]) & (prepanel["year"]==2008), "idstd"].iat[0])
	for no in int_nos:
		idstd08=prepanel.loc[(prepanel["interview_no"]==no) & (prepanel["year"]==2008), "idstd"].iat[0]
		# print(idstd08)
		prepanel.loc[(prepanel["interview_no"]==no)&(prepanel["year"]==2005), "idstd"]=idstd08

	# idstd_nums=[idstd for idstd in panel["idstd"]]
	# for idstd in idstd_nums:
	# 	new_id=prepanel.loc[prepanel["idstd"]==idstd, "panelid"].iat[0]
	# 	panel.loc[panel["idstd"]==idstd, "idstd"]=new_id

	panel["idstd"]=panel["panelid"]

	first=prepanel[prepanel["year"]==2005]
	second=prepanel[prepanel["year"]==2008]
	third=panel[panel["year"]==2013]
	fourth=panel[panel["year"]==2019]


	first_ls=first["idstd"].tolist()
	second_ls=second["idstd"].tolist()
	third_ls=third["idstd"].tolist()
	fourth_ls=fourth["idstd"].tolist()
	rd1_ls=rd1["idstd"].tolist()
	rd2_ls=rd2["idstd"].tolist()
	rd3_ls=rd3["idstd"].tolist()

	from0508=[idstd for idstd in first_ls if idstd in second_ls]
	print("firms in 2005: ", len(first_ls))
	print("firms from 05 to 08: ", len(from0508))
	print("firms dropped out from 05 to 08: ", len(first_ls) - len(from0508))
	# print(len(prepanel[prepanel["panel"]=="2005 and 2008"]["idstd"].tolist()))

	from0509=[idstd for idstd in from0508 if idstd in rd1_ls]
	print(f"firms from 05 to 09 {len(from0509)}\n firms dropped out in 2009 but part from 05 to 08: {len(from0508) - len(from0509)}")

	from05rd2=[idstd for idstd in from0509 if idstd in rd2_ls]
	print("firms from 05 to 2010rd2: ", len(from05rd2))
	print("firms dropped out of 2010rd2 but part from 05 to 2009: ", len(from0509) - len(from05rd2))

	from05rd3=[idstd for idstd in from0509]
	print("firms from 05 to 2010rd3: ", len(from05rd3))
	print("firms dropped out of 2010rd3 but part from 05 to 2009: ", len(from0509) - len(from05rd3))

	dropped_out_FCS_surv=[idstd for idstd in from0509
							if idstd not in from05rd2
							and idstd not in from05rd3]
	print("firms dropped out of 2010 that participated from 05 to 09: ", len(dropped_out_FCS_surv))

	dpFCS_but_in13=[idstd for idstd in dropped_out_FCS_surv if idstd in third_ls]
	print("firms dropped out of 2010 but still in 2013: ", len(dpFCS_but_in13))

	from050913=[idstd for idstd in from0509 if idstd in third_ls]
	print("firms from 2005 to 2013:", len(from050913))
	print("firms dropped out from 2013 but part from 2005 to 2009:", len(from0509) - len(from050913))

	from0513=[idstd for idstd in from0508 if idstd in third_ls]
	print("firms from 2005 to 2013 skipping FCS surv: ", len(from0513))
	print("firms dropped out of 2013 but in 2005 to 2008: ", len(from0508) - len(from050913))

	from0519=[idstd for idstd in from050913 if idstd in fourth_ls]
	print("firms from 05 to 2019: ", len(from0519))
	print("firms that dropped out in 2019: ", len(from050913) - len(from0519))

if __name__ == '__main__':
	count_dpout()