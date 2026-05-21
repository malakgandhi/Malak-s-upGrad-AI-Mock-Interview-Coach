# AI Mock Interview Coach

A multi-agent mock interview system that simulates a realistic 5-7 turn interview, adapts to answer quality, and produces structured coaching at the end.

## Features
- Role-aware interview planning
- Adaptive follow-up questions
- Multi-dimensional answer evaluation
- End-of-session coaching with specific practice advice

## Multi-Agent Architecture
1. Strategist
Designs the interview plan based on target role, candidate background, and chosen focus area.

2. Interviewer
Runs the live interview, asks one question at a time, and decides whether to probe deeper or move on.

3. Evaluator
Scores each answer on multiple dimensions such as relevance, depth, communication, and confidence.

4. Coach
Synthesizes the full interview history into clear final feedback, strengths, gaps, and practice drills.

## Orchestration
- Candidate provides role, background, and focus area.
- Strategist creates a 5-7 turn plan.
- Interviewer asks the opening question.
- After each answer, Evaluator scores the response.
- Interviewer uses the evaluation to decide the next question.
- Coach produces final feedback after the interview ends.

## Setup
```bash
pip install -r requirements.txt