import multiprocessing
import random
import time
import threading
import sys
import constants


class Receiver:
    def __init__(self, name, walshTable, channelToReceiver):
        self.name               = name
        self.walshTable         = walshTable
        self.channelToReceiver  = channelToReceiver
        self.senderToReceive    = self.selectSender()
        self.codeLength         = len(self.walshTable[0])
        
    def selectSender(self):
        while(1):
        s = int(input("SELECT A SENDER FOR RECEIVER {}: ".format(self.name+1)))
        if(s<=0 or s>constants.TOT_SENDER):
        print("INVALID SENDER SELECTED! TRY AGAIN")
        else:
        s = s - 1
        break
        return s
    
    def getCharacter(self, data):
        print("Data:" + str(data))
        sum = 0
        for i in range(8):
            sum += pow(2,i)*data[7-i]
        character = chr(sum)
        print("[RECEIVER {}: ] RECEIVED CHARACTER: {}".format(self.name+1, character))
        return character
    
    def openFile(self, sender):
        file = open(constants.OUT_FILE_PATH+'output'+str(sender+1)+'.txt', 'a+')
        return file
    
    def startReceiving(self):
        print("[RECEIVER {}: ] RECEIVING DATA FROM SENDER {}".format(self.name+1,self.senderToReceive+1))
        totalData = []
        while True:
            channelData = self.channelToReceiver.recv()
            # extract data
            summation = 0
            for i in range(len(channelData)):
            summation += channelData[i] * self.walshTable[self.senderToReceive][i]
            # extract data bit
            summation /= self.codeLength
            if summation == 1:
                bit = 1
            elif summation == -1:
                bit = 0
            else: bit = -1
            
            print("[RECEIVER {}: ] RECEIVED BIT: {}".format(self.name+1, bit))

            if len(totalData) < 8 and bit != -1:
                totalData.append(bit)

            if(len(totalData) == 8):
                character = self.getCharacter(totalData)
                outFile = self.openFile(self.name)
                outFile.write(character)
                outFile.close()
                totalData = []
                

    def startReceiver(self):
        t = threading.Thread(name='Receiver', target=self.startReceiving)
        t.start()
        t.join()
