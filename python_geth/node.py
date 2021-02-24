import atexit
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime
from shutil import which, copyfile
from subprocess import Popen

from web3 import Web3, HTTPProvider


class Node:
    def __init__(self, datadir, port=30303, rpcport=8000, name="Node01", netowrk_id=1900, genesis_file=''):
        """
        Create a Node object

        :param datadir: Absolute path to a directory to be used for data of the node
        :type datadir: str
        :param port: Geth port
        :type port: int
        :param rpcport: Geth RpcPort (old: http port)
        :type rpcport: int
        :param name: Name of your node
        :type name:str
        :param netowrk_id: The id of your ETH network
        :type netowrk_id: int
        :param genesis_file: Absolute path to genesis file
        :type genesis_file: str
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
        """
        Starts the node in a process
        :return: null
        :rtype: null
        """
        if os.name == 'nt':
            command = "geth --identity {0} -cache=1024 --syncmode \"fast\" --http --http.port {1} --http.corsdomain \"*\" " \
                      "--datadir \"{2}\" --port " \
                      "{3} --nodiscover --http.api  \"eth,net,web3,personal,miner,admin\" --networkid {4} --nat " \
                      "\"any\" --ipcdisable --allow-insecure-unlock ".format(str(self.name), str(self.rpcport),
                                                                             str(self.datadir),
                                                                             str(self.port), str(self.network_id))

            self.process = Popen(command)

        else:
            command = "exec geth --identity {0}  -cache=1024 --syncmode \"fast\" --http --http.port {1} --http.corsdomain \"*\" --datadir \"{2}\" " \
                      "--port " \
                      "{3} --nodiscover --http.api  \"eth,net,web3,personal,miner,admin\" --networkid {4} --nat " \
                      "\"any\" --ipcdisable --allow-insecure-unlock ".format(str(self.name), str(self.rpcport),
                                                                             str(self.datadir),
                                                                             str(self.port), str(self.network_id))

            self.process = Popen(command, stdout=subprocess.PIPE, shell=True)

        self.w3 = Web3(HTTPProvider('http://127.0.0.1:{}'.format(self.rpcport)))
        counter = 0

        # This is a brute force way of waiting for an async call
        while not self.w3.isConnected() or counter >= 5:
            time.sleep(1)
            counter += 1
        if self.w3.isConnected():
            print('STARTED PID: ', self.process.pid)
            atexit.register(self.stop_node)
        else:
            self.stop_node()

    def stop_node(self):
        """
        Stops the nodes process
        """
        try:
            print("Killing process")
            self.process.kill()
            self.process.wait()
        except Exception as e:
            print('PLease report this!')
            print(e)
            if os.name == 'nt':
                print("Killing process failed: Forcing!")
                os.system("taskkill /im geth.exe /f")

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
        """
        Wrapper method called on __init__ to create a geth node.
        """
        try:
            os.mkdir("{}".format(self.datadir))
        except FileExistsError:
            print("WARNING: The folder for the node exists, but will proceed to use it!")

        if self.genesisFile is None:
            try:
                os.mkdir("{}/config".format(self.datadir))
            except FileExistsError:
                print("WARNING: The folder for the config exists, but will proceed to use it!")

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            pass_path = "{0}/pass_first.txt".format(self.datadir)
            with open(pass_path, "w") as pass_file:
                pass_file.write(hashlib.sha256(date_time.encode('utf-8')).hexdigest())

            os.system("geth --datadir \"{0}\" account new --password \"{1}\"".format(self.datadir, pass_path))

            accounts_adresses = {}

            for root, dirs, files in os.walk("{}/keystore".format(self.datadir)):
                for file in files:
                    with open(os.path.join(root, file)) as account:
                        data = json.load(account)
                        accounts_adresses[data['address']] = {"balance": "1000000000000000000"}
            fn = os.path.join(os.path.dirname(__file__), 'templates/genesis.json')

            with open(fn) as template:
                data = json.load(template)
                data['alloc'] = accounts_adresses
                with open("{}/config/genesis.json".format(self.datadir), 'w+') as write_file:
                    json.dump(data, write_file, indent=4)

            os.system("geth --datadir \"{0}\" init \"{0}/config/genesis.json\" ".format(self.datadir))
        else:
            os.system("geth --datadir \"{0}\" init \"{1}\" ".format(self.datadir, self.genesisFile))

    def add_node(self, enode, localhost=True):
        """
        Add a node to the chain.

        :param enode: The enode address of the node to be added
        :type enode: string
        :param localhost: whether the node is running on localhost or not
        :type localhost: bool
        :return: success indicator
        :rtype: bool
        """
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

    def add_foreign_account(self, key, name):
        copyfile(key, "{}/keystore/{}".format(self.datadir, name))

    def get_first_account(self):
        """
        Get the first account that gets created as part of the create node function.
        This account can be used to interface with geth for easy contract deployment.

        :return: string of account number, string of password
        :rtype: str,str
        """
        account = self.w3.eth.accounts[0]
        if os.path.exists("{0}/pass_first.txt".format(self.datadir)):
            with open("{0}/pass_first.txt".format(self.datadir), "r") as pass_file:
                passwd = pass_file.read()
        else:
            passwd = ''

        return account, passwd.strip()

    def configure_truffle(self, config_file=None):
        """
        Set up default truffle to be ready to deploy contracts. This method needs to be called before
        creating contract interfaces.

        :param config_file: optional absolute path to config file to be supplied in case of specific config
        :type config_file: str

        """
        if config_file is not None:
            template_file = config_file
        else:
            template_file = os.path.join(os.path.dirname(__file__), 'templates/truffle-config.txt')

        os.system("cd {} && npx truffle init".format(self.datadir))
        os.system("rm {}/truffle-config.js".format(self.datadir))
        with open(template_file, 'r') as template_f:
            template = template_f.read()
            template = template.replace('<PORT>', str(self.rpcport))
            template = template.replace('<FROM>', "\"{}\"".format(self.get_first_account()[0]))
            with open('{}/truffle-config.js'.format(self.datadir), 'w+') as original_config_f:
                original_config_f.write(template)
