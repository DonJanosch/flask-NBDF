// Script to handle SocketIO-Connection to Server
var infochat = io.connect('http://' + document.domain + ':' + location.port+'/infochat');

var addToDisplay = function(text){
  $('#infochat').append('<li>'+text+'</li>');
}

var sendTextBox = function(){
  let msg = $('#infochat_textbox').val();
  infochat.send(msg);
  console.log('Sent message, ',msg);
  $('#infochat_textbox').val('');
}

infochat.on('connect', function(){
  infochat.send('User connected');
});

infochat.on('message', function(msg){
  addToDisplay(msg);
  console.log('Recieved message, ',msg);
});

$('#infochat_sendbutton').on('click', function(){
  sendTextBox();
});
