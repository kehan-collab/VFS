# main.py
from vfs.filesystem import FileSystem
from vfs.users import UserManager
from vfs.permissions import Permissions, PermissionManager
from vfs.journaling import Journal
from vfs.search import search_by_name, search_by_content
from vfs.protection import ProtectionManager

fs = FileSystem.load()
users = UserManager()
perm = PermissionManager()
journal = Journal()
protect = ProtectionManager()

def help_menu():
    print("""
Commands:
login <user>               - login as user
adduser <user>             - add a new user
mkdir <name>               - create folder
create <name>              - create file
write <name> <content>     - write file
read <name>                - read file
ls                         - list directory
search -n <name>           - search by name
search -c <text>           - search by content
journal show               - show journal
save                       - save filesystem
exit                       - exit shell
""")

def shell():
    while True:
        cmd = input(f"{users.current_user or 'guest'}:/ > ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "help":
            help_menu()
        elif cmd[0] == "login" and len(cmd) > 1:
            pw = input("Password: ")
            users.login(cmd[1], pw)
        elif cmd[0] == "adduser" and len(cmd) > 1:
            pw = input("Password: ")
            users.add_user(cmd[1], pw)
        elif cmd[0] == "mkdir" and len(cmd) > 1:
            fs.mkdir(cmd[1])
            journal.log("mkdir", cmd[1], users.current_user)
        elif cmd[0] == "create" and len(cmd) > 1:
            fs.create_file(cmd[1])
            journal.log("create", cmd[1], users.current_user)
        elif cmd[0] == "write" and len(cmd) > 2:
            name = cmd[1]
            content = " ".join(cmd[2:])
            fs.write_file(name, content)
            journal.log("write", name, users.current_user)
        elif cmd[0] == "read" and len(cmd) > 1:
            fs.read_file(cmd[1])
        elif cmd[0] == "ls":
            fs.list_dir()
        elif cmd[0] == "search" and len(cmd) > 2:
            if cmd[1] == "-n":
                results = search_by_name(fs.current_folder, cmd[2])
                for r in results: print(r)
            elif cmd[1] == "-c":
                results = search_by_content(fs.current_folder, cmd[2])
                for r in results: print(r)
        elif cmd[0] == "journal" and len(cmd) > 1 and cmd[1] == "show":
            journal.show()
        elif cmd[0] == "save":
            fs.save()
            users.save_users()
            print("Saved")
        elif cmd[0] == "exit":
            fs.save()
            users.save_users()
            break
        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    help_menu()
    shell()
