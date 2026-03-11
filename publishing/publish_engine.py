from platform_adapters.adapter_manager import PlatformAdapterManager

class PublishEngine:
    def __init__(self):
        self.adapters = PlatformAdapterManager()

    def prepare_payload(self, release_package):
        return self.adapters.build_all_payloads(release_package)

    def simulate_publish(self, release_package):
        return {
            "publish_mode": "simulation",
            "platforms": self.adapters.list_platforms(),
            "results": self.adapters.simulate_all_uploads(release_package)
        }
