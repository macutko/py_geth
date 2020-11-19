import hashlib
import json
import os
import subprocess
from datetime import datetime
from multiprocessing import Process
from shutil import which

import demjson


class Node:
    def __init__(self, port="30303", rpcport="8000",
                 datadir="\"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\manual_install_geth\\node01\"",
                 name="Node01", netowrkid="1900"):
        self._check_for_geth()
        self.port = port
        self.rpcport = rpcport
        self.datadir = datadir
        self.name = name
        self.networkid = netowrkid
        self.process = None
        self.http = "http://127.0.0.1:{}".format(rpcport)
        self._create_node()

    def start_node(self):
        command = "geth --identity {0} --http --http.port {1} --http.corsdomain \"*\" --datadir \"{2}\" --port " \
                  "{3} --nodiscover --http.api  \"eth,net,web3,personal,miner,admin\" --networkid {4} --nat " \
                  "\"any\" --ipcdisable --allow-insecure-unlock ".format(str(self.name), str(self.rpcport),
                                                                         str(self.datadir),
                                                                         str(self.port), str(self.networkid))

        self.process = Process(target=self._start_process, args=(command,))
        self.process.start()

    @staticmethod
    def _start_process(command):
        return os.system(command)

    @staticmethod
    def _check_for_geth():
        if not which("geth") is not None:
            print("Geth needs to be installed and added to path! ")
            print("Exiting!")
            exit(1)

    def _create_node(self):
        try:
            os.mkdir("{}".format(self.datadir))
            os.mkdir("{}\\config".format(self.datadir))
        except FileExistsError:
            print("WARNING: The folder for the node exists, but will proceed to use it!")

        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        pass_path = "{0}\\pass_{1}.txt".format(self.datadir, now.strftime("%H_%M_%S"))
        with open(pass_path, "w") as pass_file:
            pass_file.write(hashlib.sha256(date_time.encode('utf-8')).hexdigest())

        os.system("geth --datadir \"{0}\" account new --password \"{1}\"".format(self.datadir, pass_path))

        accounts_adresses = {}

        for root, dirs, files in os.walk("{}\\keystore".format(self.datadir)):
            for file in files:
                with open(os.path.join(root, file)) as account:
                    data = json.load(account)
                    accounts_adresses[data['address']] = {"balance": "1000000000000000000"}

        with open("./pyGeth/genesis.json") as template:
            data = json.load(template)
            data['alloc'] = accounts_adresses
            with open("{}\\config\\genesis.json".format(self.datadir), 'w+') as write_file:
                json.dump(data, write_file, indent=4)

        os.system("geth --datadir \"{0}\" init \"{0}\\config\\genesis.json\" ".format(self.datadir))

    def get_enode(self):
        result = subprocess.check_output(("geth attach {} --exec \"admin.nodeInfo\" ".format(self.http)), shell=True)
        data = demjson.decode(result.decode('utf-8'))
        return data['enode']

    def add_node(self, enode):
        enode_address = enode
        enode_address = enode.split("@")
        ending = enode_address[1].split("?")
        ip = ending[0].split(":")
        ip[0] = "[::]"
        ip = ":".join(ip)
        enode_address = "\\\"" + enode_address[0] + "@" + ip + "?" + ending[1] + "\\\""

        print("geth attach {0} --exec \"admin.addPeer({1})\" ".format(self.http, enode_address))

        result = subprocess.check_output(
            ("geth attach {0} --exec \"admin.addPeer({1})\" ".format(self.http, enode_address)), shell=True)

        data = result.decode('utf-8')
        print(data)

        result = subprocess.check_output(
            ("geth attach {0} --exec \"net.peerCount\" ".format(self.http)), shell=True)

        data = result.decode('utf-8')
        print(data)
