" fix tabulation. enable long lines highlighting

augroup python
    au BufNewFile,BufRead *.py_tmpl set filetype=python
    au BufNewFile,BufRead *.py,*.py_tmpl setlocal tabstop=4
    au BufNewFile,BufRead *.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.py,*.py_tmpl setlocal shiftwidth=4
    au BufNewFile,BufRead *.py,*.py_tmpl call PythonBinding()
    au BufWinEnter *.py,*.py_tmpl let w:longline1=matchadd('Search', '\%<80v.\%>76v', -1)
    au BufWinEnter *.py,*.py_tmpl let w:longline2=matchadd('ErrorMsg', '\%>79v.\+', -1)
    au BufWinLeave *.py,*.py_tmpl call clearmatches()

    au BufNewFile,BufRead *.rst setf rst
    au BufNewFile,BufRead *.txt call RstDetect()

    au BufNewFile,BufRead *.mako setf mako
    au BufNewFile,BufRead *.mak call MakoDetect()
augroup END

function! PythonBinding()
    imap <buffer> xxx import pdb;pdb.set_trace()
    imap <buffer> ixx import ipdb;ipdb.set_trace()
endfunction

function! RstDetect()
    for line in getline(1, 3)
        if line =~ '^========'
            setlocal filetype=rst
            break
        elseif line =~ '^.. \w\+'
            setlocal filetype=rst
            break
        endif
    endfor
endfunction

function! MakoDetect()
    for line in getline(1, 2)
        if line =~ '^## -*-'
            setlocal filetype=mako
            break
        endif
    endfor
endfunction
