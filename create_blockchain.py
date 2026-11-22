from justblockchain import justblockchain
from pprint import pprint

import secrets

def generate_random_hash():
    return secrets.token_hex(32)

def create_blockchains(list_of_strings):
    dict_of_strings = {}
    IS_PRESENT = True
    for string in list_of_strings:
        dict_of_strings[string] = IS_PRESENT
    list_of_strings = sorted(list(dict_of_strings.keys()))
    blockchain = justblockchain.Blockchain()
    for string in list_of_strings:
        blockchain.add_block(string)
    blockchains = blockchain.chain[1:]
    first_blockchain_non_existent_hash = blockchains[0]['previous_hash']
    first_blockchain_non_existent_hash = generate_random_hash()
    blockchains[0]['previous_hash'] = first_blockchain_non_existent_hash
    return blockchains

if __name__=="__main__":
    list_of_strings = ["a","b","bb","a","a","c"]
    blockchains = create_blockchains(list_of_strings)
    pprint(blockchains)
    pprint(len(blockchains))
