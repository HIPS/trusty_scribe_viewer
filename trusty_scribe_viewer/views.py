from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import gitio
from datetime import datetime

def index(request):
    return HttpResponseRedirect("/lab_notebook/50/")

def lab_notebook(request, max_entries=None):
    commit_list = []
    commit = gitio.get_head_commit()
    remaining = int(max_entries) if max_entries else -1
    while True:
        message_lines = commit.message.splitlines()
        title = message_lines[0]
        body = "\n".join(message_lines[1:])
        commit_list.append({'title'         : title,
                            'commit_id'     : commit.sha,
                            'timestamp'     : format_time(commit.timestamp),
                            'prev_commit_id': 0,
                            'body'          : body})
        remaining -= 1
        commit = commit.prev
        if commit is None or remaining == 0: break
        # Note: 'prev' commit based on timestamp. May not actually be a parent.
        commit_list[-1]['prev_commit_id'] = commit.sha

    context = {'repo_name'   : gitio.repo_name,
               'commit_list' : commit_list}
    return render(request, 'notebook.html', context)

def format_time(t):
    return datetime.fromtimestamp(t).strftime('%m-%d %H:%M')

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
            return render(request, 'directory.html', context)
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
