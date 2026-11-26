BASE = "https://rgwebd.github.io/13gypsies-v3/"
V = 4
NAME = "13 Gypsies"
PHONE = "(904) 389-0330"
TEL = "+19043890330"
ADDR1 = "887 Stockton St"
CITY = "Jacksonville"
REGION = "FL"
ZIP = "32204"
HOOD = "Riverside"
GEO = (30.315061, -81.6891814)
MAPS = "https://www.google.com/maps/place/13+Gypsies/@30.315061,-81.6891814,17z/data=!4m6!3m5!1s0x88e5b77e70ce003f:0x64ff0fd11cca072a!8m2!3d30.315061!4d-81.6891814!16s%2Fg%2F1hc1bsvmt"
OT = "https://www.opentable.com/r/13-gypsies-jacksonville"
OT_RID = "283390"
# 0=Mon ... 6=Sun ; (open, close) in minutes, None = closed
HOURS = {0: None, 1: (17*60, 21*60), 2: (17*60, 21*60), 3: (17*60, 21*60), 4: (17*60, 22*60), 5: (17*60, 22*60), 6: None}
HOLIDAYS = {"2026-11-26": "Thanksgiving", "2026-11-27": "Black Friday"}

MARQUEE_A = [
  ("gnocchi", "Roman-style gnocchi", "Roman-style gnocchi: flat squares under beef and mushroom stock and pecorino"),
  ("mushrooms", "Roasted crimini mushrooms", "Roasted crimini mushrooms with saffron aioli and sautéed kale"),
  ("ricotta", "House-made ricotta", "House-made ricotta with grilled peasant bread"),
  ("cabbage", "Butter-braised cabbage", "Butter-braised cabbage with brown butter and house kimchi paste"),
  ("albondigas", "Albóndigas", "Albóndigas, pork and beef meatballs in house red sauce, with house bread"),
  ("mongolian-beef", "Mongolian beef skewers", "Mongolian beef skewers with honey-soy dipping sauce"),
  ("chamber", "From the Chamber", "House dry-cured meat from the chamber with peasant bread"),
]
MARQUEE_B = [
  ("empanada", "Empanada of kale", "Empanada of kale with dill buttermilk dressing"),
  ("risotto", "Risotto of the day", "A bowl of the daily risotto"),
  ("tres-leches", "Tres leches", "A slice of house-made tres leches cake"),
  ("brussels", "Pan-roasted Brussels sprouts", "Pan-roasted Brussels sprouts"),
  ("pasta", "House-made pasta", "House-made filled pasta"),
  ("cheesecake", "Mason jar cheesecake", "Mason jar cheesecake topped with berries"),
]

# Menu: OpenTable dinner menu (last updated 19 Apr 2022) + in-house dessert board. No prices (dated).
MENU = [
  ("cold", "Cold", [
    ("Honey Garlic Hummus", "flatbread, clover honey"),
    ("House-Made Ricotta", "smoked honey, grilled peasant bread"),
    ("Grilled House-Made Peasant Bread", "olive oil, sea salt, black pepper"),
    ("Mushroom Escabeche", "Spanish olive oil, sherry vinegar, white wine, onion, garlic, rosemary, toasted house baguette"),
    ("Tomato and Cucumber Salad", "couscous, citronette, dill whipped feta, pickled red onion"),
    ("Zanahorias", "Moorish spiced carrots, pickled sultanas, cilantro, roasted almonds, olive oil"),
  ]),
  ("veg", "Vegetables", [
    ("Patatas Fritas", "sea salt, sweet onion curry sauce"),
    ("Cauliflower", "sautéed with curry sauce and sweet peas"),
    ("Mushroom Sevilla", "cream sherry sauce, goat cheese toast"),
    ("Roasted Crimini Mushrooms", "garlic, rosemary, saffron aioli, sautéed kale"),
    ("Empanada of Kale", "parmesan, black pepper, dill buttermilk dressing"),
    ("Pan-Roasted Brussels Sprouts", "blue cheese sauce, roasted almonds"),
    ("Butter-Braised Cabbage", "brown butter, house kimchi paste"),
  ]),
  ("meat", "Meat & Seafood", [
    ("House-Made Fresh Chorizo", "honey-sautéed pear, warm spiced dates", "ddd"),
    ("Mongolian Beef", "honey-soy dipping sauce"),
    ("Vietnamese-Style Meatballs", "house chili-garlic oil, sweet lime sauce"),
    ("Spanish Pork Mojo", "house cultured cream"),
    ("Gambas al Ajillo", "olive oil, cream sherry, tomatoes, parsley, house baguette"),
    ("Pan-Fried Fish", "lightly floured, brown butter, lemon, parsley"),
  ]),
  ("pasta", "Pasta & More", [
    ("Roman-Style Gnocchi", "beef and mushroom stock, butter, herbs, pecorino", "ddd"),
    ("Gnudi", "house cultured cream sauce, lemony kale, pecorino"),
  ]),
  ("daily", "Daily Offerings", [
    ("Risotto of the Day", "ask your server what's in the pot tonight"),
    ("From the Chamber", "true, in-house, handcrafted dry-cured meat, peasant bread"),
  ]),
  ("dessert", "Housemade Desserts", [
    ("Tres Leches", "from the dessert board"),
    ("Mason Jar Cheesecake", "from the dessert board"),
  ]),
]
