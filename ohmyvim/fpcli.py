#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2008, Mickaël Guérin <kael@crocobox.org>
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
Friendpaste
=======

Paste your code to Friendpaste' services like friendpaste.com

The last paste Id is saved in ~/.friednpaste or $APPDATA\_friendpaste
in order to use the -u flag to update it.

Copy to clipboard code (copy_url) taken from LodgeIt shell script (lodgeit.pocoo.org)
"""

import httplib
import os
import re
import socket
import sys

import json

FRIENDPASTE_SERVER = os.environ.get("FRIENDPASTE_SERVER", "friendpaste.com")
DEFAULT_LANG = os.environ.get("FRIENDPASTE_DEFAULT_LANG", "text")

build_url_withrev = lambda (base_url, nb_revision): ('%s?rev=%s' %
        (base_url, nb_revision))
if os.name == 'nt' and 'APPDATA' in os.environ:
    IDFILE_PATH = os.path.expandvars(r'$APPDATA\_friendpaste')
else:
    IDFILE_PATH = os.path.expanduser('~/.friendpaste')

def handle_errors(f):
    """
    decorator to drop the exceptions
    """
    def _temp(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (httplib.HTTPException, socket.error, socket.herror, socket.gaierror), e:
            print >> sys.stderr, 'HTTP error: %s' % e
        except Exception, e:
            print >> sys.stderr, 'Error while decoding response: %s' % e
        return None
    return _temp

@handle_errors
def save_last_snippet_id(paste_id):
    fd = file(IDFILE_PATH, 'w')
    fd.write(paste_id)
    fd.close

@handle_errors
def read_last_snippet_id():
    fd = file(IDFILE_PATH, 'r')
    paste_id = fd.read()
    fd.close
    return paste_id

def copy_url(url):
    """Copy the url into the clipboard."""
    if sys.platform == 'darwin':
        url = re.escape(url)
        os.system(r"echo %s | pbcopy" % url)
        return True

    try:
        import win32clipboard
        import win32con
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(url)
        win32clipboard.CloseClipboard()
        return True
    except ImportError:
        try:
            if os.environ.get('DISPLAY'):
                import pygtk
                pygtk.require('2.0')
                import gtk
                import gobject
                gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD).set_text(url)
                gobject.idle_add(gtk.main_quit)
                gtk.main()
                return True
        except:
            pass
    return False
@handle_errors
def get_languages():
    c = httplib.HTTPConnection(FRIENDPASTE_SERVER)
    c.request('GET','/_all_languages', None, {'Accept': 'application/json'})
    languages = json.load(c.getresponse())
    c.close()
    return languages

@handle_errors
def paste(title, snippet, language, paste_id=None):
    if language not in [l for l, d in get_languages()]:
        raise Exception("Language '%s' unavailable" % language)
    paste_data = {'title': title, 'snippet': snippet, 'language': language}
    if paste_id:
        import re
        m = re.compile(r'(.*/)?(?P<paste_id>[a-zA-Z0-9]+)(\?rev=.*)?').match(paste_id)
        if m:
            paste_id = m.group('paste_id')
        else:
            raise Exception('invalid Id while updating snippet')
    c = httplib.HTTPConnection(FRIENDPASTE_SERVER)
    if paste_id:
        # update a paste
        c.request('PUT','/%s' % paste_id, json.dumps(paste_data),
                {'Accept': 'application/json',
                    'Content-Type': 'application/json'})
    else:
        # new paste
        c.request('POST','/', json.dumps(paste_data),
                {'Accept': 'application/json',
                    'Content-Type': 'application/json'})
    resp = json.load(c.getresponse())
    c.close()
    return resp

def main():
    # parse command line
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--languages', action='store_true',
            dest='print_languages',
            help='print the list of supported languages')
    parser.add_option('-t', '--title', action='store',
            dest="title",
            default='', help='title')
    parser.add_option('-l', '--language', action='store',
            dest="language",
            default=DEFAULT_LANG, help='language used for syntax coloration')
    parser.add_option('-i', '--update-id', action='store',
            dest="paste_id",
            default=None, help='update the snippet with this id')
    parser.add_option('-u', '--update-last', action='store_true',
            dest="update_last",
            default=False, help='update your last snippet')
    (options, args) = parser.parse_args()

    if len(args) > 1:
        print >> sys.stderr, 'Too many parameters'
        sys.exit(1)

    if options.print_languages:
        languages = get_languages()
        for language, description in languages:
            print "\t%12s   %s" % (language, description)
        sys.exit(0)

    # create a new paste
    if args:
        fd = file(args[0], 'r')
    else:
        fd = sys.stdin
    data = fd.read().strip()
    fd.close()

    if not data:
        print >> sys.stderr, 'Error: empty snippet'
        sys.exit(1)

    paste_id = None
    if options.paste_id:
        paste_id = options.paste_id
    elif options.update_last:
        paste_id = read_last_snippet_id()

    resp = paste(options.title, data, options.language, paste_id=paste_id)
    if not resp:
        sys.exit(1)

    if resp['ok']:
        if options.paste_id:
            print '%s  ->  %s' % (resp['url'],
                    build_url_withrev((resp['url'],resp['nb_revision'])))
        else:
            print '%s' % (resp['url'])
        copy_url(resp['url'])
        save_last_snippet_id(resp['id'])
    else:
        print >> sys.stderr, 'An error occured: %s' % resp['reason']

if __name__ == '__main__':
    main()
