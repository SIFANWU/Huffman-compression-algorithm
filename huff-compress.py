# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 04:05:04 2017  
@author: Administrator
"""
import re 
import pickle 
import array 
import time
import sys
import getopt,collections

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'hs:o:i:')
        opts = dict(opts)

        if '-h' in opts:
            self.printHelp()

        if '-s' in opts:
            if opts['-s'] in ('char','word'):
                self.method = opts['-s']
            else:
                warning = ('Fail, try again！')
                print(warning, file=sys.stderr)
                self.printHelp()
        else:
            self.method='char'
        #The default symbol-model is char

        if '-o' in opts:
            self.outfile = opts['-o']
        else:
            self.outfile ='infile.bin'
        #The default output filr is called 'infile.bin'
            
        if '-i' in opts:
            self.inputfile = opts['-i']
        else:
            self.inputfile='infile.txt'
        #The default input file is called 'infile.txt'
            
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()


class ReadFile:
    def __init__(self,method,inputfile):
        self.inputfile=inputfile
        self.method=method
        self.list1=[]
        list2=[]
        self.mylist=[]
        
        with open(self.inputfile,"r") as f:
            data = f.read() 
            
        if self.method=='char':
            pattern= re.compile('[a-zA-Z0-9\W]')
            
        elif self.method=='word':
            pattern = re.compile('[\w]+|[\W]')
        # Here are two different patterns one is for character-based 
        # the other is for word-based
        characterlist=pattern.findall(data)
        self.list1=characterlist
        wsf=collections.Counter(characterlist)
        # Calculate the frequency and save as a dictionary 
        
        for key,value in wsf.items():
            list2.append([value,key])
        list2.sort()
        self.mylist=list2
        #convert the dictionary to a list
                      
    def getsortcharacterlist(self):
        return self.mylist
    
    def getoriginallost(self):
        return self.list1
    
class Node:
    def __init__(self,freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq
    def isLeft(self):
        return self.father.left == self
'''
define a class called Node for the huffman tree and its left child, right 
child and father node
 
make a method to make sure this node is the father node's left child
'''    
def createNodes(freqs):
    return [Node(freq) for freq in freqs]

def createHuffmanTree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item:item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_father = Node(node_left.freq + node_right.freq)
        node_father.left = node_left
        node_father.right = node_right
        node_left.father = node_father
        node_right.father = node_father
        queue.append(node_father)
    queue[0].father = None
    return queue[0]
'''
Create a huffmanTree: get the two lowest probability nodes and combine 
them to form a new subtree and add the new node into the list of nodes.
Keep repeating this step until only one node lefts.
'''
def huffmanEncoding(nodes,root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.father
    return codes
'''
If the node is the root then left child is mark with '0', the right child
is marked with '0'.
'''
def Picklingdata(dic):
    with open('infile-symbol-model.pkl', 'wb') as f:
        pickle.dump(dic, f)
# save the dictionary as a key to decompress the file    
class CompressFile:
    def __init__(self,outfile):
        self.outfile=outfile

    def CompressFile(self,list):
        sum=''
        str=''
        string=list
        for item in string:
            sum+=item
        number=8-(len(sum) % 8)
        sum+="0"*number
        str='{0:08b}'.format(number)
        sum=str+sum   
        # Make sure the total number of string can be multiples of eight
        # I add the enough '0' in the end of string and write its binary 
        # number at the beginning for decompressing.
        codearray = array.array('B')
        for i in range(0,len(sum),8):
            c=sum[i:i+8]
            codearray.append(int(c,2))
        f = open(self.outfile, 'wb')
        codearray.tofile(f)
        f.close()
        # Save as a binary file
if __name__ == '__main__':
    start = time.clock()
    config = CommandLine()
    readfile=ReadFile(config.method,config.inputfile)
    finallist=[]
    zipfile=[]
    chars_freqs = readfile.getsortcharacterlist()
    nodes = createNodes([item[0] for item in chars_freqs])
    root = createHuffmanTree(nodes)
    codes = huffmanEncoding(nodes,root)
    
    for item in zip(chars_freqs,codes):
        # frequency :item[0][0]
        # Character :item[0][1]
        # Encoding : item[1]
        #print ("Character:%s freq:%-2d   encoding: %s" % (item[0][1],item[0][0],item[1]))
       finallist.append([item[0][1],item[1]])
       
    dic=dict(finallist)   
    Picklingdata(dic)
    # make the huffman code-tree as a dictionary and save it
    elapsed1 = (time.clock() - start)
    print("The time of building the symbol model:")
    print(elapsed1)
    middle=time.clock()
     
    for item in readfile.getoriginallost():
        if item in dic.keys():
            zipfile.append(dic.get(item))
    # Transform the original file with huffman code       
    compress=CompressFile(config.outfile)
    compress.CompressFile(zipfile)
    # Compress the file 
    elapsed2 = (time.clock() - middle)
    print("The time of encoding the input file given the symbol model:")
    print(elapsed2)  
