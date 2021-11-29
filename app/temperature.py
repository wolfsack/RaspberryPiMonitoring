import os

# get file to read
TEMPERATURE_FILE = os.environ['ROOT_FS'] + "/sys/class/hwmon/hwmon0/temp1_input"

# function to get temperature as float
def get_temp() -> float :
    # open file in read mode
    with open(TEMPERATURE_FILE, 'r') as f:
        # read file and cast to int
        tmp_string = f.read()
        tmp_int = int(tmp_string)

        # return as float
        return tmp_int / 1000