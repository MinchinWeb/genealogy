$(document).ready(function () {
 
    $('[data-toggle="tooltip"]').tooltip({
      placement: 'auto bottom'
    });
    
    $('[data-toggle="popover"]').popover({
			offset: 10,
			trigger: 'manual',
			html: true,
			placement: 'auto bottom',
//			animation: false, // set to false if repeated hoving works intermittently
			template: '<div class="popover" onmouseover="$(this).mouseleave(function() {$(this).hide();});"><div class="arrow"></div><div class="popover-inner"><h3 class="popover-title"></h3><div class="popover-content"><p></p></div></div></div>'
		}).on('mouseover', function(e) {
			$(this).popover('show');
			$(this).siblings('.popover').popover('hide');
		}).on('mouseleave', function(e) {
			var _this = this;
			setTimeout(function() {
				if (!$(".popover:hover").length) {
				  $(_this).popover("hide");
				}
			}, 0);
		}); 

});
