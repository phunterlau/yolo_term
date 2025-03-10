#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Headlines module for Yolo Terminal game.
Contains a collection of hilarious news headlines to display at the bottom of the interface.
"""

import random
from colorama import Fore

# Collection of hilarious news headlines (each within 70 chars)
HEADLINES = [
    # Original headlines (shortened if needed)
    "Man sues himself and wins; doesn't know whether to pay or collect",
    "Scientists confirm talking to plants helps; plants still not responding",
    "Local baker creates bread that doesn't go stale; scientists baffled",
    "Study: Money can't buy happiness, but it can rent it indefinitely",
    "Man breaks record for most records broken; record keepers confused",
    "Area dog learns to use toilet; cat plotting revenge",
    "New diet: Eat whatever you want, but only while standing on one leg",
    "Psychic wins lottery; claims 'total surprise'",
    "Man finds 20-year-old wallet; money inside now worthless",
    "Scientists name new element 'Surprisium'; no one saw it coming",
    "World's oldest person dies; title now held by someone else",
    "Study: People who say 'literally' don't know what it means",
    "Man with 'YOLO' tattoo lives very cautious life",
    "Woman finds pearl in oyster; restaurant still charges full price",
    "Meteorologists achieve 100% accuracy by saying 'it might rain'",
    "Conspiracy theorists debate if they themselves exist",
    "Study: Procrastination beneficial; details coming next year",
    "Man accidentally completes marathon while looking for bathroom",
    "Cat elected mayor; promises more naps for all",
    "Study: Looking at cute animal pictures increases productivity",
    "Man finally uses last bit of shampoo and conditioner at same time",
    "Coffee drinkers live longer, sleep less, and twitch more",
    "Restaurant's 'pay what you weigh' promotion loses money instantly",
    "Man builds time machine; warns past self it won't work",
    "Research: Chocolate officially a vegetable; nation rejoices",
    "Gym offers 'Couch to 5K' program where you carry your couch 5K",
    "Average person spends 4 years looking for lost items",
    "Man sets selfie record; no one cares",
    "New spider species discovered; everyone pretends they didn't see it",
    "Library book returned 67 years late; fine exceeds small nation's GDP",
    "Study: Users of big words unnecessarily have small vocabularies",
    "Man joins marathon instead of waiting for bus; finishes third",
    "Restaurant adds surcharge for saying 'literally' too much",
    "Study: Dogs understand humans, just choose to ignore them",
    "Man still uses 'password'; hackers respectfully leave account alone",
    "Study: People who point out typos have no friends",
    "Woman assembles IKEA furniture without crying; sets record",
    "Man finds Bigfoot; Bigfoot claims better hiding spot",
    "New planet named 'Not Pluto' to avoid controversy",
    "Man reads entire terms and conditions; regrets everything",
    "Study: People who talk to themselves are good listeners",
    "Restaurant introduces 'silent dining'; customers won't stop talking",
    "Man trains squirrels for mail delivery; postal service sues",
    "Study: Socks disappear in dryer to another dimension",
    "Woman sets plant ownership record; still can't keep basil alive",
    "Study: Workplace emoji users taken 37% less seriously :(",
    "Man builds robot for his job; robot hires him as assistant",
    "Bar's 'Phone-Free Friday' fails; no one can post about it",
    "New color discovered; no one agrees what to call it",
    "Man's computer still updating after three days",
    "Study: Exercise extends life but makes time feel slower",
    "Restaurant offers 'Honest Menu' featuring 'Mediocre Pasta'",
    "Man solves world's problems; solution lost when phone dies",
    "Study: Shopping carts have minds of their own",
    "Woman returns from vacation more tired than before",
    "Study: Headline-only readers are most misinformed",
    "Man finds 2010 gift card; discovers it expired in 2011",
    "Man invents lost-phone finder app; can't find phone to install it",
    "Study: Plants scream when cut; vegans in crisis",
    "Coffee shop charges extra for correct name spelling; profits soar",
    "Study: Multitaskers just do multiple things poorly",
    "Restaurant's 'Instagram Menu' has less flavor, better looks",
    "Man finds TV remote after record search time; was sitting on it",
    "Study: Cats domesticated humans, not vice versa",
    "Gym's 'Napercise' classes fully booked",
    "Study: 'Slept like a baby' users haven't met actual babies",
    "Man 'invents' word; dictionary says it already exists",
    "Study: Talking about exercise burns zero calories",
    "Woman organizes sock drawer; achieves nirvana",
    "Study: Diet posters online gain more weight",
    "Restaurant bans food photos; customers confused",
    "Man returns to gym after 5 years; equipment unchanged",
    "Study: 'Diet starts Monday' never actually arrives",
    "Bookstore's 'Blind Date with Book' all romance novels",
    "Study: 'Not morning people' also not afternoon people",
    "Man still using first layer of dental floss from 2018",
    "Man claims to have read entire internet; remembers nothing",
    "New fitted sheet folding method still impossible for humans",
    "Woman finds 'ancient artifact'; turns out to be first iPod",
    "Study: Bed-makers happier; unmade bed people disagree",
    "Restaurant's 'Pay in Compliments' day; staff quits",
    "Man trains pet rock to sit; wins talent show",
    "Study: 99% of earbuds tangle themselves",
    "Man finishes toothpaste tube; celebrates with new one",
    "Study: 'No offense' always precedes offensive statement",
    "Cafe sells 'Deconstructed Water' for $7",
    "Man claims crypto expertise; can't explain it to anyone",
    "Study: Plants grow better when complimented regularly",
    "Woman sets record: 3 hours without checking phone",
    "Study: 'Not here to make friends' people have no friends",
    "Restaurant's 'Mystery Meat Monday' sees 97% attendance drop",
    "Man builds Amazon box fort; wife files for divorce",
    "Study: Hungry shoppers make interesting food choices",
    "Barber offers personality-based haircuts; business fails",
    "Study: People who say 'trust me' least trustworthy",
    "Gym offers 'Pretend to Work Out' classes for influencers",
    "Man claims to have read all terms ever; lawyers skeptical",
    "Study: Immediate folding prevents wrinkles; nation ignores",
    "Cafe's 'Rude Service' night has customers lining up",
    "Study: Public speakerphone users universally disliked",
    
    # New financial and international headlines
    "Stock market plunges; investors wish they'd bought lottery tickets",
    "Nation's economy grows 0.1%; government declares 'economic miracle'",
    "Bitcoin hits new high; owner forgets password",
    "Bank introduces 'honesty fee'; no one knows what it's for",
    "Wall Street trader retires at 30; parents still ask when getting real job",
    "Country changes name to improve SEO ranking",
    "Central bank prints money; accidentally uses washable ink",
    "Billionaire buys island; forgets where he put it",
    "Global summit ends with leaders agreeing to disagree",
    "Currency collapses; citizens using Monopoly money instead",
    "Nation celebrates 'No Tax Day'; government mysteriously closed",
    "Stock trader makes millions by accidentally hitting wrong button",
    "Country claims to have invented everything; provides no evidence",
    "Economists predict recession; also predict it might not happen",
    "World leaders agree climate important; fly home in private jets",
    "Bank ATM gives double cash; line now visible from space",
    "Nation bans Mondays; productivity mysteriously improves",
    "Investor buys company without knowing what it does; profits soar",
    "Country changes timezone to avoid meetings with neighbors",
    "Stock market explained with emojis; finally makes sense",
    "Nation makes all citizens millionaires; bread now costs billions",
    "Global peace achieved while world leaders' mics were muted",
    "Country outsources government; citizens give 5-star reviews",
    "Economists shocked when prediction actually comes true",
    "Nation adopts 4-day weekend; somehow GDP increases",
    "Bank accidentally transfers trillions; asks nicely for it back",
    "Country declares itself tax haven; forgets to build harbor",
    "Stock market reaches record high; nobody knows why",
    "Nation replaces currency with compliments; inflation skyrockets",
    "IMF loan comes with terms and conditions; no one reads them",
    "Country builds wall; neighbor builds taller tourist attraction",
    "Billionaire can't find cash for parking meter; buys parking lot",
    "Nation's debt clock breaks; technicians can't afford to fix it",
    "Stock exchange closes early; traders discover outside world exists",
    "Country accidentally deletes entire budget; uses last year's",
    "Bank introduces 'surprise fees'; customers actually surprised",
    "Nation makes happiness mandatory; reports record sadness",
    "Investor becomes billionaire; still uses coupons",
    "Country's new tourism slogan: 'Not as bad as you've heard'",
    "Central bank loses decimal point; economy unexpectedly booms",
    "Nation runs out of storage space; rents from neighbor",
    "Stock market crashes; investors wish they'd bought beanie babies",
    "Country adopts new flag; looks suspiciously like corporate logo",
    "Bank's 'no fee' account has record number of fees",
    "Nation celebrates budget surplus; accountant admits math error",
    "Economists debate theory; real world continues to ignore them",
    "Country claims to own moon; moon has no comment",
    "Investor diversifies portfolio with Pokémon cards; outperforms market",
    "Nation switches to cashless society; power immediately goes out",
    "Global conference ends; nothing accomplished but great photos"
]

# News agency acronyms with their corresponding colors
NEWS_AGENCIES = [
    {"acronym": "CNN", "color": Fore.RED},
    {"acronym": "BBC", "color": Fore.BLUE},
    {"acronym": "AP", "color": Fore.GREEN},
    {"acronym": "RT", "color": Fore.YELLOW},
    {"acronym": "NYT", "color": Fore.CYAN},
    {"acronym": "WSJ", "color": Fore.MAGENTA},
    {"acronym": "FOX", "color": Fore.RED},
    {"acronym": "NPR", "color": Fore.BLUE},
    {"acronym": "ABC", "color": Fore.GREEN},
    {"acronym": "CBS", "color": Fore.YELLOW}
]

def get_random_headline() -> tuple:
    """
    Get a random headline from the collection along with a random news agency.
    
    Returns:
        tuple: (headline, agency_acronym, agency_color)
    """
    headline = random.choice(HEADLINES)
    agency = random.choice(NEWS_AGENCIES)
    return headline, agency["acronym"], agency["color"]
