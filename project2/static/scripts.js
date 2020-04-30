//if (!localStorage.getItem('username') && !localStorage.getItem('current_channel')) {
  //var username = prompt('Enter a username');
  //localStorage.setItem('username', username)
  //localStorage.setItem('current_channel', )
//}

document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // Get user's local localStorage
  var my_storage = window.localStorage;
  // var username = '<%= Session["username"] %>';
  // var username = document.querySelector("#username");
  var username = localStorage.setItem('username', 'testuser');
  //localStorage.setItem('username', username);
  //document.querySelector('#user').innerHTML = `Heyyy, ${username}!`;
  //localStorage.setItem('username', username);

  // When connected, configure buttons
  socket.on('connect', () => {
    function joinchannel() {
      // tell people someone joined
      socket.emit('joined', current_channel);
    }
    var leave_btn = document.getElementById('leave');
    if (leave_btn){
      // tell people when someone left and remove the last channel from that user
      leave_btn.addEventListener('click', () => {
        var room_to_leave = localStorage.getItem('current_channel');
        socket.emit('left', room_to_leave);
        localStorage.removeItem('last_channel');
      });
    };

    // similar to above with clicking Log Out
    var logout_btn = document.getElementById('logout');
    if (logout_btn){
      document.querySelector('#logout').addEventListener('click', () => {
        localStorage.removeItem('last_channel');
      });
    };

    // sending messages with a timestamp in the message field
    document.querySelector('#send-button').addEventListener('click', function(event){
      event.preventDefault();

      // get the message that they wrote
      var message_content = document.querySelector('#message-input').value
      // save time
      var timestamp = new Date();
      timestamp = timestamp.toLocaleString('en-US');
      var user = username;
      var current_channel = localStorage.getItem('current_channel');
      // put all the pieces of the message into one variable
      let message_data = {"message_content": message_content,
                          "timestamp": timestamp};
                          //"user": user,
                          //"current_channel": current_channel};

      socket.emit('send message', message_data);
      console.log(message_data);
      // clear the input field
      document.querySelector('#message-input').value = '';
      return false;
    });
  });

  socket.on('status', data => {
    console.log('Recieved status');
    let row = '<' + `${data.msg}` + '>';
    document.querySelector('#chat').value += row + '\n';
    localStorage.setItem('last_channel', data.channel)
  });

  socket.on('announce message', message_data => {

    const li = document.createElement('li');
    li.setAttribute('class', 'media comment-item');

    const div_media_body = document.createElement('div');
    div_media_body.setAttribute('class', 'media-body comment-media');

    const h5 = document.createElement('h5');
    h5.setAttribute('class', 'mt-0 mb-1 comment-user');
    let midpt = '&middot';
    let space = '\u0020';
    h5.innerHTML = `the user's name here${space}${midpt}${space}`;
    //h5.innerHTML = `${message_data["user"]}${space}${midpt}${space}`;

    const div_time = document.createElement('div');
    div_time.setAttribute('class', 'comment-time');
    div_time.setAttribute('id', 'time');
    div_time.innerHTML = message_data["timestamp"];

    const div_comment = document.createElement('div');
    div_comment.setAttribute('class', 'comment-comment');
    div_comment.innerHTML = message_data["message_content"];

    div_media_body.appendChild(h5);
    div_media_body.appendChild(div_time);
    div_media_body.appendChild(div_comment);

    //li.appendChild(div_media_body);
    li.innerHTML = `this is a test`;

    document.querySelector('#comment-list').append(li);
    li.scrollIntoView();
  });


});
