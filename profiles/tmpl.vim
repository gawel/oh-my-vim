" templates for new files

command! -complete=file -nargs=1 Template call Template("<args>")

function! Template(args)
    execute "edit ".a:args
    let filename = expand("%:p:t")
    for path in pathogen#split(&runtimepath)
        let tmpl = path."/templates/".filename
        if filereadable(tmpl)
            execute "read ".tmpl
            execute "1:del"
            break
        endif
        let splitted = split(filename, "\.")
        if len(splitted)
            let tmpl = path."/templates/tmpl.".splitted[-1]
            if filereadable(tmpl)
                execute "read ".tmpl
                execute "1:del"
                break
            endif
        endif
    endfor
endfunction
