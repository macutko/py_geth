import os

from pyGeth.node import Node


def main():
    os.system("rm -rf \"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node01\"")  # debug purposes
    os.system("rm -rf \"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node02\"")  # debug purposes
    node1 = Node(datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node01", port=30303,
                 rpcport=8000, name="Node01")
    node1.start_node()

    node2 = Node(datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\auto_gen\\node02", port=30304,
                 rpcport=8001, name="Node02")
    node2.start_node()

    ########################################################################


#     we have 2 nodes running, now lets connect them!
    node1.add_node(node2.get_enode())

if __name__ == '__main__':
    main()
