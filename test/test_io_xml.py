"""Testing the io.xml module."""

# $Id: test_io_xml.py 22614 2015-07-15 18:14:53Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-07-15 13:14:53 -0500 (Wed, 15 Jul 2015) $
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
import inspect
import io
import os
import unittest

from algebraixlib.io.json import import_json
from algebraixlib.io.xml import import_xml
from algebraixlib.mathobjects import Atom, Couplet, Set


class IoXmlTests(unittest.TestCase):

    _print_examples = False

    @staticmethod
    def path(file):
        return os.path.join(os.path.dirname(__file__), file)

    def test_xml(self):
        xml_text = """<?xml version="1.0"?>
            <employee id="0034404">
               <name first="john" last="doe"></name>
               <project lead="Foo">
                  <name>GAaaS</name>
               </project>
               <project name="Data Algebra">
                  <lead>Bar</lead>
               </project>
            </employee>
            """
        xml_set = import_xml(io.StringIO(xml_text))

        json_text = """
            {
                "employee": {
                    "id": "0034404",
                    "name": {
                        "first": "john",
                        "last": "doe"
                    },
                    "project": [
                        {
                            "lead": "Foo",
                            "name": "GAaaS"
                        },
                        {
                            "name": "Data Algebra",
                            "lead": "Bar"
                        }
                    ]
                }
            }
            """
        json_set = import_json(io.StringIO(json_text))
        self.assertEqual(json_set, xml_set)

        from algebraixlib.algebras.relations import compose
        c = next(iter(xml_set))
        self.assertEqual(Atom('employee'), c.left)
        self.assertEqual(4, len(c.right))
        cid = compose(c.right, Set(Couplet('id', 'id')))
        self.assertEqual(cid, Set(Couplet('id', '0034404')))
        name = next(iter(compose(c.right, Set(Couplet('name', 'name')))))
        self.assertEqual(name.right, Set([Couplet('first', 'john'), Couplet('last', 'doe')]))
        projects = compose(c.right, Set(Couplet('project', 'project')))
        self.assertEqual(2, len(projects))
        ep = Set([Couplet('project', Set([Couplet('name', x['name']), Couplet('lead', x['lead'])]))
                  for x in [{'name': 'GAaaS', 'lead': 'Foo'},
                            {'lead': 'Bar', 'name': 'Data Algebra'}]])
        self.assertEqual(projects, ep)

    def test_xml2(self):
        """Test filled with multiple attributes and a text node"""
        xml_text = """<?xml version="1.0" encoding="utf-8"?>
            <Root>
                <record>
                    <field name="Country or Area">
                        <key>USA</key>
                        United States
                    </field>
                </record>
            </Root>
            """
        xml_set = import_xml(io.StringIO(xml_text))
        expected = \
            Set(Couplet('Root',
                Set(Couplet('record',
                    Set(Couplet('field',
                        Set(
                            Couplet('$', 'United States'),
                            Couplet('key', 'USA'),
                            Couplet('name', 'Country or Area')
                        )
                    ))
                ))
            ))
        self.assertEqual(xml_set, expected)

# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # The print is not really necessary. It helps making sure we always know what we ran in the IDE.
    print('main: {file}'.format(file=os.path.basename(inspect.getfile(inspect.currentframe()))))
    unittest.main()
