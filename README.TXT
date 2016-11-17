cinpy - write C in Python


Dependencies
------------

TCC	Tiny C Compiler, well... at least libtcc.so
	http://bellard.org/tcc/

Installation
------------

Install the required software (tcc). Download from link above, extract,
and run:

./configure --disable-static 
make

Then copy libtcc.so to appropriate place, for example to the directory
that contains cinpy.py or to /usr/local/lib, or run (sudo) make install.

Once they are installed, run "python cinpy.py" to execute the cinpy
module test. If all tests passed, cinpy is ready for use.


Benchmarking
------------

cinpy_test.py is a very small benchmark program. It reports the time
required to execute the same functions written in Python and in C.



Authors
-------

This seems to be originally from Antti Kervinen (ask@cs.tut.fi),
see
http://www.redditmirror.cc/cache/websites/www.cs.tut.fi_7ea3v/www.cs.tut.fi/_ask/cinpy/index.html

