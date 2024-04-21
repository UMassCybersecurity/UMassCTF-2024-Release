from typing import List, Tuple

quick_foods: List[Tuple[str, int, str]] = [
    ('Bran Flakes', 30, '$4'),
    ('Fried Oyster Skins', 120, '$6'),
    ('Popcorn', 60, '$4.5'),
    ('Seanut Brittle Sandwich', 90, '$7.50'),
    ('Banana', 15, '$3'),
]

slow_foods: List[Tuple[str, int, str]] = [
    ('SpongeBob\'s Sundae', 370, '$12'),
    ('Holographic Meatloaf', 550, '$13.50'),
    ('Krabby Fries', 450, '$6'),
    ('Pretty Patty Combo', 520, '$18.50'),
    ('Aged Patty', 600, '$23'),
]

foods = [{'name': food[0], 'price': food[2], 'time': food[1]} for food in quick_foods + slow_foods]
probabilities = [.08] * 5 + [.12] * 5
