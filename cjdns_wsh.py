import json

def web_socket_do_extra_handshake(request):
    #if request.ws_origin == 'http://localhost' or ws.origin == "http://laptop.thefinn93.com":
    return
    #raise ValueError('Unacceptable origin: %r' % request.ws_origin)

def web_socket_transfer_data(request):
    from cjdns import *
    password = None
    authenticated = False
    while True:
        rawline = request.ws_stream.receive_message()
        if rawline is None:
            return
        try:
            line = json.loads(rawline)
        except ValueError:
            request.ws_stream.send_message(json.dumps({"error": "Lol that's not JSON"}), binary=False)
        if "function" in line:
            result = {"error":"You shouldn't be seeing this message"}
            if line['function'] == "auth":
                result = {"error": "Authentication appears to have failed"}
                if not "args" in line:
                    line['args'] = {}
                if not "port" in line['args']:
                    line['args']['port'] = 11234
                if not "addr" in line['args']:
                    line['args']['addr'] = "127.0.0.1"
                if not "password" in line['args']:
                    result = {"error": "Please supply a password"}
                else:
                    try:
                        cjdns = cjdns_connect(line['args']['addr'], line['args']['port'], line['args']['password'])
                        authenticated = True
                        result = {"authentication": "success"}
                        password = line['args']['password']
                    except Exception as e:
                        result = {"error": e}
            else:
                if not "args" in line:
                    line['args'] = {}
                args = {}
                for arg in line['args'].keys():
                    if type(line['args'][arg]) != int:
                        args[arg] = str(line['args'][arg])
                    else:
                        args[arg] = line['args'][arg]
                result = callfunc(cjdns, str(line['function']), password, args)
            if "txid" in line:
                result['txid'] = line['txid']
            request.ws_stream.send_message(json.dumps(result), binary=False)
        else:
            request.ws_stream.send_message(json.dumps({"error": "Lol that's not a function"}), binary=False)
