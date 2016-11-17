#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import ctypes
import cinpy
import time
from six.moves import range

fibc=cinpy.defc("fib",ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int),
          """
          int fib(int x) {
              if (x<=1) return 1;
              return fib(x-1)+fib(x-2);
          }
          """)

def fibpy(x):
    if x<=1: return 1
    return fibpy(x-1)+fibpy(x-2)

forc=cinpy.defc("forc",ctypes.CFUNCTYPE(ctypes.c_int,ctypes.c_int),
          """
          int forc(int x) {
              int z=0;
              int i=0;
              for (i=0;i<x;i++)
                  z++;
              return z;
          }
          """)

def forpy(x):
    z=0
    for i in range(x):
       z+=1
    return z

t=time.time

print("Calculating fib(32)...")
sc,rv_fibc,ec=t(),fibc(32),t()
sp,rv_fibpy,ep=t(),fibpy(32),t()
print("fibc :",rv_fibc,"time: %6.5f s" % (ec-sc))
print("fibpy:",rv_fibpy,"time: %6.5f s" % (ep-sp))

print("Calculating for(1000000)...")
sc,rv_forc,ec=t(),forc(1000000),t()
sp,rv_forpy,ep=t(),forpy(1000000),t()
print("forc :",rv_forc,"time: %6.5f s" % (ec-sc))
print("forpy:",rv_forpy,"time: %6.5f s" % (ep-sp))
