# -*- coding: ISO-8859-1 -*-

# standard library imports
from types import StringType
from struct import unpack
from cStringIO import StringIO

# custom import
from DataTypeConverters import writeBew, writeVar, fromBytes

class RawOutstreamFile:
    
    """
    
    Writes a midi file to disk.
    
    """

    def __init__(self, outfile=''):
        self.buffer = StringIO()
        self.outfile = outfile


    # native data reading functions


    def writeSlice(self, str_slice):
        "Reads the next text slice from the raw data, with length"
        self.buffer.write(str_slice)
        
        
    def writeBew(self, value, length=1):
        "Writes a value to the file as big endian word"
        self.writeSlice(writeBew(value, length))


    def writeVarLen(self, value):
        "Writes a variable length word to the file"
        var = self.writeSlice(writeVar(value))


    def write(self):
        "Writes to disc"
        if self.outfile:
            if isinstance(self.outfile, StringType):
                outfile = open(self.outfile, 'wb')
                outfile.write(self.getvalue())
                outfile.close()
            else:
                self.outfile.write(self.getvalue())
                
                
    def getvalue(self):
        return self.buffer.getvalue()


if __name__ == '__main__':

    out_file = 'test/midifiles/midiout.mid'
    rawOut = RawOutstreamFile(out_file)
    rawOut.writeSlice('MThd')
    rawOut.writeBew(6, 4)
    rawOut.writeBew(1, 2)
    rawOut.writeBew(2, 2)
    rawOut.writeBew(15360, 2)
    rawOut.write()
