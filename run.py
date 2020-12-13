from spotify_opus import create_app

app = create_app()

if __name__ == '__main__':
    context = "opus.pem", "opus_key.pem"
    app.run(debug=True, ssl_context=context)

