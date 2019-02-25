// Script to handle SocketIO-Connection to Server
var infochat = io.connect('http://' + document.domain + ':' + location.port+'/infochat');
infochat.on('connect', function(){
  infochat.emit('message','User connected');
});

infochat.on('message', function(msg){
  $('#infochat').append('<li>'+msg+'</li>')
});

$('#infochat_sendbutton').on('click', function(){
  infochat.send($('#infochat_textbox').val());
  $('#infochat_textbox').val('');
});
