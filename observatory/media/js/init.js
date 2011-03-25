/**
 *  Copyright (c) 2010, Colin Sullivan <colinsul [at] gmail.com>
 *
 *  Permission to use, copy, modify, and/or distribute this software for any
 *  purpose with or without fee is hereby granted, provided that the above
 *  copyright notice and this permission notice appear in all copies.
 *
 *  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 *  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 *  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 *  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 *  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 *  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 *  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 **/



/**
 *  This should be called from the template to initialize any client-side code.
 *
 *  @param  {String}    js_page_id    -    The identifier so we know which page.
 **/
function initialize_page(js_page_id) {
    /* The page identifiers that we know of */
    var page_classes = {
        'login-register': observatory.LoginRegisterPage,
        'add_project': observatory.AddProjectPage,
        'show_project': observatory.ShowProjectPage
    };
    
    var page_class = page_classes[js_page_id];
    
    if(!page_class) {
        throw new Error('No initializer found for page: '+js_page_id);
    }
    
    $(document).ready(function(page_class) {
        return function() {
            var page = new page_class({});
        };
    }(page_class));
    
}

