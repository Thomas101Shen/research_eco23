import pandas as pd

def nc_var():
	first=pd.read_csv("./data_files/digit/t2005digit.csv", index_col=[0])
	second=pd.read_csv("./data_files/digit/t2008digit.csv", index_col=[0])
	third=pd.read_csv("./data_files/digit/t2013digit.csv", index_col=[0])

	# print(len(second["idstd"].tolist()))

	first=first[first["q72"]>0]
	second=second[second["l1"]>0]
	third=third[third["l1"]>0]

	first["tot_emp"]=first["q72"]
	second["tot_emp"]=second["l1"]
	third["tot_emp"]=third["l1"]

	# print(len(second["idstd"].tolist()))

	first["q3a_ii"]=pd.to_numeric(first["q3a_ii"])
	second["b2b"]=pd.to_numeric(second["b2b"])

	third=third[third["b2b"]!="Don't know"]
	third["b2b"]=pd.to_numeric(third["b2b"])

	first=first[first["q3a_ii"]>=0]
	second=second[second["b2b"]>=0]
	third=third[third["b2b"]>=0]

	first["perc_foriegn_own"]=first["q3a_ii"]
	second["perc_foriegn_own"]=second["b2b"]
	third["perc_foriegn_own"]=third["b2b"]

	# testing sample size with total sales
	# third=third[third["d2"]!="Don't know"]
	# third=third[third["d2"]!="Refusal"]
	# third["d2"]=pd.to_numeric(third["d2"])
	# third=third[third["d2"]>=0]

	# first["tot_sales"]=first["p1a1_2004"]
	# second["tot_sales"]=second["d2"]
	# third["tot_sales"]=third["d2"]
	# print(len(second["idstd"].tolist()))

	first=first[first["p1a1_2004"]>=0]
	second=second[second["d2"]>=0]

	first.to_csv("./data_files/non_control_var/t2005non_con_var.csv")
	second.to_csv("./data_files/non_control_var/t2008non_con_var.csv")
	third.to_csv("./data_files/non_control_var/t2013non_con_var.csv")

if __name__ == '__main__':
	nc_var()