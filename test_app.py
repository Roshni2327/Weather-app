from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form action="/weather" method="post">
            <input type="text" name="city" placeholder="Enter city" required>
            <button type="submit">Get Weather</button>
        </form>
    '''

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    if not city:
        return "City name is required", 400
    return f"City received: {city}"

if __name__ == '__main__':
    app.run(debug=True)
