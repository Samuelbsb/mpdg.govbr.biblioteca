$(document).ready(function(){
	
	$.tablesorter.addParser({ 
        // set a unique id 
        id: 'spanValue', 
        is: function(s) { 
            // return false so this parser is not auto detected 
            return false; 
        }, 
        format: function(s) { 
            // format your data for normalization
        	alert(s)
        	
            return s.value
        }, 
        // set type, either numeric or text 
        type: 'numeric' 
    });
    
    $('table.tablesorter').tablesorter();
})