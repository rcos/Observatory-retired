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
 *  This contains the functionality for adding a project.
 *  @class
 **/
observatory.AddProjectPage = function(params) {
    if(params) {
        this.init(params);
    }
}
observatory.AddProjectPage.prototype = new observatory.Page();

observatory.AddProjectPage.prototype.init = function(params) {
    observatory.Page.prototype.init.call(this, params);
    
    var $ = jQuery;
    
    /* Different parts of form */
    var partOneElement = $('#part-1');
    var partTwoLeftElement = $('#part-2-form-left');
    var partTwoRightElement = $('#part-2-form-right');
    var partThreeLeftElement = $('#part-3-form-left');
    var partThreeRightElement = $('#part-3-form-right');


    /* part one of the form */
    var partOneForm = new observatory.Form({
        el: partOneElement, 
        container: $('#content')
    });

    /* part two of the form */
    var partTwoLeftForm = new observatory.Form({
        el: partTwoLeftElement, 
        container: $('#part-2-form-left-container')
    });
    
    var partTwoRightForm = new observatory.Form({
        el: partTwoRightElement, 
        container: $('#part-2-form-right-container')
    });
    
    /* Make only one of the forms work */
    new observatory.ExclusiveOrForms({
        formA: partTwoLeftForm, 
        formB: partTwoRightForm 
    });

    /* If we are on part 3 of the form */
    var partThreeLeftForm = new observatory.Form({
        el: partThreeLeftElement, 
        container: $('#part-3-form-left-container')
    });
    
    var partThreeRightForm = new observatory.Form({
        el: partThreeRightElement, 
        container: $('#part-3-form-right-container')
    });
    
    /* Make only one side work */
    new observatory.ExclusiveOrForms({
        formA: partThreeLeftForm, 
        formB: partThreeRightForm
    });
    
    
};