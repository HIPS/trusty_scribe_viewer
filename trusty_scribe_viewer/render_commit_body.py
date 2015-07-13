import gitio
import re
import operator
from django.utils.html import format_html
from django.template import Context, loader

link_re_expr = r'\[(?P<name>[\w./-]+)\]\((?P<path>[\w./-]+)\)'
link_re = re.compile(link_re_expr)
bullet_link_re = re.compile(r'\* ' + link_re_expr)
parbreak_re = re.compile('\n\n+')
image_patterns = re.compile(r'.png$|.jpg$')

def body_as_html(sha, md_text):
    def parse_paragraph(md_text):
        nonempty_lines = filter(bool, md_text.split("\n"))
        bullet_matches = map(bullet_link_re.match, nonempty_lines)
        if all(bullet_matches):
            return {'type'     : 'bullet_links',
                    'elements' : map(parse_bullet_match, bullet_matches)}
        else:
            return {'type'     : 'prose',
                    'elements' : parse_prose_paragraph(md_text)}

    def parse_bullet_match(match):
        name, path = match.group('name'), match.group('path')
        if image_patterns.search(path):
            return {'type' : 'image',
                    'name' : name,
                    'path' : path}
        else:
            return {'type'     : 'text',
                    'name'     : name,
                    'path'     : path,
                    'contents' : str(commit.obj_from_path_str(path)[0])}

    def parse_prose_paragraph(md_text):
        pieces = link_re.split(md_text)
        text, rest = pieces[0], pieces[1:]
        elements = [{'type' : 'text', 'text' : text}]
        while rest:
            (name, path, text), rest = rest[:3], rest[3:]
            elements += [{'type' : 'link', 'name' : name, 'path' : path},
                         {'type' : 'text', 'text' : text}]
        return elements

    commit = gitio.Commit(sha)
    paragraphs = map(parse_paragraph, filter(bool, parbreak_re.split(md_text)))
    template = loader.get_template('commit_content.djhtml')
    return template.render({'paragraphs' : paragraphs, 'sha' : sha})
