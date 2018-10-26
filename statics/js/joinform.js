$(function(){
	btn = $('#btn-emailcheck');
	email = $('#email');
	image = $('#img-emailcheck');

	email.change(function(){
		console.log('change!!')
		btn.show();
		image.hide();
	});

	btn.click(function(){
		if(email.val() == ''){
			return;
		}
		$.ajax({
			'url':'/user/checkemail?email=' + email.val(),
			'type':'get',
			'data':'',
			'dataType':'json',
			success: function(response){
				if(response.result == false){
					alert('이미 존재하는 email입니다.');
					email.val('').focus();
					return;
				}
				btn.hide();
				image.show();
			}
		});
	});
});