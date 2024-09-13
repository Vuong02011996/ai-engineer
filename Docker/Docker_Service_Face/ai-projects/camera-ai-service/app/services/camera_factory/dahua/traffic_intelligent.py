from app.services.camera_factory.camera import ICamera


class TrafficIntelligent(ICamera):
    # traffic intelligent dont have person
    def update_image_person(self):
        pass

    def create_person(self):
        pass

    def delete_person(self):
        pass

    def update_person(self):
        pass
