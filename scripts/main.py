import pandas as pd
from panel_data import main as step1
from digit import main as step2
from non_control_var import main as step3
from control_var import main as step4

def main():
	step1()
	step2()
	step3()
	step4()

if __name__ == '__main__':
	main()