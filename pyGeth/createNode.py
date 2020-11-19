import hashlib
import os
from datetime import datetime


def create_node(path="C:\\"):
    try:
        os.mkdir("{}".format(path))
    except FileExistsError:
        print("WARNING: The folder for the node exists, but will proceed to use it!")

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    pass_path = "{0}\\pass.txt".format(path)
    with open(pass_path, "w") as pass_file:
        pass_file.write(hashlib.sha256(date_time.encode('utf-8')).hexdigest())

    os.system("geth --datadir \"{0}\" account new --password \"{1}\"".format(path, pass_path))
