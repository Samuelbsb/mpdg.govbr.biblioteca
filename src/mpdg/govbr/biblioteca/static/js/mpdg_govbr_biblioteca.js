$(function(){
	$(".accordion").accordion({
		collapsible : true,
		heightStyle : "content",
		active : false,
		icons: { "header": "ui-icon-carat-1-w", "activeHeader": "ui-icon-carat-1-s" }
	});
	
    $("input[type='date']").dateinput({ format: 'dd/mm/yyyy' });
	
//	$(".ampliar").fancybox({'type':"iframe"});
});