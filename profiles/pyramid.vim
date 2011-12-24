" some settings for django

augroup pyramid
    au BufNewFile,BufRead *.py call PyramidDetect()
    au BufNewFile,BufRead *.pt set filetype=pagetemplate.xml
    au BufNewFile,BufRead *.pt silent call PagetemplatesBindings()
augroup END

function! PyramidDetect()
    for line in getline(1, 10)
        if line =~ '^from pyramid'
            setlocal filetype=python.pyramid
            break
        endif
    endfor
endfunction

function! PagetemplatesBindings()
    imap <buffer> aaa tal:attributes=""<Esc>i
    imap <buffer> ccc tal:content=""<Esc>i
    imap <buffer> ddd tal:define=""<Esc>i
    imap <buffer> rrr tal:repeat=""<Esc>i
    imap <buffer> iii tal:condition=""<Esc>i
    imap <buffer> ttt i18n:translate=""<Esc>i
endfunction

