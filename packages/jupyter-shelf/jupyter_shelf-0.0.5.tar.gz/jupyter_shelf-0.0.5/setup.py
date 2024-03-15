import os
import sys
import setuptools

setuptools.setup(
    entry_points={
        'console_scripts': [
            'shelf = jupyter_shelf:main',
        ],
    },
)

# Post-installation: Add the script directory to PATH
script_dir = os.path.expanduser('~/.local/bin/')
path_update = '\n# Added by jupyter_shelf installation\nexport PATH="$PATH:' + script_dir + '"\n'

# Check if we are NOT in a virtual environment  and NOT in a Conda environment
if sys.prefix == sys.base_prefix and 'conda' not in sys.version:
    bashrc_path = os.path.expanduser('~/.bashrc')
    with open(bashrc_path, 'r') as f:
        if path_update in f.read():
            print("The PATH is already updated.")
        else:
            with open(bashrc_path, 'a') as f:
                f.write(path_update)
            print("The PATH has been updated.")