from web3 import Web3, constants

ALLOWANCE = {
    "inputs": [
        {"internalType": "address", "name": "owner", "type": "address"},
        {"internalType": "address", "name": "spender", "type": "address"}
    ],
    "name": "allowance",
    "outputs": [
        {"internalType": "uint256", "name": "", "type": "uint256"}
    ],
    "stateMutability": "view",
    "type": "function"
}
APPROVE = {
    'inputs': [
        {'internalType': 'address', 'name': '_spender', 'type': 'address'},
        {'internalType': 'uint256', 'name': '_tokens', 'type': 'uint256'}
    ],
    'name': 'approve',
    'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}],
    'stateMutability': 'nonpayable',
    'type': 'function'
}
BALANCEOF = {
    'inputs': [
        {'internalType': 'address', 'name': '_user', 'type': 'address'}
    ],
    'name': 'balanceOf',
    'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
    'stateMutability': 'view',
    'type': 'function'
}

def transfer_eth(w3:Web3, pk, to_address, value, chainid):
    account = w3.eth.account.from_key(pk) 
    tx = {
        'to':to_address,
        'gasPrice': w3.eth.gasPrice,
        'gasLimit': 21000,
        'data':b'',
        'value':value,
        'chainId': chainid, 
    }     
    signed_txn = w3.eth.account.sign_transaction(dict(
        to=bytes.fromhex(tx['to'][2:]),
        gasPrice=int(tx['gasPrice']),
        gas=int(tx['gasLimit']),
        data=tx['data'],
        nonce=w3.eth.getTransactionCount(account.address),
        value=int(tx['value']),
        chainId=chainid,
    ), pk)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"转账交易发送成功")
    print(w3.toHex(tx_hash))
    freceipt = w3.eth.waitForTransactionReceipt(tx_hash, 30000)
    print(f"转账 {freceipt.status}")
    return True
    
def get_eth_bal(w3:Web3, address):
    return Web3.fromWei(w3.eth.getBalance(address), 'ether')
    
def get_bal(w3:Web3, address, token_address):
    token_con = w3.eth.contract(address=constants.ADDRESS_ZERO, abi=[APPROVE, BALANCEOF, ALLOWANCE])
    return token_con.functions.balanceOf(address).call({'to': token_address})

def approve_token(w3:Web3, chainid, pk, token_address, swap_add, value, multiplier=100):
    account = w3.eth.account.from_key(pk) 
    token_con = w3.eth.contract(address=constants.ADDRESS_ZERO, abi=[APPROVE, BALANCEOF, ALLOWANCE])
    token_allowance = token_con.functions.allowance(account.address, w3.toChecksumAddress(swap_add)).call({'to': token_address})
    print('token_allowance:', token_allowance)
    if token_allowance > value:
        print(f"{token_address}授权额度足够，无需再次授权")
        return True    
    else:
        tx = token_con.functions.approve(w3.toChecksumAddress(swap_add), value*multiplier).buildTransaction({
            'from': account.address,
            'chainId': chainid,
            'gas': 1000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address)
        })
        tx['to'] = token_address
        estimateGas = w3.eth.estimateGas(tx)
        tx['gas'] = int(estimateGas * 1.3)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=pk)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"授权{token_address}发送 成功")
        freceipt = w3.eth.waitForTransactionReceipt(tx_hash, 3000)
        if freceipt.status == 1:
            print(f"授权{token_address}成功")
            return True    
        else:
            print(f"授权{token_address}交易 失败")
            return False    

def get_allowance(w3:Web3, address, token_address, swap_add):
    token_con = w3.eth.contract(address=constants.ADDRESS_ZERO, abi=[APPROVE, BALANCEOF, ALLOWANCE])
    token_allowance = token_con.functions.allowance(address, swap_add).call({'to': token_address})
    return token_allowance
