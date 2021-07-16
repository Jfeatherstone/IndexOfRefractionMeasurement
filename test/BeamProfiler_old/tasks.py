import cffi

print("Building CFFI Module for Beam Profiler")

ffi = cffi.FFI()

sourceDir = r'resources' # For this directory

hFileFullPath = sourceDir + '\\' + 'TLBP2.h'

with open(hFileFullPath) as hFile:
    ffi.cdef(hFile.read())

ffi.set_source(
        'TLBP2W',
        # Include all of the necessary imports
        '#include <iostream>',
        # And libraries
        libraries=["iostream"],
        library_dirs=[sourceDir],
        extra_link_args=['-Wl,-rpath,.'],
        )

ffi.compile() 
