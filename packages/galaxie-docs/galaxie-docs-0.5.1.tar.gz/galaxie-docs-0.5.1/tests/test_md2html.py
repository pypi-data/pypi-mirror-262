#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Docs Team, all rights reserved

import unittest
from glxdocs.md2html import Md2Html
import os
import codecs


class TestDocs(unittest.TestCase):

    def setUp(self):
        self.md2html = Md2Html()
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.md_file = os.path.join(self.cwd, 'README.md')
        self.html_file = os.path.join(self.cwd, 'README.html')

    def test_lang(self):
        self.assertEqual('en', self.md2html.lang)
        self.md2html.lang = None
        self.assertEqual('en', self.md2html.lang)

        self.assertRaises(TypeError, setattr, self.md2html, 'lang', 42)

    def test_charset(self):
        self.assertEqual('utf-8', self.md2html.charset)
        self.md2html.charset = None
        self.assertEqual('utf-8', self.md2html.charset)

        self.assertRaises(TypeError, setattr, self.md2html, 'charset', 42)

    def test_src_dirname(self):
        self.md2html.src_dirname = None
        self.assertIsNone(self.md2html.src_dirname)

        self.md2html.src_dirname = os.environ['HOME']
        self.assertEqual(os.environ['HOME'], self.md2html.src_dirname)
        self.md2html.src_dirname = None
        self.assertIsNone(self.md2html.src_dirname)

        self.assertRaises(TypeError, setattr, self.md2html, 'src_dirname', 42)
        self.assertRaises(FileNotFoundError, setattr, self.md2html, 'src_dirname', '42')
        self.assertRaises(NotADirectoryError, setattr, self.md2html, 'src_dirname', '/etc/hosts')

    def test_src_base_name(self):
        self.md2html.src_basename = None
        self.assertIsNone(self.md2html.src_basename)
        self.md2html.src_basename = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.src_basename)
        self.md2html.src_basename = None
        self.assertIsNone(self.md2html.src_basename)

        self.assertRaises(TypeError, setattr, self.md2html, 'src_basename', 42)

    def test_src_base_extension(self):
        self.md2html.src_extension = None
        self.assertIsNone(self.md2html.src_extension)
        self.md2html.src_extension = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.src_extension)
        self.md2html.src_extension = None
        self.assertIsNone(self.md2html.src_extension)

        self.assertRaises(TypeError, setattr, self.md2html, 'src_extension', 42)

    def test_dst_base_dir(self):
        self.assertIsNone(self.md2html.dst_dirname)
        self.md2html.dst_dirname = os.environ['HOME']
        self.assertEqual(os.environ['HOME'], self.md2html.dst_dirname)
        self.md2html.dst_dirname = None
        self.assertIsNone(self.md2html.dst_dirname)

        self.assertRaises(TypeError, setattr, self.md2html, 'dst_dirname', 42)
        self.assertRaises(FileNotFoundError, setattr, self.md2html, 'dst_dirname', '42')
        self.assertRaises(NotADirectoryError, setattr, self.md2html, 'dst_dirname', '/etc/hosts')

    def test_dst_base_name(self):
        self.assertIsNone(self.md2html.dst_basename)
        self.md2html.dst_basename = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.dst_basename)
        self.md2html.dst_basename = None
        self.assertIsNone(self.md2html.dst_basename)

        self.assertRaises(TypeError, setattr, self.md2html, 'dst_basename', 42)

    def test_dst_base_extension(self):
        self.assertIsNone(self.md2html.dst_extension)
        self.md2html.dst_extension = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.dst_extension)
        self.md2html.dst_extension = None
        self.assertIsNone(self.md2html.dst_extension)

        self.assertRaises(TypeError, setattr, self.md2html, 'dst_extension', 42)

    def test_input_file(self):
        self.md2html.input_file = codecs.open(self.md_file,
                                           mode="r",
                                           encoding="utf-8"
                                           )
        self.assertTrue(isinstance(self.md2html.input_file, codecs.StreamReaderWriter))
        self.md2html.input_file.close()

        self.assertRaises(TypeError, setattr, self.md2html, 'input_file', 42)

    def test_output_file(self):
        self.md2html.output_file = codecs.open(self.html_file,
                                            "w",
                                            encoding="utf-8",
                                            errors="xmlcharrefreplace"
                                            )

        self.assertTrue(isinstance(self.md2html.output_file, codecs.StreamReaderWriter))
        self.md2html.output_file.close()

        self.assertRaises(TypeError, setattr, self.md2html, 'output_file', 42)

        if os.path.exists(self.html_file):
            os.remove(self.html_file)

    def test_text(self):
        self.md2html.text = None
        self.assertIsNone(self.md2html.text)
        self.md2html.text = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.text)

        self.assertRaises(TypeError, setattr, self.md2html, 'text', 42)

    def test_body(self):
        self.md2html.body = None
        self.assertIsNone(self.md2html.body)
        self.md2html.body = 'Hello.42'
        self.assertEqual('Hello.42', self.md2html.body)

        self.assertRaises(TypeError, setattr, self.md2html, 'body', 42)

    def test_input_file_path(self):
        self.md2html.src_dirname = os.getcwd()
        self.md2html.src_basename = 'README'
        self.md2html.src_extension = '.md'
        self.assertEqual(
            os.path.join(os.getcwd(), '{0}{1}'.format('README', '.md')),
            self.md2html.input_file_path
        )
        self.md2html.src_dirname = None
        self.md2html.src_basename = None
        self.md2html.src_extension = None

    def test_output_file_path(self):
        self.md2html.dst_dirname = os.getcwd()
        self.md2html.dst_basename = 'README'
        self.md2html.dst_extension = '.html'
        self.assertEqual(
            os.path.join(os.getcwd(), '{0}{1}'.format('README', '.html')),
            self.md2html.output_file_path
        )
        self.md2html.dst_dirname = None
        self.md2html.dst_basename = None
        self.md2html.dst_extension = None

    def test_add_src_file_name(self):
        self.md2html.add_src_file_name(os.path.join(os.getcwd(), '{0}{1}'.format('README', '.md')))
        self.assertEqual(os.getcwd(), self.md2html.src_dirname)
        self.assertEqual('README', self.md2html.src_basename)
        self.assertEqual('.md', self.md2html.src_extension)

        self.md2html.add_src_file_name(None)
        self.assertIsNone(self.md2html.src_dirname)
        self.assertIsNone(self.md2html.src_basename)
        self.assertIsNone(self.md2html.src_extension)

        self.assertRaises(TypeError, self.md2html.add_src_file_name, 42)

    def test_add_dst_file_name(self):
        self.md2html.add_dst_file_name(os.path.join(os.getcwd(), '{0}{1}'.format('README', '.html')))
        self.assertEqual(os.getcwd(), self.md2html.dst_dirname)
        self.assertEqual('README', self.md2html.dst_basename)
        self.assertEqual('.html', self.md2html.dst_extension)

        self.md2html.add_dst_file_name(None)
        self.assertIsNone(self.md2html.dst_dirname)
        self.assertIsNone(self.md2html.dst_basename)
        self.assertIsNone(self.md2html.dst_extension)

        self.assertRaises(TypeError, self.md2html.add_dst_file_name, 42)

    def test_style(self):
        self.assertEqual(str, type(self.md2html.style))
        self.assertTrue(len(self.md2html.style) > 0)

    def test_html_code(self):
        self.md2html.body = ''
        prev_size = len(self.md2html.html_code)
        self.assertTrue(len(self.md2html.style) > 0)
        self.assertTrue(len(self.md2html.html_code) > 0)
        self.assertEqual(prev_size, len(self.md2html.html_code))
        self.md2html.body = '1'
        self.assertNotEqual(prev_size, len(self.md2html.html_code))
        self.md2html.body = ''
        self.assertEqual(prev_size, len(self.md2html.html_code))

    def test_run(self):
        self.md2html.add_src_file_name(self.md_file)
        self.md2html.add_dst_file_name(self.html_file)
        self.md2html.run()
        if os.path.exists(self.html_file):
            os.remove(self.html_file)


if __name__ == '__main__':
    unittest.main()
