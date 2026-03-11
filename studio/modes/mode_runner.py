def describe_mode(mode: str) -> str:
    if mode == 'manual':
        return 'AI prepares assets; human reviews and publishes.'
    if mode == 'assisted':
        return 'AI prepares and recommends actions; human approves major steps.'
    if mode == 'auto':
        return 'AI attempts end-to-end execution using wired providers.'
    return 'Unknown mode.'

def run_mode(mode: str, action: str, publish: bool = False) -> dict:
    return {
        'mode': mode,
        'action': action,
        'publish': publish,
        'operator_policy': describe_mode(mode)
    }
