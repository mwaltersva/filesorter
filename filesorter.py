import os, fnmatch, re

def get_regmatches(dir):
    reg_matches = []
    subdirs = [name for name in os.listdir(dir)]
    for subdir in subdirs:
        full_path = dir + '/' + subdir
        if os.path.isfile(full_path +  '/.regmatch'):
            with open(full_path + '/.regmatch') as f:
                reg_match = f.readline().strip()
                reg_matches.append({
                    'dir': full_path + '/',
                    'reg_match': reg_match,
                })
        else:
            with open(full_path + '/.regmatch', 'w+') as f:
                reg_match = '(?i).*' + subdir.replace(' ', '.') + '.*\n'
                f.write(reg_match)
                reg_matches.append({
                    'dir': full_path + '/',
                    'reg_match': reg_match,
                })

    return reg_matches

def search_incoming(dir, reg_matches):
    matches = []
    files = []
    for root, directories, filenames in os.walk(dir):
        for filename in filenames:
            files.append({
            'filename': filename,
            'full_path': os.path.join(root, filename),
            })
    for reg_match in reg_matches:
        reobj = re.compile(reg_match['reg_match'])
        for file in files:
            if reobj.match(file['filename']) is not None:
                matches.append({
                'source': file['full_path'],
                'destination': reg_match['dir'] + file['filename'],
                })

    return matches


def move_files(files):
    with open('/media/raid/filesorter/log.txt', 'w+') as f:
        for file in files:
            out = 'Moving %s to %s\n' % (file['source'], file['destination'])
            f.write(out)
            os.rename(file['source'], file['destination'])

move_files(
    search_incoming(
        '/media/raid/incoming/complete',
        get_regmatches('/media/raid/Videos/anime')
    )
)