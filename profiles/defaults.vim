" some defaults settings
syntax on
filetype plugin indent on

set ruler
set number
set autoread
set expandtab
set nocompatible
set noerrorbells
set visualbell t_vb=
set showcmd showmode
set hlsearch incsearch ignorecase smartcase

set ls=2
set noai
set mouse=a
set tabstop=4
set shiftwidth=4

" rhis is arbitrary. but the default is full and havind a list is pretty handy
set wildmenu wildmode=list:full

" a more user friendly statusbar
set statusline=%F%m%r%h%w\ format=%{&ff}\ type=%Y\ x=%l\ y=%v\ %p%%\ %{strftime(\"%d/%m/%y\ -\%H:%M\")}

" few gui stuff
if has('gui_running')
    set noerrorbells
    if $VIM == '/Applications/MacVim.app/Contents/Resources/vim'
        set guifont="Menlo Regular:h11"
        win 150 50
    else
        set lines 50
    endif
endif
