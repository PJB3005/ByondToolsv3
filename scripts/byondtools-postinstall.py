#------------------------------------------------------------------------------
# Originally cxfreeze-postinstall
#   Script run after installation on Windows to fix up the Python location in
# the script as well as create batch files.
#------------------------------------------------------------------------------

import distutils.sysconfig
import glob, os, sys

vars = distutils.sysconfig.get_config_vars()
prefix = vars["prefix"]
python = sys.executable #os.path.join(prefix, "python.exe")
scriptDir = os.path.join(prefix, "Scripts")

# Keep in sync with setup.py.
scripts = [
    'dmm',
    'dmi',
    'dmindent',
    'dmmrender',
    'dmmfix',
    
    #TODO: Combine into dmi.
    'ss13_makeinhands',
    
    # Our post-install.  Now run on Linux, as well.
    "byondtools-postinstall"
]

for fileName in glob.glob(os.path.join(scriptDir, "*.py")):
    # skip already created batch files if they exist
    name, ext = os.path.splitext(os.path.basename(fileName))
    if name not in scripts or name == 'byondtools-postinstall':
        continue

    print('Running post-install for {}.'.format(name))
    # copy the file with the first line replaced with the correct python
    fullName = os.path.join(scriptDir, fileName)
    strippedName = os.path.join(scriptDir, name)
    lines = open(fullName).readlines()
    startidx=1
    if not lines[0].strip().startswith('#!'):
        print('WARNING: {} does not have a shebang.'.format(name))
        startidx=0
    
    targetFile = strippedName
    if sys.platform == 'win32':
        targetFile = fullName
    with open(targetFile, "w") as outFile:
        outFile.write("#!{}\n".format(python)) # Not sure why this is done on Windows...
        for line in lines[startidx:]:
            outFile.write(line.rstrip('\r\n \t')+"\n") # Shit happens on Linux if this isn't done.

    if sys.platform == 'win32':
        # create the batch file
        batchFileName = strippedName + ".bat"
        command = "{} {} %*".format(python, targetFile)
        open(batchFileName, "w").write("@echo off\n\n{}".format(command))

