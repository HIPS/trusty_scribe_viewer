import os
import pygit2

repo = pygit2.Repository(os.environ['REPOPATH'])

def obj_from_path(commit_hash, path):
    root_tree = repo[commit_hash].tree
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
