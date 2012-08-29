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
map ,r :call RangerChooser()<CR>
map ,rr :split +call\ RangerChooser()<CR>
