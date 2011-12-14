" always try to convert file to utf-8

function! UTF8Settings()
    try
        silent setlocal fileformat=unix
        silent setlocal encoding=utf-8
        silent setlocal fileencoding=utf-8
        silent setlocal termencoding=utf-8
	catch /.*/
        echo ''
    endtry
endfunction

if has("multi_byte")
    au BufNewFile,BufRead * silent call UTF8Settings()
endif

