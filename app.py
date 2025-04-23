from flask import Flask, render_template_string, send_file
from io import BytesIO
import os

app = Flask(__name__)

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Swipe Simulator</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            touch-action: none;
            background: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        #swipeArea {
            width: 300px;
            height: 300px;
            background: #fff;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        #status {
            margin-top: 20px;
            padding: 10px;
            background: #fff;
            border-radius: 8px;
            width: 80%;
            text-align: center;
        }
        .button {
            margin-top: 20px;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
        }
        #stopBtn {
            background: #ff4444;
            color: white;
        }
        #downloadBtn {
            background: #44ff44;
            color: white;
        }
    </style>
</head>
<body>
    <h1>Swipe Simulator</h1>
    <div id="swipeArea">Swipe Here</div>
    <div id="status">Status: Ready</div>
    <button id="stopBtn" class="button">Stop (L)</button>
    <a href="/download" class="button" id="downloadBtn" style="text-decoration: none;">Download</a>

    <script>
        let isRunning = false;
        let wasRunning = false;
        let startX, startY;
        const swipeArea = document.getElementById('swipeArea');
        const status = document.getElementById('status');
        const stopBtn = document.getElementById('stopBtn');

        function sleep(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                wasRunning = isRunning;
            } else {
                if (wasRunning) {
                    isRunning = false;
                    status.textContent = 'Status: Stopped (tab return)';
                }
            }
        });

        async function simulateSwipes() {
            while (isRunning) {
                status.textContent = 'Status: Swiping forward';
                await sleep(2500);
                
                if (!isRunning) break;
                
                status.textContent = 'Status: Swiping left';
                await sleep(500);
            }
            status.textContent = 'Status: Stopped';
        }

        swipeArea.addEventListener('touchstart', (e) => {
            if (!isRunning) {
                isRunning = true;
                status.textContent = 'Status: Started';
                simulateSwipes();
            }
        });

        stopBtn.addEventListener('click', () => {
            isRunning = false;
            status.textContent = 'Status: Stopped';
        });

        document.addEventListener('keydown', (e) => {
            if (e.key.toLowerCase() === 'l') {
                isRunning = false;
                status.textContent = 'Status: Stopped';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

@app.route('/download')
def download():
    buffer = BytesIO()
    buffer.write(HTML_CONTENT.encode('utf-8'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name='swipe_simulator.html',
        mimetype='text/html'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
