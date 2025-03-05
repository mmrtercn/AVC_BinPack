# profiles_db.py

# Profil veritabanı: {Article Code: Profile Name}
profiles_db = {
    "PRG070WCE001": "VS1N",
    "PRG080WCE001": "VS1",
    "PRG080WCE002": "VS3",
    "PRGXXXWCE001": "S12N",
    "PRG020WWA001": "VF3",
    "PRG070WWA001": "VF4",
    "PRG070WWA002": "SW3",
    "PRG080WWA001": "C21",
    "PRG080WWA002": "SW2",
    "PRGXXXWWA001": "SW5",
    "PRGXXXWWA005": "C3",
    "PRG070WCO001": "V19",
    "PRG070WCO002": "V21",
    "PRG070WCO003": "V28",
    "PRG070WCO004": "V18",
    "PRG070WCO005": "V11G",
    "PRG070WCO006": "V20",
    "PRG080WCO001": "V1",
    "PRG080WCO002": "V8",
    "PRGXXXWCO003": "V30",
    "PRG070WTR001": "S17",
    "PRG070WGA001": "S18",
    "PRG070WGA002": "S19",
    "PRG080WGA001": "S13",
    "PRGXXXWGA007": "V32",
    "PRGXXXWGA008": "V33",
    "PRGXXXWGA013": "S14",
    "PRGXXXWGA014": "S15N",
    "PRGXXXWRP002": "S09",
    "PRD080DAP100": "RP",
    "PRK070DAP100": "RPW",
    "PRS100WWA001": "S100B",
    "PRD100DAP100": "S100C",
    "PRSXXXWWA001": "S70B"
}

def get_profiles():
    """
    Veritabanındaki tüm profillerin listesini döndürür.
    :return: [(Article Code, Profile Name), ...]
    """
    return list(profiles_db.items())

def get_profile_names():
    """
    Sadece profil isimlerini döndürür (arayüzde gösterim için).
    :return: [Profile Name, ...]
    """
    return list(profiles_db.values())
