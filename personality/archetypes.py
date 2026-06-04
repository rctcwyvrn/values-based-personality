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
        "two_truths": "You're the most fun person to make plans with and the least likely to keep them exactly as planned.",
        "thriving": "You're pure momentum: trying things, meeting people, dragging the group toward something better than the original plan.",
        "empty": "You're restless and scattered, starting six things to dodge finishing one and chasing the next hit of new.",
        "kryptonite": "A meeting that could've been an email, and a calendar with zero white space.",
        "green_flags": ["Up for anything, last-minute", "Makes the ordinary feel like an adventure", "Genuinely curious about you"],
        "red_flags": ["Vanishes the moment things get routine", "Commitment makes them twitchy", "Always has one foot out the door"],
        "quick_stats": [
            {"label": "Spontaneity", "level": 5},
            {"label": "Follow-through", "level": 2},
            {"label": "Wanderlust", "level": 5},
        ],
        "portrait": [
            "You're the one who says \"let's just go\" before anyone's checked "
            "the forecast. New places, new people, new ideas, you're in. The "
            "only thing that genuinely unsettles you is standing still.",
            "Plans are loose suggestions and comfort zones are for other "
            "people. You'd rather try and fumble than sit around wondering "
            "\"what if,\" and life is basically a pile of experiences waiting "
            "to be had.",
        ],
        "recognize": [
            "You've booked the trip first and figured out the details later.",
            "An empty weekend feels like an invitation, not a void.",
            "Routine starts to itch after about a week.",
        ],
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
            "On the self-focus axis you're roughly balanced: you're not "
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
        "neighbors": ["connector", "free_spirit"],
    },
    {
        "key": "creator",
        "name": "The Creator",
        "emoji": "🎨",
        "tagline": "Compelled to make, express, and originate",
        "two_truths": "You're bursting with ideas and quietly terrified that none of them are good enough.",
        "thriving": "You're in flow, making and shaping and losing track of time, leaving the world a little more beautiful than you found it.",
        "empty": "You're blocked and self-critical, measuring your rough drafts against everyone else's highlight reels.",
        "kryptonite": "A blank template, a committee, and the words 'just keep it standard.'",
        "green_flags": ["Sees the version of things that doesn't exist yet", "Makes you feel like a muse", "Brings beauty to the boring stuff"],
        "red_flags": ["Disappears into the work for days", "Takes feedback as a personal verdict", "Allergic to 'because that's how it's done'"],
        "quick_stats": [
            {"label": "Imagination", "level": 5},
            {"label": "Tolerance for rules", "level": 2},
            {"label": "Finishing things", "level": 3},
        ],
        "portrait": [
            "You see the version of things that doesn't exist yet, and it bugs "
            "you until you make it real. Hand you a blank page, an empty room, "
            "a half-formed idea, and you'll turn it into something with your "
            "fingerprints all over it.",
            "You're not chasing applause; the making is the point. What you "
            "can't stand is being boxed in, handed a template, or told there's "
            "only one right way to do it.",
        ],
        "recognize": [
            "You've got three half-finished projects and ideas for ten more.",
            "\"Just follow the instructions\" makes your eye twitch.",
            "You notice when something is ugly, and you can't quite let it go.",
        ],
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
            "work a reach beyond yourself. You want what you make to matter "
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
        "opposite": "provider",
        "neighbors": ["sage", "connector"],
    },
    {
        "key": "sage",
        "name": "The Sage",
        "emoji": "🦉",
        "tagline": "Seeking understanding, truth, and perspective",
        "two_truths": "You're the calmest head in the room and the slowest to say what you actually feel.",
        "thriving": "You're clear and unflappable, the one who cuts through the noise and says the true thing simply.",
        "empty": "You retreat into your head, analysing instead of acting and calling the distance objectivity.",
        "kryptonite": "Being rushed to a hot take before you've had time to think.",
        "green_flags": ["Listens more than they talk", "Won't fake certainty they don't have", "Changes their mind when the facts do"],
        "red_flags": ["Lives in the library, skips the party", "Hard to read emotionally", "Can analyse the feeling right out of a moment"],
        "quick_stats": [
            {"label": "Depth", "level": 5},
            {"label": "Patience for nonsense", "level": 1},
            {"label": "Composure", "level": 5},
        ],
        "portrait": [
            "You want to actually understand things, not just the headline but the "
            "whole picture. While everyone else is busy reacting, you're the "
            "one quietly asking \"okay, but is that really true?\"",
            "You take your time, weigh the sides, and you're hard to stampede. "
            "People come to you when they need a clear head and an honest read, "
            "not a hot take.",
        ],
        "recognize": [
            "You've fallen down a research rabbit hole just to be sure.",
            "You're comfortable saying \"it's complicated\" and meaning it.",
            "Snap judgments make you a little uneasy.",
        ],
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
        "opposite": "provider",
        "neighbors": ["idealist", "creator"],
    },
    {
        "key": "caregiver",
        "name": "The Caregiver",
        "emoji": "🤲",
        "tagline": "Devoted to nurturing and protecting others",
        "two_truths": "You're the first to notice everyone else's needs and the last to admit your own.",
        "thriving": "You're warm and steady, the safe place people come back to, giving freely and feeling full.",
        "empty": "You over-give until you're hollow, then quietly resent that nobody thought to refill the cup.",
        "kryptonite": "Watching someone you love struggle and not being allowed to help.",
        "green_flags": ["Shows up when it actually counts", "Remembers the small stuff", "Makes people feel safe"],
        "red_flags": ["Says 'I'm fine' on an empty tank", "Loyal past their own breaking point", "Bad at letting you give back"],
        "quick_stats": [
            {"label": "Warmth", "level": 5},
            {"label": "Saying no", "level": 1},
            {"label": "Reliability", "level": 5},
        ],
        "portrait": [
            "You're the one who notices the person going quiet at the table. "
            "Other people's wellbeing isn't a side quest for you; it's the "
            "whole map. You show up, you follow through, and people feel safe "
            "around you.",
            "You measure a good day by who you helped. The catch is that your "
            "own name tends to slide to the bottom of the list, and you'll "
            "stay loyal long after you should have tapped out.",
        ],
        "recognize": [
            "You've checked on someone before checking on yourself.",
            "\"I'm fine, don't worry about me\" is basically your catchphrase.",
            "You remember everyone's little things: the coffee order, the bad week.",
        ],
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
            "You sit deep in Self-Transcendence, anchored by benevolence, a "
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
        "neighbors": ["seeker", "idealist"],
    },
    {
        "key": "connector",
        "name": "The Connector",
        "emoji": "🫂",
        "tagline": "Alive in warmth, closeness, and shared joy",
        "two_truths": "You can talk to anyone, and you'll dodge the one hard conversation that actually matters.",
        "thriving": "You're the social glue, lighting up rooms and turning a handful of strangers into a group that lasts.",
        "empty": "You're spread thin and people-pleasing, keeping everyone happy while nobody notices you're not.",
        "kryptonite": "Tension you can't smooth over, and a long stretch of being alone.",
        "green_flags": ["Makes everyone feel included", "Remembers your birthday and your dog's name", "Brings the energy"],
        "red_flags": ["Avoids conflict until it festers", "Says yes to everyone, themselves last", "Goes quiet about their own needs"],
        "quick_stats": [
            {"label": "Charm", "level": 5},
            {"label": "Comfort with conflict", "level": 2},
            {"label": "Group chats", "level": 5},
        ],
        "portrait": [
            "You turn a handful of people into a group. You clock who's on the "
            "edge of the circle and pull them in, and somehow the gathering "
            "doesn't really start until you arrive.",
            "Closeness is your fuel, and it's supposed to feel good, not "
            "dutiful. Your one real blind spot is smoothing things over so "
            "everyone stays happy, even when something needs to be said.",
        ],
        "recognize": [
            "You're the one who actually organizes the reunion.",
            "A good long catch-up recharges you more than a nap.",
            "You'd usually rather keep the peace than win the point.",
        ],
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
        "opposite": "provider",
        "neighbors": ["creator", "explorer"],
    },
    {
        "key": "guardian",
        "name": "The Guardian",
        "emoji": "🛡️",
        "tagline": "Anchored in stability, duty, and dependability",
        "two_truths": "You're the most reliable person in the room and the one quietly craving a single unplanned weekend.",
        "thriving": "You're the steady ground everyone stands on, calm, prepared, holding it all together without being asked.",
        "empty": "You white-knuckle the routine, treating every change as a threat and every risk as reckless.",
        "kryptonite": "A plan that changes at the last minute for no good reason.",
        "green_flags": ["Does exactly what they said they'd do", "Calm when everything's on fire", "Always has the spare charger"],
        "red_flags": ["Mistakes a new idea for an attack", "Defaults to 'we've always done it this way'", "Slow to loosen the grip"],
        "quick_stats": [
            {"label": "Dependability", "level": 5},
            {"label": "Love of surprises", "level": 1},
            {"label": "Crisis composure", "level": 5},
        ],
        "portrait": [
            "You're the person everyone secretly relies on. If you said you'd "
            "do it, it's done. While other people chase the new shiny thing, "
            "you're busy keeping the lights on and the ship steady.",
            "Calm in a crisis, loyal to a fault, allergic to chaos. Your "
            "growth edge: not every rule is sacred, and not every change is a "
            "threat. Sometimes the steady move is to bend.",
        ],
        "recognize": [
            "You've got a backup plan for the backup plan.",
            "People hand you the keys because you won't lose them.",
            "Last-minute changes make your jaw tighten.",
        ],
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
            "You anchor the Conservation pole of the circle: security, "
            "conformity, and tradition together. You value stability, do what "
            "you say you'll do, and honour your commitments and the structures "
            "that hold things together. Where the Explorer runs toward change, "
            "you run toward what's dependable.",
            "On the focus axis you're balanced but quietly protective: your "
            "diligence is in service of keeping people and promises safe, not "
            "of winning. People rely on you precisely because you're "
            "predictable in the best sense. The growth edge is flexibility: "
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
        "neighbors": ["provider", "seeker"],
    },
    {
        "key": "achiever",
        "name": "The Achiever",
        "emoji": "🏆",
        "tagline": "Striving toward mastery, results, and influence",
        "two_truths": "You make it all look effortless and you're worn out from how much effort it actually takes.",
        "thriving": "You're unstoppable, clear goals and high standards turning ambition into things that actually get done.",
        "empty": "You pin your whole worth to the scoreboard and can't sit still long enough to enjoy the win.",
        "kryptonite": "Coming second, and being told to 'just relax.'",
        "green_flags": ["Gets things done", "Roots for you to level up too", "Owns it when it's on them"],
        "red_flags": ["Can't switch off the scoreboard", "Steamrolls slower people", "Treats worth as win rate"],
        "quick_stats": [
            {"label": "Drive", "level": 5},
            {"label": "Off switch", "level": 2},
            {"label": "Standards", "level": 5},
        ],
        "portrait": [
            "You set the bar high and then clear it. Goals don't stress you "
            "out; they switch you on. You like being good at things, and you "
            "like making things happen.",
            "You take ownership when others hesitate and you don't flinch at a "
            "target. Just watch the scoreboard trap: your worth isn't the same "
            "as your win rate, and the people around you matter more than the "
            "next milestone.",
        ],
        "recognize": [
            "You've turned a hobby into a leaderboard.",
            "\"Good enough\" rarely feels good enough.",
            "You measure the year by what you actually pulled off.",
        ],
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
            "You anchor the Self-Enhancement pole: achievement (demonstrated "
            "competence) paired with power (influence and the ability to shape "
            "outcomes). You set goals, measure progress, and take ownership of "
            "results. On the change axis you're pragmatic: you'll innovate or "
            "follow the process, whichever wins.",
            "This drive makes you effective and dependable under a target. The "
            "classic tension is that the self-enhancement that fuels you sits "
            "directly opposite self-transcendence on the circle, so the "
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
        "opposite": "idealist",
        "neighbors": ["free_spirit", "sovereign"],
    },
    {
        "key": "idealist",
        "name": "The Idealist",
        "emoji": "⚖️",
        "tagline": "Fighting for justice, fairness, and a better world",
        "two_truths": "You'd fix the whole world if you could, and it quietly breaks your heart that you can't.",
        "thriving": "You're a conscience with momentum, naming what's wrong and pulling people toward something better.",
        "empty": "You're disillusioned and heavy, carrying problems too big to hold and judging anyone who looks away.",
        "kryptonite": "Unfairness you can see clearly and can't do anything about.",
        "green_flags": ["Stands up for people who can't", "Means every word about fairness", "Cares well past their own front door"],
        "red_flags": ["The moral high ground gets crowded up there", "Burns out on caring", "Can mistake disagreement for villainy"],
        "quick_stats": [
            {"label": "Conviction", "level": 5},
            {"label": "Letting it go", "level": 1},
            {"label": "Sense of justice", "level": 5},
        ],
        "portrait": [
            "You can't un-see unfairness. While others shrug and move on, "
            "you're the one who says \"wait, that's not right\" and means it. "
            "The world as it could be is always a little louder in your head "
            "than the world as it is.",
            "You care way past your own front door: about people you'll never "
            "meet, about the planet, about the principle of the thing. Just "
            "don't let the gap between what is and what should be grind you "
            "down, or let conviction harden into judging everyone who isn't "
            "there yet.",
        ],
        "recognize": [
            "You've gotten heated about something that doesn't even affect you.",
            "\"That's just how it is\" is not an answer you accept.",
            "You feel the world's problems a little too personally.",
        ],
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
            "You're the purest Self-Transcendence type, led by universalism, a "
            "concern that reaches past your own circle to everyone and "
            "everything. Benevolence keeps it personal as well as principled. "
            "Your reforming instinct leans you toward Openness to Change: the "
            "status quo is rarely good enough.",
            "At your best you're a conscience: you see injustice others "
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
        "opposite": "sovereign",
        "neighbors": ["caregiver", "sage"],
    },
    {
        "key": "seeker",
        "name": "The Seeker",
        "emoji": "🧘",
        "tagline": "Grounded in meaning, faith, and inner depth",
        "two_truths": "You're deeply at peace and quietly restless for something you can't quite name.",
        "thriving": "You're grounded and present, unshaken by the noise because you're tuned to something deeper.",
        "empty": "You drift from the practical world, mistaking detachment for wisdom and certainty for peace.",
        "kryptonite": "Small talk, fluorescent lights, and a life with no room to breathe.",
        "green_flags": ["Genuinely present with you", "Unbothered by petty drama", "Asks the questions that matter"],
        "red_flags": ["Floats above the practical stuff", "Can get rigid about their beliefs", "Hard to pin down for plans"],
        "quick_stats": [
            {"label": "Inner calm", "level": 5},
            {"label": "Patience for small talk", "level": 1},
            {"label": "Depth", "level": 5},
        ],
        "portrait": [
            "You're after something deeper than the daily noise. Meaning, "
            "stillness, a sense of something bigger, that's the thread you're "
            "always following. Surface drama rolls off you because you're "
            "tuned to a longer frequency.",
            "You bring a groundedness that's rare and quietly steadying to be "
            "around. The trick is staying plugged into the ordinary, practical "
            "world too, and holding your beliefs with open hands.",
        ],
        "recognize": [
            "You've wandered off to be alone with your thoughts on purpose.",
            "Small talk drains you; the 3am conversation lights you up.",
            "You ask \"but what's it all for?\" more than most.",
        ],
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
            "Tradition anchors you on the Conservation side of the circle, "
            "not as rule-following but as reverence for what endures and gives "
            "meaning. Touches of universalism and self-direction make it your "
            "own search rather than an inherited script, and pull you toward "
            "Self-Transcendence in aim.",
            "You bring depth and groundedness; you're rarely rattled by "
            "surface noise because you're oriented to something deeper. The "
            "tension is staying engaged with the ordinary, practical world, "
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
        "opposite": "achiever",
        "neighbors": ["guardian", "caregiver"],
    },
    {
        "key": "free_spirit",
        "name": "The Free Spirit",
        "emoji": "🦋",
        "tagline": "Living for joy, spontaneity, and the present",
        "two_truths": "You're the best night out anyone's had and the worst person to ask about the schedule.",
        "thriving": "You're pure aliveness, present and playful, the reason an ordinary evening turns into a story.",
        "empty": "You dodge anything dull or hard, chasing the next good feeling while the boring bits pile up.",
        "kryptonite": "A color-coded calendar and a room full of people taking themselves too seriously.",
        "green_flags": ["Makes everything more fun", "Fully present in the moment", "Gives you permission to lighten up"],
        "red_flags": ["Allergic to admin and follow-through", "Bolts when things get heavy", "Treats plans as loose suggestions"],
        "quick_stats": [
            {"label": "Fun", "level": 5},
            {"label": "Admin energy", "level": 1},
            {"label": "Living in the now", "level": 5},
        ],
        "portrait": [
            "You're here for the good stuff, right now. Play, pleasure, "
            "spontaneity: not guilty pleasures, just the point. You give "
            "everyone around you quiet permission to lighten up.",
            "Your joy is contagious and you're rarely the one sweating the "
            "schedule. The flip side: a little structure goes a long way, and "
            "the good times last longer when someone (occasionally you) "
            "handles the boring bits.",
        ],
        "recognize": [
            "You've said yes to the fun thing and dealt with the fallout later.",
            "A color-coded calendar feels like a tiny prison.",
            "You're often the reason the night got better.",
        ],
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
            "You live where hedonism meets stimulation, the most "
            "present-tense corner of the Openness-to-Change side. You're here "
            "for the experience of being alive: pleasure, play, novelty, the "
            "good moment as it happens. Plans and obligations are useful only "
            "insofar as they don't kill the spark.",
            "Your joy is contagious and you give others permission to "
            "lighten up. Directly opposite you on the circle sits the "
            "Guardian's world of duty and restraint, which is exactly your "
            "growth edge: a little structure and follow-through let the good "
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
        "neighbors": ["explorer", "achiever"],
    },
    {
        "key": "sovereign",
        "name": "The Sovereign",
        "emoji": "👑",
        "tagline": "Built to lead, to influence, and to call the shots",
        "two_truths": "You're the one everyone looks to in a crisis and the one who finds it hardest to ask for help.",
        "thriving": "You're decisive and commanding, turning a leaderless mess into a plan and a direction within minutes.",
        "empty": "You're domineering and guarded, mistaking control for respect and treating people like pieces on a board.",
        "kryptonite": "Being overlooked, sidelined, or told to wait your turn.",
        "green_flags": ["Takes charge when no one else will", "Says the hard thing out loud", "Fights for the people who follow them"],
        "red_flags": ["Has to be the one in control", "Keeps score of wins and slights", "Hard to be vulnerable with"],
        "quick_stats": [
            {"label": "Command", "level": 5},
            {"label": "Asking for help", "level": 1},
            {"label": "Drive", "level": 5},
        ],
        "portrait": [
            "You read a room for who actually holds the power, and you're "
            "comfortable being that person. You don't wait for permission or "
            "for your turn; you see the lever and you pull it. Status, "
            "influence, being the one who decides, that's oxygen to you.",
            "You'd rather be respected than liked, and you'll make the hard "
            "call nobody else wants to. The risk is forgetting that power is a "
            "tool, not a scoreboard, and that the people you lead are people, "
            "not pieces.",
        ],
        "recognize": [
            "You've ended up running the thing you only meant to join.",
            "You map the org chart of any room within five minutes.",
            "\"Who's in charge here?\" is a question you either ask or answer.",
        ],
        "schwartz": {"power": 0.7, "achievement": 0.3},
        "big_five_hint": "very high Extraversion with low Agreeableness",
        "axis_change": {
            "pole": "Balanced",
            "note": "Equally willing to shake things up or hold the line, whichever puts you in a stronger position.",
        },
        "axis_focus": {
            "pole": "Self-Enhancement",
            "note": "Power and standing drive you: influence, authority, and being the one who decides.",
        },
        "big_five_profile": [
            {"label": "Extraversion", "level": "very high"},
            {"label": "Conscientiousness", "level": "high"},
            {"label": "Agreeableness", "level": "lower"},
        ],
        "description": (
            "You're drawn to influence, authority, and the top of the pecking "
            "order. You lead by instinct and you're comfortable holding the "
            "power that others shy away from."
        ),
        "detail": [
            "You anchor the Self-Enhancement pole through power: status, "
            "authority, and control over outcomes, with achievement close "
            "behind. Where the Achiever wants to be the best at something, you "
            "want to be the one in charge of it. You read hierarchies clearly "
            "and you'd rather shape them than submit to them.",
            "On the change axis you're pragmatic, happy to disrupt or preserve "
            "depending on what strengthens your hand. That makes you formidable "
            "and decisive, but power sits directly opposite self-transcendence "
            "on the circle, so the growth work is keeping influence in service "
            "of something beyond your own standing, and letting people close "
            "enough to see you without the armour.",
        ],
        "strengths": [
            "Decisive and comfortable taking command",
            "Persuasive and hard to intimidate",
            "Willing to own responsibility and risk",
            "Protects and advances the people who follow them",
        ],
        "tensions": [
            "Can dominate or steamroll others",
            "Equates being in control with being safe",
            "Struggles to show weakness or ask for help",
        ],
        "opposite": "idealist",
        "neighbors": ["achiever", "provider"],
    },
    {
        "key": "provider",
        "name": "The Provider",
        "emoji": "🏠",
        "tagline": "Building a safe, stable foundation that holds",
        "two_truths": "You're the most prepared person anyone knows and the most reluctant to leave the safe option.",
        "thriving": "You're steady and prepared, the solid ground others build on, with a plan for the rainy day before it clouds over.",
        "empty": "You're anxious and defensive, treating every change as a threat and hoarding a security you never let yourself enjoy.",
        "kryptonite": "Sudden change, open-ended uncertainty, and being asked to bet the foundation.",
        "green_flags": ["Always has a backup and a buffer", "Steady when money or plans get shaky", "Quietly makes sure no one goes without"],
        "red_flags": ["Treats every risk as a threat", "Slow to try anything unproven", "Worries out loud about worst cases"],
        "quick_stats": [
            {"label": "Preparedness", "level": 5},
            {"label": "Risk appetite", "level": 1},
            {"label": "Stability", "level": 5},
        ],
        "portrait": [
            "You sleep better knowing the base is solid. A stocked pantry, "
            "money in the account, a plan for when things go sideways, that's "
            "not paranoia, it's peace of mind. You build the kind of stability "
            "other people get to take for granted.",
            "You're the one who reads the fine print and keeps the spare. The "
            "flip side: not every risk is a threat, and a life spent only "
            "defending the walls can forget to enjoy what's inside them.",
        ],
        "recognize": [
            "You have an emergency fund and an emergency plan.",
            "\"What's the catch?\" is your honest first reaction.",
            "A disrupted routine gives you a quiet sense of dread.",
        ],
        "schwartz": {"security": 0.8, "conformity": 0.2},
        "big_five_hint": "high Conscientiousness with lower Openness",
        "axis_change": {
            "pole": "Conservation",
            "note": "Stability and safety come first; you protect the foundation and treat the proven as precious.",
        },
        "axis_focus": {
            "pole": "Balanced",
            "note": "Not chasing status or applause; your effort goes into securing a solid base for yourself and your people.",
        },
        "big_five_profile": [
            {"label": "Conscientiousness", "level": "very high"},
            {"label": "Emotional Stability", "level": "moderate"},
            {"label": "Openness", "level": "lower"},
        ],
        "description": (
            "You build a safe, stable foundation and guard it well. Security, "
            "preparedness, and a dependable base for the people you're "
            "responsible for are what you organise your life around."
        ),
        "detail": [
            "You anchor the Conservation side of the circle through security: "
            "safety, stability, and a well-defended foundation, with a thread "
            "of conformity that keeps you doing things the proven way. Where "
            "the Guardian is led by duty and order, you're led by the need for "
            "a solid base: the savings, the backup, the margin that means a bad "
            "week doesn't become a disaster.",
            "On the focus axis you're balanced, neither chasing status nor "
            "giving yourself away; the point is a stable life, secured. That "
            "makes you the dependable foundation others build on, but security "
            "sits opposite openness on the circle, so the growth work is "
            "remembering that not every change is a threat, and that a "
            "foundation is meant to be lived on, not just defended.",
        ],
        "strengths": [
            "Prepared for whatever goes wrong",
            "Level-headed and steady about risk",
            "Builds lasting stability and security",
            "Quietly dependable when it counts",
        ],
        "tensions": [
            "Risk-averse to the point of missing out",
            "Slow to embrace change or the unproven",
            "Can mistake a safe life for a full one",
        ],
        "opposite": "connector",
        "neighbors": ["sovereign", "guardian"],
    },
]


def archetype_by_key(key: str) -> dict | None:
    for a in ARCHETYPES:
        if a["key"] == key:
            return a
    return None
