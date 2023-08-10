from app import app
from app.models.login import User

# Check if the script is being run directly
if __name__ == '__main__':
    # Start the Flask development server with debugging enabled
    #app.run(debug=False)
    app.run()