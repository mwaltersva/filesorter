import os, fnmatch, re

def get_regmatches(dir):
	reg_matches = []
	subdirs = [x[0] for x in os.walk(dir)]
	for subdir in subdirs:
		if os.path.isfile(subdir + '/.regmatch'):
			with open(subdir + '/.regmatch') as f:
				reg_match = f.readline().strip()
				reg_matches.append({
					'dir': subdir + '/',
					'reg_match': reg_match,
				})
			f.close()
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
	for file in files:
		os.rename(file['source'], file['destination'])
"""
move_files(
	search_incoming(
		'/media/raid/incoming/complete',
		get_regmatches('/media/raid/Videos/anime')
	)
)
"""

print(search_incoming('/media/raid/incoming/complete',get_regmatches('/media/raid/Videos/anime')))
