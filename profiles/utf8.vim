" always try to convert file to utf-8

function! UTF8Settings()
    try
        setlocal termencoding=utf-8
        setlocal encoding=utf-8
        setlocal fileformat=unix
        setlocal fileencoding=utf-8
	catch /.*/
        echo ''
    endtry
endfunction

if has("multi_byte")
    au BufNewFile,BufRead * if &ft != 'help' | call UTF8Settings() | endif
endif

