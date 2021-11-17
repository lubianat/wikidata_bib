#!/usr/bin/zsh
cd "$(dirname "$0")"
cd notes
grep -r --color=always  $1 
echo -n "Open notes in Virtual Studio Code(y/n)? "
old_stty_cfg=$(stty -g)
stty raw -echo ; answer=$(head -c 1) ; stty $old_stty_cfg # Careful playing with stty
if echo "$answer" | grep -iq "^y" ;then
    grep -r -l $1 | xargs code
else
    echo Ok!
fi