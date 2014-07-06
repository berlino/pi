#!/usr/bin/env python
"""Enhanced Serial Port class
part of pyserial (http://pyserial.sf.net)  (C)2002 cliechti@gmx.net

another implementation of the readline and readlines method.
this one should be more efficient because a bunch of characters are read
on each access, but the drawback is that a timeout must be specified to
make it work (enforced by the class __init__).

this class could be enhanced with a read_until() method and more
like found in the telnetlib.
"""

from serial import Serial
import sys

class EnhancedSerial(Serial):
    def __init__(self, *args, **kwargs):
        #ensure that a reasonable timeout is set
        timeout = kwargs.get('timeout',0.1)
        if timeout < 0.01: timeout = 0.1
        kwargs['timeout'] = timeout
        Serial.__init__(self, *args, **kwargs)
        self.buf = ''
        
    def readline(self, maxsize=None, timeout=1):
        """maxsize is ignored, timeout in seconds is the max time that is way for a complete line"""
        tries = 0
        while 1:
            self.buf += self.read(512)
            begin_pos = self.buf.find('@')
            end_pos=begin_pos+1023
            #if begin_pos >= 0 and end_pos<=len(self.buf) and self.buf[end_pos]=='r':
	    if begin_pos>=0 and end_pos<=len(self.buf):
		line=self.buf[begin_pos:begin_pos+1023]
		self.buf=self.buf[begin_pos+1023:]
                #line, self.buf = self.buf[begin_pos+1:end_pos], self.buf[end_pos+1:]
                #print 'berlin'
                return line
            tries += 1
            if tries * self.timeout > timeout:
                break
	    #print str(tries)+' try '+self.buf
	    #print self.buf.find('@'),self.buf[self.buf.find('@'):].find('r')
        line, self.buf = '', ''
        return line

    def readlines(self, sizehint=None, timeout=1):
        """read all lines that are available. abort after timout
        when no more data arrives."""
        lines = []
	count=1
        while 1:
            line = self.readline(timeout=timeout)
            if line:
                lines.append(line)
		count=count+1
            if not line or count>2:
                break
        return lines

if __name__=='__main__':
    
    #test, only with Loopback HW (shortcut RX/TX pins (3+4 on DSUB 9 and 25) )
    s = EnhancedSerial("/dev/ttyAMA0",baudrate=115200)
    #write out some test data lines
    #s.write('\n'.join("hello how are you".split()))
    #and read them back
 
    result=s.readlines(timeout=1)

    print result
    
    if result:	
    	space_pos=result[0].find(' ')
	length=len(result[0][1:space_pos])+2
	if length>255:
		sound=chr(253)+chr(length/256)+chr(length%256)+chr(1)+chr(1)+result[0][1:space_pos]
	else:
    		sound=chr(253)+chr(0)+chr(length)+chr(1)+chr(1)+result[0][1:space_pos]
    	print len(sound)
	print sound
    	s.write(sound)    



