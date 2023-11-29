import pandas as pd

def final_merge():
	timeline = pd.read_csv("./data_files/concat_data/no_dropouts0513.csv", index_col=[0])
	FCS = pd.read_csv("./data_files/concat_data/fcs_data.csv", index_col=[0])

	# Select rows from timeline in the FCS survey
	timeline = timeline[timeline["idstd"].isin(FCS["idstd"].tolist())]

	# Adding 2008 values for variables other than tot_emp to FCS data since it's ommited from the actual data
	second_val = timeline[timeline["year"]==2008]

	# First drop 2008 tot_emp numbers and years
	second_val.drop(columns=["tot_emp", "year"], inplace=True)

	# Then, merge 2008 columns with FCS
	fcs_vals = pd.merge(FCS, second_val, on="idstd")
	fcs_vals.to_csv("./data_files/concat_data/fcs_variables.csv")

if __name__=="__main__":
	final_merge()