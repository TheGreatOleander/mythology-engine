import json, os

ENGINE_OUTPUT = "engine_last_run.json"
OUTDIR = "/sdcard/mythology-engine/output/episode_bundle"

def main():

    if not os.path.exists(ENGINE_OUTPUT):
        print("engine_last_run.json not found")
        return

    data = json.load(open(ENGINE_OUTPUT))
    episode = data["episode_result"]

    os.makedirs(OUTDIR, exist_ok=True)

    open(os.path.join(OUTDIR,"script.txt"),"w").write(episode["script_text"])

    bundle = {
        "bundle_version":"1.0",
        "project":"mythology-engine",
        "episode_id":"engine_run",
        "title":episode["title"]["title"],
        "topic":episode["topic"],
        "paths":{
            "script":"script.txt",
            "metadata":"metadata.json",
            "scene_prompts":"scene_prompts.json",
            "episode_plan":"episode_plan.json"
        }
    }

    json.dump(bundle,open(os.path.join(OUTDIR,"bundle.json"),"w"),indent=2)

    metadata = {
        "series":"Mythology Engine",
        "tags":["engine"],
        "tone":"documentary"
    }

    json.dump(metadata,open(os.path.join(OUTDIR,"metadata.json"),"w"),indent=2)

    scene=[{
        "scene_id":"scene_01",
        "prompt":"generated scene",
        "narration":episode["script_text"][:120]
    }]

    json.dump(scene,open(os.path.join(OUTDIR,"scene_prompts.json"),"w"),indent=2)

    plan={
        "hook":episode["title"]["hook"],
        "beats":["intro","investigation","reveal"],
        "target_duration_sec":60
    }

    json.dump(plan,open(os.path.join(OUTDIR,"episode_plan.json"),"w"),indent=2)

    print("episode_bundle exported to",OUTDIR)


if __name__=="__main__":
    main()
