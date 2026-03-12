from studio.config.loader import load_profile, load_secrets
from studio.providers.provider_registry import ProviderRegistry
from studio.modes.mode_runner import run_mode
from core.orchestrator.master_orchestrator import MasterOrchestrator
from publishing.provider_layer.video.ffmpeg_provider import FFmpegProvider
from publishing.provider_layer.image.title_card_provider import TitleCardProvider
from publishing.provider_layer.audio.piper_provider import PiperProvider
from production.episode_pipeline import EpisodePipeline
from release.review.release_review_engine import ReleaseReviewEngine
from publishing.publish_engine.publish_engine import PublishEngine
from publishing.oauth_manager import OAuthManager
from publishing.scheduler import PublishScheduler
from audience.channel_brain import ChannelBrain


class StudioController:
    def __init__(self, profile_path="configs/studio_profile.json", secrets_path="configs/secrets.json"):
        self.profile = load_profile(profile_path)
        self.secrets = load_secrets(secrets_path)

        self.providers = ProviderRegistry(self.profile, self.secrets)
        self.orchestrator = MasterOrchestrator()

        self.ffmpeg = FFmpegProvider()
        self.image_provider = TitleCardProvider()
        self.piper = PiperProvider(
            model_path=self.secrets.get("audio_model_path", "models/en_US-lessac-medium.onnx")
        )

        self.pipeline = EpisodePipeline(
            image_provider=self.image_provider,
            audio_provider=self.piper,
            video_provider=self.ffmpeg
        )

        self.reviewer = ReleaseReviewEngine()
        self.publisher = PublishEngine()
        self.oauth = OAuthManager(self.secrets)
        self.scheduler = PublishScheduler()
        self.channel_brain = ChannelBrain()

    def run(self, mode="manual", action="episode-test", publish=False):
        run_policy = run_mode(mode, action, publish)

        if action == "episode-test":
            result = self.pipeline.run(topic="The Origin of the Impossible Map")
            return {"episode_result": result, "run_policy": run_policy}

        if action == "review-release":
            review = self.reviewer.inspect()
            return {"release_review": review, "run_policy": run_policy}

        if action == "publish-sim":
            episode = self.pipeline.run(topic="The Origin of the Impossible Map")
            publish_result = self.publisher.simulate_publish(episode["release_package"])
            return {
                "publish_simulation": publish_result,
                "oauth_status": self.oauth.status(),
                "schedule": self.scheduler.build_schedule(),
                "channel_brain": self.channel_brain.summarize_direction(),
                "run_policy": run_policy
            }

        if action == "platforms":
            episode = self.pipeline.run(topic="The Origin of the Impossible Map")
            payloads = self.publisher.prepare_payload(episode["release_package"])
            return {
                "platform_payloads": payloads,
                "oauth_status": self.oauth.status(),
                "schedule": self.scheduler.build_schedule(),
                "channel_brain": self.channel_brain.summarize_direction(),
                "run_policy": run_policy
            }

        cycle = self.orchestrator.run_cycle()
        return {"cycle_result": cycle, "run_policy": run_policy}
