# Generative Design Scaffold

AI agent that takes a natural language design brief and generates structured design
directions, feasibility flags, and synthesis recommendations.

Directly inspired by Ford Studio's AI and Generative Workflows initiative.

## Multi-Agent Pipeline
```
Design Brief (natural language)
    |
Aesthetic Agent  -> 3 distinct design directions
    |
Feasibility Agent -> regulatory + engineering flags per direction
    |
Synthesis Agent  -> recommended path + next steps
    |
Structured JSON scaffold (CAD pipeline ready)
```

## Sample Output
```
DESIGN SCAFFOLD - 2026-05-28
Brief: Aggressive front fascia, performance SUV, pedestrian safety compliance

DIRECTION 1: Apex Predator
  Sharp angular hood with swept LED signature
  Risk: Hood height may conflict with ECE-R127 pedestrian impact regulation

DIRECTION 2: Technical Brutalism
  Flat-plane surfacing with functional aero vents
  Risk: Active shutters add ~8kg and $340 cost delta

RECOMMENDATION: Direction 2 geometry + Direction 1 LED above 625mm datum
NEXT STEPS: CFD validation, LED packaging review, cost delta sign-off
```

## Real-World Extension
Pipe JSON output into Catia/3DX surface scaffold workflows.
Feed feasibility flags into Design Feasibility Checkpoint Process automation.

## Usage
```bash
export ANTHROPIC_API_KEY=your_key
python scaffold.py
```
