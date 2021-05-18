$(document).ready(function(){
    $('.collapsible').collapsible({
		onOpenStart: function(element) {
			let header = $(element).children()[0];
			let labelName = $(header).children()[0];
			let icon = $(labelName).children()[0];
			$(icon).rotate({animateTo: 180});
		},
		onCloseStart: function(element) {
			let header = $(element).children()[0];
			let labelName = $(header).children()[0];
			let icon = $(labelName).children()[0];
			$(icon).rotate({animateTo: 0});
		}
	});

	$('.tooltipped, .trafficlight').tooltip();

	$('.modal').modal();

	$('main:has(.box-middle)').css('background', 'transparent');
});