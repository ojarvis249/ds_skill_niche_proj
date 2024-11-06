import spacy
import string
from spacy.lang.en import English


class DescriptionProcessor:
    # Load the English tokenizer once for the class
    nlp = spacy.load("en_core_web_sm")

    # Load the English tokenizer and create the 'sentencizer' for sentence segmentation
    nlp_sentencizer = English()
    nlp_sentencizer.add_pipe("sentencizer")

    @staticmethod
    def text_lowercase(text):
        """Convert text to lowercase."""
        return text.lower()

    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from text."""
        translator = str.maketrans("", "", string.punctuation)
        return text.translate(translator)

    @staticmethod
    def remove_whitespace(text):
        """Remove extra whitespace from text."""
        return " ".join(text.split())

    @staticmethod
    def remove_stopwords(text):
        """Remove stopwords using spaCy."""
        doc = DescriptionProcessor.nlp(text)  # Process the text with spaCy
        filtered_text = " ".join(
            [token.text for token in doc if not token.is_stop]
        )  # Remove stopwords
        return filtered_text

    @staticmethod
    def sentence_segmentation(text):
        """Split the text into sentences using the 'sentencizer'."""
        doc = DescriptionProcessor.nlp_sentencizer(text)
        sents_list = [sent.text for sent in doc.sents]
        return sents_list
