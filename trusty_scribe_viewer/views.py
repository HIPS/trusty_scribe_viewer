from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import gitio

def index(request):
    return HttpResponseRedirect("/lab_notebook/50/")

def commit(request, sha):
    return render(request, 'commit.djhtml', {'commit' : gitio.Commit(sha)})

def lab_notebook(request, max_entries=None):
    if max_entries:
        max_entries = int(max_entries)
    context = {'repo_name'   : gitio.repo_name,
               'commits'      : gitio.lifo_commits(max_entries),
               'max_entries' : bool(max_entries)}
    return render(request, 'notebook.djhtml', context)

def browse(request, sha, path_str):
    commit = gitio.Commit(sha)
    obj, obj_type = commit.obj_from_path_str(path_str)
    if obj_type == 'directory':
        if path_str and path_str[-1] != '/':
            url_with_trailing_slash = "/browse/{0}/{1}/".format(sha, path_str)
            return HttpResponseRedirect(url_with_trailing_slash)
        else:
            context = {'dirname'  : path_str,
                       'sha'      : commit.sha,
                       'relpaths' : obj + [".."]}
            return render(request, 'directory.djhtml', context)
    elif obj_type == 'file':
        return HttpResponse(obj, content_type='text/plain')
    else:
        raise Exception

def diff(request, sha_1, sha_2):
    return HttpResponse(gitio.get_diff(gitio.Commit(sha_1),
                                       gitio.Commit(sha_2)),
                        content_type='text/plain')
