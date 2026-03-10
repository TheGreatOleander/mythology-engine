from core.governor.governor import MythologyGovernor
from core.studio.orchestrator import StudioOrchestrator
from production.script_engine.script_engine import ScriptEngine
from production.scene_engine.scene_engine import SceneEngine
from production.render_engine.render_engine import RenderEngine
from production.subtitle_engine.subtitle_engine import SubtitleEngine
from production.music_engine.music_engine import MusicEngine
from channel.title_engine.title_engine import TitleEngine
from channel.thumbnail_engine.thumbnail_engine import ThumbnailEngine
from channel.release_package.package_builder import ReleasePackageBuilder
from publishing.platform_adapters.adapters import build_platform_packages
from publishing.publish_engine.publish_engine import PublishEngine
from intelligence.learning_engine.learning_engine import LearningEngine

class MasterOrchestrator:
    def __init__(self):
        self.governor = MythologyGovernor()
        self.studio = StudioOrchestrator()
        self.script_engine = ScriptEngine()
        self.scene_engine = SceneEngine()
        self.render_engine = RenderEngine()
        self.subtitle_engine = SubtitleEngine()
        self.music_engine = MusicEngine()
        self.title_engine = TitleEngine()
        self.thumbnail_engine = ThumbnailEngine()
        self.release_builder = ReleasePackageBuilder()
        self.publisher = PublishEngine()
        self.learning_engine = LearningEngine()

    def run_cycle(self):
        governor_state = self.governor.evaluate()
        brief = self.studio.build_episode_brief(governor_state)
        script = self.script_engine.generate(brief)
        scenes = self.scene_engine.plan(script)
        render_result = self.render_engine.render(script, scenes)
        captions = self.subtitle_engine.generate(render_result["script_lines"])
        soundtracked = self.music_engine.mix(render_result["video"])
        best_title = self.title_engine.generate(brief["topic"])[0]
        thumbnail = self.thumbnail_engine.generate(best_title["title"], brief["topic"])
        release = self.release_builder.build(best_title["title"], script["summary"], soundtracked, thumbnail, captions)
        packages = build_platform_packages({"title": best_title["title"], "hook": best_title["hook"], "summary": script["summary"]})
        publish = self.publisher.publish(packages, release)
        learning = self.learning_engine.evaluate({"views": 12000, "ctr": 8.4})
        return {
            "governor_state": governor_state,
            "episode_brief": brief,
            "script": script,
            "scenes": scenes,
            "render_result": render_result,
            "captions": captions,
            "soundtracked_video": soundtracked,
            "best_title": best_title,
            "thumbnail": thumbnail,
            "release_package": release,
            "platform_packages": packages,
            "publish_result": publish,
            "learning": learning
        }
