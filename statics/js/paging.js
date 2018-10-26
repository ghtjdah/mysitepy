
var tabBox = {
	__aElementSelected: null,

	init: function(){
		for(var i=1; i<=5; i++){
			var aElement = document.getElementById("tab-"+i);
			aElement.onclick = this.__onTabClicked;
		}
	},
	__onTabClicked: function(){
	    //console.log(this)
		this.className = "selected";
		if(tabBox.__aElementSelected != null)
		{
			tabBox.__aElementSelected.className = "";
		}
		tabBox.__aElementSelected = this;
	}// aElement.onclick일 때 발생하는 이벤트 핸들러 함수 이므로 이 함수 내부에서 this는 aElement 이다.
}

// call after dom loaded
window.onload = function(){
	tabBox.init();
}




var pagelist = {{pagenum}}/5;

if((Math.floor(pagelist) == Math.celi(pagelist)){
//필요한 페이지 수가 5의 배수가 아닐 때
    for(var i=(Math.floor(pagelist)*5); i<=(Math.celi(pagelist)*5); i++){
        document.write('<li><a href="/board/list?page=' + i
            + '" id="tab-' + i
            + '">' + i
            + '</a></li>')

        if( (i%5) == 0 ){
            document.write('<li><a href="' + (i+1) + '">▶</a></li>')
        }
    }
}
else{

}
}
pagelist = parseInt({{pagenum}}/5);
document.write("<li>" + pagelist + "</li>");

//<!--document.write("<li><a href="/board/list?page={{ forloop.counter }}" id="tab-{{ forloop.counter }}">{{ forloop.counter }}</a></li>")-->


{% with ''|center:len as range %}
						{% for _ in range %}
							<li><a href='/board/list?page={{ forloop.counter }}' id='tab-{{ forloop.counter }}'>{{ forloop.counter }}</a></li>
							<!--<script>-->
								<!--var pagelist = 5/5;-->
								<!--document.write("<li><a href='/board/list?page={{ forloop.counter }}' id='tab-{{ forloop.counter }}'>{{ forloop.counter }}</a></li>")-->
							<!--</script>-->
						{% endfor %}
						{% endwith %}
						<li><a href="">▶</a></li>