import os
import pygit2

repo_path = os.environ['REPOPATH']
repo_name = os.path.basename(os.path.abspath(repo_path))
repo = pygit2.Repository(repo_path)

class Commit(object):
    def __init__(self, sha):
        self.sha = sha
        self.obj = repo[sha]

    @property
    def prev(self):
        walker = repo.walk(self.sha, pygit2.GIT_SORT_TIME)
        try:
            walker.next()
            return Commit(str(walker.next().id))
        except StopIteration:
            return None

    @property
    def timestamp(self):
        return self.obj.commit_time

    @property
    def message(self):
        return self.obj.message

    def obj_from_path(self, path):
        root_tree = repo[self.sha].tree
        obj = obj_from_tree(root_tree, path)
        if type(obj) is pygit2.Tree:
            return [child.name for child in obj], 'directory'
        elif type(obj) is pygit2.Blob:
            return obj.data, 'file'
        else:
            raise Exception

def obj_from_tree(tree, path):
    if path:
        subtree = repo[tree[path[0]].id]
        return obj_from_tree(subtree, path[1:])
    else:
        return tree

def get_head_commit():
    return Commit(str(repo.head.target))

def get_diff(commit_1, commit_2):
    return repo.diff(commit_1.obj, commit_2.obj).patch
