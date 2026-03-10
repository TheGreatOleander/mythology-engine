class PublishEngine:
    def publish(self, packages, release):
        return {"status":"manual_first","platforms":list(packages.keys()),"release_dir":release["package_dir"]}
