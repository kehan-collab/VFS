# VFS Mini-Shell

## Overview
A Python-based Virtual File System (VFS) Mini-Shell.  
Simulates a file system stored in a single binary file with multi-user support, journaling, search, and folder protection.

## Features
- Create, read, write, and delete files/folders.
- Multi-user login with password hashing.
- Permission simulation (read/write/execute).
- Journaling of all operations.
- Search files by name or content.
- Password-protected folders.

## Installation & Running
1. Clone the repository:
```bash
git clone https://github.com/kehan-collab/VFS.git
cd VFS_MiniShell
```

2. Run the shell:
```bash
python3 main.py
```

3. Example commands inside the shell:
```bash
adduser admin
login admin
mkdir projects
create report.txt
write report.txt "Hello VFS!"
read report.txt
search -n report
journal show
save
exit
```

### Files

- filesystem.bin – stores virtual file system (ignored in Git)

- users.bin – stores users (ignored in Git)

- vfs/ – Python modules for VFS