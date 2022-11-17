class MyMiniClass(object):
    def __init__(self, instance_name: str):
        self.name = instance_name

    def get_name(self) -> str:
        return self.name
