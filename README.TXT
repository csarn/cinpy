cinpy - write C in Python


Dependencies
------------

TCC	Tiny C Compiler, well... at least libtcc.so
	http://fabrice.bellard.free.fr/tcc/

ctypes	Python module for easy usage of dll's
	http://starship.python.net/crew/theller/ctypes/


Installation
------------

Install the required software (tcc and ctypes). Note that you may have
to link libtcc.so by yourself. To do so, go to the directory with tcc
sources and run:

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

