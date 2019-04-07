document.addEventListener('DOMContentLoaded', () => {
    var username;
    var chatroomList;
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

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
        }
        else {
            for (var chatroom in chatroomList) {
                const div = document.createElement('div')
                div.innerHTML = `${chatroom}`;
                div.dataset.name = chatroom;
                document.querySelector('#chatrooms').prepend(div);
            }
        }
    }
    request.send();

    // set username
    document.querySelector('#set-username-btn').onclick = () => {
        const username = document.querySelector('#username').value;
        localStorage.setItem('username', username);
    }

    // create chatroom
    socket.on('connect', () => {
        document.querySelector('#create-chatroom-btn').onclick = () => {
            const newChatroom = document.querySelector('#new-chatroom').value;
            if (!(newChatroom in chatroomList)) {
                socket.emit('create chatroom', {'chatroom': newChatroom});
            }
        }
    })

    // update list of chatrooms and show new chatroom
    socket.on('new chatroom', data => {
        // delete no chatrooms message
        const noChatrooms = document.querySelector('#no-chatrooms-div');
        if (noChatrooms) {
            noChatrooms.remove();
        }

        chatroomList = data.chatrooms;
        const div = document.createElement('div');
        div.innerHTML = `${data.newChatroom}`;
        div.dataset.name = data.newChatroom;
        document.querySelector('#chatrooms').prepend(div);
    })
})
