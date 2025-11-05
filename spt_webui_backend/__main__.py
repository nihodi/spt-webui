import uvicorn

from spt_webui_backend import app
from spt_webui_backend.environment import ENVIRONMENT


def main():
    uvicorn.run(app, host="0.0.0.0", port=ENVIRONMENT.port)


if __name__ == "__main__":
    main()