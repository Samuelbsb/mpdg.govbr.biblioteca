$(function() {
	
	$(document).on('click', '.call-advanced-search', function(ev){
		var $this = $(this),
		    $form = $this.parents('form.form-filter');
			$ad_search = $('.advanced-search', $form);
			
		if ($ad_search) {
			var sign = $('.sign', $this);
			
			if ($ad_search.css('display') == 'block')
				sign.text('+');
			else
				sign.text('-');
			
			$ad_search.toggle(200);
		}
	});
	
	
	$('.form-filter input[name="SearchableText"]').keypress(function(ev){
		if(ev.keyCode == 13) {
			$('.form-filter input[name="submitted"]').trigger('click');
		}
	});
	
});