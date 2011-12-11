" git helpers

au FileType gitcommit map <buffer> <C-D> :DiffGitCached<CR>
au FileType gitcommit imap <buffer> <C-D> <Esc>:DiffGitCached<CR>

