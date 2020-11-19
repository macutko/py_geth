from shutil import which


def check_for_geth():
    if not which("geth") is not None:
        print("Geth needs to be installed and added to path! ")
        print("Exiting!")
        exit(1)
