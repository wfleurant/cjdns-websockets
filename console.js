var socket = null;
document.getElementById("entrybox").focus();

function output(data, style) {
    if(style) {
        data = "<span class=\"" + style + "\">" + data + "</span>";
    }
    console = document.getElementById("console")
    if(console.innerHTML != "") {
        console.innerHTML += "\n";
    }
    console.innerHTML += data;
}

function connected(evt) {
    output("Connected", "good");
}

function disconnected(evt) {
    output("Disconnected", "bad");
}

function incomingMessage(evt) {
    output(evt.data, "received");
}

function error(evt) {
    output(evt.data, "bad");
}

function send(fn) {
    if(socket != null) {
        socket.send(JSON.stringify({"function": fn}));
        output(message, "sent");
    } else {
        connect(fn);
    }
}

function connect(uri) {
    uri = uri || prompt("Enter the websocket URI you wish to connect to");
    output("connecting to " + uri, "informational");
    try {
        socket = new WebSocket(uri);
    } catch(e) {
        output(e, "bad");
    }
    socket.onopen = connected;
    socket.onclose = disconnected;
    socket.onmessage = incomingMessage;
    socket.onerror = error;
}
