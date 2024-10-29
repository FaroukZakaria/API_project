from project import app

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    print(f"Starting server: http://localhost:8080")
    app.run(host='localhost', port=8080, debug=True)