from bootstrap.engines.environment_check import run_environment_check
from bootstrap.engines.path_bootstrap import build_paths
from bootstrap.engines.provider_check import run_provider_check
from bootstrap.engines.config_bootstrap import write_config_bundle

def run_bootstrap():
    env = run_environment_check()
    paths = build_paths()
    providers = run_provider_check()
    config = write_config_bundle(paths["config_dir"])

    return {
        "environment": env,
        "paths": paths,
        "providers": providers,
        "config_bundle": config
    }
