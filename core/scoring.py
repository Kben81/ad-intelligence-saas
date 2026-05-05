def calculate_opportunity(trend, competition):

    opportunity = (trend * 0.7) + ((100 - competition) * 0.3)

    if opportunity > 65:
        level = "🔥 forte opportunité"
    elif opportunity > 40:
        level = "🟡 opportunité moyenne"
    else:
        level = "🔴 marché difficile"

    return opportunity, level