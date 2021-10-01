import multiprocessing
import random
import time
import threading
import constants
import os


class Sender:
    def __init__(self, name, walshCode, senderToChannel):
        self.name               = name
        self.senderToChannel    = senderToChannel 
        self.walshCode          = walshCode # tuple containg the walshCode
   
   
    def fileLength(self, sender):
        path = constants.IN_FILE_PATH+'input'+str(sender+1)+'.txt'
        size = os.path.getsize(path)
        return size

    
    def startSending(self):
        startTime = time.time()
        totBy = self.fileLength(self.name)
        file = self.openFile(self.name)

        totalBitSent = 0
        byte = file.read(constants.DATA_PACK_SIZE)
        while byte:

            # send the data bits of byte
            data = '{0:08b}'.format(ord(byte))
            for i in range(len(data)):
                dataToSend = []
                dataBit = int(data[i])
                if dataBit == 0: dataBit = -1
               

                for j in self.walshCode:
                    dataToSend.append(j * dataBit)
                self.senderToChannel.send(dataToSend)
                print("[SENDER {}: ] DATA BIT SENT: {} ...........".format(self.name+1, dataBit))
                time.sleep(1)

            byte = file.read(constants.DATA_PACK_SIZE)
        
        print("[SENDER {}: ] THE ENTIRE DATA HAS BEEN SUCCESSFULLY TRANSMITTED......".format(self.name + 1))
        endTime = time.time()
        totTime = endTime - startTime
        print("\n!---------------------------------SHOW STATS------------------------------------------!\n")
        print("\n______________________SENDER {}_________________________\n".format(self.name+1))
        print("\nTOTAL BYTES SENT: {}\nTIME REQUIRED FOR THE ENTIRE TRANSMISSION: {}\n".format(totBy,totTime))
        print("\n!-------------------------------------------------------------------------------------!\n")
        
    

    def startSender(self):
        senderThread = threading.Thread(name="sender"+str(self.name+1),
                                        target=self.startSending)
        
        senderThread.start()
        senderThread.join()
        
