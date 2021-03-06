
import os
from http import server
import io
import json
import socketserver
import subprocess
import sys
import urllib.parse
import webbrowser
import threading
from http import HTTPStatus
import execution
import ok_interface
import log
from documentation import search
from execution_parser import strip_comments
from file_manager import get_scm_files, save, read_file, new_file
from formatter import prettify
from persistence import save_config, load_config
from runtime_limiter import TimeLimitException, OperationCanceledException, scheme_limiter
from scheme_exceptions import SchemeError, ParseError, TerminatedError
PORT = 8012
main_files = []
state = {

}


class Handler(server.BaseHTTPRequestHandler):
    cancellation_event = threading.Event()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        raw_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(raw_data)
        path = urllib.parse.unquote(self.path)
        result = self.handle_post_thread(data, path)
        return result

    def handle_post_thread(self, data, path):
        if (b'code[]' not in data):
            data[b'code[]'] = [b'']
        if (path == '/cancel'):
            self.cancellation_event.set()
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
        if (path == '/process2'):
            self.cancellation_event.clear()
            code = [x.decode('utf-8') for x in data[b'code[]']]
            curr_i = int(data[b'curr_i'][0])
            curr_f = int(data[b'curr_f'][0])
            global_frame_id = int(data[b'globalFrameID'][0])
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(handle(code, curr_i, curr_f, global_frame_id,
                                          cancellation_event=self.cancellation_event), 'utf-8'))
        elif (path == '/save'):
            code = [x.decode('utf-8') for x in data[b'code[]']]
            filename = data[b'filename'][0]
            do_save = (data[b'do_save'][0] == b'true')
            if do_save:
                save(code, filename)
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({
                'result': 'success',
                'stripped': strip_comments(code),
            }), 'utf-8'))
        elif (path == '/instant'):
            code = [x.decode('utf-8') for x in data[b'code[]']]
            global_frame_id = int(data[b'globalFrameID'][0])
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(instant(code, global_frame_id), 'utf-8'))
        elif (path == '/reformat'):
            code = [x.decode('utf-8') for x in data[b'code[]']]
            javastyle = (data[b'javastyle'][0] == b'true')
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({
                'result': 'success',
                'formatted': prettify(code, javastyle),
            }), 'utf-8'))
        elif (path == '/test'):
            self.cancellation_event.clear()
            output = cancelable_subprocess_call(self.cancellation_event, (sys.argv[0], (os.path.splitext(
                ok_interface.__file__)[0] + '.py')), (- 1), sys.executable, subprocess.PIPE, subprocess.PIPE, None)
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(output)
        elif (path == '/list_files'):
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(get_scm_files()), 'utf-8'))
        elif (path == '/read_file'):
            filename = data[b'filename'][0]
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(read_file(filename)), 'utf-8'))
        elif (path == '/new_file'):
            filename = data[b'filename'][0].decode('utf-8')
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({
                'success': new_file(filename),
            }), 'utf-8'))
        elif (path == '/save_state'):
            global state
            for (key, val) in json.loads(data[b'state'][0].decode('utf-8')).items():
                if (key == 'states'):
                    if ('states' not in state):
                        state['states'] = val
                    else:
                        merge(state['states'], val)
                else:
                    state[key] = val
            if ('settings' in state):
                save_config('settings', state['settings'])
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
        elif (path == '/load_state'):
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            if ('states' not in state):
                self.wfile.write(b'fail')
            else:
                self.wfile.write(bytes(json.dumps(state), 'utf-8'))
        elif (path == '/load_settings'):
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            try:
                if ('settings' not in state):
                    state['settings'] = {

                    }
                for (key, val) in load_config('settings').items():
                    state['settings'][key] = val
            except FileNotFoundError:
                self.wfile.write(b'fail')
            else:
                self.wfile.write(bytes(json.dumps(state['settings']), 'utf-8'))
        elif (path == '/documentation'):
            self.send_response(HTTPStatus.OK, 'test')
            self.send_header('Content-type', 'application/JSON')
            self.end_headers()
            query = data.get(b'query', [b''])[0].decode('utf-8')
            self.wfile.write(bytes(json.dumps(search(query)), 'utf-8'))
        elif (path == '/kill'):
            self.server.shutdown()
            self.server.socket.close()

    def do_GET(self):
        self.send_response(HTTPStatus.OK, 'test')
        path = ('editor/static/' + urllib.parse.unquote(self.path)[1:])
        if (('scripts' in path) and (not path.endswith('.js'))):
            path += '.js'
        if path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
        elif path.endswith('.js'):
            self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        if (path == 'editor/static/'):
            path = 'editor/static/index.html'
        try:
            with open(path, 'rb') as f:
                self.wfile.write(f.read().replace(b'<START_DATA>', bytes(repr(json.dumps({
                    'files': main_files,
                })), 'utf-8')))
        except Exception as e:
            print(e)

    def log_message(self, *args, **kwargs):
        pass


def merge(states, new_states):
    for (i, new_state) in enumerate(new_states):
        if (i == len(states)):
            states.append(new_state)
        else:
            for (key, val) in new_state.items():
                states[i][key] = val


def cancelable_subprocess_call(cancellation_event, *args, **kwargs):
    buffered = io.BytesIO()
    with subprocess.Popen(*args, **kwargs) as proc:
        proc.stdin.close()

        def pipeline(source, *sinks):
            while True:
                s = source.readline()
                if (not s):
                    break
                for sink in sinks:
                    sink.write(s)
        reader_thread = threading.Thread(
            target=pipeline, args=(proc.stdout, buffered))
        reader_thread.daemon = True
        reader_thread.start()
        try:
            poll_interval = (
                socketserver.BaseServer.serve_forever.__defaults__[0] / 8)
            while (proc.poll() is None):
                if cancellation_event.wait(poll_interval):
                    proc.terminate()
                    break
        finally:
            proc.terminate()
            reader_thread.join()
    return buffered.getvalue()


def handle(code, curr_i, curr_f, global_frame_id, cancellation_event):
    try:
        global_frame = log.logger.frame_lookup.get(global_frame_id, None)
        log.logger.new_query(global_frame, curr_i, curr_f)
        scheme_limiter(cancellation_event, execution.string_exec, code, log.logger.out,
                       (global_frame.base if (global_frame_id != (- 1)) else None))
    except OperationCanceledException:
        return json.dumps({
            'success': False,
            'out': [str('operation was canceled')],
        })
    except ParseError as e:
        return json.dumps({
            'success': False,
            'out': [str(e)],
        })
    out = log.logger.export()
    return json.dumps(out)


def instant(code, global_frame_id):
    global_frame = log.logger.frame_lookup[global_frame_id]
    log.logger.new_query(global_frame)
    try:
        log.logger.preview_mode(True)
        scheme_limiter(0.3, execution.string_exec, code,
                       log.logger.out, global_frame.base)
    except (SchemeError, ZeroDivisionError) as e:
        log.logger.out(e)
    except TimeLimitException:
        pass
    except Exception as e:
        raise
    finally:
        log.logger.preview_mode(False)
    return json.dumps({
        'success': True,
        'content': log.logger.export()['out'],
    })


def supports_color():
    "\n    Returns True if the running system's terminal supports color, and False\n    otherwise.\n    "
    plat = sys.platform
    supported_platform = ((plat != 'Pocket PC') and (
        (plat != 'win32') or ('ANSICON' in os.environ)))
    is_a_tty = (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty())
    if ((not supported_platform) or (not is_a_tty)):
        return False
    return True


class ThreadedHTTPServer(socketserver.ThreadingMixIn, server.HTTPServer):
    daemon_threads = True


def start(file_args, port, open_browser):
    global main_files
    main_files = file_args
    global PORT
    PORT = port
    url = ''.join(['http://localhost:', '{}'.format(PORT)])
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = ThreadedHTTPServer(('localhost', PORT), Handler)
    except OSError:
        if supports_color():
            print('\x1b[91m', end='')
        print(''.join(['Port ', '{}'.format(
            PORT), ' is already in use, likely for another instance of the editor.']))
        print('To open a second instance of the editor, specify a different port using --port.')
        print(''.join(['To replace the previous editor instance with a new one:\n    1. Go to ', '{}'.format(
            url), '\n    2. Press "Stop Editor" at the top\n    3. Run `python3 editor` again']))
        if supports_color():
            print('\x1b[0m', end='')
        return
    print(url)
    if open_browser:
        webbrowser.open(
            ''.join(['http://localhost:', '{}'.format(PORT)]), new=0, autoraise=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(' - Ctrl+C pressed')
        print('Shutting down server - all unsaved work may be lost')
        print('\n      _____   _______    ____    _____  \n     / ____| |__   __|  / __ \\  |  __ \\ \n    | (___      | |    | |  | | | |__) |\n     \\___ \\     | |    | |  | | |  ___/ \n     ____) |    | |    | |__| | | |     \n    |_____/     |_|     \\____/  |_|     \n')
        if supports_color():
            print((('\x1b[91m' + '\x1b[1m') + '\x1b[4m'), end='')
        print('Remember that you should run python ok in a separate terminal window, to avoid stopping the editor process.')
        if supports_color():
            print(('\x1b[0m' * 3), end='')
