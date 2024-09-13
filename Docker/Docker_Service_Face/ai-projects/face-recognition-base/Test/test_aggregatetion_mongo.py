import connect_db
import time
from app.mongo_dal.identity_dal import IdentityDAL
identity_dal = IdentityDAL()

face_id = 1630164561686148164
start_time = time.time()
name, url = identity_dal.find_url_with_face_id(face_id)
print(time.time() - start_time)
print(name, url)
a = 0