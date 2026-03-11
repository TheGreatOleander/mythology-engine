import argparse
import json
from studio.core.studio_controller import StudioController

def build_parser():
    parser = argparse.ArgumentParser(prog="mythology")
    parser.add_argument(
        "--action",
        default="episode-test",
        choices=["episode-test", "review-release", "publish-sim", "platforms"]
    )
    parser.add_argument("--mode", default="manual", choices=["manual", "assisted", "auto"])
    parser.add_argument("--profile", default="configs/studio_profile.json")
    parser.add_argument("--secrets", default="configs/secrets.json")
    return parser

def main():
    args = build_parser().parse_args()
    controller = StudioController(profile_path=args.profile, secrets_path=args.secrets)
    result = controller.run(mode=args.mode, action=args.action)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
