from api import create_app

app = create_app("api.config.Config")

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)  # Set debug=False for production
