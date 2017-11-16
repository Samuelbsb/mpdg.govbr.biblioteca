$(document).ready(function () {

	$(document).on('click', '.check-all', function(ev){
		var checked = this.checked,
			cb_name = this.id;
		
		if (checked) {
			this.checked = !checked;
			checked = !checked;
			
		} else {
			this.checked = true;
			checked = true;
		}

		$("input[name='"+cb_name+"'").attr('checked', checked);
		
		return false;
	});
	
});