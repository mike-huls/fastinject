class DummyRegistry:
    def get(self, _type, default=None):
        raise ValueError(
            "DummyRegistry throws error when resolving while resolving"
        )  # Always return None to simulate missing dependency
