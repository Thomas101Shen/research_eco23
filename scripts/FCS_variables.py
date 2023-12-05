import pandas as pd

def grab_firms():
	fcs = pd.read_csv("./data_files/stage_1/full_FCS_data.csv", index_col=[0])
	timeline = pd.read_csv("./data_files/concat_data/no_dropouts0513.csv", index_col=[0])
	firms = set(timeline["idstd"].tolist())
	firms=list(firms)
	fcs_firms = [firm for firm in firms if firm in fcs["idstd"].tolist()]
	print(len(fcs_firms))
	tdz = set(timeline[timeline["tdz"]==1]["idstd"].tolist())
	tdz_fcs = [firm for firm in tdz if firm in fcs["idstd"].tolist()]
	print("tdz firms in the financial crisis surveys: ", len(tdz_fcs))
	fcs = fcs[fcs["idstd"].isin(tdz_fcs)]

	first = fcs[fcs["year"]==2009.0]
	second = fcs[fcs["year"]==2010.0]
	third = fcs[fcs["year"]==2010.5]

	first["tot_emp"]=pd.to_numeric(first["e1"], errors='coerce').dropna()
	second["tot_emp"]=pd.to_numeric(second["c1"], errors='coerce').dropna()
	third["tot_emp"]=pd.to_numeric(third["c1"], errors='coerce').dropna()

	# first["tot_sales"]=pd.to_numeric(first["d1a"], errors='coerce').dropna()
	# second["tot_sales"]=pd.to_numeric(second["e6"], errors='coerce').dropna()
	# third["tot_sales"]=pd.to_numeric(third["e6"], errors='coerce').dropna()
	firms_third=third["idstd"].tolist()
	firms_second=second["idstd"].tolist()

	second = second[~second["idstd"].isin(firms_third)]
	second = second[second["idstd"].isin(first["idstd"].tolist())]

	first = first[(first["idstd"].isin(firms_third)) | (first["idstd"].isin(firms_second))]
	third = third[third["idstd"].isin(first["idstd"].tolist())]
	third["year"]=2010
	FCS_merg=pd.concat([first, second, third], axis=0)
	FCS_merg=FCS_merg[FCS_merg["tot_emp"]>0]

	col_ls = FCS_merg.columns.tolist()
	FCS_merg=FCS_merg.iloc[:, [col_ls.index("idstd"), col_ls.index("tot_emp"),
							# col_ls.index("tot_sales"),
							col_ls.index("year"),]]

	tdz_fcs=timeline[timeline["idstd"].isin]

	FCS_merg.to_csv("./data_files/concat_data/fcs_data.csv")

if __name__ == '__main__':
	grab_firms()