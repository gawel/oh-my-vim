" utf8 conversion

command! ToUnixFormat :set fileformat=unix

command! ToUtf8 call FuToUtf8()
function! FuToUtf8()
    silent! setlocal encoding=utf-8
    silent! setlocal fileencoding=utf-8
    silent! setlocal termencoding=utf-8
endfunction

if has("multi_byte")
    call FuToUtf8()
    au BufNewFile,BufRead * :silent call FuToUtf8()
endif
