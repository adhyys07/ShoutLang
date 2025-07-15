from flask import Flask, render_template, request, jsonify
import sys
import io
from contextlib import redirect_stdout
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shoutlang.cli import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    code = request.json.get('code', '')

    temp_file = 'temp_program.shout'
    with open(temp_file, 'w') as f:
        f.write(code)
    
    output_buffer = io.StringIO()
    with redirect_stdout(output_buffer):
        sys.argv = ['shoutlang', temp_file]
        main()
    
    # Clean up temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)
    
    return jsonify({'output': output_buffer.getvalue()})

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True)