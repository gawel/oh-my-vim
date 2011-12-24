" helpers for zope page templates

augroup zpt
    au BufNewFile,BufRead *.?pt,*.pt set filetype=pagetemplate.xml
    au BufNewFile,BufRead *.?pt,*.pt silent call PagetemplatesBindings()
augroup END

function! PagetemplatesBindings()
    imap <buffer> aaa tal:attributes=""<Esc>i
    imap <buffer> ccc tal:content=""<Esc>i
    imap <buffer> ddd tal:define=""<Esc>i
    imap <buffer> rrr tal:repeat=""<Esc>i
    imap <buffer> iii tal:condition=""<Esc>i
    imap <buffer> ttt i18n:translate=""<Esc>i
endfunction
