" some settings for django

augroup django
    au BufNewFile,BufRead *.html set filetype=htmldjango.html
    au BufNewFile,BufRead *.py set filetype=python.django
augroup END
