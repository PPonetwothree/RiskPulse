"""
Simulator: Generates realistic-looking geopolitical event data.
Used when real API keys are not configured.
"""

import random
import time
from datetime import datetime, timedelta


COUNTRIES = ['SY', 'UA', 'YE', 'SD', 'ET', 'AF', 'IQ', 'ML', 'MM', 'SO']

COUNTRY_NAMES = {
    'SY': 'SYRIA', 'UA': 'UKRAINE', 'YE': 'YEMEN', 'SD': 'SUDAN',
    'ET': 'ETHIOPIA', 'AF': 'AFGHANISTAN', 'IQ': 'IRAQ', 'ML': 'MALI',
    'MM': 'MYANMAR', 'SO': 'SOMALIA'
}

LOCATIONS = {
    'SY': ['DAMASCUS', 'ALEPPO', 'IDLIB', 'HOMS', 'RAQQA'],
    'UA': ['KYIV', 'KHARKIV', 'MARIUPOL', 'DONETSK', 'KHERSON'],
    'YE': ['SANAA', 'ADEN', 'HODEIDAH', 'MARIB', 'TAIZ'],
    'SD': ['KHARTOUM', 'DARFUR', 'PORT-SUDAN', 'KASSALA'],
    'ET': ['ADDIS-ABEBA', 'TIGRAY', 'AMHARA', 'OROMIA'],
    'AF': ['KABUL', 'KANDAHAR', 'HERAT', 'KUNDUZ'],
    'IQ': ['BAGHDAD', 'MOSUL', 'BASRA', 'FALLUJA'],
    'ML': ['BAMAKO', 'TIMBUKTU', 'GAO', 'KIDAL'],
    'MM': ['YANGON', 'MANDALAY', 'SAGAING', 'KAYAH'],
    'SO': ['MOGADISHU', 'BAIDOA', 'KISMAAYO', 'GAROWE'],
}

GDELT_EVENT_TYPES = [
    'ARMED_ATTACK', 'PROTEST', 'POLITICAL_TENSION', 'CEASEFIRE',
    'DIPLOMATIC_MEETING', 'MILITARY_OPERATION', 'RIOT', 'SABOTAGE',
    'EXPLOSION', 'SEIZURE', 'BLOCKADE', 'MASS_DISPLACEMENT'
]

ACLED_EVENT_TYPES = [
    'BATTLES', 'VIOLENCE_CIVILIANS', 'EXPLOSIONS', 'PROTESTS',
    'STRATEGIC_DEVELOPMENTS', 'RIOTS'
]

REDDIT_SUBREDDITS = [
    'r/geopolitics', 'r/worldnews', 'r/GlobalConflict',
    'r/CredibleDefense', 'r/UkrainianConflict'
]

SUMMARIES_TEMPLATES = {
    'GDELT': [
        'ARMED_CLASH REPORTED IN {loc}',
        'MILITARY_MOVEMENT DETECTED NEAR {loc}',
        'PROTEST_OUTBREAK IN {loc} DISTRICT',
        'CEASEFIRE_VIOLATION REPORTED AT {loc}',
        'EXPLOSION NEAR {loc} MARKET',
        'DIPLOMATIC_TALKS STALLED OVER {loc}',
        'SIEGE_CONDITIONS IN {loc} SECTOR',
        'ARTILLERY_EXCHANGE ALONG {loc} FRONT',
        'MASS_DISPLACEMENT FROM {loc} REGION',
        'POLITICAL_CRISIS DEEPENS IN {loc}',
    ],
    'ACLED': [
        'BATTLE_ENGAGEMENT: ARMED_GROUP vs GOVERNMENT FORCES AT {loc}',
        'CIVILIAN_FATALITIES: AIRSTRIKE HIT {loc}',
        'IED_EXPLOSION: ROADSIDE_DEVICE DETONATED NEAR {loc}',
        'PROTEST_TURNED_VIOLENT IN {loc} CENTRAL',
        'STRATEGIC_POINT CAPTURED AT {loc}',
        'SHELLING REPORTED IN {loc} SUBURBS',
        'EXECUTION_REPORTED NEAR {loc}',
    ],
    'Reddit': [
        '[{sub}] SITUATION DETERIORATING IN {loc} — THREAD',
        '[{sub}] ANALYSIS: ESCALATION RISK AT {loc}',
        '[{sub}] BREAKING: CONFLICT UPDATE FROM {loc}',
        '[{sub}] HUMANITARIAN_CRISIS DEEPENING IN {loc}',
        '[{sub}] GEOPOLITICAL_SHIFT: {loc} DEVELOPMENTS',
    ]
}

# Country-level base risk (0-1) for more realistic simulation
COUNTRY_BASE_RISK = {
    'SY': 0.85, 'UA': 0.82, 'YE': 0.78, 'SD': 0.72, 'ET': 0.68,
    'AF': 0.75, 'IQ': 0.60, 'ML': 0.65, 'MM': 0.70, 'SO': 0.73,
}


def _sentiment_for_country(country_code):
    """Generate a sentiment score biased by country's base risk."""
    base = COUNTRY_BASE_RISK.get(country_code, 0.5)
    # Higher risk → more negative sentiment (lower score)
    center = 1.0 - base  # [0.15 .. 0.55]
    return max(0.0, min(1.0, center + random.gauss(0, 0.12)))


def _severity_for_type(event_type):
    high_severity = {'ARMED_ATTACK', 'BATTLE_ENGAGEMENT', 'CIVILIAN_FATALITIES',
                     'EXPLOSION', 'BATTLES', 'SHELLING'}
    medium_severity = {'PROTEST', 'RIOT', 'SIEGE_CONDITIONS', 'MASS_DISPLACEMENT'}
    if any(h in event_type for h in high_severity):
        return 'critical' if random.random() < 0.3 else 'high'
    elif any(m in event_type for m in medium_severity):
        return 'medium'
    return random.choice(['low', 'medium', 'medium'])


def generate_gdelt_events(count=None):
    """Generate simulated GDELT events."""
    if count is None:
        count = random.randint(8, 25)

    events = []
    for _ in range(count):
        country = random.choices(
            COUNTRIES,
            weights=[COUNTRY_BASE_RISK[c] * 100 for c in COUNTRIES]
        )[0]
        event_type = random.choice(GDELT_EVENT_TYPES)
        loc = random.choice(LOCATIONS[country])
        template = random.choice(SUMMARIES_TEMPLATES['GDELT'])
        summary = template.format(loc=loc)
        fatalities = 0
        if 'ATTACK' in event_type or 'EXPLOSION' in event_type:
            fatalities = int(random.expovariate(0.3))

        events.append({
            'source': 'GDELT',
            'event_type': event_type,
            'country': country,
            'location': loc,
            'summary': summary,
            'severity': _severity_for_type(event_type),
            'fatalities': fatalities,
            'sentiment_score': _sentiment_for_country(country),
        })
    return events


def generate_acled_events(count=None):
    """Generate simulated ACLED events."""
    if count is None:
        count = random.randint(3, 12)

    events = []
    for _ in range(count):
        country = random.choices(
            COUNTRIES,
            weights=[COUNTRY_BASE_RISK[c] * 100 for c in COUNTRIES]
        )[0]
        event_type = random.choice(ACLED_EVENT_TYPES)
        loc = random.choice(LOCATIONS[country])
        template = random.choice(SUMMARIES_TEMPLATES['ACLED'])
        summary = template.format(loc=loc)
        fatalities = 0
        if 'FATALITIES' in event_type or 'BATTLE' in event_type:
            fatalities = int(random.expovariate(0.2))

        events.append({
            'source': 'ACLED',
            'event_type': event_type,
            'country': country,
            'location': loc,
            'summary': summary,
            'severity': _severity_for_type(event_type),
            'fatalities': fatalities,
            'sentiment_score': _sentiment_for_country(country) - 0.05,
        })
    return events


def generate_reddit_posts(count=None):
    """Generate simulated Reddit posts."""
    if count is None:
        count = random.randint(4, 10)

    posts = []
    for _ in range(count):
        country = random.choice(COUNTRIES)
        loc = random.choice(LOCATIONS[country])
        sub = random.choice(REDDIT_SUBREDDITS)
        template = random.choice(SUMMARIES_TEMPLATES['Reddit'])
        summary = template.format(loc=loc, sub=sub)

        posts.append({
            'source': 'Reddit',
            'event_type': 'SOCIAL_POST',
            'country': country,
            'location': loc,
            'summary': summary,
            'severity': 'low',
            'sentiment_score': _sentiment_for_country(country) + random.gauss(0, 0.08),
        })
    return posts


def generate_historical_series(country_code, days=90):
    """
    Generate a 90-day event count time series for a country.
    Used by the forecaster agent.
    """
    base = COUNTRY_BASE_RISK.get(country_code, 0.5)
    base_count = int(base * 30)  # 0-30 events/day at baseline

    series = []
    trend = 0.0
    for i in range(days):
        # Add slow trend + noise + weekly seasonality
        trend += random.gauss(0.02, 0.1)
        weekly = 3 * (1 if i % 7 < 5 else -1)  # lower on weekends
        noise = random.gauss(0, 3)
        count = max(1, base_count + int(trend) + int(weekly) + int(noise))
        series.append(count)

    return series
