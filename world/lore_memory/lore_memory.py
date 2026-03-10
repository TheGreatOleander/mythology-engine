import json
from pathlib import Path
class LoreMemory:
    def __init__(self, path='examples/lore/lore_database.json'):
        self.path=Path(path)
        if not self.path.exists(): self.path.write_text('[]', encoding='utf-8')
    def search(self, keyword):
        items=json.loads(self.path.read_text(encoding='utf-8'))
        return [i for i in items if keyword.lower() in i.get('description','').lower()]
