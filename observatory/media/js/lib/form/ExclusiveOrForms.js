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
 *  This class handles a pair of forms where only one of which is to be used at
 *  a time.  It will disable one of the forms if the other is being used.
 *  @class
 **/
observatory.ExclusiveOrForms = function(params) {
    if(params) {
        this.init(params);
    }
}

observatory.ExclusiveOrForms.prototype.init = function(params) {
    
    /* One of the forms */
    var formA = params.formA;
    if(typeof(formA) == 'undefined') {
        throw new Error('params.formA is undefined');
    }
    this.formA = formA;
    
    /* The other form */
    var formB = params.formB;
    if(typeof(formB) == 'undefined') {
        throw new Error('params.formB is undefined');
    }
    this.formB = formB;
    
    formA.el.bind('change', function(me){
        return function(e){
            me.form_has_changed(me.formA, me.formB, e);
        };
    }(this));
    
    formB.el.bind('change', function(me){
        return function(e) {
            me.form_has_changed(me.formB, me.formA, e);
        };
    }(this));
};

observatory.ExclusiveOrForms.prototype.form_has_changed = function(changed, other, e) {
    var inputElements = e.currentTarget.elements;
    
    var formIsEmpty = true;
    for(var i = 0, il = inputElements.length; i < il; i++) {
        var inputElement = $(inputElements[i]);
        
        /* If this isn't an input element */
        if(!inputElement.is('input')) {
            continue;
        }

        var defaultValue = inputElement.attr('defaultValue');
        var currentValue = inputElement.attr('value');
        
        if(defaultValue != currentValue) {
            formIsEmpty = false;
            break;
        }
    }
    
    /* If the form is not empty */
    if(!formIsEmpty) {
        /* If neither form is disabled */
        if(!changed.disabled && !other.disabled) {
            other.disable(); 
        }
    }
    /* The form has been emptied, see if we need to bring other form back */
    else {
        /* If other form is disabled */
        if(other.disabled) {
            other.enable();
        }
    }
};

