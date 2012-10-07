" some mapping to navigate in vim
"
" copy text to "+ (clipboard)
vmap <Leader>yy "+y

" paste text from "+ (clipboard)
map <Leader>pp "+P
vmap <Leader>pp "+P
imap <Leader>pp <Space><Esc>"+P<Right>xi

" only show the current buffer
map <Leader>o :only<CR>

" open BufExplorer if available
map <Leader>b :BufExplorer<CR>
map <Leader>bb :split +BufExplorer<CR>

" toogle nerdtree
map <Leader>t :NERDTreeToggle<CR>

" create a new file in the current directory
map <Leader>n :call histadd(':','edit '.substitute(expand('%:p:h'),$HOME,"~","").'/')<CR>:<Up>

" open a browser in the current directory
map <Leader>e :edit %:p:h<CR>:5<CR>

" split horizontaly and open a browser in the current directory
map <Leader>ee :split %:p:h<CR>:5<CR>

" split verticaly and open a browser in the current directory
map <Leader>vv :vsplit %:p:h<CR>:5<CR>

" window left
map <C-L> <C-W>l

" window right
map <C-H> <C-W>h

" window bellow
map <C-J> <C-W>j<C-W>_

" window above
map <C-K> <C-W>k<C-W>_

" maximize window
map <C-F> <C-W>_

