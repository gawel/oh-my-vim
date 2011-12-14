" fix tabulation. enable long lines highlighting

augroup python
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl set filetype=python
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal fileformat=unix
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal tabstop=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.?py,*.py,*.py_tmpl call PythonBinding()
    au BufWinEnter *.?py,*.py,*.py_tmpl let b:longline1=matchadd('Search', '\%<80v.\%>76v', -1)
    au BufWinEnter *.?py,*.py,*.py_tmpl let b:longline2=matchadd('ErrorMsg', '\%>79v.\+', -1)
    au BufWinLeave *.?py,*.py,*.py_tmpl call matchdelete(b:longline1)
    au BufWinLeave *.?py,*.py,*.py_tmpl call matchdelete(b:longline2)
augroup END

function! PythonBinding()
    imap <buffer> xxx import pdb;pdb.set_trace()
    imap <buffer> ixx import ipdb;ipdb.set_trace()
endfunction

