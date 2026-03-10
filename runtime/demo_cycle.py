from core.orchestrator.master_orchestrator import MasterOrchestrator
import json
print(json.dumps(MasterOrchestrator().run_cycle(), indent=2))
