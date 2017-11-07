r"""Utilities that present `MathObject`\s as HTML pages."""

# Copyright Algebraix Data Corporation 2015 - 2017
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
import algebraixlib.util.latexprinter as _latexprinter


# --------------------------------------------------------------------------------------------------

#: Named `tuple` for collecting information about a `MathObject`.
#: It contains:
#: -    ``input_title``: (Optional) A string that can serve as a name, origin expression or title.
#: -    ``data_algebra_construct``: The `MathObject` or container of `MathObject`\s.
#: -    ``description_brief``: (Optional) A string to display more detail.
DataAlgebraHtmlDescriptor = _collections.namedtuple(
    'DataAlgebraHtmlDescriptor',
    'input_title data_algebra_construct description_brief')


def math_object_as_html(title: str, data_algebra_html_descriptors: [],
                        header_template: str=None, footer_template: str=None,
                        mathobject_template: str=None) -> str:
    r"""Return the contents of an HTML webpage representing a `MathObject`, using templates.

    :param title: The title for this page of `MathObject`\s.
    :param data_algebra_html_descriptors: An array of `DataAlgebraHtmlDescriptor` instances
        (containing math objects and their related descriptive strings).
    :param header_template: HTML markup that starts the webpage. May contain the template variable
        ``page_title``; it is set to the value of ``title``.
    :param footer_template: HTML markup that ends the page.
    :param mathobject_template: The HTML markup that is emited for each math object. May contain
        the template variables ``input_title``, ``description_brief`` and
        ``data_algebra_construct``, which are replaced with the respective values in the
        associated ``DataAlgebraHtmlDescriptor``.
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
            description_brief=as_html_handle_basic_parameter(
                dataAlgebraDescriptor.description_brief),
            data_algebra_construct=as_html_handle_data_algebra(
                dataAlgebraDescriptor.data_algebra_construct))
         for dataAlgebraDescriptor in data_algebra_html_descriptors]))

    # Ends the web page with the provided footer.
    writer.write(footer_template)

    html_out = writer.getvalue()
    # print(html_out)
    return html_out


def as_html_handle_basic_parameter(html_input: str) -> str:
    """Return the string of ``html_input``, properly escaped for using it in HTML."""
    return _html.escape(str(html_input))


def as_html_handle_data_algebra(mathobj):
    r"""Return ``mathobj`` converted into a string safe to be used in HTML.

    -   If ``mathobj`` is a `MathObject`, it will be represented as LaTeX markup and wrapped in the
        mathjax escape token.
    -   If it is a container of `MathObject`\s, then each one will be represented as LaTeX
        markup and displayed on its own line.
    -   If it is not a `MathObject` then the ``str`` function will be invoked.
    """
    if isinstance(mathobj, _mo.MathObject):
        # print this one math object
        return "$$" + _html.escape(_latexprinter.math_object_to_latex(mathobj)) + "$$"
    elif isinstance(mathobj, _collections.Iterable):
        temp = ""
        for elem in mathobj:
            if isinstance(elem, _mo.MathObject):
                # latex
                temp += r"$$\(\require{color}\)\(\require{xcolor}\)" + \
                        _html.escape(_latexprinter.math_object_to_latex(elem)) + "$$ <br //>"
            else:
                # str
                temp += _html.escape(str(elem)) + "<br //>"

        return temp
    else:
        # print this one non-math object using str(mathobjects)
        return _html.escape(str(mathobj))


def build_descriptors_from_math_obj(mathobjects):
    """Return an array of simple `DataAlgebraHtmlDescriptor` of the objects in ``mathobjects``.

    :param mathobjects: List of objects from which to create descriptors.
    """
    data_alg_descriptors = []

    for mathobj in mathobjects:
        data_alg_descriptors.append(
            DataAlgebraHtmlDescriptor(str(mathobj), mathobj, "No Description,"))

    return data_alg_descriptors


def create_simple_web_page(mathobj: _mo.MathObject) -> str:
    """Return an HTML string for a simple HTML page from a single `MathObject`."""
    web_template = r"""\
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
        <div id="latexArea">$$\(\require{color}\){latex_out}$$</div>
    </body></html>
    """
    web_out = web_template.format(
        data_algebra_in=mathobj, latex_out=_latexprinter.math_object_to_latex(mathobj))
    print(web_out)
    return web_out
