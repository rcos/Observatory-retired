FADE_TIME = 350
FADE_INITIALIZED = false

current_tab = "{{ tab }}"
function tabclicked(new_index) {
	// ignore if it's the active tab
	if (new_index.toString() == current_tab.toString()) return;
	current_tab = new_index
	
	// current and new content
	current = $(".active-content")
	new_content = $("#content-" + new_index)
	
	// initialize if required
	if (!FADE_INITIALIZED) {
		FADE_INITIALIZED = false
		$("#content-container").height(current.height())
		$(".tab-content").css('position', 'absolute')
	}
	
	// hide the current content
	current.animate({ opacity: 0 }, FADE_TIME,
					function() { current.css('display', 'none') })
	current.removeClass("active-content")
	
	// show the new content
	new_content.css('display', 'block')
	new_content.animate({ opacity: 1 }, FADE_TIME)
	new_content.addClass("active-content")
	
	// set the height of the container
	$("#content-container").animate({ height: new_content.height() },
									FADE_TIME)
	
	// switch the tabs
	$(".active").removeClass("active")
	$("#tab-" + new_index).addClass("active")
}

function hide_just_post_form() {
	$("#write-post-box").animate({
		"opacity": 0,
		"top": "-400px"
	}, OVERLAY_FADE_TIME, function() {
		$("#write-post-box").css("display", "none")
	})
}

OVERLAY_FADE_TIME = 500

function hide_post_form() {
	hide_just_post_form()

	overlay = $("#write-post-box-overlay")
	overlay.animate({ "opacity": 0 }, OVERLAY_FADE_TIME)
	overlay.css("display", "none")
}

function show_post_form() {
	box = $("#write-post-box")
	box.css("display", "block")
	box.animate({
		"opacity": 1,
		"top": "50px"
	}, OVERLAY_FADE_TIME)
	overlay = $("#write-post-box-overlay")
	overlay.animate({ "opacity": 0.75 }, OVERLAY_FADE_TIME)
	overlay.css("display", "block")
}

$(document).ready(function() {
	write_post = $("#write-post-button")
	write_post.attr("onClick", "show_post_form()")
	write_post.removeAttr("href")
	
	tabs = ["#tab-link-1", "#tab-link-2", "#tab-link-3", "#tab-link-4"]
	for (i in tabs) {
		tab = $(tabs[i])
		tab.removeAttr("href")
		tab_id = parseInt(i) + 1
		tab.attr("onClick", "tabclicked(" + tab_id + ")")
	}
})
