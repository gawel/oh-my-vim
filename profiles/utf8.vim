" utf8 conversion

function! UTF8Settings()
    setlocal fileformat=unix
    setlocal encoding=utf-8
    setlocal fileencoding=utf-8
    setlocal termencoding=utf-8
endfunction

if has("multi_byte")
    au BufNewFile,BufRead * silent call UTF8Settings()
endif

