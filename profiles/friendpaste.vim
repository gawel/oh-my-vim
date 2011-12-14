" Paste your selected lines to friendpaste.org

command! -nargs=0 -range=% FriendPaste :call FriendPaste()
function! FriendPaste()
    let a:tmpfile = tempname()
    let a:bin = 'fpcli'
    if executable(a:bin) == 0 && executable(g:ohmyvim)
        let a:bin = fnamemodify(g:ohmyvim, ':h').'/fpcli'
    endif
    if executable(a:bin)
        silent exe "'<,'>write! ".a:tmpfile
        let a:out = system(a:bin." ".a:tmpfile)
        silent echo system("rm ".a:tmpfile)
        let a:splitted = split(a:out, '\n')
        if len(a:splitted) == 1
            echo a:splitted[0]
        else
            echo a:out
        endif
    else
        echo 'fpcli is not in your PATH'
    endif
endfunction
