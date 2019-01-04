import os
import glob
import subprocess

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
    "-Wnull-dereference", # warn if a null dereference is detected
    "-Wdouble-promotion", # warn if float is implicit promoted to double
    "-Wformat=2", # warn on security issues around functions that format output
    ]

# retrieves system includes from compiler
def get_default_includes():
    magic_command = 'clang++ -E -x c++ - -v < /dev/null 2>&1  | egrep "^\s+\/" | sed -e "s/ //g"'
    includes = ["-isystem" + include for include in
                    subprocess.check_output(magic_command, shell=True).splitlines()]
    return includes

def get_default_flags(filename):
    result = get_default_includes()
    result.append('-I' +
            os.path.abspath(
                os.path.join(os.path.dirname(filename), '../include')))
    return result  + ["-xc++", "-std=c++17"] + warnings

def split_on_extension(filename):
    return os.path.splitext(filename)

def is_header_file(extension):
    return extension in [ '.H', '.h', '.hxx', '.hpp', '.hh' ]

# public header are located in lib/include/lib
def is_public_header(header_file):
    return os.path.basename(
            os.path.abspath(
             os.path.join(os.path.dirname(header_file), "../"))) == "include"

def get_name_with_src_dir(public_header_name):
    without_path = os.path.basename(public_header_name)
    return os.path.abspath(os.path.join(os.path.dirname(public_header_name), "../../src" , without_path))

def get_probable_source_file_names(header_name):
    source_extensions = [ '.c', '.cpp', '.cxx' , '.cc', '.C' ]
    if is_public_header(header_name):
        header_name = get_name_with_src_dir(header_name)
    return [header_name + ext for ext in source_extensions]

def get_file_names_to_browse_in_compilation_db(filename):
    without_ext, ext = split_on_extension
    if not is_header_file(ext):
        return [filename] # already a source file
    return get_probable_source_file_names(without_ext)

def get_actual_source_file_to_check(possible_source_names):
    for src_filename in possible_source_names:
        if os.path.exists(src_filename):
            return src_filename
    raise Exception("matching source file not found")

def get_project_root(src_filename):
    return os.path.abspath(os.path.join(os.path.dirname(src_filename), "../../"))

def find_db_from_root(project_root_dir):
    dbs = glob.glob(project_root_dir + "/build*/compile_commands.json")
    if dbs:
        db = ymc_core.CompilationDatabase(os.path.dirname(dbs[0]))
    if not db:
        raise Exception("No valid db found")
    return db

def get_db(src_filename):
    project_root_dir = get_project_root(src_filename)
    return find_db_from_root(project_root_dir)

def fixed_relative_flags(flags, working_directory):
  if not working_directory:
    return list( flags )
  new_flags = []
  make_next_absolute = False
  path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
  for flag in flags:
    new_flag = flag

    if make_next_absolute:
      make_next_absolute = False
      if not flag.startswith( '/' ):
        new_flag = os.path.join( working_directory, flag )

    for path_flag in path_flags:
      if flag == path_flag:
        make_next_absolute = True
        break

      if flag.startswith( path_flag ):
        path = flag[ len( path_flag ): ]
        new_flag = path_flag + os.path.join( working_directory, path )
        break

    if new_flag:
      new_flags.append( new_flag )
  return new_flags

def get_info_from_db(actual_src):
    comptilation_db = get_db(actual_src)
    raw_flags = compilation_db.GetCompilationInfoForFile(actual_src)
    if not raw_flags:
        raise Exception("No flags available in db for file.")
    return fixed_relative_flags(raw_flags,
            compilation_info.compiler_working_dir_)

def get_flags(filename):
    try:
        possible_src_names = get_file_names_to_browse_in_compilation_db(filename)
        actual_src = get_actual_source_file_to_check(possible_src_names)
        return get_default_includes() + get_info_from_db(actual_src)
    except Exception:
        return get_default_flags(filename)

def FlagsForFile (filename, **kwargs):
    return {
      'flags': get_flags(filename),
      'do_cache': True
    }

