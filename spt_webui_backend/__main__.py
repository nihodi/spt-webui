import uvicorn

from spt_webui_backend.environment import ENVIRONMENT


def main():
    uvicorn.run("spt_webui_backend:app", host="0.0.0.0", port=ENVIRONMENT.port, reload=ENVIRONMENT.api_dev)


if __name__ == "__main__":
    main()