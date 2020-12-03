import os


class ContractInterface:
    def __init__(self, w3, datadir):
        self.w3 = w3
        self.datadir = datadir

    def deploy_contract(self, contract_location):
        """
        Make sure your account is unlocked!
        :param contract_location:
        :return:
        """
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

            command = "cd {}\\contracts && npx truffle migrate".format(self.datadir)
            os.system(command)
