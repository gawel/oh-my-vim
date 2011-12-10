if exists("b:loaded_py_plugin")
  finish
endif
let b:loaded_py_plugin = 1

command! OhMyVimReload :source ~/.vim/ohmyvim/ohmyvim.vim


command! -nargs=+ OhMyVim :echo system(g:ohmyvim.' <args>')
