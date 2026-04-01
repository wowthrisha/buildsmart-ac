RULES = {
    'setback': (
        "Setback is the minimum distance your building must be from the plot boundary. "
        "TNPCR Table II requires: Front setback ≥ 3 ft, Rear setback ≥ 1.5 ft, "
        "Side setback ≥ 1.5 ft for residential plots.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'frontage': (
        "Frontage is the width of your plot along the road. "
        "TNPCR Table II requires a minimum frontage of 20 ft for residential plots. "
        "If your frontage is less, you may need a special variance or redesign.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'area': (
        "Plot area is the total size of your land. "
        "TNPCR requires a minimum of 600 sq ft for a residential building approval. "
        "Smaller plots may qualify for regularisation under special provisions.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'track': (
        "Track A is the standard residential approval route for plots under 1,500 sq ft. "
        "Track B applies to larger or commercial plots and requires additional documentation. "
        "Your architect determines which track your project qualifies for.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'patta': (
        "Patta is the legal document proving you are the registered owner of the land. "
        "It is issued by the Revenue Department and is mandatory for building approval.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'ec': (
        "EC stands for Encumbrance Certificate. It shows whether your property has any "
        "loans, mortgages, or legal disputes attached. Required for building approval.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
    'approval': (
        "Building plan approval in Tamil Nadu is processed through onlineppa.tn.gov.in. "
        "Your architect handles the submission. You need to provide documents like Patta, EC, "
        "and ID proof.\n\n"
        "_Always verify with your architect before finalising your design._"
    ),
}

DEFAULT = (
    "I couldn't find a specific TNPCR rule for your question. "
    "Please ask your architect for clarification on this point.\n\n"
    "_Always verify with your architect before making decisions._"
)

def query(question):
    q = question.lower()
    for keyword, answer in RULES.items():
        if keyword in q:
            return answer
    return DEFAULT
