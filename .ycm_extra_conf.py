import os
import ycm_core

# list of include flags obtained by running: echo | clang -E -v -x c++ -
flags = [
    '-xc++',
    '-std=c++17',
    '-isystem/usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/8.2.1/../../../../include/c++/8.2.1',
    '-isystem/usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/8.2.1/../../../../include/c++/8.2.1/x86_64-pc-linux-gnu',
    '-isystem/usr/bin/../lib64/gcc/x86_64-pc-linux-gnu/8.2.1/../../../../include/c++/8.2.1/backward',
    '-isystem/usr/local/include',
    '-isystem/usr/lib/clang/7.0.0/include',
    '-isystem/usr/include',
]

warnings = [
    '-Wall',
    '-Werror',
    "-Wextra", # reasonable and standard
    "-Wshadow",# warn the user if a variable declaration shadows one from a
    "-Wnon-virtual-dtor", # warn the user if a class with virtual functions has a
                         # non-virtual destructor. This helps catch hard to
                         # track down memory errors
    "-Wold-style-cast", # warn for c-style casts
    "-Wcast-align", # warn for potential performance problem casts
    "-Wunused", # warn on anything being unused
    "-Woverloaded-virtual", # warn if you overload (not override) a virtual
    "-Wpedantic", # warn if non-standard C++ is used
    "-Wconversion", # warn on type conversions that may lose data
    "-Wsign-conversion", # warn on sign conversions
    "-Wmisleading-indentation", # warn if identation implies blocks where blocks
    "-Wduplicated-cond", # warn if if / else chain has duplicated conditions
    "-Wduplicated-branches", # warn if if / else branches have duplicated code
    "-Wlogical-op", # warn about logical operations being used where bitwise were
                   # probably wanted
    "-Wnull-dereference", # warn if a null dereference is detected
    "-Wuseless-cast", # warn if you perform a cast to the same type
    "-Wdouble-promotion", # warn if float is implicit promoted to double
    "-Wformat=2", # warn on security issues around functions that format output
    "-Wlifetime"
    ]

def get_flags(filename):
    result = flags
    flags.append('-I' + os.path.abspath(os.path.dirname(filename)))
    flags.append('-I' +
            os.path.abspath(
                os.path.join(os.path.dirname(filename), '../include')))
    return result + warnings


def FlagsForFile( filename, **kwargs ):
  return {
    'flags': get_flags(filename),
    'do_cache': True
  }

