"""A conversion utility that manipulates a math object into a LaTeX representation."""

# $Id: html.py 22614 2015-07-15 18:14:53Z gfiedler $
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
import collections as _collections
import html as _html
import io as _io

import algebraixlib.mathobjects as _mo
from algebraixlib.util.latexprinter import math_object_to_latex as _math_object_to_latex

# Named Tuple for containing information about a math object.
# DataAlgebraHtmlDescriptor contains
# input_title: A string (optional) which can serve as a name, origin expression or title
# data_algebra_construct: The math object or container of math objects.
# description_brief: A string Optional to offer up a little more detail
DataAlgebraHtmlDescriptor = _collections.namedtuple(
    'DataAlgebraHtmlDescriptor',
    'input_title data_algebra_construct description_brief')


def math_object_as_html(title: str, data_algebra_html_descriptors: [],
                        header_template: str=None, footer_template: str=None,
                        mathobject_template: str=None) -> str:
    """Return the contents of an HTML webpage representing a math object, using templates.

    :param title: The title for this page of math objects.
    :param data_algebra_html_descriptors: An array of ``DataAlgebraHtmlDescriptor`` instances
        (containing math objects and their related descriptive strings).
    :param header_template: HTML markup that starts the webpage. May contain the template
        ``page_title``; it is set to the value of ``title``.
    :param footer_template: HTML markup that ends the page.
    :param mathobject_template: The HTML markup that is emited for each math object. May contain
        the templates ``input_title``, ``description_brief`` and ``data_algebra_construct``, which
        are replaced with the respective values in the associated ``DataAlgebraHtmlDescriptor``.
    :return: The final HTML webpage.
    """

    # The default header template. Start the web page and set up some basic styles for the various
    # display elements. Requires the template argument 'page_title' (the title for the document that
    # is being created).
    default_header_template = """\
    <html>
      <head>
        <script
          src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
        </script>
        <script type="text/javascript">
        //<![CDATA[  //]]>
        </script>
        <style>
          body {{background-color: #F8F8FF}}
          #page_title{{}}
          #input_title{{}}
          #description_brief{{
            border: 1px solid black;
            padding: 5px;
            background-color: white;
          }}
          #data_algebra_construct{{
            border: 1px solid black;
            padding: 5px;
            background-color: white;
          }}
        </style>
      </head>
      <body>
        <h1 id="page_title">{page_title}</h1>
    """
    if header_template is None:
        header_template = default_header_template

    # The default footer. Only closes the body and html tags, assumed to have been opened by the
    # header. It is not an actual template.
    default_footer = """</body></html>"""
    if footer_template is None:
        footer_template = default_footer

    # The default math object template. Add a section to the page that displays a math object with
    # associated descriptive text. Requires three template arguments (the names match the members of
    # DataAlgebraHtmlDescriptor):
    # - input_title: A string naming the math object, displayed in an h2 header. May contain HTML
    #   markup, but it needs to be consistent with being used in an h2 header.
    # - description_brief: A description of the mathobject, displayed in a preformatted section. May
    #   contain HTML markup, but it needs to be consistent with being used in preformatted text.
    # - data_algebra_construct: Normally the LaTeX representation of the mathobject, but could also
    #   be HTML markup, or a simple string representation of the math object. Is shown as standard
    #   text.
    default_mathobject_template = """\
      <h2 id="input_title">{input_title}</h2>
      <div id="description_brief"><pre>{description_brief}</pre></div>
      <div id="data_algebra_construct">{data_algebra_construct}</div>
    """
    if mathobject_template is None:
        mathobject_template = default_mathobject_template

    writer = _io.StringIO()

    # Start the web page by appending the header, and injecting the title.
    writer.write(header_template.format(page_title=as_html_handle_basic_parameter(title)))

    # Appends the template, with replaced elements from the descriptors, for each description.
    # Makes use of delegate functions for rendering the different parameters.
    writer.write(''.join(
        [mathobject_template.format(
            input_title=as_html_handle_basic_parameter(dataAlgebraDescriptor.input_title),
            description_brief=as_html_handle_basic_parameter(dataAlgebraDescriptor.description_brief),
            data_algebra_construct=as_html_handle_data_algebra(dataAlgebraDescriptor.data_algebra_construct))
         for dataAlgebraDescriptor in data_algebra_html_descriptors])
    )

    # Ends the web page with the provided footer.
    writer.write(footer_template)

    html_out = writer.getvalue()
    # print(html_out)
    return html_out


def as_html_handle_basic_parameter(html_input: str) -> str:
    """Convert the string of ``html_input`` into an HTML-safe character sequence.

    :param html_input: The value to convert so that it can be added to HTML content.
    :return: An HTML-safe string.
    """
    return _html.escape(str(html_input))


def as_html_handle_data_algebra(mathobj):
    """Add some logic to allow the client to provide the math object in several ways:

    - If it is a mathobject, it will be turnied into LaTeX and wrapped in the mathjax escape token.
    - If it is a container of mathobjects, then each one will be turned into LaTeX and presented on
      its own line.
    - If it is not a mathobject then the str function will be invoked.

    :param mathobj: The data algebra construct to be rendered on HTML
    :return: The HTML snippet of the mathobject.
    """

    if isinstance(mathobj, _mo.MathObject):
        # print this one math object
        return "$$" + _html.escape(_math_object_to_latex(mathobj)) + "$$"
    elif isinstance(mathobj, _collections.Iterable):
        temp = ""
        for elem in mathobj:
            if isinstance(elem, _mo.MathObject):
                # latex
                temp += "$$\(\\require{color}\)\(\\require{xcolor}\)" + \
                        _html.escape(_math_object_to_latex(elem)) + "$$ <br //>"
            else:
                # str
                temp += _html.escape(str(elem)) + "<br //>"

        return temp
    else:
        # print this one non-math object using str(mathobjects)
        return _html.escape(str(mathobj))


def build_descriptors_from_math_obj(mathobjects):
    """
    A utility function if a client does not wish to create their own descriptor objects.  This
    function will create a descriptor array from a list of mathobjects.

    :param mathobjects: List to build descriptors out of.
    :return: DataAlgebraHtmlDescriptors
    """
    data_alg_descriptors = []

    for mathobj in mathobjects:
        data_alg_descriptors.append(
            DataAlgebraHtmlDescriptor(str(mathobj), mathobj, "No Description,"))

    return data_alg_descriptors


def create_simple_web_page(mathobj: _mo.MathObject) -> str:
    """Convert a math object into an HTML file.  This does not offer much client specification or
    HTML injection.  Create a basic webpage for one mathobject.

    :param mathobj: The mathobject to create a webpage for.
    :return: The web page (HTML) for ``mathobj``.
    """
    web_template = """\
<html>
    <head>
        <script
        src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
        </script>
        <script type="text/javascript">
        //<![CDATA[  //]]>
        </script>
        <style>
            body {{background-color: #F8F8FF}}
            #latexArea, #dataAlgebraArea{{
                width: 1000px;
                height: 200px;
                border: 1px solid black;
                padding: 5px;
                overflow: scroll;
                background-color: white;
                resize: both;
            }}
        </style>
    </head>
    <body>
        <h1>MathJax is Easy!</h1>
        <h2>Input:</h2>
        <div id="dataAlgebraArea">{data_algebra_in!s}</div>
        <h2>Output:</h2>
        <div id="latexArea">$$\(\\require{color}\){latex_out}$$</div>
    </body></html>
    """

    web_out = web_template.format(data_algebra_in=mathobj, latex_out=_math_object_to_latex(mathobj))
    print(web_out)
    return web_out


#
# Build unit test up here for now
#
import unittest
class DataAlgToWebTest(unittest.TestCase):
    """Test the latex printer functions."""

    # Test Input Data
    _a1 = _mo.Atom('scooby')
    _a2 = _mo.Atom('doo')
    _c1 = _mo.Couplet(left=_a1, right=_a2)
    _a3 = _mo.Atom('shaggy')
    _a4 = _mo.Atom('rogers')
    _c2 = _mo.Couplet(left=_a3, right=_a4)
    _a5 = _mo.Atom('mystery')
    _a6 = _mo.Atom('van')
    _c3 = _mo.Couplet(left=_a5, right=_a6)
    _s1 = _mo.Set([_c1, _c2, _c3])

    _a7 = _mo.Atom('velma')
    _a8 = _mo.Atom('dinkley')
    _c4 = _mo.Couplet(left=_a7, right=_a8)
    _a9 = _mo.Atom('fred')
    _a10 = _mo.Atom('jones')
    _c5 = _mo.Couplet(left=_a9, right=_a10)
    _a11 = _mo.Atom('daphne')
    _a12 = _mo.Atom('blake')
    _c6 = _mo.Couplet(left=_a11, right=_a12)
    _a13 = _mo.Atom('mystery')
    _a14 = _mo.Atom('team')
    _c7 = _mo.Couplet(left=_a13, right=_a14)
    _s2 = _mo.Set([_c4, _c5, _c6, _c7])
    _s3 = _mo.Set([_s1, _s2])

    @unittest.skip('This test creates non-deterministic results, so sometimes fails.')
    def test_data_alg_to_web_simple(self):
        # large comparisons needs diff size increased
        self.maxDiff = None
        print("test_data_alg_to_web_simple Begin:")
        # Actual LaTeX Output Data
        html_output = create_simple_web_page(self._s3)
        # Expected LaTeX Output Data
        html_output_ex = """<html>
    <head>
        <script
        src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
        </script>
        <script type="text/javascript">
        //<![CDATA[  //]]>
        </script>
        <style>
            body {background-color: #F8F8FF}
            #latexArea, #dataAlgebraArea{
                width: 1000px;
                height: 200px;
                border: 1px solid black;
                padding: 5px;
                overflow: scroll;
                background-color: white;
                resize: both;
            }
        </style>
    </head>
    <body>
        <h1>MathJax is Easy!</h1>
        <h2>Input:</h2>
        <div id="dataAlgebraArea">{{('doo'^'scooby'), ('rogers'^'shaggy'), ('van'^'mystery')},
        {('dinkley'^'velma'), ('team'^'mystery'), ('jones'^'fred'), ('blake'^'daphne')}}</div>
        <h2>Output:</h2>
        <div id="latexArea">
        $$\left\{\ \\begin{array}{l}\\\\
            \quad\left\{\ (\mbox{'blake'}^{\mbox{'daphne'}}),\ (\mbox{'jones'}^{\mbox{'fred'}}),\
                (\mbox{'team'}^{\mbox{'mystery'}}),\ (\mbox{'dinkley'}^{\mbox{'velma'}})\ \\right\},\\\\
            \quad\left\{\ (\mbox{'van'}^{\mbox{'mystery'}}),\ (\mbox{'doo'}^{\mbox{'scooby'}}),\
                (\mbox{'rogers'}^{\mbox{'shaggy'}})\ \\right\}\\\\
            \end{array}\\right\}$$</div>
    </body></html>"""
        self.assertEqual(html_output_ex, html_output)
        print("Test End.")

    #    @unittest.skip('Skipping this test as it is more an example program at the moment.')
    #    def test_data_alg_to_web(self):
    #        #large comparisons needs diff size increased
    #        self.maxDiff = None
    #        print("test_data_alg_to_web Begin:")
    #        # Actual LaTeX Output Data
    #        html_output = create_web_page([self._s1, self._s2, self._s3])
    #        # Expected LaTeX Output Data
    #        html_output_ex = """Insert something like expected results here."""
    #        self.assertEqual(html_output_ex, html_output)
    #        print("Test End.")

    @unittest.skip('Skipping this test as it is more an example program at the moment.')
    def test_data_alg_to_web(self):
        # large comparisons needs diff size increased
        self.maxDiff = None
        print("test_data_alg_to_web Begin:")
        # Actual LaTeX Output Data
        html_output = math_object_as_html("TestTitle", build_descriptors_from_math_obj(
            [self._s1, self._s2, self._s3]))
        # Expected LaTeX Output Data
        html_output_ex = """Insert something like expected results here."""
        self.assertEqual(html_output_ex, html_output)
        print("Test End.")