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
    try:
        code = request.json.get('code', '')
        
        if not code.strip():
            return jsonify({'output': 'Error: No code provided'})

        temp_file = 'temp_program.shout'
        with open(temp_file, 'w') as f:
            f.write(code)
        
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        with redirect_stdout(output_buffer):
            try:
                sys.argv = ['shoutlang', temp_file]
                main()
            except Exception as e:
                error_buffer.write(f"Error executing ShoutLang code: {str(e)}")
        
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        output = output_buffer.getvalue()
        error = error_buffer.getvalue()
        
        if error:
            return jsonify({'output': error})
        
        return jsonify({'output': output if output else 'Code executed successfully (no output)'})
    
    except Exception as e:
        return jsonify({'output': f'Server error: {str(e)}'})

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(host='127.0.0.1', port=5000, debug=True)