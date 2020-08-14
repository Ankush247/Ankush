import hashlib
import json
from datetime import datetime
class Transaction():
    def __init__(self,from_address,to_address,amount):
        self.from_address = from_address
        self.to_address=to_address
        self.amount=amount
class Block():
    def __init__(self,tstamp,transactionsList,prevhash=''):
        self.nonce=0
        self.tstamp=tstamp
        self.transactionsList=transactionsList
        self.prevhash=prevhash
        self.hash=self.calcHash()
    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"tstamp":str (self.tstamp),"transaction":self.transactionsList[0].amount,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != str('').zfill(diffic)):
            self.nonce += 1
            self.hash=self.calcHash()
        print("Block mined",self.hash)
    def __str__(self):
        string= "nonce:" + str(self.nonce) + "\n"
        string += "tstamp:" + str(self.tstamp) + "\n"
        string += "transaction:" + str(self.transaction) + "\n"
        string += "prevhash:" +str(self.prevhash) + "\n"
        string += "hash:" + str(self.hash) + "\n"

        return string

class BlockChain():
    def __init__(self):
        self.chain=[self.generateGenesisBlock(),]
        self.pendingTransactions=[]
        self.mining_reward = 100
        self.difficulty= 2
    def generateGenesisBlock(self):
        return Block('07/08/2020',[Transaction(None,None,0)])
    def getLastBlock(self):
        return self.chain[-1]
    def minePendingTransaction(self,mining_reward_address):
        block=Block(datetime.now(),self.pendingTransactions)
        block.mineBlock(self.difficulty)
        print("block is mined and you got the reward",self.mining_reward)
        self.chain.append(block)
        self.pendingTransactions=[Transaction(None,mining_reward_address,self.mining_reward)]

    def createTransaction(self,T):
        self.pendingTransactions.append(T)  
    def getBalance(self,address):
        balance = 0
        for b in self.chain:
            for t in b.transactionsList:
                if t.to_address == address:
                    balance += t.amount
                if t.from_address == address:
                    balance += t.amount
        return balance

    def isChainValid(self):
        for i in range(1,len(self.chain)):
            prevb=self.chain[i-1]
            currb=self.chain[i]
            if(currb.hash != currb.calcHash()):
                print("invalid block")
                return False
            if(currb.prevhash != prevb.hash):
                print("invalid chain")
                return False
        return True

rupee=BlockChain()

rupee.createTransaction(Transaction('address1','address2',100))
rupee.createTransaction(Transaction('address2','address1',200))
print("starting mining")
rupee.minePendingTransaction("ankushaddress")
print("Ankush miner balance is ",rupee.getBalance("ankushaddress"))


rupee.createTransaction(Transaction('address1','address2',250))
rupee.createTransaction(Transaction('address2','address1',300))
print("starting mining")
rupee.minePendingTransaction("ankushaddress")
print("Ankush miner balance is ",rupee.getBalance("ankushaddress"))

rupee.createTransaction(Transaction('address1','address2',350))
rupee.createTransaction(Transaction('address2','address1',400))
print("starting mining")
rupee.minePendingTransaction("ankushaddress")
print("Ankush miner balance is ",rupee.getBalance("ankushaddress"))