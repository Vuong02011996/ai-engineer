class ObserverEvent:
    def update(self, message):
        raise NotImplementedError("Subclasses must implement update method")
