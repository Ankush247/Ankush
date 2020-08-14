import hashlib
import json
from datetime import datetime
from flask import Flask
from flask import jsonify
from time import  time
class Block():
    def __init__(self,nonce,tstamp,transactionsList,prevhash='',hash=''):
        self.nonce=nonce
        self.tstamp=tstamp
        self.transactionsList=transactionsList
        self.prevhash=prevhash
        if hash == '':
            self.hash=self.calcHash()
        else:
            self.hash=hash
    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"tstamp":str (self.tstamp),"transaction":self.transactionsList,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != str('').zfill(diffic)):
            self.nonce += 1
            self.hash=self.calcHash()
        print("Block mined",self.hash)
    def toDict(self):
        return{"nonce":self.nonce,"tstamp":str(self.tstamp),"transactionsList":self.transactionsList,"prevhash":self.prevhash,"hash":self.hash}

class BlockChain():
    def __init__(self):
        self.chain=[]
        self.pendingTransactions=[]
        self.mining_reward = 100
        self.difficulty= 3
        self.generateGenesisBlock()
    def generateGenesisBlock(self):
        dict={"nonce":0,"tstamp":'07/08/2020',"transactionsList":[{"from_address":None , "to_address":None,"amount":0},],"hash":''}
        b=Block(**dict)
        self.chain.append(b.toDict()) 
    def getLastBlock(self):
        return Block(**self.chain[-1])
    def minePendingTransaction(self,mining_reward_address):
        block=Block(0,str(datetime.now()),self.pendingTransactions)
        block.prevhash=self.getLastBlock().hash
        block.mineBlock(self.difficulty)
        print("block is mined and you got the reward",self.mining_reward)
        self.chain.append(block.toDict())
        self.pendingTransactions=[{"from_address":None,"to_address":mining_reward_address,"amount":self.mining_reward},]

    def createTransaction(self,from_address,to_address,amount):
        self.pendingTransactions.append({'from_address':from_address,'to_address':to_address,'amount':amount})  
    def getBalance(self,address):
        balance = 1000
        for index  in range (len(self.chain)):
            dictList=self.chain[index]["transactionsList"]
            for dic in dictList:
                if dic ["to_address"] == address:
                    balance += t.amount
                if dic ["from_address"] == address:
                    balance -= t.amount
        return balance

    def isChainValid(self):
        for i in range(1,len(self.chain)):
            prevb=Block(**self.chain[i-1])
            currb=Block(**self.chain[i])
            if(currb.hash != currb.calcHash()):
                print("invalid block")
                return False
            if(currb.prevhash != prevb.hash):
                print("invalid chain")
                return False
        return True

rupee=BlockChain()

rupee.createTransaction('address1','address2',300)
rupee.createTransaction('address2','address1',200)

print("starting mining")
rupee.minePendingTransaction("ankushaddress")
print("Ankush miner balance is ",rupee.getBalance("ankushaddress"))
print(rupee.isChainValid())

app = Flask(__name__)

@app.route("/mine",methods=['GET'])
def mine():
    return "we are going to mine the block with new transactions here"
 
@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    return None

@app.route("/chain",methods=['GET'])
def display_full_chain():
    response={
        'chain':rupee.chain,
        'length':len(rupee.chain)
    }
    return jsonify(response)

@app.route("/")
def hello():
    return "Hello you are in the main page of this node"

if __name__ =="__main__":
    app.run()

