import pandas as pd

def grab_firms():
	fcs = pd.read_csv("./data_files/stage_1/full_FCS_data.csv")
	timeline = pd.read_csv("./data_files/final_data/no_dropouts0513.csv")
	firms = set(timeline["idstd"].tolist())
	firms=list(firms)
	fcs_firms = [firm for firm in firms if firm in fcs["idstd"].tolist()]
	print(len(fcs_firms))
	tdz = set(timeline[timeline["tdz"]==1]["idstd"].tolist())
	tdz_fcs = [firm for firm in tdz if firm in fcs["idstd"].tolist()]
	print("tdz firms in the financial crisis surveys: ", len(tdz_fcs))
	


if __name__ == '__main__':
	grab_firms()