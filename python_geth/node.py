import hashlib
import json
import os
from datetime import datetime
from multiprocessing import Process
from shutil import which

from web3 import Web3, HTTPProvider


class Node:
    def __init__(self, datadir, port=30303, rpcport=8000, name="Node01", netowrk_id=1900, genesis_file=''):
        """

        :param port:
        :param rpcport:
        :param datadir:
        :param name:
        :param netowrk_id:
        :param genesis_file:
        """
        self._check_for_geth()
        self.port = port
        self.rpcport = rpcport
        self.datadir = datadir
        self.name = name
        self.network_id = netowrk_id
        self.process = None
        self.http = "http://127.0.0.1:{}".format(rpcport)
        self.genesisFile = genesis_file if genesis_file != '' else None
        self._create_node()
        self.w3 = None

    def start_node(self):
        command = "geth --identity {0} --http --http.port {1} --http.corsdomain \"*\" --datadir \"{2}\" --port " \
                  "{3} --nodiscover --http.api  \"eth,net,web3,personal,miner,admin\" --networkid {4} --nat " \
                  "\"any\" --ipcdisable --allow-insecure-unlock ".format(str(self.name), str(self.rpcport),
                                                                         str(self.datadir),
                                                                         str(self.port), str(self.network_id))

        self.process = Process(target=self._start_process, args=(command,))
        self.process.start()
        self.w3 = Web3(HTTPProvider('http://127.0.0.1:{}'.format(self.rpcport)))

    @staticmethod
    def _start_process(command):
        return os.system(command)

    @staticmethod
    def _check_for_geth():
        if not which("geth") is not None:
            print("Geth needs to be installed and added to path! ")
            print("Exiting!")
            exit(1)

    @staticmethod
    def _check_for_npm():
        if not which("npx") is not None:
            print("Npm needs to be installed and added to path! ")
            print("Exiting!")
            exit(1)

    def _create_node(self):
        try:
            os.mkdir("{}".format(self.datadir))
        except FileExistsError:
            print("WARNING: The folder for the node exists, but will proceed to use it!")

        if self.genesisFile is None:
            try:
                os.mkdir("{}\\config".format(self.datadir))
            except FileExistsError:
                print("WARNING: The folder for the config exists, but will proceed to use it!")

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            pass_path = "{0}\\pass_first.txt".format(self.datadir)
            with open(pass_path, "w") as pass_file:
                pass_file.write(hashlib.sha256(date_time.encode('utf-8')).hexdigest())

            os.system("geth --datadir \"{0}\" account new --password \"{1}\"".format(self.datadir, pass_path))

            accounts_adresses = {}

            for root, dirs, files in os.walk("{}\\keystore".format(self.datadir)):
                for file in files:
                    with open(os.path.join(root, file)) as account:
                        data = json.load(account)
                        accounts_adresses[data['address']] = {"balance": "1000000000000000000"}
            fn = os.path.join(os.path.dirname(__file__), 'templates/genesis.json')

            with open(fn) as template:
                data = json.load(template)
                data['alloc'] = accounts_adresses
                with open("{}\\config\\genesis.json".format(self.datadir), 'w+') as write_file:
                    json.dump(data, write_file, indent=4)

            os.system("geth --datadir \"{0}\" init \"{0}\\config\\genesis.json\" ".format(self.datadir))
        else:
            os.system("geth --datadir \"{0}\" init \"{1}\" ".format(self.datadir, self.genesisFile))

    def add_node(self, enode, localhost=True):
        if localhost:
            enode_address = enode.split("@")
            ending = enode_address[1].split("?")
            ip = ending[0].split(":")
            ip[0] = "[::]"
            ip = ":".join(ip)
            enode_address = enode_address[0] + "@" + ip + "?" + ending[1]
        else:
            enode_address = enode
        count = self.w3.net.peer_count
        self.w3.geth.admin.add_peer(enode_address)
        if count + 1 == self.w3.net.peer_count:
            return True
        else:
            return False

    def get_first_account(self):
        account = self.w3.eth.accounts[0]
        if os.path.exists("{0}\\pass_first.txt".format(self.datadir)):
            with open("{0}\\pass_first.txt".format(self.datadir), "r") as pass_file:
                passwd = pass_file.read()
        else:
            passwd = ''

        return account, passwd.strip()

    def configure_truffle(self, config_file=None):
        if config_file is not None:
            template_file = config_file
        else:
            template_file = os.path.join(os.path.dirname(__file__), 'templates/truffle-config.txt')

        os.system("cd {} && npx truffle init".format(self.datadir))
        os.system("rm {}\\truffle-config.js".format(self.datadir))
        with open(template_file, 'r') as template_f:
            template = template_f.read()
            template = template.replace('<PORT>', str(self.rpcport))
            template = template.replace('<FROM>', "\"{}\"".format(self.get_first_account()[0]))
            with open('{}\\truffle-config.js'.format(self.datadir), 'w+') as original_config_f:
                original_config_f.write(template)
