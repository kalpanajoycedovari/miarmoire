"""
Mi Armoire — Test Prompt Bank
Fixed inputs for reproducible eval runs.
"""

TEST_PROMPTS = [
    {
        "id": "T01",
        "label": "Minimal Wardrobe — Casual",
        "occasion": "Casual",
        "input": (
            "I have a white fitted t-shirt, black high-waist jeans, and white Nike Air Force 1s. "
            "I also have gold hoop earrings. I'm 5'4\" and 130 lbs."
        ),
    },
    {
        "id": "T02",
        "label": "Full Wardrobe — Mixed Occasions",
        "occasion": "Any",
        "input": (
            "Tops: white linen button-up, black silk blouse, cream knit jumper, striped navy tee. "
            "Bottoms: tailored black trousers, light wash straight jeans, midi floral skirt, beige cargo pants. "
            "Shoes: white trainers, black block heel mules, tan leather loafers, strappy gold sandals. "
            "Jewellery: gold layered necklaces, pearl studs, silver cuff bracelet. "
            "I'm 5'7\" and 145 lbs, fairly athletic build."
        ),
    },
    {
        "id": "T03",
        "label": "Evening / Formal",
        "occasion": "Evening",
        "input": (
            "Black satin slip dress, white oversized blazer, black stiletto heels, silver strappy heels. "
            "Jewellery: diamond stud earrings, silver tennis bracelet. "
            "I'm 5'2\" and 125 lbs, petite frame."
        ),
    },
    {
        "id": "T04",
        "label": "Office / Smart Casual",
        "occasion": "Office",
        "input": (
            "Tops: white structured blouse, pastel blue fitted cardigan, camel turtleneck. "
            "Bottoms: high-waist grey wide-leg trousers, black pencil skirt, navy tailored shorts. "
            "Shoes: black pointed-toe flats, tan oxford shoes. "
            "Accessories: structured black tote, tortoiseshell glasses. "
            "No jewellery. I'm 5'9\" and 160 lbs, tall and curvy."
        ),
    },
    {
        "id": "T05",
        "label": "Colourful — Pattern Heavy",
        "occasion": "Weekend",
        "input": (
            "Leopard print midi skirt, hot pink ribbed crop top, cobalt blue oversized blazer, "
            "white wide-leg trousers, red knit top. "
            "Shoes: nude block heels, white platform sneakers, red mules. "
            "Jewellery: chunky gold chains, mismatched earrings, gold bangles. "
            "I'm 5'5\" and 138 lbs."
        ),
    },
    {
        "id": "T06",
        "label": "Edge Case — Very Short List",
        "occasion": "Any",
        "input": (
            "One black dress and white sneakers. I'm 5'6\" and 140 lbs."
        ),
    },
    {
        "id": "T07",
        "label": "Edge Case — No Body Info",
        "occasion": "Casual",
        "input": (
            "Beige trench coat, white t-shirt, straight jeans, black ankle boots, "
            "grey knit sweater, dark green cargo trousers, silver jewellery."
        ),
    },
    {
        "id": "T08",
        "label": "Festival / Statement",
        "occasion": "Festival",
        "input": (
            "Denim cut-off shorts, mesh overlay top, sheer white maxi dress, "
            "cowboy boots, chunky white trainers. "
            "Accessories: fringe bag, bandana, sunglasses. "
            "Lots of gold jewellery — rings, stacked bracelets, long pendant necklace. "
            "I'm 5'6\" and 135 lbs, slim build."
        ),
    },
]