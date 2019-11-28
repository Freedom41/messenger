document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelector('#send').onclick = () => {
            let time = new Date()
            time = time.getHours() + ":" + time.getMinutes() + ":" + time.getSeconds()
            const msg = document.querySelector('#input').value;
            console.log(msg.length)
            if (msg.length > 1) {
                document.querySelector('#input').value = " ";
                socket.emit('send message', { 'message': msg, 'time': time })
            }
        }

        document.querySelector('#login').onclick = () => {
            let user = document.querySelector('#user').value;
            if(user.length > 1) {
                socket.emit('add_user', {'user': user})
            } 
        }
    });

    socket.on('addmsg', messages => {
        len = messages.length
        len = len - 1;
        li = document.createElement('li')
        p = document.createElement('p')
        p.innerHTML = messages[len].time;
        li.innerHTML = messages[len].message;
        document.querySelector('#msglist').append(li)
        document.querySelector('#msglist').append(p)
    });

    socket.on('addusers', users => {
        user = document.createElement('p')
        user.innerHTML = users
        document.querySelector('#user-list').append(p)
    });
});

document.getElementById("msglist").style.overflowY = "scroll";
