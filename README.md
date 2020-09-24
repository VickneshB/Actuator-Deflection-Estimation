# Actuator-Deflection-Estimation
This is to determine the deflection of my colleague's Soft Robotics' specimen when heated

1.  Create an virtual environment using
	```
	$ python3 -m venv  virtual environment name.
	```
2.  Run 
	```
	$ pip3 install -r requirements.txt
	```
3.  Run
	```
	$ python3 main.py {Input Video Name}
	```
	This will take the default Output Video name {Input}_Output.avi
	
	Other Options:
	
	For a custom Ouput Video Name,
	```
	$ python3 main.py {Input Video Name} -o {Output Video Name}
	```
	
	For help, 
	```
	$ python3 main.py -h
	```
	
	
	
