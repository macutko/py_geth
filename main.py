import os

from pyGeth.node import Node


def main():
    """
    This is an example of how to run it. The paths should be local to your device. The documentation will improve through time!
    """
    os.system("rm -rf \"C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node01\"")  # debug purposes
    os.system("rm -rf \"C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node02\"")  # debug purposes
    node1 = Node(datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node01", port=30303,
                 rpcport=8000, name="Node01")
    node1.start_node()

    node2 = Node(datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node02", port=30304,
                 rpcport=8001, name="Node02",
                 genesisFile="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node01\\config\\genesis"
                             ".json")
    node2.start_node()

    ########################################################################

    #     we have 2 nodes running, now lets connect them!
    node1.add_node(node2.get_enode())
    # # node1.start_miner()
    node1.configure_truffle()
    node1.deploy_contract(
        contract_location="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\hello_world.sol")


if __name__ == '__main__':
    main()

    #
    #
    # def _config_truffle(self,config_template=None):
    #     self._check_for_npm()
    #     os.system("cd {} && truffle init".format(self.datadir))
    #
    #     os.system("rm {}\\truffle-config.txt".format(self.datadir))
    #     config = "{ networks: { development: { host: \"127.0.0.1\",port: %s,network_id: \"*\", gas: 621975," \
    #              "from: \"%s\" }}} " % (self.port, self._get_first_account()[0])
    #
    #     with open("{}\\truffle-config.txt".format(self.datadir),
    #               'w+') as write_file:
    #         write_file.write('module.exports={}'.format(config))
    #
    # def unlock_account(self, account, password):
    #     command = "geth attach {0} --exec \"personal.unlockAccount(\\\"{1}\\\", \\\"{2}\\\")\" ".format(self.http,
    #                                                                                                     account,
    #                                                                                                     password)
    #     result = subprocess.check_output(command, shell=True)
    #     data = result.decode('utf-8')
    #     print(data)
    #
    # def deploy_contract(self, contract_location=None):
    #     self._check_for_truffle()
    #     if contract_location is None:
    #         print("We need a contract location!")
    #         return
    #     else:
    #         self._check_for_npm()
    #         filename = contract_location.split('\\')
    #         filename = filename[-1]
    #         contract_name = filename.split('.')
    #         contract_name = contract_name[0]
    #         os.system("cp {} {}".format(contract_location, "{}\\contracts".format(self.datadir)))
    #
    #         with open("{}\\migrations\\1_initial_migration.js".format(self.datadir), "r+") as migrations_file:
    #             migrations = migrations_file.read()
    #             migrations = migrations.split(';')
    #             new_const = 'const {0} = artifacts.require(\"{0}\")'.format(contract_name)
    #
    #             for i in migrations:
    #                 if "deployer.deploy" in i:
    #                     indx = i.index("deployer.deploy")
    #                     new_deployer = i[:indx] + "deployer.deploy({});\n".format(contract_name) + i[indx:]
    #
    #                     indx = migrations.index(i)
    #                     break
    #
    #             migrations.pop(indx)
    #             migrations.insert(indx, new_deployer)
    #             migrations.insert(0, new_const)
    #             migrations_file.seek(0)
    #             migrations_file.truncate()
    #             migrations_file.write(";\n".join(migrations))
    #
    #         account, passwd = self._get_first_account()
    #         self.unlock_account(account, passwd)
    #         os.system("cd {}\\contracts && truffle migrate".format(self.datadir))
