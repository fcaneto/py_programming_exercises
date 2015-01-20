import sys
import os
import shutil

new_dir = sys.argv[1]
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

shutil.copyfile('boilerplate.py', os.path.join(new_dir, 'solution.py'))

