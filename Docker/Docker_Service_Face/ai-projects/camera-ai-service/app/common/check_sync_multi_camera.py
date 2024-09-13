class CheckSyncMultiCamera(object):
    list_camera = {}
    list_action = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CheckSyncMultiCamera, cls).__new__(cls)
        return cls.instance

    def set_sync_multi_camera(self, id_camera: str, status: bool,action: str):
        self.list_camera[id_camera] = status
        self.list_action[id_camera] = action
        if status is False:
            del self.list_camera[id_camera]
            del self.list_action[id_camera]


    def get_sync_multi_camera(self, id_camera):
        if id_camera not in self.list_camera:
            return {"status": False, "action": None}
        return {"status": self.list_camera[id_camera], "action": self.list_action[id_camera]}
