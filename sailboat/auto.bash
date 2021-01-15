_sailboat_complete () {
	WORDS=`python -m sailboat.autocomplete "${COMP_LINE}"`
  COMPREPLY=( `compgen -W "${WORDS}" -- ${COMP_WORDS[COMP_CWORD]} `)
}

complete -F _sailboat_complete sail