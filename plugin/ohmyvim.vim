
" oh-my-vim related command / tools

command! -complete=custom,OhMyVimCmpl -nargs=+ OhMyVim :call OhMyVim("<args>")

function! OhMyVim(args)
    let a:splitted = split(a:args, ' ')
    echo system(g:ohmyvim.' '.a:args)
    if a:splitted[0] == 'theme' && len(a:splitted) > 1
        call pathogen#runtime_append_all_bundles()
        source ~/.vim/ohmyvim/theme.vim
    endif
endfunction

function! OhMyVimCmpl(A,L,P)
    " a lot of improvment can be done here...
    let a:splitted = split(a:L, ' ')
    if len(a:splitted) == 2
        let a:cmds='search ,upgrade ,list ,remove ,theme ,profiles ,install '
        return join(sort(split(a:cmds, ',')), "\n")
    endif
    if len(a:splitted) >= 3
        if a:splitted[1] == 'theme'
            return system(g:ohmyvim.' theme -l')
        elseif a:splitted[1] == 'upgrade'
            return system(g:ohmyvim.' upgrade')
        elseif a:splitted[1] == 'remove'
            return system('ls ~/.vim/bundle/')
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

