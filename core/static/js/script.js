$(document).ready(function(){
    $('.collapsible').collapsible({
		onOpenStart: function(element) {
			let header = $(element).children()[0];
			let icon = $(header).children()[0];
			$(icon).rotate({animateTo: 180});
		},
		onCloseStart: function(element) {
			let header = $(element).children()[0];
			let icon = $(header).children()[0];
			$(icon).rotate({animateTo: 0});
		}
	});
});