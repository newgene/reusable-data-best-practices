# -*- coding: utf-8 -*-
"""
    sphinxjp.themes.basicstrap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :author: tell-k <ffk2005@gmail.com>
    :copyright: tell-k. All Rights Reserved.
"""

from os import path
from docutils import nodes
from sphinx.environment.collectors import EnvironmentCollector
from sphinx import addnodes
from sphinx.util.osutil import relative_uri
from .directives import setup as _setup
import json

__version__ = '0.5.0'

package_dir = path.abspath(path.dirname(__file__))
template_path = path.join(package_dir, 'templates', 'basicstrap')


class SimpleTocTreeCollector(EnvironmentCollector):
    """A TocTree collector that saves toctrees in a simple dict.
    sphinx.environment.collectors.toctree.TocTreeCollector saves
    TocTree as docutils.nodes which are hard to work with...
    Executed once per document/page, at sphinx's "read" phase.
    Saved data example:
    {
        'sections': [{'title': 'Demo', 'href': '#demo'}],
        'toctrees': [<toctree: >]
    }
    """
    def enable(self, app):
        super().enable(app)
        # env is populated from cache, if not cache create/initalize attibute
        #if not hasattr(app.env, 'toc_dict'):
            #app.env.toc_dict = {}

    def clear_doc(self, app, env, docname):
        if not hasattr(app.env, 'toc_dict'):
            app.env.toc_dict = {}
        env.toc_dict.pop(docname, None)

    def merge_other(self, app, env, docnames, other):
        if not hasattr(app.env, 'toc_dict'):
            app.env.toc_dict = {}
        for docname in docnames:
            env.toc_dict[docname] = other.toc_dict[docname]

    def process_doc(self, app, doctree):
        if not hasattr(app.env, 'toc_dict'):
            app.env.toc_dict = {}
        try:
            from docs.conf import depth
        except Exception as e:
            # set default depth as 2
            depth = 2
        
        docname = app.env.docname # sphinx mutates this, ouch!!!

        # print(f"================ Collector\n{docname}\n============\n")
        # get 1 level document toc (sections)
        # section_nodes = [s for s in doctree if isinstance(s, nodes.section)]

        section_nodes = []

        for node in doctree:
            if isinstance(node, nodes.section):
                node.level = 0
                section_nodes.append(node)
        # if first level is a single section,
        # ignore it and use second level of sections
        if len(section_nodes) == 1:
            final_nodes = []
            for node in section_nodes[0]:
                node.level = 1
                if isinstance(node, nodes.section):
                    final_nodes.append(node)
                    # only add this if depth level is >= 3
                    if depth>=3:
                        for innernode in node:
                            innernode.level = 2
                            if isinstance(innernode, nodes.section):
                                final_nodes.append(innernode)

            section_nodes = final_nodes

        sections = []

        # we should mark each section with its corresponding level
        # Example 'title': title, 'level': enum[0,1,2]
        # Probably have to find the nodes.section element and add the level depending on the
        # header level
        for node in section_nodes:
            sections.append({
                'title': node[0].astext(),
                'href': '#{}'.format(node['ids'][0]),
                'level': node.level
            })

        app.env.toc_dict[docname] = {
            'sections': sections,
            'toctrees': doctree.traverse(addnodes.toctree)
        }


def add_toctree_data(app, pagename, templatename, context, doctree):
    """Create toctree_data, used to build sidebar navigation
    :param pagename: The name of the page
    :type pagename: str
    :param templatename: The name of the templatename
    :type templatename: str
    :param context: The context
    :type context: dict
    :param doctree: A doctree
    :type doctree: docutils.nodes.document
    Add to `toctree_data` to `context` that will be available on templates.
    Although data is "global", it is called once per page because current
    page is "highlighted", and some part of TOC might be collapsed.
    :return: None
    """
    # print(f"---------- Context\n{pagename}\n-------------\n")
    if not hasattr(app.env, 'toc_dict'):
        app.env.toc_dict = {}
    # start from master_doc

    master = app.env.get_doctree(app.env.config.master_doc)
    '''rendered = app.builder.templates.render_string(
        'chapters/chapter1', app.config.html_context
    )'''
    # each toctree will create navigation section
    res = [] # list of top level toctrees in master_doc
    for tree in master.traverse(addnodes.toctree):
        # special case for toctree that includes a single item
        # that contains a nested toctree.
        # In this case, just use the referenced toctree directly
        if len(tree['entries']) == 1:
            entry_docname = tree['entries'][0][1]
            toctrees = app.env.toc_dict[entry_docname]['toctrees']

            if toctrees:
                assert len(toctrees) == 1, "Press: Not supported more then one toctree on nested toctree"
                tree = toctrees[0]

        current0 = False # same page might have multiple tocs

        # add toc tree items, expand one more level if toctree is current page
        # TODO fix level 3 headers here
        entries = []
        for title, name in tree['entries']:
            if not title:
                title = app.env.titles[name].astext()

            current1 = (pagename == name)
            children = []
            if current1:
                current0 = True
                # if current, add another level
                children = app.env.toc_dict[name]['sections']
            
            # add page_toc for current page
            entries.append({
                'name': name,
                'title': title,
                'level': 0,
                'current': current1,
                'children': children,
            })
            

        toc_docname = tree['parent'] # docname where this toc appears
        title = tree['caption']
        level = tree['level'] if 'level' in tree else 0

        # Anchor element is the section containing the toc,
        # as the toc itself does not contain ID.
        anchor_id = ''

        # tree.parent is the parent docutils node.
        # First parent is "compound" node toctree-wrapper,
        # second parent is the section containing the toctree
        toc_section = tree.parent.parent
        if toc_section['ids']: # no id means toc actually not in a section
            # TODO: should we be strict about toc being inside a section
            anchor_id = toc_section['ids'][0]
            if not title:
                title = toc_section['names'][0]

        # sphinx `pathto` does not play nice with anchors when
        # `allow_sharp_as_current_path` is True
        baseuri = app.builder.get_target_uri(pagename).rsplit('#', 1)[0]
        toc_uri = app.builder.get_target_uri(toc_docname).rsplit('#', 1)[0]
        toc_href = '{}#{}'.format(relative_uri(baseuri, toc_uri), anchor_id)
        res.append({
            'docname': toc_docname,
            'href': toc_href,
            'title': title,
            'level': 0,
            'current': current0,
            'entries': entries,
        })
    context['toctree_data'] = res
    context['toctree_data_json'] = json.dumps(res)

def get_path():
    """entry-point for theme."""
    return template_path


def setup(app):
    """entry-point for sphinx directive."""
    app.add_env_collector(SimpleTocTreeCollector)
    app.connect('html-page-context', add_toctree_data)
    app.add_html_theme('basicstrap', get_path())
    _setup(app)
