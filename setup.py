from setuptools import setup

setup(
    name="alertai",
    version="1.0.0",
    description="AI-Powered Emergency Response System",
    py_modules=[],
    install_requires=[
        "Flask>=3.0.0",
        "requests>=2.31.0",
        "google-genai>=1.60.0",
        "flask-cors>=4.0.0",
        "python-dotenv>=1.0.0",
        "twilio>=8.10.0",
        "flask-socketio>=5.3.6",
        "python-socketio>=5.10.0",
        "websockets>=12.0",
        "gunicorn>=21.2.0",
    ],
    python_requires=">=3.8",
)