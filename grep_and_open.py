#!/usr/bin/python3

import os
import sys


search_string = text = input("Add your search string:")

os.system(
    f"""
#!/usr/bin/zsh
cd "$(dirname "{sys.argv[0]}")"
cd notes
grep -r --color=always  "{search_string}"
echo -n "Open notes in Virtual Studio Code(y/n)? "
old_stty_cfg=$(stty -g)
stty raw -echo ; answer=$(head -c 1) ; stty $old_stty_cfg # Careful playing with stty
if echo "$answer" | grep -iq "^y" ;then
    grep -r -l "{search_string}" | xargs code
else
    echo Ok!
fi
"""
)
