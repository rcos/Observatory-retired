$(document).ready(function() {
	lightbox();
});

function lightbox() {
	var images = $("a[rel^=lightbox]");
	var overlay = $(jQuery("<div id='lb-overlay' style='display:none'></div>"));
	var container = $(jQuery("<div id='lb-container'></div>"));
	var target = $(jQuery('<div class="target"></div>'));
	var header = $(jQuery('<h2></h2>'));
	var close = $(jQuery('<a href="#close", class="lb-close">&times;</a>'));
	
	$('body').append(overlay).append(container);
	container.append(header).append(close).append(target);
	container.show().css({
		'top': Math.round(($(window).height() - container.outerHeight()) / 2) + 'px',
		'left': Math.round(($(window).width() - container.outerWidth()) / 2) + 'px',
		'margin-top': 0,
		'margin-left': 0
	}).hide();
	
	var lb_open = function(href, title) {
		if (container.is(":visible")) {
			target.children().fadeOut('normal', function() {
				target.children().remove()
				lb_load(href, title);
			});
		}
		else {
			overlay.add(container).fadeIn('normal', function() {
				lb_load(href, title);
			});
		}
	};
	
	close.click(function(c) {
		c.preventDefault();
		container.animate({
			"top": '-400px'
		}, 'normal');
		overlay.add(container).fadeOut('normal', function() {
			target.children().remove();
		});
	});
	
	images.each(function(i) {
		var link = $(this);
		link.click(function(c) {
			c.preventDefault();
			lb_open(link.attr("href"), link.attr("title"));
		});
	});
	
	var lb_load = function(href, title) {
		if (container.is('.loading')) return;
		container.addClass('loading');
		header.html(title);
		
		var img = new Image();
		img.onload = function() {
			var mw = $(window).width() - 100;
			var mh = $(window).height() - 100;
			if (img.width > mw || img.height > mh) {
				var ratio = img.width / img.height;
				if (img.height >= mh) {
					img.height = mh;
					img.width = mh * ratio;
				}
				else {
					img.width = mw;
					img.height = mw / ratio;
				}
			}
			
			container.css({
				"width": img.width,
				"height": img.height,
				"top": Math.round(($(window).height() - img.height) / 2) - 500 + 'px',
				"left": Math.round(($(window).width() - img.width) / 2) + 'px'
			});

			target.append(img);
			
			container.animate({
				"top": Math.round(($(window).height() - img.height) / 2) + 'px',
				"opacity": 1
			}, 'normal', function() {
				container.removeClass('loading');
			});
		}
		img.src = href;
	};
}
