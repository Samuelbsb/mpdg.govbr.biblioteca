$(document).ready(function () {
	
	var $tab_content = $('[tab-content]');
	
	if ($tab_content) {
		$tab_content.hide();
		
		$tab_content.eq(0).show();
		var ref = $tab_content.attr('tab-content');
		$('a[tab-ref="'+ref+'"]').addClass('selected');
	}
	
    $(document).on('click', 'a[tab-ref]', function(ev){
        ev.preventDefault();
        
        var $this = $(this),
        	ref = $this.attr('tab-ref'),
        	$content = $('[tab-content="'+ref+'"]');
        
        $('[tab-content]').hide();
        $('a[tab-ref]').removeClass('selected');
        $content.show();
        $this.addClass('selected');
    });
});