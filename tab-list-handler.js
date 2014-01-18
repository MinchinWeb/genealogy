$(document).ready(function () {

  // http://stackoverflow.com/questions/9685968/best-way-to-make-twitter-bootstrap-tabs-persistent
  
  // activates hash tab on click
  // adds the hash to the address bar
  // allows typing hash on address bar
  // adds the hash to the history
	
	// cache the id
	var navbox = $('#tab-list');
	// activate tab on click
	navbox.on('click', 'a', function (e) {
		var $this = $(this);
		// prevent the Default behavior
		e.preventDefault();
		// set the hash to the address bar
		window.location.hash = $this.attr('href');
		// activate the clicked tab
		$this.tab('show');
	});

	function refreshHash(){
			navbox.find('a[href="'+window.location.hash+'"]').tab('show');
	}

	$(window).bind('hashchange', refreshHash);
	
	if(window.location.hash){
		// show right tab on load (read hash from address bar)
		refreshHash();
	}
  
  
});
