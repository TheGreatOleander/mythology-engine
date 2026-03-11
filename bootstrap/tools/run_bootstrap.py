from bootstrap.engines.bootstrap_engine import run_bootstrap
import json

print(json.dumps(run_bootstrap(), indent=2))
