document.addEventListener('DOMContentLoaded', () => {

    var username;
    var chatroomSelected;
    var chatroomList;
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    function createClickableChatroom(name) {
        /*
        Creates a chatroom that has a clickable event.
        Once chatroom is clicked, messages are displayed and
        user is able to send messages in that chatroom
        */
        const div = document.createElement('div');
        div.innerHTML = `${name}`;
        div.dataset.name = name;
        div.className = 'chatroom-card';
        div.onclick = () => {
            if (chatroomSelected !== name) {

                // delete contents of message area
                document.querySelector('#message-area').innerHTML = '';

                // display contents of selected chatroom
                chatroomSelected = name;
                document.querySelector('#chatroom-heading').innerHTML = name;
                var numMessages = chatroomList[name].length;
                for (var i = 0; i < numMessages; i++) {
                    let div = document.createElement('div');
                    div.innerHTML = `${chatroomList[name][i]["user"]} said: ${chatroomList[name][i]["text"]}`
                    div.className = 'message';
                    document.querySelector('#message-area').append(div)
                }
            }
        }
        return div;
    }

    // remember username when user visits page
    username = localStorage.getItem('username');
    if (username) {
        document.querySelector('#username').value = username;
    }

    // get list of channels
    const request = new XMLHttpRequest();
    request.open('GET', '/chatroom_list');
    request.onload = () => {
        chatroomList = JSON.parse(request.responseText);
        if (Object.keys(chatroomList).length === 0) {
            const div = document.createElement('div')
            div.innerHTML = 'No chatrooms'
            div.id = 'no-chatrooms-div'
            document.querySelector('#chatrooms').prepend(div);
        } else {
            for (var chatroom in chatroomList) {
                const div = createClickableChatroom(chatroom)
                document.querySelector('#chatrooms').prepend(div);
            }
        }
    }
    request.send();

    // set username
    document.querySelector('#set-username-btn').onclick = () => {
        username = document.querySelector('#username').value;
        localStorage.setItem('username', username);
    }

    socket.on('connect', () => {

        // create chatroom
        document.querySelector('#create-chatroom-btn').onclick = () => {
            const newChatroom = document.querySelector('#new-chatroom').value;
            if (!(newChatroom in chatroomList)) {
                socket.emit('create chatroom', {'chatroom': newChatroom})
            }
        }

        // send new message
        document.querySelector('#send-message-btn').onclick = () => {
            const text = document.querySelector('#new-message').value;
            const newMessage = {
                'user': username,
                'chatroom': chatroomSelected,
                'text': text
            };
            socket.emit('new message', newMessage)
        }
    })

    // display new chatroom
    socket.on('new chatroom', data => {
        const noChatrooms = document.querySelector('#no-chatrooms-div');
        if (noChatrooms) {
            noChatrooms.remove();
        }
        chatroomList = data.chatrooms;
        var div = createClickableChatroom(data.newChatroom)
        document.querySelector('#chatrooms').prepend(div);
    })

    // display new massage
    socket.on('broadcast new message', data => {
        chatroomList = data.chatrooms;
        var div = document.createElement('div');
        div.innerHTML = `${data["new_message"]["user"]} said: ${data["new_message"]["text"]}`
        div.className = 'message';
        document.querySelector('#message-area').append(div);
    })
})
