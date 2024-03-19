#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from unittest import TestCase, main
from glxdocs.yaml2md import Yaml2Md
from glxdocs.yaml2md import State

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Docs Team, all rights reserved


class TestDocs(TestCase):

    def setUp(self):
        self.yaml2md = Yaml2Md()
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.roles_src_path = os.path.join(self.cwd, 'data', 'roles')
        self.roles_dst_reference = os.path.join(self.cwd, 'data', 'reference', 'role')

    def test_yamle2md_property_state(self):
        self.yaml2md.state = State.YAML
        self.assertEqual(State.YAML, self.yaml2md.state)

        self.yaml2md.state = None
        self.assertEqual(State.TEXT, self.yaml2md.state)

        self.assertRaises(TypeError, setattr, self.yaml2md, "state", "Hello42")

    def test_yaml2md(self):

        ignore_role_list = [
            'galaxie_clans.dns',
            'galaxie_clans.clan_host',
            'galaxie_clans.system_base',
            'galaxie_clans.system_users'
        ]

        for element in os.listdir(self.roles_src_path):
            default_directory = os.path.abspath(os.path.join(self.roles_src_path, element, 'defaults'))
            if not os.path.isdir(default_directory) or element in ignore_role_list:
                continue
            for path, sub_dirs, files in os.walk(default_directory):
                for filename in files:
                    if filename.startswith("."):
                        continue

                    self.yaml2md.file_input.path = os.path.join(path, filename)
                    self.yaml2md.file_output.path = self.roles_dst_reference + "_" + element + ".md"

                    self.yaml2md.convert_file()

                    sys.stdout.write("Converted {0}".format(self.roles_dst_reference + "_" + element + "\n"))
                    sys.stdout.flush()


if __name__ == "__main__":
    main()
