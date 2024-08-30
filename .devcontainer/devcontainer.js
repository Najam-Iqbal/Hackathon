{
    "name": "Python Flask Development",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.9",
    "features": {
        "python": {
            "version": "3.9",
            "install": "pip",
            "packages": [
                "Flask==2.0.3",
                "PyMuPDF==1.19.6",
                "transformers==4.28.1",
                "requests==2.26.0"
            ]
        }
    },
    "postCreateCommand": "pip install -r requirements.txt",
    "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
    ],
    "forwardPorts": [
        5000
    ],
    "settings": {
        "python.pythonPath": "/usr/local/bin/python"
    }
}
