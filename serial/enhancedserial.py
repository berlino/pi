#!/usr/bin/env python
import sys
from serial import Serial
import sqlite3

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
            end_pos=self.buf.find('xww');
	    if begin_pos>=0 and end_pos>0:
		line=self.buf[begin_pos+1:end_pos]
		self.buf=self.buf[end_pos+4:]
                return line
            tries += 1
            if tries * self.timeout > timeout:
                break
	    #print str(tries)+' try '+self.buf
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
    
    s = EnhancedSerial("/dev/ttyAMA0",baudrate=115200)
 
    result=s.readlines(timeout=1)

    print result
    
    if result:	
	conn=sqlite3.connect('vics.db')
    	c=conn.cursor()
    	for i in range(6):
		block=int(result[2*i])
		state=int(result[2*i]+1)
		c.execute("update entries set state=? where block=?",[state,block])
		conn.commit()
    
    	parking=int(result[12])
    	park_num=int(result[13])
    	c.execute("update entries set park_num=? where parking=?",[park_num,parking])
    	conn.commit()

	cur=c.execute("select * from entries")
    	print cur.fetchall()

	length=len(result[14:])
	if length>255:
		sound=chr(253)+chr(length/256)+chr(length%256)+chr(1)+chr(1)+result[0][14:]
	else:
    		sound=chr(253)+chr(0)+chr(length)+chr(1)+chr(1)+result[0][14:]
    	print len(sound)
	print sound
    	s.write(sound)    



