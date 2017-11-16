$(function() {
	
	var abs_url = $('base').attr('href');
	$('.navigation-bibliotecatiles span.arrow a').attr('ajax-evaljs', abs_url+'/++resource++mpdg.govbr.biblioteca/js/pagedcarousel.js');
	
	$('.tile-pagedcarousel')
	.each(function(){
		var $items = $('.title-item', $(this));
		
	    var base_height = Math.max.apply(null, $items.map(function() { return $(this).height();}).get());
	    $items.height(base_height);
	});
});