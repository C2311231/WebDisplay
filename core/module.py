import abc


class module:
    
    @abc.abstractmethod
    def shutdown(self):
        pass
    
    @abc.abstractmethod
    def update(self, delta_time: float):
        pass
    
    @abc.abstractmethod
    def start(self):
        pass
    