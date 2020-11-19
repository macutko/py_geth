import os

from pyGeth.node import Node


def main():
    os.system("rm -rf \"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node01\"") # debug purposes
    node = Node(datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node01")
    node.create_node()
    node.start_node()
    print(node.getEnode())

if __name__ == '__main__':
    main()
