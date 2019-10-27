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

            // make the clicked card color different
            let previousSelected = document.querySelector('.chatroom-card-selected');
            if (previousSelected) {
                previousSelected.className = 'chatroom-card';
            }
            div.className = 'chatroom-card-selected';

            // delete contents of message area
            document.querySelector('#message-area').innerHTML = '';

            // display contents of selected chatroom
            chatroomSelected = name;
            document.querySelector('#chatroom-heading').innerHTML = `Current room: ${name}`;
            var numMessages = chatroomList[name].length;
            for (var i = 0; i < numMessages; i++) {
                let div = document.createElement('div');
                div.innerHTML = `(${chatroomList[name][i]["datetime"]}) ${chatroomList[name][i]["user"]} said: ${chatroomList[name][i]["text"]}`
                div.className = 'message';
                document.querySelector('#message-area').append(div)
            }

            var messageArea = document.querySelector('#message-area');
            messageArea.scrollTop = messageArea.scrollHeight;
            document.querySelector('#chatroom-not-selected').style.display = 'none';
            document.querySelector('#current-chatroom-area').style.display = 'flex';
            document.querySelector('#new-message').focus();
            localStorage.setItem('rememberedChatroom', chatroomSelected);
        }
        return div;
    }

    // remember username when user visits page
    username = localStorage.getItem('username');
    if (username) {
        document.querySelector('#change-username').value = username;

        // bypass welcome page if user visited before
        document.querySelector('#welcome-page').style.display = 'none';
        document.querySelector('#logged-in-page').style.display = 'block';
    }

    // get list of channels
    const request = new XMLHttpRequest();
    request.open('GET', '/chatroom_list');
    request.onload = () => {
        chatroomList = JSON.parse(request.responseText);
        if (Object.keys(chatroomList).length === 0) {
            const div = document.createElement('div')
            div.innerHTML = 'No chatrooms';
            div.id = 'no-chatrooms-div';
            document.querySelector('#chatrooms').prepend(div);
        }
        else {
            for (var chatroom in chatroomList) {
                const div = createClickableChatroom(chatroom)
                document.querySelector('#chatrooms').prepend(div);
            }

            // remember chatroom when user visits page
            var rememberedChatroom = localStorage.getItem('rememberedChatroom');
            if (rememberedChatroom) {
                let remembered = document.querySelectorAll(`[data-name=${rememberedChatroom}]`);
                remembered[0].click();
            }
        }
    }
    request.send();

    // configure buttons
    var setUsernameInput = document.querySelector('#username');
    setUsernameInput.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#set-username-btn').click();
        }
    })
    var newMassageInput = document.querySelector('#new-message');
    newMassageInput.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#send-message-btn').click();
        }
    })
    var newChatroomInput = document.querySelector('#new-chatroom');
    newChatroomInput.addEventListener('keyup', event => {
        if (event.keyCode === 13) {
            document.querySelector('#create-chatroom-btn').click();
        }
    })

    // configure change-username input
    var changeUsernameInput = document.querySelector('#change-username');
    changeUsernameInput.addEventListener('keyup', event => {
        if (changeUsernameInput.value.length > 0) {
            username = changeUsernameInput.value;
            localStorage.setItem('username', username);
        }
        else {
            username = 'anonymous';
            localStorage.setItem('username', username);
        }
    })

    // set username
    document.querySelector('#set-username-btn').onclick = () => {
        username = document.querySelector('#username').value;
        if (username.length > 0) {
            localStorage.setItem('username', username);
            document.querySelector('#change-username').value = username;
            document.querySelector('#welcome-page').style.display = 'none';
            document.querySelector('#logged-in-page').style.display = 'block';
        }
    }

    socket.on('connect', () => {

        // create chatroom
        document.querySelector('#create-chatroom-btn').onclick = () => {
            const newChatroom = document.querySelector('#new-chatroom').value;
            if (!(newChatroom in chatroomList) && (newChatroom.length > 0)) {
                socket.emit('create chatroom', {'chatroom': newChatroom})
            }
            document.querySelector('#new-chatroom').value = '';
        }

        // send new message
        document.querySelector('#send-message-btn').onclick = () => {
            const text = document.querySelector('#new-message').value;
            if (text.length > 0 && chatroomSelected) {
                const datetime = new Date();
                const newMessage = {
                    'user': username,
                    'chatroom': chatroomSelected,
                    'text': text,
                    'datetime': datetime.toUTCString()
                };
                socket.emit('new message', newMessage)
                document.querySelector('#new-message').value = '';
            }
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
        if (chatroomSelected === data["new_message"]["chatroom"]) {
            var div = document.createElement('div');
            div.innerHTML = `(${data["new_message"]["datetime"]}) ${data["new_message"]["user"]} said: ${data["new_message"]["text"]}`
            div.className = 'message';
            var messageArea = document.querySelector('#message-area');
            messageArea.append(div);
            messageArea.scrollTop = messageArea.scrollHeight;
        }
    })
})
