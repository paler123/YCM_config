import unittest
from ycm_extra_conf import *

class FileNameParsingMethods(unittest.TestCase):

    def test_recognizes_header_extension(self):
        self.assertTrue(is_header_file(".hpp"))
        self.assertTrue(is_header_file(".hh"))
        self.assertTrue(is_header_file(".hxx"))
        self.assertFalse(is_header_file(".cpp"))

    def test_recognizes_public_headers(self):
        self.assertTrue(is_public_header("/usr/lib/include/lib/header"))
        self.assertTrue(is_public_header("/opt/lib/include/some_fancy_lib/header"))
        self.assertFalse(is_public_header("/home/usr/lib/src/header"))

    def test_properly_substitutes_src_dir_into_public_headers(self):
        self.assertEqual("/usr/lib/src/header",
                get_name_with_src_dir("/usr/lib/include/lib/header"))

    def test_produces_correct_list_of_source_file_suggestions_for_header(self):
        self.assertIn("/usr/lib/src/filename.cpp",
                      get_probable_source_file_names("/usr/lib/src/filename"))
        self.assertIn("/usr/lib/src/filename.cpp",
                      get_probable_source_file_names("/usr/lib/include/lib/filename"))

    def test_finds_root_given_src_file(self):
        self.assertEquals("/usr/lib/include/project",
                          get_project_root("/usr/lib/include/project/lib/src/filename"))

if __name__ == "__main__":
    unittest.main()
