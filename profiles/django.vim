" some settings for django

augroup django
    au BufNewFile,BufRead *.html call DjangoDetect()
    au BufNewFile,BufRead *.py call DjangoDetect()
augroup END

function! DjangoDetect()
    for line in getline(1, 10)
        if line =~ '^from django'
            setlocal filetype=python.django
            break
        elseif line =~ '^{% extends'
            setlocal filetype=htmldjango.html
            break
        endif
    endfor
endfunction
