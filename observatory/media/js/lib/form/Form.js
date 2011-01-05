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
 *  This is the base class for a form.  Override this to create a class for a 
 *  specific kind of form.
 *  @class
 **/
observatory.Form = function(params) {
    if(params) {
        this.init(params);
    }
}

observatory.Form.prototype.init = function(params) {
 
    var el = params.el;
    if(typeof(el) == 'undefined') {
        throw new Error('params.el is undefined');
    }
    else if(el.length == 0) {
        throw new Error('el not found');
    }
    this.el = el;
    
    var container = params.container;
    if(typeof(container) == 'undefined') {
        throw new Error('params.container is undefined');
    }
    else if(container.length == 0) {
        throw new Error('container not found');
    }
    this.container = container;
    
    /* If we are disabled */
    this.disabled = false;

    /* Enable client side validation */
    el.html5form();
};

/**
 *  When a form is to be disabled to the user.
 **/
observatory.Form.prototype.disable = function() {
    /* make container look disabled */
    this.container.addClass('disabled');
    
    /* Make all fields actually disabled */
    var fields = this.el.attr('elements');
    for(var i = 0, il = fields.length; i < il; i++) {
        var field = fields[i];
        
        $(field).attr('disabled', 'true');
    }
    
    this.disabled = true;
};

/**
 *  When a form should be enabled.
 **/
observatory.Form.prototype.enable = function() {
    this.container.removeClass('disabled');
    
    /* Make all fields actually enabled */
    var fields = this.el.attr('elements');
    for(var i = 0, il = fields.length; i < il; i++) {
        var field = fields[i];
        
        $(field).removeAttr('disabled');
    }
    
    this.disabled = false;
};
