"""
generative_design_scaffold.py
Multi-agent AI pipeline for generative design exploration and feasibility pre-screening.
Aesthetic Agent -> Feasibility Agent -> Synthesis Agent -> Structured JSON scaffold.
"""

import json, os, urllib.request
from dataclasses import dataclass
from datetime import datetime
from typing import List

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
DEFAULT_BRIEF = ("Aggressive front fascia for a next-gen performance SUV, "
                 "pedestrian safety compliant, target emotion: apex predator")

@dataclass
class DesignDirection:
    name: str; description: str; key_features: List[str]; risks: List[str]

@dataclass
class Scaffold:
    brief: str; timestamp: str; directions: List[DesignDirection]
    recommended: str; next_steps: List[str]

def claude(system: str, user: str) -> str:
    payload = json.dumps({"model":"claude-3-5-sonnet-20241022","max_tokens":1024,
        "system":system,"messages":[{"role":"user","content":user}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
        headers={"x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01","content-type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["content"][0]["text"].strip()

def aesthetic_agent(brief: str) -> List[dict]:
    sys = 'Senior automotive design AI. Generate 3 distinct design directions. Respond ONLY with JSON array: [{"name":str,"description":str,"key_features":[3 strings]},...]'
    try: return json.loads(claude(sys, f"Brief: {brief}"))
    except: return [{"name":"Direction A","description":brief,"key_features":["TBD","TBD","TBD"]}]

def feasibility_agent(brief: str, directions: List[dict]) -> dict:
    sys = 'Automotive engineering feasibility AI. Knowledge: ECE-R127, FMVSS, hardpoints, cost. For each direction identify the top risk. Respond ONLY with JSON: {"DirectionName":"risk",...}'
    dirs = json.dumps([{"name":d["name"],"description":d["description"]} for d in directions])
    try: return json.loads(claude(sys, f"Brief: {brief}\nDirections: {dirs}"))
    except: return {}

def synthesis_agent(brief: str, directions: List[dict], feasibility: dict) -> dict:
    sys = 'Design synthesis AI. Recommend best path forward. Respond ONLY with JSON: {"recommended":"direction+rationale","next_steps":["s1","s2","s3"]}'
    ctx = json.dumps({"directions":directions,"feasibility":feasibility})
    try: return json.loads(claude(sys, f"Brief: {brief}\nContext: {ctx}"))
    except: return {"recommended":"Review with design team","next_steps":["Manual review"]}

def generate(brief: str) -> Scaffold:
    print("[1/3] Aesthetic Agent: generating directions...")
    directions = aesthetic_agent(brief)
    print("[2/3] Feasibility Agent: screening conflicts...")
    feasibility = feasibility_agent(brief, directions)
    print("[3/3] Synthesis Agent: recommending path...")
    synthesis = synthesis_agent(brief, directions, feasibility)
    return Scaffold(
        brief=brief, timestamp=datetime.now().isoformat(),
        directions=[DesignDirection(name=d.get("name","?"), description=d.get("description",""),
            key_features=d.get("key_features",[]),
            risks=[feasibility.get(d.get("name",""),"No major risks identified")]) for d in directions],
        recommended=synthesis.get("recommended",""), next_steps=synthesis.get("next_steps",[])
    )

def print_scaffold(s: Scaffold):
    print(f"\n{'='*60}\nDESIGN SCAFFOLD - {s.timestamp[:10]}\nBrief: {s.brief}\n{'='*60}\n")
    for i, d in enumerate(s.directions, 1):
        print(f"DIRECTION {i}: {d.name}\n  {d.description}")
        print(f"  Features: {' | '.join(d.key_features)}\n  Risk: {d.risks[0]}\n")
    print(f"RECOMMENDATION: {s.recommended}\n\nNEXT STEPS:")
    for step in s.next_steps: print(f"  -> {step}")

if __name__ == "__main__":
    brief = input("Design brief (Enter for default): ").strip() or DEFAULT_BRIEF
    s = generate(brief)
    print_scaffold(s)
    out = f"scaffold_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(out,"w") as f:
        json.dump({"brief":s.brief,"timestamp":s.timestamp,
            "directions":[{"name":d.name,"description":d.description,
                "key_features":d.key_features,"risks":d.risks} for d in s.directions],
            "recommended":s.recommended,"next_steps":s.next_steps},f,indent=2)
    print(f"\nSaved to {out}")
