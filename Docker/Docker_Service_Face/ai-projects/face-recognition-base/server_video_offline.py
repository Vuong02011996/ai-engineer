from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
import multiprocessing as mp

from app.app_utils.file_io_untils import ip_run_service_ai
from app.services.video_offline_face_detection.face_detection_services_video_offline import blueprint as video_offline_face_detection_namespace
from pathlib import Path  # Python 3.6+ only
# from app.controllers.identity_controller import namespace as identity_namespace

import sentry_sdk
sentry_sdk.init("https://ae7bda33e6284fbcb6b5392b71aeea34@sentry.oryza.vn/3")
sentry_sdk.capture_message(f"[FACE][{ip_run_service_ai}] START SERVICE")

if len(sys.argv) > 1:
    print("The script run with file {}".format(sys.argv[1]))
    env_path = Path(".") / sys.argv[1]
    print("env_path", env_path)
    load_dotenv(dotenv_path=env_path)
    print("Running in PORT: ", os.getenv("SERVER_PORT_VIDEO_OFFLINE"))
else:
    print("The script run with file .env")
    env_path = Path(".") / ".env"
    load_dotenv(dotenv_path=env_path)

# load_dotenv()


app = Flask(__name__)

CORS(app)
# Using both register_blueprint and namespace
api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, title="Face Detection Video Offline Project", version="1.0.0",
        description="Swagger API Homepage")

# Using only namespace
# api = Api(app, title="Face Detection  Project", version="1.0.0", description="Swagger API Homepage", )

# api.add_namespace(identity_namespace, path="/identities")
# api.add_namespace(camera_namespace, path="/cameras")
# api.add_namespace(vms_face_detection_namespace, path="/vms_face_detection")

# Using api for oryza AI from root
app.register_blueprint(video_offline_face_detection_namespace)
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    mp.set_start_method('spawn')
    app.run(host=os.getenv("SERVER_HOST"), port=os.getenv("SERVER_PORT_VIDEO_OFFLINE"), threaded=True, debug=True, use_reloader=False)

    """
    Run pm2 auto start when reboot 
    pm2 start ecosystem.staging.config.yaml
    pm2 startup - copy command and run 
    pm2 save 
    """

