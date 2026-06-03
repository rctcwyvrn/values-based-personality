"""Values list based on the Acceptance and Commitment Therapy (ACT) framework,
each tagged with how it loads onto two personality frameworks.

In ACT, values are freely chosen life directions — qualities of ongoing action
rather than goals to be achieved. Here each value also carries:

  * ``schwartz`` — loadings on the 10 Schwartz basic human values. These are
    arranged on a circumplex by two axes (Openness-to-Change <-> Conservation,
    Self-Enhancement <-> Self-Transcendence) and form the geometric engine for
    classification.

  * ``big_five`` — loadings on the Big Five (OCEAN), using emotional_stability
    in place of neuroticism so every dimension points in a desirable direction.
    These provide the lay-legible language of the final readout.

Each loading dict's weights are non-negative and sum to 1.0, so each value
contributes one unit of "emphasis" spread across the dimensions it expresses.
The set is curated so emphasis is spread reasonably evenly across all ten
Schwartz values and all five Big Five traits, rather than piling onto the
prosocial cluster that dominates raw ACT value lists.

Schwartz keys: self_direction, stimulation, hedonism, achievement, power,
               security, conformity, tradition, benevolence, universalism
Big Five keys: openness, conscientiousness, extraversion, agreeableness,
               emotional_stability
"""

VALUES = [
    {
        "name": "Acceptance",
        "description": "Being open to and making room for experience as it is, rather than fighting it",
        "schwartz": {"universalism": 0.5, "tradition": 0.5},
        "big_five": {"emotional_stability": 0.6, "openness": 0.4},
    },
    {
        "name": "Adventure",
        "description": "Seeking out, creating, or exploring novel and stimulating experiences",
        "schwartz": {"stimulation": 0.8, "self_direction": 0.2},
        "big_five": {"openness": 0.6, "extraversion": 0.4},
    },
    {
        "name": "Ambition",
        "description": "Striving with drive toward meaningful accomplishment and advancement",
        "schwartz": {"achievement": 0.6, "power": 0.4},
        "big_five": {"conscientiousness": 0.5, "extraversion": 0.5},
    },
    {
        "name": "Assertiveness",
        "description": "Standing up respectfully for what I need and what I believe in",
        "schwartz": {"power": 0.5, "self_direction": 0.3, "achievement": 0.2},
        "big_five": {"extraversion": 0.8, "conscientiousness": 0.2},
    },
    {
        "name": "Authenticity",
        "description": "Being genuine and true to myself rather than putting on a front",
        "schwartz": {"self_direction": 0.8, "hedonism": 0.2},
        "big_five": {"openness": 0.5, "emotional_stability": 0.3, "extraversion": 0.2},
    },
    {
        "name": "Authority",
        "description": "Taking and exercising legitimate responsibility and command",
        "schwartz": {"power": 0.8, "conformity": 0.2},
        "big_five": {"extraversion": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Beauty",
        "description": "Appreciating, creating, and nurturing beauty in myself and the world",
        "schwartz": {"universalism": 0.7, "self_direction": 0.3},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Belonging",
        "description": "Building and feeling part of a group, place, or community",
        "schwartz": {"security": 0.5, "benevolence": 0.3, "conformity": 0.2},
        "big_five": {"agreeableness": 0.6, "extraversion": 0.4},
    },
    {
        "name": "Boldness",
        "description": "Acting daringly and stepping forward where others hesitate",
        "schwartz": {"stimulation": 0.5, "power": 0.3, "self_direction": 0.2},
        "big_five": {"extraversion": 0.6, "emotional_stability": 0.4},
    },
    {
        "name": "Calm",
        "description": "Maintaining an unhurried, settled state of mind",
        "schwartz": {"security": 0.5, "universalism": 0.5},
        "big_five": {"emotional_stability": 0.9, "agreeableness": 0.1},
    },
    {
        "name": "Challenge",
        "description": "Stretching myself to grow, learn, and improve",
        "schwartz": {"achievement": 0.5, "stimulation": 0.5},
        "big_five": {"openness": 0.5, "conscientiousness": 0.3, "extraversion": 0.2},
    },
    {
        "name": "Charisma",
        "description": "Drawing and energizing others through personal presence",
        "schwartz": {"power": 0.5, "hedonism": 0.5},
        "big_five": {"extraversion": 0.9, "openness": 0.1},
    },
    {
        "name": "Compassion",
        "description": "Acting with kindness toward those who are suffering",
        "schwartz": {"benevolence": 0.5, "universalism": 0.5},
        "big_five": {"agreeableness": 1.0},
    },
    {
        "name": "Connection",
        "description": "Engaging fully and warmly with whoever I am with",
        "schwartz": {"benevolence": 0.7, "hedonism": 0.3},
        "big_five": {"agreeableness": 0.5, "extraversion": 0.5},
    },
    {
        "name": "Contentment",
        "description": "Resting in satisfaction with what I have and who I am",
        "schwartz": {"security": 0.4, "hedonism": 0.4, "tradition": 0.2},
        "big_five": {"emotional_stability": 0.8, "agreeableness": 0.2},
    },
    {
        "name": "Cooperation",
        "description": "Working collaboratively and considerately with others",
        "schwartz": {"benevolence": 0.5, "conformity": 0.5},
        "big_five": {"agreeableness": 0.8, "conscientiousness": 0.2},
    },
    {
        "name": "Courage",
        "description": "Acting on what matters even in the presence of fear",
        "schwartz": {"self_direction": 0.5, "stimulation": 0.3, "achievement": 0.2},
        "big_five": {"emotional_stability": 0.5, "extraversion": 0.3, "openness": 0.2},
    },
    {
        "name": "Creativity",
        "description": "Bringing imagination and originality to what I do",
        "schwartz": {"self_direction": 0.8, "stimulation": 0.2},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Curiosity",
        "description": "Being open, interested, and eager to explore and discover",
        "schwartz": {"self_direction": 0.5, "stimulation": 0.5},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Daring",
        "description": "Embracing risk and venturing beyond the safe and certain",
        "schwartz": {"stimulation": 0.6, "power": 0.4},
        "big_five": {"extraversion": 0.6, "openness": 0.4},
    },
    {
        "name": "Dependability",
        "description": "Being someone others can count on",
        "schwartz": {"security": 0.4, "conformity": 0.4, "benevolence": 0.2},
        "big_five": {"conscientiousness": 0.8, "agreeableness": 0.2},
    },
    {
        "name": "Discipline",
        "description": "Following through on what I set out to do",
        "schwartz": {"conformity": 0.5, "achievement": 0.5},
        "big_five": {"conscientiousness": 1.0},
    },
    {
        "name": "Diversity",
        "description": "Valuing and welcoming difference and variety",
        "schwartz": {"universalism": 1.0},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Duty",
        "description": "Fulfilling my obligations and doing what is required of me",
        "schwartz": {"conformity": 0.5, "security": 0.3, "benevolence": 0.2},
        "big_five": {"conscientiousness": 0.8, "agreeableness": 0.2},
    },
    {
        "name": "Empathy",
        "description": "Understanding and sharing the feelings of others",
        "schwartz": {"benevolence": 0.5, "universalism": 0.5},
        "big_five": {"agreeableness": 0.8, "openness": 0.2},
    },
    {
        "name": "Enthusiasm",
        "description": "Bringing eager, animated energy to what I pursue",
        "schwartz": {"stimulation": 0.5, "achievement": 0.5},
        "big_five": {"extraversion": 0.7, "emotional_stability": 0.3},
    },
    {
        "name": "Equality",
        "description": "Treating people as equally deserving of dignity and opportunity",
        "schwartz": {"universalism": 1.0},
        "big_five": {"agreeableness": 0.6, "openness": 0.4},
    },
    {
        "name": "Equanimity",
        "description": "Staying balanced and steady through life's ups and downs",
        "schwartz": {"tradition": 0.4, "security": 0.3, "universalism": 0.3},
        "big_five": {"emotional_stability": 0.9, "openness": 0.1},
    },
    {
        "name": "Excellence",
        "description": "Holding myself to a high standard of quality in what I do",
        "schwartz": {"achievement": 0.8, "conformity": 0.2},
        "big_five": {"conscientiousness": 0.8, "openness": 0.2},
    },
    {
        "name": "Excitement",
        "description": "Pursuing and embracing thrilling, energizing experiences",
        "schwartz": {"stimulation": 0.7, "hedonism": 0.3},
        "big_five": {"extraversion": 0.6, "openness": 0.4},
    },
    {
        "name": "Fairness",
        "description": "Acting justly and even-handedly toward all",
        "schwartz": {"universalism": 0.8, "benevolence": 0.2},
        "big_five": {"agreeableness": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Faith",
        "description": "Trusting in something larger than myself",
        "schwartz": {"tradition": 1.0},
        "big_five": {"emotional_stability": 0.5, "conscientiousness": 0.3, "agreeableness": 0.2},
    },
    {
        "name": "Fitness",
        "description": "Maintaining and improving my physical health and strength",
        "schwartz": {"achievement": 0.4, "security": 0.3, "hedonism": 0.3},
        "big_five": {"conscientiousness": 0.7, "extraversion": 0.3},
    },
    {
        "name": "Flexibility",
        "description": "Adapting and adjusting readily to changing circumstances",
        "schwartz": {"self_direction": 0.5, "stimulation": 0.5},
        "big_five": {"openness": 0.7, "agreeableness": 0.3},
    },
    {
        "name": "Forgiveness",
        "description": "Letting go of resentment toward myself and others",
        "schwartz": {"benevolence": 0.6, "universalism": 0.4},
        "big_five": {"agreeableness": 0.7, "emotional_stability": 0.3},
    },
    {
        "name": "Freedom",
        "description": "Living and choosing without unnecessary constraint",
        "schwartz": {"self_direction": 1.0},
        "big_five": {"openness": 0.7, "extraversion": 0.3},
    },
    {
        "name": "Frugality",
        "description": "Living thriftily and making careful, deliberate use of resources",
        "schwartz": {"conformity": 0.4, "security": 0.4, "tradition": 0.2},
        "big_five": {"conscientiousness": 0.8, "emotional_stability": 0.2},
    },
    {
        "name": "Fun",
        "description": "Seeking out and creating enjoyment and play",
        "schwartz": {"hedonism": 0.8, "stimulation": 0.2},
        "big_five": {"extraversion": 0.6, "openness": 0.4},
    },
    {
        "name": "Generosity",
        "description": "Giving freely of my time, energy, and resources",
        "schwartz": {"benevolence": 0.7, "universalism": 0.3},
        "big_five": {"agreeableness": 1.0},
    },
    {
        "name": "Gratitude",
        "description": "Noticing and appreciating the good in my life",
        "schwartz": {"benevolence": 0.4, "tradition": 0.4, "universalism": 0.2},
        "big_five": {"agreeableness": 0.5, "emotional_stability": 0.5},
    },
    {
        "name": "Growth",
        "description": "Continually developing and expanding as a person",
        "schwartz": {"self_direction": 0.6, "achievement": 0.4},
        "big_five": {"openness": 0.7, "conscientiousness": 0.3},
    },
    {
        "name": "Harmony",
        "description": "Cultivating balance and peace within myself and my relationships",
        "schwartz": {"universalism": 0.4, "security": 0.4, "conformity": 0.2},
        "big_five": {"agreeableness": 0.5, "emotional_stability": 0.5},
    },
    {
        "name": "Heritage",
        "description": "Honoring and carrying forward where I come from",
        "schwartz": {"tradition": 0.6, "security": 0.4},
        "big_five": {"conscientiousness": 0.5, "agreeableness": 0.5},
    },
    {
        "name": "Honesty",
        "description": "Being truthful and sincere in what I say and do",
        "schwartz": {"benevolence": 0.5, "universalism": 0.3, "self_direction": 0.2},
        "big_five": {"conscientiousness": 0.5, "agreeableness": 0.5},
    },
    {
        "name": "Honor",
        "description": "Upholding my principles and earning a good name",
        "schwartz": {"tradition": 0.4, "conformity": 0.3, "power": 0.3},
        "big_five": {"conscientiousness": 0.6, "agreeableness": 0.4},
    },
    {
        "name": "Hope",
        "description": "Holding on to a sense of possibility and a better future",
        "schwartz": {"benevolence": 0.4, "security": 0.3, "tradition": 0.3},
        "big_five": {"emotional_stability": 0.7, "openness": 0.3},
    },
    {
        "name": "Humility",
        "description": "Staying modest and open about my limits and what I can learn",
        "schwartz": {"tradition": 0.6, "benevolence": 0.4},
        "big_five": {"agreeableness": 0.6, "emotional_stability": 0.4},
    },
    {
        "name": "Humor",
        "description": "Bringing lightness and laughter to life",
        "schwartz": {"hedonism": 0.7, "stimulation": 0.3},
        "big_five": {"extraversion": 0.5, "openness": 0.5},
    },
    {
        "name": "Independence",
        "description": "Relying on and thinking for myself",
        "schwartz": {"self_direction": 1.0},
        "big_five": {"openness": 0.5, "conscientiousness": 0.3, "extraversion": 0.2},
    },
    {
        "name": "Industry",
        "description": "Working diligently and applying myself with effort",
        "schwartz": {"achievement": 0.7, "conformity": 0.3},
        "big_five": {"conscientiousness": 1.0},
    },
    {
        "name": "Influence",
        "description": "Shaping outcomes and moving others toward what matters",
        "schwartz": {"power": 0.7, "achievement": 0.3},
        "big_five": {"extraversion": 0.7, "conscientiousness": 0.3},
    },
    {
        "name": "Integrity",
        "description": "Living in line with my values and being honest with myself",
        "schwartz": {"self_direction": 0.4, "benevolence": 0.3, "universalism": 0.3},
        "big_five": {"conscientiousness": 0.5, "agreeableness": 0.5},
    },
    {
        "name": "Justice",
        "description": "Standing up for what is right and fair",
        "schwartz": {"universalism": 1.0},
        "big_five": {"agreeableness": 0.5, "conscientiousness": 0.5},
    },
    {
        "name": "Kindness",
        "description": "Being considerate, gentle, and caring toward others",
        "schwartz": {"benevolence": 1.0},
        "big_five": {"agreeableness": 1.0},
    },
    {
        "name": "Leadership",
        "description": "Guiding, motivating, and bringing out the best in others",
        "schwartz": {"power": 0.6, "achievement": 0.4},
        "big_five": {"extraversion": 0.7, "conscientiousness": 0.3},
    },
    {
        "name": "Learning",
        "description": "Continually acquiring new skills and understanding",
        "schwartz": {"self_direction": 0.6, "achievement": 0.4},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Loyalty",
        "description": "Being faithful and steadfast to the people and causes I value",
        "schwartz": {"benevolence": 0.6, "tradition": 0.2, "conformity": 0.2},
        "big_five": {"agreeableness": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Mastery",
        "description": "Pursuing deep competence and command of a craft",
        "schwartz": {"achievement": 0.7, "power": 0.3},
        "big_five": {"conscientiousness": 0.6, "openness": 0.4},
    },
    {
        "name": "Mindfulness",
        "description": "Being present and aware of the here and now without judgment",
        "schwartz": {"universalism": 0.4, "self_direction": 0.3, "tradition": 0.3},
        "big_five": {"emotional_stability": 0.7, "openness": 0.3},
    },
    {
        "name": "Openness",
        "description": "Being receptive to new experiences, feelings, and information",
        "schwartz": {"self_direction": 0.5, "stimulation": 0.3, "universalism": 0.2},
        "big_five": {"openness": 1.0},
    },
    {
        "name": "Order",
        "description": "Creating and maintaining structure and organization",
        "schwartz": {"security": 0.5, "conformity": 0.5},
        "big_five": {"conscientiousness": 1.0},
    },
    {
        "name": "Patience",
        "description": "Waiting calmly and persisting without frustration",
        "schwartz": {"conformity": 0.4, "benevolence": 0.3, "tradition": 0.3},
        "big_five": {"emotional_stability": 0.7, "agreeableness": 0.3},
    },
    {
        "name": "Peace",
        "description": "Cultivating calm and tranquility within and around me",
        "schwartz": {"universalism": 0.5, "security": 0.5},
        "big_five": {"emotional_stability": 0.7, "agreeableness": 0.3},
    },
    {
        "name": "Persistence",
        "description": "Continuing on despite difficulties and setbacks",
        "schwartz": {"achievement": 0.7, "conformity": 0.3},
        "big_five": {"conscientiousness": 0.8, "emotional_stability": 0.2},
    },
    {
        "name": "Playfulness",
        "description": "Approaching life with lightness, spontaneity, and fun",
        "schwartz": {"hedonism": 0.6, "stimulation": 0.4},
        "big_five": {"extraversion": 0.5, "openness": 0.5},
    },
    {
        "name": "Pleasure",
        "description": "Embracing and enjoying the good feelings life offers",
        "schwartz": {"hedonism": 1.0},
        "big_five": {"extraversion": 0.5, "openness": 0.5},
    },
    {
        "name": "Power",
        "description": "Acting effectively and having a meaningful influence",
        "schwartz": {"power": 1.0},
        "big_five": {"extraversion": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Presence",
        "description": "Showing up fully engaged in the moment",
        "schwartz": {"tradition": 0.4, "self_direction": 0.3, "universalism": 0.3},
        "big_five": {"emotional_stability": 0.6, "openness": 0.4},
    },
    {
        "name": "Prudence",
        "description": "Acting with care, foresight, and good practical judgment",
        "schwartz": {"conformity": 0.4, "security": 0.4, "self_direction": 0.2},
        "big_five": {"conscientiousness": 0.7, "emotional_stability": 0.3},
    },
    {
        "name": "Reciprocity",
        "description": "Giving and receiving in fair, mutual exchange",
        "schwartz": {"benevolence": 0.5, "conformity": 0.3, "security": 0.2},
        "big_five": {"agreeableness": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Recognition",
        "description": "Earning acknowledgment and respect for my contributions",
        "schwartz": {"power": 0.5, "achievement": 0.5},
        "big_five": {"extraversion": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Reliability",
        "description": "Doing consistently what I say I will do",
        "schwartz": {"security": 0.4, "conformity": 0.4, "benevolence": 0.2},
        "big_five": {"conscientiousness": 0.9, "agreeableness": 0.1},
    },
    {
        "name": "Resilience",
        "description": "Recovering and carrying on in the face of hardship",
        "schwartz": {"security": 0.4, "achievement": 0.3, "self_direction": 0.3},
        "big_five": {"emotional_stability": 0.8, "conscientiousness": 0.2},
    },
    {
        "name": "Respect",
        "description": "Treating myself and others with consideration and regard",
        "schwartz": {"conformity": 0.4, "benevolence": 0.3, "universalism": 0.3},
        "big_five": {"agreeableness": 0.7, "conscientiousness": 0.3},
    },
    {
        "name": "Responsibility",
        "description": "Owning my actions and their consequences",
        "schwartz": {"conformity": 0.4, "security": 0.3, "benevolence": 0.3},
        "big_five": {"conscientiousness": 0.9, "agreeableness": 0.1},
    },
    {
        "name": "Romance",
        "description": "Expressing and nurturing love and affection",
        "schwartz": {"hedonism": 0.6, "benevolence": 0.2, "stimulation": 0.2},
        "big_five": {"extraversion": 0.5, "agreeableness": 0.3, "openness": 0.2},
    },
    {
        "name": "Safety",
        "description": "Protecting and securing myself and those I care about",
        "schwartz": {"security": 1.0},
        "big_five": {"conscientiousness": 0.5, "emotional_stability": 0.5},
    },
    {
        "name": "Self-care",
        "description": "Tending to my own needs and well-being",
        "schwartz": {"hedonism": 0.4, "security": 0.4, "self_direction": 0.2},
        "big_five": {"emotional_stability": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Self-compassion",
        "description": "Treating myself with kindness in moments of difficulty",
        "schwartz": {"benevolence": 0.4, "security": 0.3, "hedonism": 0.3},
        "big_five": {"emotional_stability": 0.8, "agreeableness": 0.2},
    },
    {
        "name": "Self-control",
        "description": "Acting deliberately rather than on impulse",
        "schwartz": {"conformity": 0.6, "security": 0.2, "tradition": 0.2},
        "big_five": {"conscientiousness": 0.7, "emotional_stability": 0.3},
    },
    {
        "name": "Self-expression",
        "description": "Sharing my thoughts, feelings, and identity openly",
        "schwartz": {"self_direction": 0.7, "stimulation": 0.3},
        "big_five": {"openness": 0.7, "extraversion": 0.3},
    },
    {
        "name": "Sensuality",
        "description": "Enjoying and attending to the experience of my senses",
        "schwartz": {"hedonism": 1.0},
        "big_five": {"openness": 0.5, "extraversion": 0.5},
    },
    {
        "name": "Service",
        "description": "Devoting myself to helping and benefiting others",
        "schwartz": {"benevolence": 0.6, "universalism": 0.4},
        "big_five": {"agreeableness": 0.8, "conscientiousness": 0.2},
    },
    {
        "name": "Sexuality",
        "description": "Honoring and expressing my sexual self",
        "schwartz": {"hedonism": 0.8, "stimulation": 0.2},
        "big_five": {"extraversion": 0.5, "openness": 0.5},
    },
    {
        "name": "Simplicity",
        "description": "Living in an uncluttered, unpretentious way",
        "schwartz": {"tradition": 0.5, "universalism": 0.3, "security": 0.2},
        "big_five": {"conscientiousness": 0.4, "emotional_stability": 0.4, "openness": 0.2},
    },
    {
        "name": "Skillfulness",
        "description": "Doing things well and developing competence",
        "schwartz": {"achievement": 1.0},
        "big_five": {"conscientiousness": 0.7, "openness": 0.3},
    },
    {
        "name": "Solitude",
        "description": "Valuing and seeking out time alone with myself",
        "schwartz": {"self_direction": 0.7, "tradition": 0.3},
        "big_five": {"openness": 0.5, "emotional_stability": 0.5},
    },
    {
        "name": "Spirituality",
        "description": "Connecting with something larger or sacred",
        "schwartz": {"tradition": 0.7, "universalism": 0.3},
        "big_five": {"openness": 0.6, "emotional_stability": 0.4},
    },
    {
        "name": "Spontaneity",
        "description": "Acting freely and naturally in the moment",
        "schwartz": {"stimulation": 0.6, "hedonism": 0.4},
        "big_five": {"openness": 0.5, "extraversion": 0.5},
    },
    {
        "name": "Stability",
        "description": "Building steadiness and security in my life",
        "schwartz": {"security": 1.0},
        "big_five": {"conscientiousness": 0.5, "emotional_stability": 0.5},
    },
    {
        "name": "Status",
        "description": "Attaining and holding a respected standing among others",
        "schwartz": {"power": 0.7, "achievement": 0.3},
        "big_five": {"extraversion": 0.6, "conscientiousness": 0.4},
    },
    {
        "name": "Stewardship",
        "description": "Caring responsibly for what is entrusted to me",
        "schwartz": {"universalism": 0.5, "benevolence": 0.3, "conformity": 0.2},
        "big_five": {"conscientiousness": 0.6, "agreeableness": 0.4},
    },
    {
        "name": "Strength",
        "description": "Drawing on my inner and outer power to meet life",
        "schwartz": {"power": 0.4, "achievement": 0.4, "security": 0.2},
        "big_five": {"emotional_stability": 0.5, "conscientiousness": 0.3, "extraversion": 0.2},
    },
    {
        "name": "Tradition",
        "description": "Honoring the customs, heritage, and practices I have inherited",
        "schwartz": {"tradition": 1.0},
        "big_five": {"conscientiousness": 0.6, "agreeableness": 0.4},
    },
    {
        "name": "Trust",
        "description": "Having and extending faith in myself and others",
        "schwartz": {"benevolence": 0.5, "security": 0.3, "conformity": 0.2},
        "big_five": {"agreeableness": 0.6, "emotional_stability": 0.4},
    },
    {
        "name": "Trustworthiness",
        "description": "Being someone whom others can rely on and confide in",
        "schwartz": {"benevolence": 0.4, "conformity": 0.4, "security": 0.2},
        "big_five": {"conscientiousness": 0.6, "agreeableness": 0.4},
    },
    {
        "name": "Vitality",
        "description": "Living with energy, aliveness, and enthusiasm",
        "schwartz": {"stimulation": 0.4, "hedonism": 0.4, "achievement": 0.2},
        "big_five": {"extraversion": 0.6, "emotional_stability": 0.4},
    },
    {
        "name": "Warmth",
        "description": "Relating to others with affection and friendliness",
        "schwartz": {"benevolence": 0.7, "hedonism": 0.3},
        "big_five": {"agreeableness": 0.6, "extraversion": 0.4},
    },
    {
        "name": "Wisdom",
        "description": "Applying knowledge and experience with good judgment",
        "schwartz": {"universalism": 0.6, "self_direction": 0.4},
        "big_five": {"openness": 0.7, "conscientiousness": 0.3},
    },
    {
        "name": "Zeal",
        "description": "Bringing passion and wholehearted energy to what I do",
        "schwartz": {"achievement": 0.5, "stimulation": 0.5},
        "big_five": {"extraversion": 0.6, "conscientiousness": 0.4},
    },
]
