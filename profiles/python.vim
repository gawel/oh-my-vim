" fix tabulation. enable long lines highlighting

augroup python
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal fileformat=unix
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal tabstop=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl call PythonBinding
    au BufWinEnter *.?py,*.py,*.py_tmpl let w:m1=matchadd('Search', '\%<81v.\%>77v', -1)
    au BufWinEnter *.?py,*.py,*.py_tmpl let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
augroup END

function! PythonBinding()
    imap <buffer> xxx import pdb;pdb.set_trace()
    imap <buffer> ixx import ipdb;ipdb.set_trace()
endfunction

