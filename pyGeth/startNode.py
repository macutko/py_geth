import os

from pyGeth.utils import check_for_geth


def start_node(port="30303", rpcport="8000",
               datadir="\"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\manual_install_geth\\node01\"",
               name="Node01", netowrkid="1900"):
    check_for_geth()
    command = "geth --identity {0} --http --http.port {1} --http.corsdomain \"*\" --datadir  {2} --port " \
              "{3} --nodiscover --http.api  \"db,eth,net,web3,personal,miner,admin\" --networkid {4} --nat " \
              "\"any\" --ipcdisable --allow-insecure-unlock ".format(str(name), str(rpcport), str(datadir),
                                                                     str(port), str(netowrkid))

    node = os.system(command)

    print(os.system("geth attach http://127.0.0.1:8000"))
