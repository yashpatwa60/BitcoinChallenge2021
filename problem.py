# I have used (0-1)knapsack technique to solve this problem
# although this method is expensive due to array intialisation
# If best possible combination wasn't a issue we could have sorted the (MempoolTransaction)objects in decresing order and added to 
# the block.

class MempoolTransaction():

    def __init__(self, txid, fee, weight, parents):
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = parents
      


def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""

    with open('mempool.csv') as f:
        next(f)                     #leaving the title row
        return ([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])


def knapsack():
    list = parse_mempool_csv()       
    items = len(list)                 
    capacity= 40000000

    ks = [[0]*(capacity+1) for i in range(items+2)]           #knapsack array intialisation

    #knapsack Implementation
    for i in range(1,items+1):

        for j in range(1,capacity+1):

            if  list[i-1].weight < j  and list[i-1].fee + ks[i-1][j-list[i-1].weight] > ks[i-1][j]:
                ks[i][j] = list[i-1].fee + ks[i-1][j-list[i-1].weight]

            else:
                ks[i][j] = ks[i-1][j]

    
    max_total = ks[items][capacity]                       #maximum possible total profit

    file1 = open('block.txt', 'w')

    #Backtracking knapsack
    for k in range(items-1,0,-1):
        if max_total>=0 and capacity>=0:
            if max_total == ks[k-1][capacity]:             
                continue

            else:
                if list[k-1].parents == '':                 #If parent list is empty
                    file1.write(list[k-1].txid + '\n')
                else:                                       #If parnet list have pending transactions
                    parent_list = list[k-1].parents.split(';')
                    for i in range(len(parent_list)-1,0,-1):
                        file1.write(parent_list[i] + '\n')         #First write old parent transactions 

                    file1.write(list[k-1].txid + '\n')             #secondly write the txid
                    max_total = max_total - list[k-1].fee
                    capacity = capacity - list[k-1].weight
        else:
            break




knapsack()


# If you are getting memory error this might be due to processor speed
# reduse capacity or number of items
# or
# f.readlines()[0:500]

  

