# Core Pkgs
import streamlit as st
# NLP Pkgs
import spacy_streamlit
import spacy
nlp = spacy.load('en_core_web_sm')
import os
from PIL import Image
from textblob import TextBlob
import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def main():
    """A Simple NLP app with Spacy-Streamlit"""
    st.title("Spacy-Streamlit NLP App")
    #our_image = Image.open(os.path.join('SpaCy_logo.svg.png'))
    #st.image(our_image)
    menu = ["Tokenization","NER", "Sentiment analysis", "Entity extraction", "Text summarization"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Tokenization":
        st.subheader("Tokenization")
        raw_text = st.text_area("Your Text","Enter Text Here")
        docx = nlp(raw_text)
        if st.button("Tokenize"):
            spacy_streamlit.visualize_tokens(docx,attrs=['text','pos_','dep_','ent_type_'])

    elif choice == "NER":
        st.subheader("Named Entity Recognition")
        raw_text = st.text_area("Your Text","Enter Text Here")
        docx = nlp(raw_text)
        spacy_streamlit.visualize_ner(docx,labels=nlp.get_pipe('ner').labels)

    elif choice == "Sentiment analysis":
        st.subheader("Sentiment analysis")
        raw_text = st.text_area("Your Text","Enter Text Here")
        docx = nlp(raw_text)
	
        # Creating graph for sentiment across each sentence in the text inputted
        sents = sent_tokenize(raw_text)
        entireText = TextBlob(raw_text)
        sentScores = []
        for sent in sents:
            text = TextBlob(sent)
            score = text.sentiment[0]
            sentScores.append(score)

        # Plotting sentiment scores per sentencein line graph
        st.line_chart(sentScores)

        # Polarity and Subjectivity of the entire text inputted
        sentimentTotal = entireText.sentiment
        st.write("The sentiment of the overall text below.")
        st.write(sentimentTotal)
	
    elif choice == "Entity extraction":
        st.subheader("Entity extraction")
        raw_text = st.text_area("Your Text","Enter Text Here")
        docx = nlp(raw_text)
	
        # Getting Entity and type of Entity
        entities = []
        entityLabels = []
        doc = nlp(text)
        for ent in doc.ents:
            entities.append(ent.text)
            entityLabels.append(ent.label_)
        entDict = dict(zip(entities, entityLabels)) #Creating dictionary with entity and entity types

        # Using function to create lists of entities of each type
        entOrg = entRecognizer(entDict, "ORG")
        entCardinal = entRecognizer(entDict, "CARDINAL")
        entPerson = entRecognizer(entDict, "PERSON")
        entDate = entRecognizer(entDict, "DATE")
        entGPE = entRecognizer(entDict, "GPE")

        # Displaying entities of each type
        st.write("Organization Entities: " + str(entOrg))
        st.write("Cardinal Entities: " + str(entCardinal))
        st.write("Personal Entities: " + str(entPerson))
        st.write("Date Entities: " + str(entDate))
        st.write("GPE Entities: " + str(entGPE))

    elif choice == "Text summarization":
        st.subheader("Text summarization")
        raw_text = st.text_area("Your Text","Enter Text Here")
        docx = nlp(raw_text)

if __name__ == '__main__':
	main()
