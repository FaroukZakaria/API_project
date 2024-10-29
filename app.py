from project import app

if __name__ == '__main__':
    print(f"Starting server: http://localhost:8080")
    app.run(host='localhost', port=8080, debug=True)