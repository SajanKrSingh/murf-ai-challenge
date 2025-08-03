from flask import Flask, render_template

# Flask app initialize karein
app = Flask(__name__)

# Ek route banayein jo homepage ko handle karega
@app.route('/')
def index():
    # 'templates' folder se index.html file ko render karega
    return render_template('index.html')

# Server ko run karne ke liye
if __name__ == '__main__':
    app.run(debug=True)