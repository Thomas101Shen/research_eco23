import pandas as pd

def main():
	first = pd.read_csv("./data_files/non_control_var/t2005non_con_var.csv", index_col=[0])
	second = pd.read_csv("./data_files/non_control_var/t2008non_con_var.csv", index_col=[0])
	third = pd.read_csv("./data_files/non_control_var/t2013non_con_var.csv", index_col=[0])


	first["q21"]=pd.to_numeric(first["q21"])
	first["credit"]=first["q21"]

	second["q21"]=pd.to_numeric(second["q21"])
	second["credit"]=second["q21"]

	third["k1c"]=pd.to_numeric(third["k1c"], errors="coerce")
	third=third.dropna(subset=["k1c"])
	third["credit"]=third["k1c"]

	print(len(second["idstd"].tolist()))

	# Brainstormed with taking out electricity as dep var to increase treatment size

	third["c30a"]=third["c30a"].replace(["Don't know", "DOES NOT APPLY", "No obstacle"], 0)
	third["c30a"]=third["c30a"].replace("Minor obstacle", 1)
	third["c30a"]=third["c30a"].replace("Moderate obstacle", 2)
	third["c30a"]=third["c30a"].replace("Major obstacle", 3)
	third["c30a"]=third["c30a"].replace("Very severe obstacle", 4)

	third["electricity"]=third["c30a"]

	second["c30a"]=second["c30a"].replace(["Don't know", "Doesn not Apply (spontaneous)", "No obstacle"], 0)
	second["c30a"]=second["c30a"].replace("Minor obstacle", 1)
	second["c30a"]=second["c30a"].replace("Moderate obstacle", 2)
	second["c30a"]=second["c30a"].replace("Major obstacle", 3)
	second["c30a"]=second["c30a"].replace("Very severe obstacle", 4)

	second["electricity"]=second["c30a"]

	print(len(second["idstd"].tolist()))

	first["q22b"]=first["q22b"].replace(-7, 0)
	first["electricity"]=first["q22b"]

	# Removing LF ed as dep var to increase size

	# first["q82a1"]=pd.to_numeric(first["q82a1"])
	# first=first[first["q82a1"]>=0]
	# first["lf_ed"]=pd.to_numeric(first["q82a1"])

	# Added the ECA don't know after removing tot sales from dep variables
	# second=second[second["ECAq69"]!="Don't know"]
	# second["ECAq69"]=pd.to_numeric(second["ECAq69"])
	# second=second[second["ECAq69"]>=0]
	# second["lf_ed"]=pd.to_numeric(second["ECAq69"])

	# third=third[third["ECAq69"]!="Don't know"]
	# third["ECAq69"]=pd.to_numeric(third["ECAq69"])
	# third=third[third["ECAq69"]>=0]
	# third["lf_ed"]=pd.to_numeric(third["ECAq69"])

	# data05=[idstd for idstd in first["idstd"]]
	# data08=[idstd for idstd in second["idstd"]]
	# data13=[idstd for idstd in third["idstd"]]
	timeline=pd.concat([first, second, third], axis=0)

	firms_0513=[idstd for idstd in first["idstd"].tolist()
				if idstd in second["idstd"].tolist()
				and idstd in third["idstd"].tolist()]
	tl0513=timeline[timeline["idstd"].isin(firms_0513)]

	print("firms from 05 to 2013: ", len(firms_0513))

	tdz={"gebze": 2, "ankara": 5, "izmir": 4, "istanbul": 6, "eskisehir": 1, "kocaeli": 3, "konya": 1, "antayla": 1
		, "trabzon": 1, "kayseri": 1, "adana": 1, "erzurum": 1, "isparta": 1, "mersin": 1, "yalova": 6,
		"bursa": 1, "gaziantep": 1, "denizli": 1, "elazig": 1, "sivas": 1, "edirne": 1, "diyarbakir": 2,
		"yogzat": 3, "burdur": 2, "amasya": 2, "kirklareli": 2, "bilecik": 2, "tunceli": 2,
		"karaman": 1, "canakkale": 1, "usak": 1, "osmaniye": 1, "kirsehir": 1, "mugla": 1,
		"gumushane": 1, "bayburt": 1, "hakkari": 1, "kilis": 1}


	# Adding digitization to 2013 firms with tdzs
	for firm in firms_0513:
		city08=tl0513.loc[(tl0513["idstd"]==firm) & (tl0513["year"]==2008), "a3x"].iat[0]
		city08=city08.lower()
		if city08 in tdz.keys():
			digit=tl0513.loc[(tl0513["idstd"]==firm) & (tl0513["year"]==2013), "digitization"].iat[0]
			digit = digit*(tdz[city08]+1)
			tl0513.loc[(tl0513["idstd"]==firm)&(tl0513["year"]==2013), "digitization"]=digit

	col_ls = tl0513.columns.tolist()
	# print(col_ls.index("digitization"))
	# print(col_ls.index("electricity"))
	# print(col_ls.index("credit"))
	# print(col_ls.index("tot_emp"))
	# print(col_ls.index("perc_foriegn_own"))
	# print(col_ls.index("perc_exports"))
	# print(col_ls.index("total_sales"))
	# print(col_ls.index("lf_ed"))
	tl0513_cont=tl0513.iloc[:, 735:742]
	tl0513=tl0513.iloc[:, [0,2]]
	tl0513=pd.concat([tl0513, tl0513_cont], axis=1)
	tl0513.to_csv("./data_files/final_data/timelinefirms0513.csv")

	timeline0813=timeline[(timeline["year"]==2008) | (timeline["year"]==2013)]
	firms_0813=[idstd for idstd in second["idstd"].tolist()
				if idstd in third["idstd"].tolist()]

	print("firms from 08 to 2013: ", len(firms_0813))

	# Adding digitization to 2013 firms in 2008 datasaet with tdzs
	for firm in firms_0813:
		city08=timeline0813.loc[(timeline0813["idstd"]==firm) & (timeline0813["year"]==2008), "a3x"].iat[0]
		city08=city08.lower()
		if city08 in tdz.keys():
			digit=timeline0813.loc[(timeline0813["idstd"]==firm) & (timeline0813["year"]==2013), "digitization"].iat[0]
			digit = digit*(tdz[city08]+1)
		timeline0813.loc[(timeline0813["idstd"]==firm)&(timeline0813["year"]==2013), "digitization"]=digit

	col_ls = timeline0813.columns.tolist()
	# print(col_ls.index("digitization"))
	# print(col_ls.index("electricity"))
	# print(col_ls.index("credit"))
	# print(col_ls.index("tot_emp"))
	# print(col_ls.index("perc_foriegn_own"))
	# print(col_ls.index("perc_exports"))
	# print(col_ls.index("total_sales"))
	# print(col_ls.index("lf_ed"))
	timeline0813_cont=timeline0813.iloc[:, 735:742]
	timeline0813=timeline0813.iloc[:, [0,2]]
	timeline0813=pd.concat([timeline0813, timeline0813_cont], axis=1)


	timeline0813=timeline0813[timeline0813["idstd"].isin(firms_0813)]
	timeline0813.to_csv("./data_files/final_data/timelinefirms0813.csv")

	firms_not_droppedout = pd.concat([tl0513, timeline0813], axis=0)

	firms_not_droppedout.to_csv("./data_files/final_data/no_dropouts0513.csv")

	first_length=len(first.columns.tolist())
	first_cont=first.iloc[:, first_length-8:first_length+1]
	first=first.iloc[:, [0,2]]
	first=pd.concat([first, first_cont], axis=1)
	# print(first.head())

	second_length=len(second.columns.tolist())
	second_cont=second.iloc[:, second_length-8:second_length+1]
	second=second.iloc[:, [0,2]]
	second=pd.concat([second, second_cont], axis=1)
	# print(second.head())

	third_length=len(third.columns.tolist())
	third_cont=third.iloc[:, third_length-8:third_length+1]
	third=third.iloc[:, [0]]
	# third["year"]=2013 Comment this part out after removing tot sales as dep var to prevent duplicate keys
	third=pd.concat([third, third_cont], axis=1)
	# print(third.head())

	first.to_csv("./data_files/final_data/t2005.csv")
	second.to_csv("./data_files/final_data/t2008.csv")
	third.to_csv("./data_files/final_data/t2013.csv")

	timeline=pd.concat([first, second, third], axis=0)
	timeline.to_csv("./data_files/final_data/timeline.csv")

	# Get firms that dropped out to compare to firms that stayed
	dropoutfirms0508=[idstd for idstd in first["idstd"].tolist()
				if idstd not in second["idstd"].tolist()]

	dropoutfirms0813=[idstd for idstd in second["idstd"].tolist()
				if idstd not in third["idstd"].tolist()]

	droppedout_2008=first[first["idstd"].isin(dropoutfirms0508)]
	droppedout_2013=second[second["idstd"].isin(dropoutfirms0813)]

	droppedoutfirms=pd.concat([droppedout_2008, droppedout_2013], axis=0)
	droppedoutfirms.to_csv("./data_files/final_data/droppedout.csv")


if __name__ == '__main__':
	main()