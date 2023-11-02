import os
import uvicorn

from app.main import app

print("Starting server...")
print(os.environ["RESTAI_URL"])
print(os.environ["RESTAI_PROJECT"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)