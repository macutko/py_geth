import json
import os


class ContractInterface:
    def __init__(self, w3, datadir):
        """
        Create a contract interface to deploy contracts and interact with them.

        :param w3: web3 object of a node object
        :type: web3 object
        :param datadir: the path to the directory where the contract data will be compiled to
        :type datadir: str
        """
        self.w3 = w3
        self.datadir = datadir

    @staticmethod
    def __get__contract_names(contract_file):
        """
        Helper method to get the name of a contract or multiple names in a single contract file

        :param contract_file: path to the contract file
        :type: str
        :return: names of contracts
        :rtype: list of strings
        """
        r = []
        with open(contract_file) as f:
            lines = f.read().splitlines()
            matching = [s for s in lines if "contract" in s]

            for item in matching:
                item = item.split(" ")
                item = item[1]
                r.append(item)
        return r

    def __amend_migrations(self, contract_names, constructor_params):
        """
        Helper method to ammend the migratiosns file before deployment.

        :param constructor_params: any paramts that contracts expect
        :type: list of strings
        :param contract_names: names of contracts
        :type: list of strings
        """
        if not isinstance(constructor_params, list) and constructor_params is not None:
            raise TypeError("Params of constructor should be passed as list")
        if constructor_params is not None and len(contract_names) != len(constructor_params):
            raise Warning(
                'contract_names and constructor_params should have the same length! If a contract does not need '
                'constructor params pass an empty string in its place')

        with open('{}/migrations/1_initial_migration.js'.format(self.datadir), 'r+') as migrations_f:
            migrations = migrations_f.read()
            migrations = migrations.split(";")
            new_deployer = ''
            new_const = ''

            for i in range(len(contract_names)):
                contract_name = contract_names[i]

                if constructor_params is None:
                    new_deployer += " deployer.deploy({0}) ".format(contract_name)
                else:
                    constructor_param = constructor_params[i]
                    new_deployer += "deployer.deploy({0},\"{1}\"); ".format(contract_name, constructor_param)
                new_const += "const {0} = artifacts.require(\"{0}\"); ".format(contract_name)

            indices = [i for i, s in enumerate(migrations) if 'artifacts.require' in s]
            migrations.insert(indices[0], new_const)

            indices = [i for i, s in enumerate(migrations) if 'deployer.deploy' in s]

            migrations.insert(indices[0] + 1, new_deployer)

            migrations = ";".join(migrations)
            migrations_f.seek(0)
            migrations_f.write(migrations)
            migrations_f.truncate()

    def set_default_account(self):
        """
        Set the default account to use for deployment as the first account created. This is as we expect
        users to create an instance of a node with a genesis file that they have access to.
        """
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]

    def get_contract_from_source(self, source, networkid='1900'):
        """
        Load a contract from a deployed source code. This is if more than 1 node is used.

        :param source: the source code
        :type: file path
        :param networkid: the network id of a running network
        :type: int or str
        """
        with open(source) as f:
            data = json.load(f)
            return self.w3.eth.contract(address=data['networks'][str(networkid)]['address'],
                                        abi=data['abi'])

    def deploy_contract(self, contract_file, constructor_params=None, networkid='1900', default_account=True):
        """
        Deploy a contract to the chain. This expects an account to be unlocked on the chain already.

        :param constructor_params:params for the contract on constructor method
        :type: list of ints or strings
        :param networkid: the network ID of the chain
        :type: string or int
        :param contract_file: the file of the contract to be deployed written in solidity
        :type: string path to file
        :return: tuple of deployed contract objects
        :rtype: tuple
        """
        if not os.path.exists(contract_file):
            raise FileNotFoundError("Cannot find the file specified {}".format(contract_file))
        else:
            os.system('cp {} {}/contracts'.format(contract_file, self.datadir))

            contract_names = self.__get__contract_names(contract_file)

            self.__amend_migrations(contract_names, constructor_params)

            command = "cd {}/contracts && npx truffle migrate".format(self.datadir)
            try:
                os.system(command)
            except Exception as e:
                print('Compilation failed: \n {}'.format(e))

            if default_account:
                self.set_default_account()

            r = []
            for contract in contract_names:
                with open('{}/build/contracts/{}.json'.format(self.datadir, contract)) as f:
                    data = json.load(f)
                    r.append(self.w3.eth.contract(address=data['networks'][str(networkid)]['address'],
                                                  abi=data['abi']))

            return tuple(r)
