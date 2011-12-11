" Paste your selected lines to friendpaste.org

command! -nargs=0 -range FriendPaste :call FriendPaste()
function! FriendPaste()
    let a:tmpfile = tempname()
    let a:bin = fnamemodify(g:ohmyvim, ':h')
    silent exe "'<,'>write! ".a:tmpfile
    echo system(a:bin."/fpcli ".a:tmpfile)
    silent echo system("rm ".a:tmpfile)
endfunction
