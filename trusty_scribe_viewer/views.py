from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.utils.html import format_html
import gitio
import operator
import re
from datetime import datetime

def index(request):
    return HttpResponseRedirect("/lab_notebook/50/")

def commit(request, sha):
    print "the sha is", sha
    commit = gitio.Commit(sha)
    title, body = split_once(parbreak_re, commit.message)
    parents = []
    changed_files = []
    commiter = '(commiter)'
    commit_info = {'commiter'        : commiter,
                   'commit_title'    : title,
                   'commit_id'       : commit.sha,
                   'timestamp'       : format_time(commit.timestamp),
                   'parents'         : parents,
                   'commit_content'  : body_as_html(commit.sha, body),
                   'changed_files'   : changed_files}
    return render(request, 'commit.djhtml', commit_info)

def lab_notebook(request, max_entries=None):
    commit_list = []
    commit = gitio.get_head_commit()
    remaining = int(max_entries) if max_entries else -1
    while commit and remaining != 0:
        title, body = split_once(parbreak_re, commit.message)
        commit_list.append({'title'           : title,
                            'commit_id'       : commit.sha,
                            'timestamp'       : format_time(commit.timestamp),
                            'content'         : body_as_html(commit.sha, body)})
        commit = commit.prev
        remaining -= 1

    context = {'repo_name'   : gitio.repo_name,
               'commit_list' : commit_list}
    return render(request, 'notebook.djhtml', context)

def split_once(p, s):
    ans = p.split(s, 1)
    if len(ans) == 1:
        return ans[0], ""
    else:
        return ans[0], ans[1]

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
        path_list = filter(bool, path.split('/'))
        obj, obj_type = gitio.Commit(commit_id).obj_from_path(path_list)
        text_kept = "\n".join(str(obj).splitlines()[-N_lines_shown:])
        return format_html("<pre><code>{0}</code></pre>", text_kept)

def format_time(t):
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')

def browse(request, path_string):
    commit_id_and_path = filter(bool, path_string.split('/'))
    commit_id, path = commit_id_and_path[0], commit_id_and_path[1:]
    commit = gitio.Commit(commit_id)
    obj, obj_type = commit.obj_from_path(path)
    if obj_type == 'directory':
        if path_string[-1] == '/':
            context = {'dirname'   : "/".join(path) + "/",
                       'commit_id' : commit_id[:10],
                       'relpaths'  : obj + [".."]}
            return render(request, 'directory.djhtml', context)
        else:
            url_with_trailing_slash = "/browse/{0}/".format(path_string)
            return HttpResponseRedirect(url_with_trailing_slash)
    elif obj_type == 'file':
        return HttpResponse(obj, content_type='text/plain')
    else:
        raise Exception

def diff(request, sha_1, sha_2):
    return HttpResponse(gitio.get_diff(gitio.Commit(sha_1), gitio.Commit(sha_2)),
                        content_type='text/plain')
