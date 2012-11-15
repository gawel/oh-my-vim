" enable ranger shortcuts

function! RangerChooser()
    if has('gui_running')
        exec "silent !gnome-terminal --disable-factory --maximize -e 'ranger --choosefile=/tmp/chosenfile " . expand("%:p:h") ."'"
    else
        exec "silent !ranger --choosefile=/tmp/chosenfile " . expand("%:p:h")
    endif
    if filereadable('/tmp/chosenfile')
        exec 'edit ' . system('cat /tmp/chosenfile')
        call system('rm /tmp/chosenfile')
    endif
    redraw!
endfunction
map <Leader>r :call RangerChooser()<CR>
map <Leader>rr :split +call\ RangerChooser()<CR>
