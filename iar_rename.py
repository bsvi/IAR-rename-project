import glob, os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Renames IAR projects.')
parser.add_argument('name', nargs=1, help="New name for IAR project")
option = parser.parse_args()

name = option.name[0]

def get_name(f):
	return os.path.splitext(os.path.basename(f))[0]

def remove_by_mask(mask):
	for fl in glob.glob(mask):
		os.remove(fl)

project = glob.glob("*.ewp");

if not project:
	print "No project"
	exit(0)

project = project[0]
new_project = name+".ewp"

# Rename project
os.rename(project, new_project)
print "Project renamed"

# Delete misc files
remove_by_mask("*.dep")
remove_by_mask("*.ewd")
remove_by_mask("*.ewt")
if os.path.exists("Debug"): shutil.rmtree('Debug')
if os.path.exists("Release"): shutil.rmtree('Release')
print "Dep filese deleted"


# Repalece in eww
workspace = glob.glob("*.eww");
if workspace:
	ws = workspace[0]

	filedata = None
	with open(ws, 'r') as f:
		filedata = f.read()

	filedata = filedata.replace(project, new_project)

	with open(ws, 'w') as f:
		f.write(filedata)
	print "Workspace record replaced"

	if get_name(ws) == get_name(project):
		os.rename(ws, get_name(new_project)+".eww")
		print "Workspace renamed"