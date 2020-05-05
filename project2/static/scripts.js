document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // Get user's local localStorage
    var my_storage = window.localStorage;

    var add_user_btn = document.getElementById('lets-go');
    if (add_user_btn){
      document.querySelector('#lets-go').onclick = () => {
        const username = document.querySelector('#username').value;
        localStorage.setItem('username', username);
        alert(`Welcome, ${username}!`)
        console.log("the user has been set.")
      };
    };
    var user = localStorage.getItem('username')
    console.log(user)

    //var cur_chan = document.getElementById('ch-name').value;
    //localStorage.setItem('current_channel', cur_chan);
    //var current_channel = localStorage.getItem('current_channel');
    // When connected, configure buttons
    socket.on('connect', () => {
      //function joinchannel() {
      //  console.log('Made it here')
        // tell people someone joined
        //socket.emit('joined', current_channel);
      //}
      var leave_btn = document.getElementById('leave');
      if (leave_btn){
        // tell people when someone left and remove the last channel from that user
        leave_btn.onclick = () => {
          socket.emit('left');
          //localStorage.setItem('current_channel', current_channel);
          //localStorage.removeItem('last_channel');
          console.log("someone left")
        };
      };
    }); // end of socket.on('connect')

    // similar to above with clicking Log Out
    var logout_btn = document.getElementById('logout');
    if (logout_btn){
        document.querySelector('#logout').addEventListener('click', () => {
          //localStorage.removeItem('last_channel');
        });
      };

      // sending messages with a timestamp in the message field
    var send_btn = document.querySelector('#send-button');
    if (send_btn){
      send_btn.onclick = () => {

          // get the message that they wrote
          var message_content = document.querySelector('#message-input').value;
          // save time
          var tstmp = new Date();
          timestp = tstmp.toLocaleString('en-US');
          timestamp = timestp.replace(/:\d+ /, ' ');
          var user = localStorage.getItem('username')
          var thechannel = document.querySelector('#thechannel').value;
          //var current_channel = localStorage.getItem('current_channel');

          // put all the pieces of the message into one variable
          let message_data = {"message_content": message_content,
                              "timestamp": timestamp,
                              "user": user,
                              "current_channel": thechannel};
          console.log(message_data);
          socket.emit('send message', message_data);
          // clear the input field
          document.querySelector('#message-input').value = '';
          event.preventDefault();
          return false;

        };// end of send button
    };

    // using Enter key as a "send", doesn't quite work yet
    //document.querySelector('#message-input').addEventListener("keydown", event => {
      //event.preventDefault();
      //if (event.key == "Enter") {
          //document.getElementById('send-button').click();
      //};
    //});

    socket.on('status', data => {
      console.log('Recieved status');
      var message_list = document.getElementById('comment-list');
      const leftli = document.createElement('li');
      leftli.innerHTML = `${data.msg}`;
      message_list.append(leftli);
      localStorage.setItem('last_channel', data.channel)
    });

    socket.once('announce message', message_data => {
      console.log("inside announce message")
      //event.preventDefault();
      var message_list = document.getElementById('comment-list');
      const li = document.createElement('li');
      li.innerHTML = `<div>
                        <li><b>${message_data["user"]}:</b> ${message_data["message_content"]}</li>
                      </div>
                      <div>
                        <li><small class="text-muted">${message_data["timestamp"]}</small></li>
                      </div>`;
      message_list.append(li);
      li.scrollIntoView();
    });

    $(document).ready(function() {
      $(".dropdown-toggle").dropdown();
    });
});
