#!/usr/bin/env python

# Copyright (C) 2005 Antti Kervinen, ask@cs.tut.fi.
#
# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301
# USA

"""
write C functions in Python code

Simple example: recursive implementation for fibonacci numbers

>>> import ctypes
>>> import cinpy

>>> fibonacci=cinpy.defc(\"fibc\",
...                      ctypes.CFUNCTYPE(ctypes.c_long,ctypes.c_int),
...                      \"\"\"
...                      long fibc(int x) {
...                          if (x<=1) return 1;
...                          return fibc(x-1)+fibc(x-2);
...                      }
...                      \"\"\")
>>> fibonacci(30)
1346269
"""

from __future__ import absolute_import
from __future__ import print_function
import ctypes
import os
import sys
import platform

version="0.10"

# try to load libtcc.so

_libtcc=None

def load_libtcc(file_and_path_to_tcclib=None):
    """If you wish to specify exactly which file is the dynamically
    loadable tcc library, call this function before calling defc. If
    this function has not been called before the first call of defc,
    libtcc.so is tried to be located from 'the usual' directories in
    addition to the directories mentioned in LD_LIBRARY_PATH.
    """
    global _libtcc

    if file_and_path_to_tcclib:
        _libtcc=ctypes.cdll.LoadLibrary(file_and_path_to_tcclib)
        return 1

    ldlibpath=os.getenv("LD_LIBRARY_PATH","").split(":")
    ldlibpath.extend([".",
                      os.path.dirname(__file__),
                      "/usr/local/lib/tcc","/usr/local/lib","/usr/lib",
                      "/opt/local/lib/tcc","/opt/local/lib","/opt/lib",
                      "/lib"])
    extension = 'dll' if platform.system() == 'Windows' else 'so'
    for path in ldlibpath:
        try:
            _libtcc=ctypes.cdll.LoadLibrary("%s/libtcc.%s" % (path, extension))
            return 1
        except OSError:
            pass
    raise ImportError("libtcc is not loaded\n")

def _req0(funname,retval):
    if retval!=0:
        raise ValueError("%s returned error code %s." % (funname,retval))

def defc(fun_name,fun_prototype,c_code):
    """Returns the function that appeared in c_code as fun_name. The
    c_code may contain also other functions, but they cannot be called
    directly from Python."""
    if not _libtcc: load_libtcc()
    # compile
    tccstate=_libtcc.tcc_new()
    _req0("tcc_set_output_type",
          _libtcc.tcc_set_output_type(tccstate,0))
    _req0("tcc_compile_string",
          _libtcc.tcc_compile_string(tccstate,c_code.encode('ascii')))
    _req0("tcc_relocate",
          _libtcc.tcc_relocate(tccstate, 1))

    # get the result
    p = _libtcc.tcc_get_symbol(tccstate,fun_name.encode('ascii'))
    assert p != 0
    return fun_prototype(p)


class C:
    """wrapper class that automatically deducts the function type
    from the c code."""

    def __init__(self, code):
        self.code = code
        self.defc()

    def defc(self):
        import pycparser
        lookup = {
            'float': ctypes.c_float,
            'unsigned char': ctypes.c_uint8,
            'char': ctypes.c_int8,
            'unsigned short': ctypes.c_ushort,
            'short': ctypes.c_short,
            'unsigned int': ctypes.c_uint,
            'int': ctypes.c_int,
            'unsigned long': ctypes.c_ulong,
            'long': ctypes.c_long,
            'unsigned long long': ctypes.c_ulonglong,
            'long long': ctypes.c_longlong,
            'double': ctypes.c_double,
        }
        p = pycparser.c_parser.CParser()
        self.ast = ast = p.parse(self.code)
        for func in ast.ext:
            if not isinstance(func, pycparser.c_ast.FuncDef):
                continue
            name = func.decl.name
            retval = ' '.join(func.decl.type.type.type.names)
            args = [retval] + [' '.join(x.type.type.names)
                               for x in func.decl.type.args.params]
            functype = ctypes.CFUNCTYPE(*[lookup[x] for x in args])
            func_obj = defc(name, functype, self.code)
            setattr(self, name, func_obj)
            # func_obj.__doc__ = self.code.split('\n')[func.coord.line+1]
            # func_obj.__str__ = lambda self: '<CFunction: {}>'.format(self.__doc__)
            # func_obj.__repr__ = func_obj.__str__


if __name__=='__main__': # test:

    print("**** cinpy module test")


    test,verdict="Load libtcc","FAIL"
    try:
        load_libtcc()
        verdict="PASS"
    except ImportError:
        print(verdict,test)
        print("Make sure that libtcc.so is in LD_LIBRARY_PATH")
        print("or in the current directory.")
        print("You may have to link it by yourself from tcc sources:")
        print("First run 'make libtcc.o', then")
        print("'gcc -shared -Wl,-soname,libtcc.so -o libtcc.so libtcc.o'")
        print("Cannot continue module test.")
        sys.exit(1)
    print(verdict,test)


    test,verdict="Define a function in C","FAIL"
    try:
        testfun=defc("testfun",ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int),
                  """
                  int testfun(int x) {
                      return x+42;
                  }
                  """)
        verdict="PASS"
    except ValueError as e:
        print(verdict,test)
        print("FAIL: tcc returned an error:",str(e))
        print("Cannot continue module test.")
        sys.exit(1)
    print(verdict,test)


    test,verdict="Call the function and check the return value","FAIL"
    try:
        if testfun(43)==85: verdict="PASS"
    finally:
        print(verdict,test)
