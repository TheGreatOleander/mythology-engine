class ContinuityEngine:
    def inject(self, script, related_lore):
        return script if not related_lore else script + '\n\nPossible connections exist.'
