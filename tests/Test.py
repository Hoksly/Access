import subprocess

'''
process = subprocess.Popen('', stdout=subprocess.PIPE)

out, err = process.communicate()
print(out.decode('utf-8'))

var = {'read_only': 'u-w-x+r', 'write_and_read': 'u-x+r+w', 'write__read_execute': 'u+r+w+x',
       'delete_all_permissions': 'u-x-w-r-s'}
'''


def ChangeFilePermissions(file, mode):
    bash = 'chmod '
    if mode == 'r':
        bash += 'u+r-w-x ' + file

    elif mode == 'wr':
        bash += 'u+r+w-x ' + file

    elif mode == 'rwx':
        bash += 'u+r+w+x ' + file

    elif mode == 'rx':
        bash += 'u+r+x-w ' + file

    elif mode == 'd':
        bash += 'u-x-r-w' + file

    else:
        bash += 'u-r-w'

    proc = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
    out, err = proc.communicate()

    if err is not None:
        return err


def ChangeDirectoryPermissions(directory, mode):
    bash = 'chmod '
    if mode == 'r':
        bash += 'a+x-w+r ' + directory

    elif mode == 'wr':
        bash += 'u+r+w+x ' + directory

    elif mode == 'rwx':
        bash += 'u+r+w+x ' + directory

    elif mode == 'rx':
        bash += 'u+r+x-w ' + directory

    elif mode == 'd':  # delete all permissions
        bash += 'u-x ' + directory

    else: # delete write and read permissions
        bash += 'u-r-w ' + directory

    process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
    out, err = process.communicate()

    if err is not None:
        return err


    
