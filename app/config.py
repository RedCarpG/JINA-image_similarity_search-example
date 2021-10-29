import os

MAX_DOCS = int(os.environ.get("JINA_MAX_DOCS", 10000))

DEFAULT_QUERY_IMAGE = 'data/toy_data/example.jpg'

BACKEND_PORT = 12345
WORKSPACE_DIR = 'workspace'
WORKSPACE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"+ WORKSPACE_DIR)
LOG_LEVEL = 'INFO'

def config_env():
    workspace_mount = f'{os.environ.get("JINA_WORKSPACE")}:/workspace/workspace'

    os.environ.setdefault('JINA_WORKSPACE', WORKSPACE_PATH)
    os.environ.setdefault('JINA_WORKSPACE_MOUNT', workspace_mount)
    os.environ.setdefault('JINA_LOG_LEVEL', LOG_LEVEL)
    os.environ.setdefault('JINA_PORT', str(BACKEND_PORT))
