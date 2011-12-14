
" oh-my-vim related command / tools

command! -complete=custom,OhMyVimCmpl -nargs=+ OhMyVim :call OhMyVim("<args>")

function! OhMyVim(args)
    let a:splitted = split(a:args, ' ')
    if a:splitted[0] == 'version'
        echo 'OhMyVim v'.split(system(g:ohmyvim.' version'), '\n')[0]
    elseif a:splitted[0] == 'theme' && len(a:splitted) > 1
        call system(g:ohmyvim.' '.a:args)
        call pathogen#runtime_append_all_bundles()
        source ~/.vim/ohmyvim/theme.vim
    else
        echo system(g:ohmyvim.' '.a:args)
    endif
endfunction

function! OhMyVimCmpl(A,L,P)
    let a:splitted = split(a:L, ' ')
    let a:cmds=sort(split('info,version,search,list,upgrade,remove,theme,profiles,install', ','))
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
            return system(g:ohmyvim.' theme --raw')
        elseif a:splitted[1] == 'info'
            return system(g:ohmyvim.' list -a --raw')
        elseif a:splitted[1] == 'install'
            return system(g:ohmyvim.' install --raw')
        elseif a:splitted[1] == 'upgrade'
            return system(g:ohmyvim.' list --raw')
        elseif a:splitted[1] == 'remove'
            return system(g:ohmyvim.' list --raw')
        endif
    endif
    return "\n"
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

if exists(g:ohmyvim) == 0
    if executable('oh-my-vim')
        let g:ohmyvim = 'oh-my-vim'
    endif
endif
