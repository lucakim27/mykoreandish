import nltk

def initialize_nltk():
    """
    Ensures that all necessary NLTK data is available.
    Downloads missing resources if required.
    """
    try:
        nltk.download('stopwords')
    except Exception as e:
        print(f"Error initializing NLTK: {e}")
