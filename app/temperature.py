import os

TEMPERATURE_FILE = os.environ['ROOT_FS'] + "/sys/class/hwmon/hwmon0"


def get_temp() -> float :
    with open('TEMPERATURE_FILE', 'r') as f:
        tmp_string =  f.read()
        tmp_int = int(tmp_string)
        return tmp_int / 1000