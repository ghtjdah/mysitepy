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
					alert('정말로 삭제하시 겠습니까??');
					email.val('').focus();
					return;
				}
				btn.hide();
				image.show();
			}
		});
	});
});