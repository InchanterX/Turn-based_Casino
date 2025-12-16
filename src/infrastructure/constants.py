import os
# log files location
LOG_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "../../.casino_log")

DEFAULT_BALANCE = 1000
DEFAULT_PLAYER_HEALTH = 100
DEFAULT_PLAYER_LUCK = 100

DENOMINATIONS = [1, 5, 25, 100]

SYMBOLS = ['🍎', '🍊', '🍌', '🍍', '🍒']
MULTIPLIERS = {
    '🍎': 0.5,
    '🍊': 2,
    '🍌': 4,
    '🍍': 8,
    '🍒': 15
}

ADVERTISEMENTS = [
    "Lost your shirt at roulette? We'll take your apartment too! Instant loans, zero questions asked! "
    "(Terms: you might need to live in the roulette wheel.)",

    "Need quick cash? Try our 'Desperation Deluxe' loan - only 999% APR! "
    "What's a few zeros between friends?",

    "Weather forecast for tomorrow: 100% chance of poor life choices! "
    "Perfect day to stay inside and lose virtual money!",

    "RAM prices so high, you'll forget what affordability means! "
    "But hey, at least your crippling gambling debt feels cheaper now!",

    "According to 'Totally Legit Science Monthly', 'dodep' is 2025's word of the year! "
    "Definition: 'that feeling when you bet on red and it lands on green 14 times in a row'.",

    "Breaking: Moscow opens beer fountain in Red Square! "
    "Finally, a liquid asset you can actually enjoy losing! (Please don't swim in it.)",

    "Failed to calculate roulette odds? Enroll in 'Casino Calculus' - "
    "learn derivatives while deriving your life savings!",

    "Local man selling garage. Perfect for: 1) Storing things 2) Crying about blackjack losses 3) Both! "
    "Comes with free 'I Should Have Bet on Red' bumper sticker!",

    "Aviasales presents: 'Escape Your Debts' package! "
    "One-way tickets to anywhere! (Note: return ticket costs 3x your original bankroll.)",

    "Feeling lucky? Our casino geese have better odds than you! "
    "Visit today and watch them honk away with your money!",

    "Tired of losing to humans? Try our new 'Goose vs Goose' tables! "
    "Watch as birds gamble better than you ever could!",

    "Pro tip: If you're winning, you're probably dreaming. Our reality distortion field is working perfectly!",

    "Remember: The house always wins. But today might be the day we're feeling charitable! "
    "(Spoiler: It's not.)",
]
