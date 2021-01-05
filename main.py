import os

from pyGeth.contract_interface import ContractInterface
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
    node1.add_node(node2.w3.geth.admin.node_info()['enode'])

    node1.w3.geth.miner.start(1)

    node1.configure_truffle()
    account, password = node1.get_first_account()
    node1.w3.geth.personal.unlock_account(account, password)

    CI = ContractInterface(w3=node1.w3,
                           datadir="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\auto_gen\\node01")

    m_con = CI.deploy_contract(
        contract_file="C:\\Users\\matus\\Desktop\\Uni\\lvl_5\\disseration\\py-geth\\GUID.sol",
        constructor_params=['2265072m'])[0]
    print(m_con)

    tx_hash = m_con.functions.setGrade("B3", "CSAI").transact()
    tx_receipt = CI.w3.eth.waitForTransactionReceipt(tx_hash)
    print(m_con.functions.getGrade("CSAI").call())
    print(m_con.functions.getID().call())


if __name__ == '__main__':
    main()
