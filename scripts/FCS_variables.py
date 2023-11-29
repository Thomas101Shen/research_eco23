import pandas as pd

def grab_firms():
	fcs = pd.read_csv("./data_files/stage_1/full_FCS_data.csv")
	firms = set(pd.read_csv("./data_files/final_data/no_dropouts0513.csv")["idstd"].tolist())
	# print(firms)
	# print(fcs.head()["idstd"])
	firms=list(firms)
	fcs_firms = [firm for firm in firms if firm in fcs["idstd"].tolist()]
	print(len(fcs_firms))

if __name__ == '__main__':
	grab_firms()