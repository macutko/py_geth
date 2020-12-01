import hashlib
import json
import os
import subprocess
from datetime import datetime
from multiprocessing import Process
from shutil import which

import demjson


class Node:
    def __init__(self, port=30303, rpcport=8000,
                 datadir="\"C:\\Users\\matus\\Desktop\\Uni\\lvl 5\\disseration\\manual_install_geth\\node01\"",
                 name="Node01", netowrkid=1900, genesisFile=''):
        self._check_for_geth()
        self.port = port
        self.rpcport = rpcport
        self.datadir = datadir
        self.name = name
        self.networkid = netowrkid
        self.process = None
        self.http = "http://127.0.0.1:{}".format(rpcport)
        self.genesisFile = genesisFile if genesisFile != '' else None
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

            with open("./pyGeth/genesis.json") as template:
                data = json.load(template)
                data['alloc'] = accounts_adresses
                with open("{}\\config\\genesis.json".format(self.datadir), 'w+') as write_file:
                    json.dump(data, write_file, indent=4)

            os.system("geth --datadir \"{0}\" init \"{0}\\config\\genesis.json\" ".format(self.datadir))
        else:
            os.system("geth --datadir \"{0}\" init \"{1}\" ".format(self.datadir, self.genesisFile))

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

        # print("geth attach {0} --exec \"admin.addPeer({1})\" ".format(self.http, enode_address))

        result = subprocess.check_output(
            ("geth attach {0} --exec \"admin.addPeer({1})\" ".format(self.http, enode_address)), shell=True)

        data = result.decode('utf-8')
        # print(data)

        result = subprocess.check_output(
            ("geth attach {0} --exec \"net.peerCount\" ".format(self.http)), shell=True)

        data = result.decode('utf-8')
        print("Amount of peers: {}".format(data))

    def start_miner(self):
        result = subprocess.check_output(
            ("geth attach {0} --exec \"miner.setEtherbase(eth.accounts[0])\" ".format(self.http)), shell=True)

        data = result.decode('utf-8')
        print(data)

        result = subprocess.check_output(
            ("geth attach {0} --exec \"miner.start()\" ".format(self.http)), shell=True)

        data = result.decode('utf-8')
        print(data)

    def get_first_account(self):
        result = subprocess.check_output(
            ("geth attach {0} --exec \"eth.accounts[0]\" ".format(self.http)), shell=True)

        data = result.decode('utf-8')
        data = data.replace('"', "")
        if os.path.exists("{0}\\pass_first.txt".format(self.datadir)):
            with open("{0}\\pass_first.txt".format(self.datadir), "r") as pass_file:
                passwd = pass_file.read()
        else:
            passwd = ''

        return data.strip(), passwd.strip()

    def unlock_account(self, account, password):
        command = (
            "geth attach {} --exec \"personal.unlockAccount(\\\"{}\\\", \\\"{}\\\")\" ".format(self.http, account,
                                                                                               password))
        result = subprocess.check_output(command, shell=True)

        data = result.decode('utf-8')

    def configure_truffle(self, config_file=None):
        if config_file is not None:
            template_file = config_file
        else:
            template_file = "./pyGeth/truffle-config.txt"
        os.system("cd {} && npx truffle init".format(self.datadir))
        os.system("rm {}\\truffle-config.js".format(self.datadir))
        with open(template_file, 'r') as template_f:
            template = template_f.read()
            template = template.replace('<PORT>', str(self.rpcport))
            template = template.replace('<FROM>', "\"{}\"".format(self.get_first_account()[0]))
            with open('{}\\truffle-config.js'.format(self.datadir), 'w+') as original_config_f:
                original_config_f.write(template)

    def deploy_contract(self, contract_location):
        if not os.path.exists(contract_location):
            print('invalid contract file')
        else:
            os.system('cp {} {}\\contracts'.format(contract_location, self.datadir))
            filename = contract_location.split('\\')[-1]
            contract_name = filename.split('.')[0]
            with open('{}\\migrations\\1_initial_migration.js'.format(self.datadir), 'r+') as migrations_f:
                migrations = migrations_f.read()
                migrations = migrations.split(";")
                new_const = "const {0} = artifacts.require(\"{0}\")".format(contract_name)
                new_deployer = "deployer.deploy({0})".format(contract_name)

                #                 get index of the const's to insert hte new one
                indices = [i for i, s in enumerate(migrations) if 'artifacts.require' in s]
                migrations.insert(indices[0], new_const)

                indices = [i for i, s in enumerate(migrations) if 'deployer.deploy' in s]

                migrations.insert(indices[0] + 1, new_deployer)

                migrations = ";".join(migrations)
                migrations_f.seek(0)
                migrations_f.write(migrations)
                migrations_f.truncate()
            account, password = self.get_first_account()
            self.unlock_account(account, password)
            command = "cd {}\\contracts && npx truffle migrate".format(self.datadir)
            os.system(command)
