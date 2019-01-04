# YCM_config
This is what I hope to use as my go to ycm_extra_conf.py, featuring:
* compile_commands.json utilisation (with flags for headers extracted based on project layout convention)
* default set of flags whenever compilation database is unavailable
* extraction of system includes from clang++

## How to use it
Download, set the value of ycm_global_extra_conf to the downloaded file.  
For everything to work as intended without modification you'll need clang++ installed, and additionally layout the projects in the following manner:
```Bash
    project_root
    ├── build # build directory, name has to start with build
    │   └── compile_commands.json # will also be found in build/debug, buildRel/whatever_arch/etc
    └── target1 # can have multiple targets 
        ├── include
        │   └── target1 # public headers, so that if you include target1/include, you address headers by e.g. target1/public.hpp
        │       └── public.hpp # this header will be matched with project_root/target1/src/public.hpp
        ├── src # all the implementation goes here
        │   ├── private.cpp
        │   ├── private.hpp
        │   └── public.cpp
        └── test


```
You can of course use it without compilation database (e.g. for quick "hello world" type of things) --> 
 stl headers will be found, some sane warnings set, workdir will be included.

## License
MIT
