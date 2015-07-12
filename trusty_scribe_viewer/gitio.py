import os
import pygit2
import itertools as it
from datetime import datetime
from render_commit_body import body_as_html

repo_path = os.environ['REPOPATH']
repo_name = os.path.basename(os.path.abspath(repo_path))
repo = pygit2.Repository(repo_path)

class Commit(object):
    def __init__(self, sha):
        self.obj = repo[sha]
        self.sha = str(self.obj.id)[:16]

    @property
    def timestamp(self):
        return datetime.fromtimestamp(self.obj.commit_time)

    @property
    def author(self):
        return self.obj.author.name

    @property
    def parents(self):
        return map(commit_from_pygit2_obj, self.obj.parents)

    @property
    def updated_files(self):
        files = set()
        for parent in self.parents:
            diff = repo.diff(self.obj, parent.obj)
            files.update([patch.new_file_path for patch in diff])
        return sorted(list(files))

    @property
    def title(self):
        return self.obj.message.split('\n', 1)[0]

    @property
    def rendered_content(self):
        body_text = self.obj.message.split('\n', 1)[1]
        return body_as_html(self.sha, body_text)

    def obj_from_path_str(self, path_str):
        path = filter(bool, path_str.split('/'))
        root_tree = repo[self.sha].tree
        obj = obj_from_tree(root_tree, path)
        if isinstance(obj, pygit2.Tree):
            return [child.name for child in obj], 'directory'
        elif isinstance(obj, pygit2.Blob):
            return obj.data, 'file'
        else:
            raise Exception

def commit_from_pygit2_obj(obj):
    assert isinstance(obj, pygit2.Commit)
    return Commit(obj.id)

def lifo_commits(N=None):
    walker = repo.walk(head_commit().sha, pygit2.GIT_SORT_TIME)
    return it.islice(it.imap(commit_from_pygit2_obj, walker), N)

def obj_from_tree(tree, path):
    if path:
        subtree = repo[tree[path[0]].id]
        return obj_from_tree(subtree, path[1:])
    else:
        return tree

def head_commit():
    return Commit(str(repo.head.target))

def get_diff(commit_1, commit_2):
    return repo.diff(commit_1.obj, commit_2.obj).patch
