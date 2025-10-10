# vfs/permissions.py


class Permissions:
    READ = 4
    WRITE = 2
    EXECUTE = 1


class PermissionManager:
    def __init__(self):
        self.permissions = {}

    def set_permission(self, path, user, perm):
        self.permissions[path] = (user, perm)

    def check_permission(self, path, user, action):
        if path not in self.permissions:
            return True
        owner, perm = self.permissions[path]
        if user == owner:
            return (perm & action) == action
        else:
            return False
