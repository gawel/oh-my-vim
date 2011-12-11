" oh-my-vim related command / tools

command! -complete=custom,OhMyVimCmpl -nargs=+ OhMyVim :call OhMyVim("<args>")

function! OhMyVim(args)
    echo system(g:ohmyvim.' '.a:args)
endfunction

function! OhMyVimCmpl(A,L,P)
    let a:cmds='search,upgrade,list,remove,theme,profiles,install'
    return join(sort(split(a:cmds, ',')), "\n")
endfunction

function! OhMyVimProfiles()
    for profile in g:profiles
        let a:filename="~/.vim/bundle/oh-my-vim/profile/".profile.".vim"
        execute("source ".a:filename)
    endfor
endfunction

if exists("g:profiles")
    call OhMyVimProfiles()
endif

