class SceneManager:
    def __init__(self):
        self.scene = None

    def set_scene(self, scene_func, *args):
        self.scene = lambda: scene_func(*args)

    def run(self):
        while self.scene:
            self.scene()
