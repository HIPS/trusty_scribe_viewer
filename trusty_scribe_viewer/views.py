from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from gitio import obj_from_path
import sys

def index(request):
    return HttpResponseRedirect("/lab_notebook/")

def lab_notebook(request):
    return HttpResponse("Lab notebook")

def files(request, path_string):
    commit_and_path = filter(bool, path_string.split('/'))
    commit, path = commit_and_path[0], commit_and_path[1:]
    obj, obj_type = obj_from_path(commit, path)
    if obj_type == 'directory':
        if path_string[-1] == '/':
            return HttpResponse(render_directory(obj, commit, path))
        else:
            url_with_trailing_slash = "/files/{0}/".format(path_string)
            return HttpResponseRedirect(url_with_trailing_slash)
    elif obj_type == 'file':
        return HttpResponse(obj, content_type='text/plain')
    else:
        raise Exception

def render_directory(children, commit, path):
    dirname = "/".join(path)
    children += [".."]
    contents = "".join(map(dir_entry_template.format, children))
    return dir_template.format(dirname=dirname, commit=commit[:10], contents=contents)

dir_template = """\
<!doctype html>
<title>Directory {dirname}</title>
<h2>Contents of directory {dirname} at commit {commit}:</h2>
<ul>{contents}</ul>
"""
dir_entry_template = """\
<li><a href="{0}/">{0}</a></li>
"""
