from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    username = ""
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')  # IST Timezone
    
    if request.method == 'POST':
        username = request.form.get('username')
    
    return render_template('index.html', current_time=current_time, username=username)

if __name__ == '__main__':
    app.run(debug=True)
