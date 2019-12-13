document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#volver').onclick = () => {
        localStorage.setItem('channel', 'home')
    }
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // When connected, configure buttons
    socket.on('connect', () => {

        document.querySelector('#boton').onclick = () => {
            const message = document.querySelector('#msg').value;
            socket.emit('send message', { 'mensaje': message, 'channel': channel, 'username': localStorage.getItem('register'), 'date': new Date() });
        }
    });

    // When a new message is announced, add to the unordered list
    socket.on('new message', data => {
        if (data.channel == channel) {
            const h3 = document.createElement('h3');
            h3.innerHTML = `Username ${data.username} at ${data.date} : ${data.mensaje}`;
            document.querySelector('#mensajes').append(h3);
            var count = document.getElementsByTagName('h3').length;
            if (count > 100) {
                var tester = document.getElementById('mensajes')
                tester.removeChild(tester.childNodes[0])
            }
        }
    });
});
