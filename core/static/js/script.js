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

toastr.options = {
	"closeButton": false,
	"debug": false,
	"newestOnTop": false,
	"progressBar": true,
	"positionClass": "toast-bottom-left",
	"preventDuplicates": false,
	"onclick": null,
	"showDuration": "300",
	"hideDuration": "1000",
	"timeOut": "5000",
	"extendedTimeOut": "1000",
	"showEasing": "swing",
	"hideEasing": "linear",
	"showMethod": "fadeIn",
	"hideMethod": "fadeOut"
}