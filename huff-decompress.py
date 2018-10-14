# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 05:33:16 2017

@author: Administrator
"""
import pickle
import time
import sys
import getopt

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'ho:i:')
        opts = dict(opts)

        if '-h' in opts:
            self.printHelp()

        if '-o' in opts:
            self.outfile = opts['-o']
        else:
            self.outfile ='infile-decompressed.txt'
        # The default output file is called 'infile-decompressed.txt'
            
        if '-i' in opts:
            self.inputfile = opts['-i']
        else:
            self.inputfile='infile.bin'
        # The default input file is called 'infile.bin'
            
    def printHelp(self):
        help = __doc__.replace('<PROGNAME>',sys.argv[0],1)
        print(help, file=sys.stderr)
        sys.exit()

class Symmodel:
    def __init__(self):
        self.dic={}
        with open("infile-symbol-model.pkl","rb") as f:
            self.dic= pickle.load(f)
            self.dic={v:k for k, v in self.dic.items()}
            # Switch the keys and values of dictionary for decompressing 

    def getmodel(self):
        return (self.dic)
    
class DecompreFile:
    def __init__(self,inputfile):
        self.inputfile=inputfile
        self.result=''
        list1=[]
        string1=''
        string2=''
        number=0
        with open(self.inputfile, "rb") as f:
            byte = f.read(1)
            while(byte != b""):
                list1.append(ord(byte))
                byte = f.read(1)
            for i in list1:
                string1=bin(i)
                string1=string1[2:]
                string1=string1.rjust(8,"0")
                string2+=string1 
       
        number=int(string2[0:8],2)
        string2=string2[:-number]
        string2=string2[8:]        
        self.result=string2
        
    '''
    Read compressed file by one byte to make sure no byte is lost 
    because I put a binary number of adding '0'. Then, converting each byte
    to binary number, adding the enough '0' at the same time.
    Finally, I take the number of adding '0' in the beginning and '0' that added
    at the end out to recover the huffman code string.
    ''' 
          
    def getbinaryfile(self):
        return(self.result)
    
    def decodefile(self,outfile,dic,string):
        self.outfile=outfile
        list1=[]
        x=0
        while True:
            i=0       
            while True:
                i+=1
                if string[x:x+i] in dic.keys():
                    list1.append(dic.get(string[x:x+i]))
                    x=x+i
                    break
            if x==len(string):
                break
        '''
        During decoding file, I choose a slice method to match the key dictionary
        If the program find it, then add related character or word to a list and 
        break this loop. reset the postion of slice
        When the postion is at the end of string, the loop is stop and decompressing
        is finished
        '''
        file=open(self.outfile,'w')
        for item in list1:
            file.write(item)
        file.close()

            
if __name__ == '__main__':
    start = time.clock()
    config = CommandLine()
    symmodel=Symmodel()
    dic=symmodel.getmodel()
    decompress=DecompreFile(config.inputfile)
    string=decompress.getbinaryfile()
    decompress.decodefile(config.outfile,dic,string)
    elapsed = (time.clock() - start)
    print("The decompress file time is:")
    print(elapsed)
