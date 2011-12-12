" Paste your selected lines to friendpaste.org

command! -nargs=0 -range FriendPaste :call FriendPaste()
function! FriendPaste()
    let a:tmpfile = tempname()
    let a:bin = 'fpcli'
    if executable(a:bin) == 0 && executable(g:ohmyvim)
        let a:bin = fnamemodify(g:ohmyvim, ':h').'/fpcli'
    endif
    if executable(a:bin)
        silent exe "'<,'>write! ".a:tmpfile
        echo system(a:bin." ".a:tmpfile)
        silent echo system("rm ".a:tmpfile)
    else
        echoerr 'fpcli is not in your PATH'
    endif
endfunction
