from websites import create_app

app = create_app()
if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port="8000")
