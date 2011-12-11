" helpers for zope page templates

augroup zpt
    au BufNewFile,BufRead *.?pt,*.pt setf html
    au BufNewFile,BufRead *.?pt,*.pt let xml_use_xhtml = 1
    au BufNewFile,BufRead *.?pt,*.pt silent call PagetemplatesBindings
augroup END

function! PagetemplatesBindings()
    syn match htmlTag "\(tal\|metal\):\([a-z]\)*"
    syn match htmlArg "\(tal\|metal\|i18n\):\([a-z]\|-\)*"
    syn match htmlArg "\([a-z]\)*-\([a-z]\)*="
    highlight Statement ctermfg=darkblue guifg=darkblue
    highlight Identifier ctermfg=darkblue guifg=darkblue
    imap <buffer> aaa tal:attributes=""<Esc>i
    imap <buffer> ccc tal:content=""<Esc>i
    imap <buffer> ddd tal:define=""<Esc>i
    imap <buffer> rrr tal:repeat=""<Esc>i
    imap <buffer> iii tal:condition=""<Esc>i
    imap <buffer> ttt i18n:translate=""<Esc>i
endfunction
