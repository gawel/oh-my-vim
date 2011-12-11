
" oh-my-vim related command / tools

command! -complete=custom,OhMyVimCmpl -nargs=+ OhMyVim :call OhMyVim("<args>")

function! OhMyVim(args)
    echo ''
    let a:splitted = split(a:args, ' ')
    if a:splitted[0] == 'theme' && len(a:splitted) > 1
        call pathogen#runtime_append_all_bundles()
        source ~/.vim/ohmyvim/theme.vim
    else
        echo system(g:ohmyvim.' '.a:args)
    endif
endfunction

function! OhMyVimCmpl(A,L,P)
    let a:splitted = split(a:L, ' ')
    let a:cmds=sort(split('search,upgrade,list,remove,theme,profiles,install', ','))
    if len(a:splitted) == 1
        return join(a:cmds, "\n")
    elseif len(a:splitted) == 2
        for a:cmd in a:cmds
            if a:cmd == a:splitted[1]
                let a:splitted = a:splitted + [3]
            endif
        endfor
        if len(a:splitted) == 2
            return join(a:cmds, "\n")
        endif
    endif
    if len(a:splitted) >= 3
        if a:splitted[1] == 'theme'
            return system(g:ohmyvim.' theme --complete')
        elseif a:splitted[1] == 'install'
            return system(g:ohmyvim.' install --complete')
        elseif a:splitted[1] == 'upgrade'
            return system(g:ohmyvim.' list --complete')
        elseif a:splitted[1] == 'remove'
            return system(g:ohmyvim.' list --complete')
        endif
        return "\n"
    endif
endfunction

function! OhMyVimProfiles()
    for profile in g:profiles
        let a:filename="~/.vim/bundle/oh-my-vim/profiles/".profile.".vim"
        execute("source ".a:filename)
    endfor
endfunction

if exists("g:profiles")
    call OhMyVimProfiles()
endif

