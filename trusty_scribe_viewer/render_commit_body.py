import gitio
import re
import operator
from django.utils.html import format_html
from django.template import Context, loader

link_re_expr = r'\[(?P<name>[\w./-]+)\]\((?P<path>[\w./-]+)\)'
link_re = re.compile(link_re_expr)
bullet_link_re = re.compile(r'\* ' + link_re_expr)
parbreak_re = re.compile('\n\n+')

def body_as_html(commit_id, md_text):
    def paragraph_to_html(paragraph):
        nonempty_lines = filter(bool, paragraph.split("\n"))
        bullet_matches = map(bullet_link_re.match, nonempty_lines)
        if all(bullet_matches):
            return concat_html(map(bullet_match_to_html, bullet_matches))
        else:
            pieces = link_re.split(paragraph)
            text, rest = pieces[0], pieces[1:]
            html = format_html("{0}", text)
            while rest:
                (name, path, text), rest = rest[:3], rest[3:]
                html += format_html('{link}{text}',
                                    text = text,
                                    link = link_html(name, path, commit_id))
            return format_html("<p>{0}</p>", html)

    def bullet_match_to_html(match):
        name, path = match.group('name'), match.group('path')
        return format_html("<p>{link}</p><p>{content}</p>",
                           link = link_html(name, path, commit_id),
                           content = content_html(path, commit_id))

    return concat_html(map(paragraph_to_html, parbreak_re.split(md_text)))

def concat_html(html_list):
    return reduce(operator.add, html_list, format_html(""))

def link_html(name, path, commit_id):
    return format_html('<a href="{full_path}">{name}</a>',
                       name=name,
                       full_path=path_to_file(commit_id, path))

def path_to_file(commit_id, path):
    return "/browse/{commit_id}/{path}".format(commit_id=commit_id, path=path)

image_patterns = re.compile(r'.png$|.jpg$')
def content_html(path, commit_id):
    if image_patterns.search(path):
        return format_html('<img src="{0}">',
                           path_to_file(commit_id, path))
    else:
        N_lines_shown = 10
        obj, obj_type = gitio.Commit(commit_id).obj_from_path_str(path)
        text_kept = "\n".join(str(obj).splitlines()[-N_lines_shown:])
        return format_html("<pre><code>{0}</code></pre>", text_kept)
