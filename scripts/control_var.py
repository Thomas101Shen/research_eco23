import pandas as pd

def merge_data():
	first = pd.read_csv("./data_files/non_control_var/t2005non_con_var.csv", index_col=[0])
	second = pd.read_csv("./data_files/non_control_var/t2008non_con_var.csv", index_col=[0])
	third = pd.read_csv("./data_files/non_control_var/t2013non_con_var.csv", index_col=[0])


	first["q21"]=pd.to_numeric(first["q21"])
	first["credit"]=first["q21"] # Some N/A values in credit, will deal with later

	second["q21"]=pd.to_numeric(second["k1e"])
	second["credit"]=second["k1e"]

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

	timeline=pd.concat([first, second, third], axis=0)

	firms_0513=[idstd for idstd in first["idstd"].tolist()
				if idstd in second["idstd"].tolist()
				and idstd in third["idstd"].tolist()]
	tl0513=timeline[timeline["idstd"].isin(firms_0513)]

	tdz13=['gebze', 'ankara', 'izmir', 'istanbul',
	'eskisehir', 'kocaeli', 'konya', 'antayla',
	'trabzon', 'kayseri', 'adana', 'erzurum',
	'isparta', 'mersin', 'yalova', 'bursa', 'gaziantep',
	'denizli', 'elazig', 'sivas', 'edirne', 'diyarbakir',
	'yogzat', 'burdur', 'amasya', 'kirklareli', 'bilecik',
	'tunceli', 'karaman', 'canakkale', 'usak', 'osmaniye',
	'kirsehir', 'mugla', 'gumushane', 'bayburt', 'hakkari', 'kilis']

	print("firms from 05 to 2013: ", len(firms_0513))

	# Adding digitization to 2013 firms with tdzs
	for firm in firms_0513:
		city08=tl0513.loc[(tl0513["idstd"]==firm) & (tl0513["year"]==2008), "city"].iat[0]
		city08=city08.lower()
		if city08 in tdz13:
			tl0513.loc[(tl0513["idstd"]==firm) & (tl0513["year"]==2013), "tdz"]=1
			third.loc[(third["idstd"]==firm), "tdz"]=1

	col_ls = tl0513.columns.tolist()
	# print(col_ls.index("digitization"))
	# print(col_ls.index("electricity"))
	# print(col_ls.index("credit"))
	# print(col_ls.index("tot_emp"))
	# print(col_ls.index("perc_foriegn_own"))
	# print(col_ls.index("perc_exports"))
	# print(col_ls.index("total_sales"))

	# print(col_ls.index("idstd"), col_ls.index("year"),
	# 						col_ls.index("E-mail"), col_ls.index("website"),
	# 						col_ls.index("electricity"), col_ls.index("credit"),
	# 						col_ls.index("perc_foriegn_own"),col_ls.index("tdz"))
	# 0, 2, 457-458, 735, 737-739
	print(tl0513.head()["city"])
	tl0513=tl0513.iloc[:, [col_ls.index("idstd"), col_ls.index("tot_emp"), col_ls.index("year"),
								col_ls.index("E-mail"), col_ls.index("website"),
								col_ls.index("electricity"), col_ls.index("credit"),
								col_ls.index("perc_foriegn_own"),col_ls.index("tdz")]
							]
	# tl0513=tl0513.iloc[:, [0,2]]
	# tl0513=pd.concat([tl0513, tl0513_cont], axis=1)
	tl0513.to_csv("./data_files/concat_data/timelinefirms0513.csv")

	timeline0813=timeline[(timeline["year"]==2008) | (timeline["year"]==2013)]

 	# # supposed to remove all firms counted twice from 2005-2013 and 2008-2013
	# timeline0813 = timeline.loc[~((timeline["year"]==2008)&timeline["idstd"].isin(firms_0513))]
	firms_0813=[idstd for idstd in second["idstd"].tolist()
				if idstd in third["idstd"].tolist()]

	print("firms from 08 to 2013: ", len(firms_0813))

	# Adding digitization to 2013 firms in 2008 datasaet with tdzs
	for firm in firms_0813:
		city08=timeline0813.loc[(timeline0813["idstd"]==firm) & (timeline0813["year"]==2008), "city"].iat[0]
		# city08=city08.lower()
		if city08 in tdz13: timeline0813.loc[(timeline0813["idstd"]==firm)&(timeline0813["year"]==2013), "tdz"]=1

	col_ls = timeline0813.columns.tolist()
	# print(col_ls.index("digitization"))
	# print(col_ls.index("electricity"))
	# print(col_ls.index("credit"))
	# print(col_ls.index("tot_emp"))
	# print(col_ls.index("perc_foriegn_own"))
	# print(col_ls.index("perc_exports"))
	# print(col_ls.index("total_sales"))
	timeline0813=timeline0813.iloc[:, [col_ls.index("idstd"), col_ls.index("tot_emp"), col_ls.index("year"),
								col_ls.index("E-mail"), col_ls.index("website"),
								col_ls.index("electricity"), col_ls.index("credit"),
								col_ls.index("perc_foriegn_own"),col_ls.index("tdz")]
							]
	# timeline0813=timeline0813.iloc[:, [0,2]]
	# timeline0813=pd.concat([timeline0813, timeline0813_cont], axis=1)


	timeline0813=timeline0813[timeline0813["idstd"].isin(firms_0813)]
	timeline0813.to_csv("./data_files/concat_data/timelinefirms0813.csv")

	# Need to get rid of firms that show up in 2005-2008-2013 and 2008-2013

	firms_not_droppedout = pd.concat([tl0513, timeline0813], axis=0)

	firms_not_droppedout.replace("No obstacle ", 0, inplace=True)
	firms_not_droppedout.replace("Very Severe obstacle", 4, inplace=True)

	firms_not_droppedout.drop_duplicates(inplace=True)
	num=len(set(firms_not_droppedout["idstd"].tolist()))
	print(f"total firms: {num}")

	firms_not_droppedout.to_csv("./data_files/concat_data/no_dropouts0513.csv")

	col_ls=first.columns.tolist()
	first=first.iloc[:, [col_ls.index("idstd"), col_ls.index("year"), col_ls.index("tot_emp"),
								col_ls.index("E-mail"), col_ls.index("website"),
								col_ls.index("electricity"), col_ls.index("credit"),
								col_ls.index("perc_foriegn_own"),col_ls.index("tdz")]
							]
	print(first.head())

	col_ls=second.columns.tolist()
	second=second.iloc[:, [col_ls.index("idstd"), col_ls.index("year"), col_ls.index("tot_emp"),
								col_ls.index("E-mail"), col_ls.index("website"),
								col_ls.index("electricity"), col_ls.index("credit"),
								col_ls.index("perc_foriegn_own"),col_ls.index("tdz")]
								]

	# second=pd.concat([second, second_cont], axis=1)
	# print(second.head())

	col_ls=third.columns.tolist()
	third=third.iloc[:, [col_ls.index("idstd"),col_ls.index("tot_emp"),
						col_ls.index("E-mail"), col_ls.index("website"),
						col_ls.index("electricity"), col_ls.index("credit"),
						col_ls.index("perc_foriegn_own"),col_ls.index("tdz")]
							]
	print(third.head())
	third["year"]=2013
	# third["year"]=2013 Comment this part out after removing tot sales as dep var to prevent duplicate keys
	# third=pd.concat([third, third_cont], axis=1)
	# print(third.head())

	first.to_csv("./data_files/concat_data/t2005.csv")
	second.to_csv("./data_files/concat_data/t2008.csv")
	third.to_csv("./data_files/concat_data/t2013.csv")

	timeline=pd.concat([first, second, third], axis=0)
	timeline.to_csv("./data_files/concat_data/timeline.csv")

	# Get firms that dropped out to compare to firms that stayed
	dropoutfirms0508=[idstd for idstd in first["idstd"].tolist()
				if idstd not in second["idstd"].tolist()]

	dropoutfirms0813=[idstd for idstd in second["idstd"].tolist()
				if idstd not in third["idstd"].tolist()]

	droppedout_2008=first[first["idstd"].isin(dropoutfirms0508)]
	droppedout_2013=second[second["idstd"].isin(dropoutfirms0813)]

	droppedoutfirms=pd.concat([droppedout_2008, droppedout_2013], axis=0)
	droppedoutfirms.to_csv("./data_files/concat_data/droppedout.csv")


if __name__ == '__main__':
	merge_data()