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
 *  When we are viewing a project this stuff will happen.
 *  @class
 **/
observatory.ShowProjectPage = function(params) {
    if(params) {
        this.init(params);
    }
}
observatory.ShowProjectPage.prototype = new observatory.Page();

observatory.ShowProjectPage.prototype.init = function(params) {
    observatory.Page.prototype.init.call(this, params);

    var current = 1
    $("a.screenshot-switcher").click(function() {
		new_index = $(this).attr("rel")
		old_switcher = "#screenshot-switcher-" + current
		new_switcher = "#screenshot-switcher-" + new_index
		if (new_switcher != old_switcher) {
			current = new_index;
			$(old_switcher).animate({ "opacity": 0.25 }, 200)
			$(new_switcher).animate({ "opacity": 1 }, 200)
			pixels = (-(new_index - 1) * 790).toString() + "px"
			$("#screenshot-page-wrapper").animate({ "left": pixels }, 500)
		}
	});
};
