"""Personality archetypes used to classify a values profile.

Each archetype is a prototype Schwartz vector (the motivational signature it
represents) plus lay-friendly descriptive material. Prototypes are positioned
around the circumplex so that together they tile the motivational space; a
user's profile is matched to the nearest one (or two) by cosine similarity in
*emphasis* space — see personality.profile.

The descriptive fields frame each type by where it falls on the two bipolar
Schwartz axes:

  * ``axis_change`` — Openness to Change  <->  Conservation
  * ``axis_focus``  — Self-Transcendence  <->  Self-Enhancement

plus a short Big Five reading. ``opposite``/``neighbors`` give the circumplex
relationships used for cross-linking the type pages.

Each ``schwartz`` prototype is a partial vector; missing keys are treated as 0.
"""

from __future__ import annotations

ARCHETYPES = [
    {
        "key": "explorer",
        "name": "The Explorer",
        "emoji": "🧭",
        "tagline": "Driven by novelty, freedom, and the next horizon",
        "schwartz": {"stimulation": 0.45, "self_direction": 0.35, "hedonism": 0.20},
        "big_five_hint": "high Openness and Extraversion",
        "axis_change": {
            "pole": "Openness to Change",
            "note": "Strongly drawn to novelty, autonomy, and stimulation; routine and restraint feel like a cage.",
        },
        "axis_focus": {
            "pole": "Self-directed (balanced focus)",
            "note": "Motivated more by personal experience and growth than by status or duty to others.",
        },
        "big_five_profile": [
            {"label": "Openness", "level": "very high"},
            {"label": "Extraversion", "level": "high"},
            {"label": "Conscientiousness", "level": "lower"},
        ],
        "description": (
            "You are pulled toward the new and the open road. Routine chafes; "
            "discovery, autonomy, and experience for its own sake are what make "
            "you feel alive."
        ),
        "detail": [
            "On the Openness-to-Change axis you sit near the far edge. "
            "Self-direction and stimulation dominate your values: you want to "
            "choose your own path and fill it with new experience. Constraint, "
            "repetition, and other people's rulebooks drain you faster than "
            "almost anything else.",
            "On the self-focus axis you're roughly balanced: you're not"
            "chasing dominance or status, and you're not primarily organised "
            "around serving others either. The point is the experience itself. "
            "That makes you a natural first-mover: you'll try the thing, go to "
            "the place, and start the conversation while others hesitate.",
        ],
        "strengths": [
            "Adapts quickly and thrives in change and ambiguity",
            "Curious and willing to take the first step",
            "Brings energy and momentum to a group",
            "Comfortable making independent decisions",
        ],
        "tensions": [
            "Follow-through and finishing can lag behind starting",
            "Long-term commitments can feel confining",
            "Restlessness when life gets predictable",
        ],
        "opposite": "guardian",
        "neighbors": ["creator", "free_spirit"],
    },
    {
        "key": "creator",
        "name": "The Creator",
        "emoji": "🎨",
        "tagline": "Compelled to make, express, and originate",
        "schwartz": {"self_direction": 0.6, "stimulation": 0.2, "universalism": 0.2},
        "big_five_hint": "very high Openness",
        "axis_change": {
            "pole": "Openness to Change",
            "note": "Self-direction is your centre of gravity. You need room to think, make, and express on your own terms.",
        },
        "axis_focus": {
            "pole": "Balanced, leaning Self-Transcendence",
            "note": "You create not just for yourself but to add beauty and meaning to the wider world.",
        },
        "big_five_profile": [
            {"label": "Openness", "level": "very high"},
            {"label": "Agreeableness", "level": "moderate"},
            {"label": "Conscientiousness", "level": "moderate"},
        ],
        "description": (
            "You see possibilities others miss and feel a need to bring them "
            "into being. Self-expression and originality are core to who you "
            "are."
        ),
        "detail": [
            "Like the Explorer you live on the Openness-to-Change side of the "
            "circle, but where they chase experience, you chase expression. "
            "Self-direction is your dominant value: the freedom to imagine and "
            "to make is non-negotiable. A streak of universalism gives your "
            "work a reach beyond yourself. You want what you make to matter"
            "and to be beautiful.",
            "That blend puts you slightly toward Self-Transcendence on the "
            "focus axis. You're rarely motivated by control or recognition for "
            "its own sake; the work is the reward. Your challenge is usually "
            "less about ideas than about the structure and persistence needed "
            "to finish and share them.",
        ],
        "strengths": [
            "Generates original ideas and sees what isn't there yet",
            "Expresses and communicates vividly",
            "Brings an aesthetic, meaning-making lens to problems",
            "Self-motivated when the work is genuinely theirs",
        ],
        "tensions": [
            "Structure, deadlines, and admin can feel hostile to the work",
            "Self-criticism or perfectionism can stall finishing",
            "Sensitivity to having creative autonomy overridden",
        ],
        "opposite": "seeker",
        "neighbors": ["explorer", "sage"],
    },
    {
        "key": "sage",
        "name": "The Sage",
        "emoji": "🦉",
        "tagline": "Seeking understanding, truth, and perspective",
        "schwartz": {"universalism": 0.5, "self_direction": 0.5},
        "big_five_hint": "high Openness with reflective calm",
        "axis_change": {
            "pole": "Openness to Change",
            "note": "Independent thought drives you. You reserve the right to reach your own conclusions.",
        },
        "axis_focus": {
            "pole": "Self-Transcendence",
            "note": "Universalism orients you outward: toward truth, fairness, and a wide view of the world.",
        },
        "big_five_profile": [
            {"label": "Openness", "level": "very high"},
            {"label": "Emotional Stability", "level": "high"},
            {"label": "Agreeableness", "level": "moderate"},
        ],
        "description": (
            "You want to understand how things really are. Knowledge, wisdom, "
            "and a wide, fair-minded view of the world guide your choices."
        ),
        "detail": [
            "You balance two values evenly: self-direction (think for yourself) "
            "and universalism (understand and protect the whole). That places "
            "you on the Openness-to-Change side for autonomy of thought, but "
            "firmly in Self-Transcendence for your aims. You're after "
            "understanding that is true, not merely useful to you.",
            "This combination tends to bring a reflective steadiness. You're "
            "slow to be swept up, comfortable holding uncertainty, and inclined "
            "to weigh many sides. The risk is staying in the library: "
            "understanding can become a substitute for acting, and detachment "
            "can read as aloofness to people who want you in the fray.",
        ],
        "strengths": [
            "Thinks independently and sees the whole picture",
            "Fair-minded and slow to distort the evidence",
            "Calm under pressure and comfortable with complexity",
            "A trusted source of perspective for others",
        ],
        "tensions": [
            "Analysis can crowd out action and decision",
            "May seem detached or above the fray",
            "Can underweight feelings, both their own and others'",
        ],
        "opposite": "achiever",
        "neighbors": ["creator", "idealist"],
    },
    {
        "key": "caregiver",
        "name": "The Caregiver",
        "emoji": "🤲",
        "tagline": "Devoted to nurturing and protecting others",
        "schwartz": {"benevolence": 0.8, "universalism": 0.2},
        "big_five_hint": "very high Agreeableness",
        "axis_change": {
            "pole": "Balanced, leaning Conservation",
            "note": "You value close, enduring bonds and the continuity of the people and groups you love.",
        },
        "axis_focus": {
            "pole": "Self-Transcendence",
            "note": "Benevolence is your core: the wellbeing of those around you is the measure of a good life.",
        },
        "big_five_profile": [
            {"label": "Agreeableness", "level": "very high"},
            {"label": "Conscientiousness", "level": "moderate"},
            {"label": "Emotional Stability", "level": "moderate"},
        ],
        "description": (
            "Other people's wellbeing is your compass. You show up with "
            "warmth, generosity, and care, and you measure a good life by who "
            "you've helped."
        ),
        "detail": [
            "You sit deep in Self-Transcendence, anchored by benevolence, a"
            "devotion to the concrete, near people in your life. A thread of "
            "universalism widens that circle of care beyond your inner ring. "
            "On the change-conservation axis you lean gently toward "
            "conservation: you protect bonds and want them to last.",
            "Your gift is presence and reliability for others; people feel "
            "safe with you. The shadow side is the one almost every Caregiver "
            "knows: your own needs slide to the bottom of the list, and you "
            "can stay loyal to people or situations past the point where it "
            "serves anyone. Caring for yourself is not a betrayal of the type; "
            "it's what keeps it sustainable.",
        ],
        "strengths": [
            "Deeply attuned to others' needs and feelings",
            "Generous, dependable, and loyal",
            "Creates safety and trust in relationships",
            "Holds groups and families together",
        ],
        "tensions": [
            "Neglecting your own needs and burning out",
            "Over-loyalty to people or situations that take advantage",
            "Difficulty setting boundaries or saying no",
        ],
        "opposite": "achiever",
        "neighbors": ["connector", "idealist"],
    },
    {
        "key": "connector",
        "name": "The Connector",
        "emoji": "🫂",
        "tagline": "Alive in warmth, closeness, and shared joy",
        "schwartz": {"benevolence": 0.5, "hedonism": 0.3, "stimulation": 0.2},
        "big_five_hint": "high Extraversion and Agreeableness",
        "axis_change": {
            "pole": "Openness to Change",
            "note": "Spontaneity and shared experience matter. You bring warmth into motion.",
        },
        "axis_focus": {
            "pole": "Self-Transcendence, with a hedonic streak",
            "note": "Relationships come first, but you believe connection should feel good, not dutiful.",
        },
        "big_five_profile": [
            {"label": "Extraversion", "level": "high"},
            {"label": "Agreeableness", "level": "high"},
            {"label": "Openness", "level": "moderate"},
        ],
        "description": (
            "Relationships and shared experience are where you come alive. You "
            "bring people together and find meaning in belonging and connection."
        ),
        "detail": [
            "You blend benevolence (care for others) with hedonism and "
            "stimulation (enjoyment and aliveness). That makes you warmer and "
            "more spontaneous than the pure Caregiver: you sit partly in "
            "Self-Transcendence and partly on the Openness-to-Change side. "
            "Connection, for you, is meant to be felt and enjoyed.",
            "You're the social glue: you notice who's left out, you start the "
            "gathering, you turn a group of people into a group. The tension is "
            "depth versus breadth: in keeping everyone close and everything "
            "pleasant, harder truths and your own quieter needs can go unsaid.",
        ],
        "strengths": [
            "Builds rapport and belonging effortlessly",
            "Warm, inclusive, and emotionally generous",
            "Brings energy and joy to shared life",
            "Reads a room and brings people together",
        ],
        "tensions": [
            "Avoiding conflict to keep the peace",
            "Spreading thin across many relationships",
            "Discomfort with solitude or stillness",
        ],
        "opposite": "guardian",
        "neighbors": ["caregiver", "free_spirit"],
    },
    {
        "key": "guardian",
        "name": "The Guardian",
        "emoji": "🛡️",
        "tagline": "Anchored in stability, duty, and dependability",
        "schwartz": {"security": 0.4, "conformity": 0.3, "tradition": 0.3},
        "big_five_hint": "high Conscientiousness with steady calm",
        "axis_change": {
            "pole": "Conservation",
            "note": "Stability, order, and continuity are your foundation; you protect what works and what lasts.",
        },
        "axis_focus": {
            "pole": "Balanced, with a protective streak",
            "note": "You're not driven by status or self-display; your effort goes to safeguarding people and commitments.",
        },
        "big_five_profile": [
            {"label": "Conscientiousness", "level": "very high"},
            {"label": "Emotional Stability", "level": "high"},
            {"label": "Agreeableness", "level": "moderate"},
        ],
        "description": (
            "You build and protect what lasts. Reliability, order, and loyalty "
            "to people and principles make you the steady ground others stand "
            "on."
        ),
        "detail": [
            "You anchor the Conservation pole of the circle: security,"
            "conformity, and tradition together. You value stability, do what "
            "you say you'll do, and honour your commitments and the structures "
            "that hold things together. Where the Explorer runs toward change, "
            "you run toward what's dependable.",
            "On the focus axis you're balanced but quietly protective: your "
            "diligence is in service of keeping people and promises safe, not "
            "of winning. People rely on you precisely because you're "
            "predictable in the best sense. The growth edge is flexibility:"
            "not every rule is worth keeping, and not every change is a threat.",
        ],
        "strengths": [
            "Reliable, organised, and true to commitments",
            "Steady and calm when others panic",
            "Protects people, standards, and continuity",
            "Builds durable systems and routines",
        ],
        "tensions": [
            "Resistance to change even when it's warranted",
            "Rules can be held more tightly than their purpose",
            "Risk-aversion may close off good opportunities",
        ],
        "opposite": "explorer",
        "neighbors": ["seeker", "achiever"],
    },
    {
        "key": "achiever",
        "name": "The Achiever",
        "emoji": "🏆",
        "tagline": "Striving toward mastery, results, and influence",
        "schwartz": {"achievement": 0.6, "power": 0.4},
        "big_five_hint": "high Conscientiousness and Extraversion",
        "axis_change": {
            "pole": "Balanced",
            "note": "You'll embrace change or structure, whichever moves you toward the goal.",
        },
        "axis_focus": {
            "pole": "Self-Enhancement",
            "note": "Achievement and influence drive you: competence, results, and the capacity to make things happen.",
        },
        "big_five_profile": [
            {"label": "Conscientiousness", "level": "very high"},
            {"label": "Extraversion", "level": "high"},
            {"label": "Agreeableness", "level": "lower"},
        ],
        "description": (
            "You set the bar high and clear it. Competence, accomplishment, "
            "and the capacity to make things happen are what you organise your "
            "life around."
        ),
        "detail": [
            "You anchor the Self-Enhancement pole: achievement (demonstrated"
            "competence) paired with power (influence and the ability to shape "
            "outcomes). You set goals, measure progress, and take ownership of "
            "results. On the change axis you're pragmatic: you'll innovate or "
            "follow the process, whichever wins.",
            "This drive makes you effective and dependable under a target. The "
            "classic tension is that the self-enhancement that fuels you sits "
            "directly opposite self-transcendence on the circle, so the"
            "growth work is making sure ambition doesn't crowd out care, and "
            "that worth isn't fully outsourced to the scoreboard.",
        ],
        "strengths": [
            "Goal-focused and gets results",
            "High standards and strong follow-through",
            "Confident taking ownership and leading",
            "Turns ambition into concrete outcomes",
        ],
        "tensions": [
            "Self-worth can hinge on achievement",
            "May push past relationships or wellbeing to win",
            "Impatience with slower or less driven people",
        ],
        "opposite": "caregiver",
        "neighbors": ["guardian", "explorer"],
    },
    {
        "key": "idealist",
        "name": "The Idealist",
        "emoji": "⚖️",
        "tagline": "Fighting for justice, fairness, and a better world",
        "schwartz": {"universalism": 0.7, "benevolence": 0.3},
        "big_five_hint": "high Openness and Agreeableness",
        "axis_change": {
            "pole": "Openness to Change, in service of reform",
            "note": "You question how things are and push for how they should be.",
        },
        "axis_focus": {
            "pole": "Self-Transcendence",
            "note": "Universalism is your core: justice, equality, and the welfare of all people and the planet.",
        },
        "big_five_profile": [
            {"label": "Openness", "level": "high"},
            {"label": "Agreeableness", "level": "high"},
            {"label": "Conscientiousness", "level": "moderate"},
        ],
        "description": (
            "You hold the world to a moral standard. Equality, justice, and "
            "the welfare of all people and the planet are causes you can't look "
            "away from."
        ),
        "detail": [
            "You're the purest Self-Transcendence type, led by universalism, a"
            "concern that reaches past your own circle to everyone and "
            "everything. Benevolence keeps it personal as well as principled. "
            "Your reforming instinct leans you toward Openness to Change: the "
            "status quo is rarely good enough.",
            "At your best you're a conscience: you see injustice others"
            "normalise and you won't let it rest. The cost of caring that "
            "widely is real: the gap between the world as it is and as it "
            "should be can wear you down, and moral clarity can tip into "
            "judgement of those who don't share your urgency.",
        ],
        "strengths": [
            "Strong moral compass and sense of justice",
            "Cares about fairness beyond their own circle",
            "Willing to stand up for principle",
            "Inspires others toward a bigger purpose",
        ],
        "tensions": [
            "Disillusionment when the world falls short",
            "Moral certainty can become judgement",
            "Carrying the weight of problems too big to fix alone",
        ],
        "opposite": "achiever",
        "neighbors": ["sage", "caregiver"],
    },
    {
        "key": "seeker",
        "name": "The Seeker",
        "emoji": "🧘",
        "tagline": "Grounded in meaning, faith, and inner depth",
        "schwartz": {"tradition": 0.6, "universalism": 0.2, "self_direction": 0.2},
        "big_five_hint": "openness paired with emotional steadiness",
        "axis_change": {
            "pole": "Conservation",
            "note": "Tradition and continuity ground you. You draw on what is timeless and inherited.",
        },
        "axis_focus": {
            "pole": "Self-Transcendence",
            "note": "You orient toward something larger than yourself: the sacred, the meaningful, the whole.",
        },
        "big_five_profile": [
            {"label": "Openness", "level": "high"},
            {"label": "Emotional Stability", "level": "high"},
            {"label": "Agreeableness", "level": "moderate"},
        ],
        "description": (
            "You look for something larger than yourself. Meaning, presence, "
            "and a connection to the sacred or timeless give your life its "
            "shape."
        ),
        "detail": [
            "Tradition anchors you on the Conservation side of the circle, but "
            "not as rule-following, but as reverence for what endures and gives "
            "meaning. Touches of universalism and self-direction make it your "
            "own search rather than an inherited script, and pull you toward "
            "Self-Transcendence in aim.",
            "You bring depth and groundedness; you're rarely rattled by "
            "surface noise because you're oriented to something deeper. The "
            "tension is staying engaged with the ordinary, practical world,"
            "and holding meaning loosely enough that it stays a living search "
            "rather than a fixed certainty.",
        ],
        "strengths": [
            "Grounded in a deep sense of meaning",
            "Calm and centred amid turbulence",
            "Reflective and spiritually or philosophically rich",
            "Brings perspective on what truly matters",
        ],
        "tensions": [
            "Can disengage from practical, everyday demands",
            "Meaning can harden into rigid certainty",
            "May feel out of step with a fast, secular world",
        ],
        "opposite": "creator",
        "neighbors": ["guardian", "idealist"],
    },
    {
        "key": "free_spirit",
        "name": "The Free Spirit",
        "emoji": "🦋",
        "tagline": "Living for joy, spontaneity, and the present",
        "schwartz": {"hedonism": 0.5, "stimulation": 0.5},
        "big_five_hint": "high Extraversion and Openness",
        "axis_change": {
            "pole": "Openness to Change",
            "note": "Hedonism and stimulation put you at the spontaneous, in-the-moment edge of the circle.",
        },
        "axis_focus": {
            "pole": "Self-directed enjoyment",
            "note": "Your own experience of pleasure and aliveness leads, not status or duty.",
        },
        "big_five_profile": [
            {"label": "Extraversion", "level": "very high"},
            {"label": "Openness", "level": "high"},
            {"label": "Conscientiousness", "level": "lower"},
        ],
        "description": (
            "You take life as it comes and savour it. Play, pleasure, and "
            "spontaneity aren't indulgences to you. They're the point."
        ),
        "detail": [
            "You live where hedonism meets stimulation, the most"
            "present-tense corner of the Openness-to-Change side. You're here "
            "for the experience of being alive: pleasure, play, novelty, the "
            "good moment as it happens. Plans and obligations are useful only "
            "insofar as they don't kill the spark.",
            "Your joy is contagious and you give others permission to "
            "lighten up. Directly opposite you on the circle sits the "
            "Guardian's world of duty and restraint, which is exactly your"
            "growth edge: a little structure and follow-through lets the good "
            "times actually last instead of fizzling.",
        ],
        "strengths": [
            "Spontaneous, playful, and fun to be around",
            "Fully present and savours the moment",
            "Resilient optimism and lightness",
            "Gives others permission to enjoy life",
        ],
        "tensions": [
            "Long-term planning and discipline take a back seat",
            "Avoiding the dull-but-necessary",
            "Commitments can feel like constraints",
        ],
        "opposite": "guardian",
        "neighbors": ["explorer", "connector"],
    },
]


def archetype_by_key(key: str) -> dict | None:
    for a in ARCHETYPES:
        if a["key"] == key:
            return a
    return None
