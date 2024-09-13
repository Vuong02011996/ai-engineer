from app.mongo_dal.object_dal import ObjectDAL
import connect_db

object_dal = ObjectDAL()
object_dal.drop_collection()