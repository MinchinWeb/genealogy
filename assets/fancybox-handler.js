$(document).ready(function () {
 
jQuery.fn.getTitle = function() { // Copy the title of every IMG tag and add it to its parent A so that fancybox can show titles
	var arr = jQuery("a.fancybox");
	jQuery.each(arr, function() {
		var title = jQuery(this).children("img").attr("alt");
		jQuery(this).attr('title',title);
	})
}

// Supported file extensions
var thumbnails = jQuery("a:has(img)").not(".nolightbox").filter( function() { return /\.(jpe?g|png|gif|bmp)$/i.test(jQuery(this).attr('href')) });

thumbnails.addClass("fancybox").attr("rel","fancybox").getTitle();

$(".fancybox").fancybox({
	openEffect  : 'fade',
	closeEffect : 'fade',
	prevEffect	: 'none',
	nextEffect	: 'none',
	closeBtn	: false,
	arrows      : false,
	nextClick   : true,
	padding     : 0,
	helpers	: {
		title	: {type: 'over'},
		buttons	: {},
		//thumbs	: {width : 50, height : 50}
	},
	beforeShow: function(){$(".fancybox-skin").css("backgroundColor","transparent");},	
	afterLoad : function() {this.title = (this.index + 1) + '/' + this.group.length + (this.title ? ' - ' + this.title : '');}
});
	
});
