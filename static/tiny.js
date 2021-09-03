var script= document.createElement('script');
script.type='text/javascript';
script.src="/static/richtexteditor/richtexteditor/rte.js";
document.head.appendChild(script);

script.onload=function(){
  var editor1 = new RichTextEditor("#desc");
}