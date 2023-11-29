import pandas as pd
from panel_data import pdata as step1
from digit import dig as step2
from non_control_var import nc_var as step3
from control_var import merge_data as step4
from FCS_variables import grab_firms as step5

def main():
	step1()
	step2()
	step3()
	step4()
	step5()

if __name__ == '__main__':
	main()