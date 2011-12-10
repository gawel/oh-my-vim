if exists("b:loaded_py_ftplugin")
  finish
endif
let b:loaded_py_ftplugin = 1

:command! OhMyVimReload :source ~/.vim/ohmyvim/ohmyvim.vim

