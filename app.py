import streamlit as st
import re
import requests
from collections import Counter

st.set_page_config(
    page_title="AI Essay Feedback System",
    page_icon="📝",
    layout="wide"
)

def check_grammar(text):

    url = "https://api.languagetool.org/v2/check"

    data = {
        "text": text,
        "language": "en-US"
    }

    try:

        response = requests.post(
            url,
            data=data,
            timeout=20
        )

        result = response.json()

        return result["matches"]

    except:

        return []


st.title("📝 AI Essay Feedback System")

st.write(
    "Analyze grammar, vocabulary, organization, readability, and overall essay quality."
)

essay = st.text_area(
    "Paste your English essay here:",
    height=300
)

if st.button("Analyze Essay"):

    if essay.strip() == "":
        st.warning("Please enter an essay.")

    else:

        words_list = re.findall(
            r"\b[a-zA-Z]+\b",
            essay.lower()
        )

        words = len(words_list)

        unique_words = len(set(words_list))

        vocab_ratio = (
            unique_words / words
            if words > 0
            else 0
        )

        paragraphs = [
            p for p in essay.split("\n\n")
            if p.strip()
        ]

        paragraph_count = len(paragraphs)

        if paragraph_count == 0:
            paragraph_count = 1

        sentences = re.split(
            r"[.!?]+",
            essay
        )

        sentences = [
            s.strip()
            for s in sentences
            if s.strip()
        ]

        sentence_count = len(sentences)

        if sentence_count == 0:
            sentence_count = 1

        avg_sentence_length = round(
            words / sentence_count,
            2
        )

        grammar_errors = check_grammar(essay)
        grammar_count = len(grammar_errors)

        word_frequency = Counter(words_list)

        repeated_words = []

        for word, count in word_frequency.items():

            if count >= 5:
                repeated_words.append(
                    (word, count)
                )

        st.subheader("📊 Essay Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Word Count", words)
            st.metric("Sentence Count", sentence_count)

        with col2:
            st.metric("Paragraph Count", paragraph_count)
            st.metric("Unique Words", unique_words)

        with col3:
            st.metric(
                "Vocabulary Diversity",
                f"{round(vocab_ratio*100,2)}%"
            )
            st.metric(
                "Average Sentence Length",
                avg_sentence_length
            )

        st.divider()

        st.subheader("📏 Essay Length Analysis")

        if words < 100:

            st.error(
                "Very short essay. More development and supporting details are needed."
            )

            length_score = 5

        elif words < 250:

            st.warning(
                "Moderate essay length. Additional examples and explanations would improve quality."
            )

            length_score = 15

        else:

            st.success(
                "Essay length is appropriate."
            )

            length_score = 20

        st.subheader("📚 Vocabulary Analysis")

        if vocab_ratio < 0.40:

            st.error(
                "Limited vocabulary variety detected."
            )

            vocab_score = 5

        elif vocab_ratio < 0.60:

            st.info(
                "Adequate vocabulary range."
            )

            vocab_score = 15

        else:

            st.success(
                "Excellent vocabulary diversity."
            )

            vocab_score = 20

        if repeated_words:

            st.write("### Frequently Repeated Words")

            for word, count in repeated_words[:10]:

                st.write(
                    f"• {word} ({count} times)"
                )

        st.subheader("📖 Sentence Structure Analysis")

        if avg_sentence_length < 8:

            st.warning(
                "Sentences are very short and may lack development."
            )

            structure_score = 5

        elif avg_sentence_length <= 20:

            st.success(
                "Sentence length is balanced."
            )

            structure_score = 10

        elif avg_sentence_length <= 30:

            st.info(
                "Some sentences are lengthy."
            )

            structure_score = 7

        else:

            st.error(
                "Many sentences are excessively long."
            )

            structure_score = 3

        st.subheader("🗂 Organization Analysis")

        if paragraph_count == 1:

            st.warning(
                "Only one paragraph detected. Consider using introduction, body, and conclusion."
            )

            organization_score = 5

        elif paragraph_count <= 3:

            st.info(
                "Basic paragraph organization detected."
            )

            organization_score = 10

        else:

            st.success(
                "Essay organization appears effective."
            )

            organization_score = 15

        st.subheader("📝 Content Development")

        if words < 100:

            st.error(
                "Ideas are not sufficiently developed."
            )

            content_score = 5

        elif words < 250:

            st.warning(
                "Ideas are present but need stronger explanations and examples."
            )

            content_score = 15

        else:

            st.success(
                "Ideas are reasonably developed."
            )

            content_score = 25

        st.subheader("✍ Grammar Analysis")

        if grammar_count == 0:

            st.success(
                "No grammar issues detected."
            )

            grammar_score = 20

        elif grammar_count <= 3:

            st.info(
                f"{grammar_count} minor grammar issues detected."
            )

            grammar_score = 15

        elif grammar_count <= 8:

            st.warning(
                f"{grammar_count} grammar issues detected."
            )

            grammar_score = 10

        else:

            st.error(
                f"{grammar_count} grammar issues detected."
            )

            grammar_score = 5

        if grammar_errors:

            st.write("### Grammar Suggestions")

            for issue in grammar_errors[:10]:

                st.write(
                    f"• {issue['message']}"
                )

        raw_score = (
            length_score +
            vocab_score +
            structure_score +
            organization_score +
            content_score +
            grammar_score
        )

        score = round(
            (raw_score / 110) * 100
        )

        st.divider()

        st.subheader("🏆 Essay Quality Score")

        st.write("### Score Breakdown")

        st.write(
            f"📌 Content Development: {content_score}/25"
        )

        st.write(
            f"📌 Vocabulary Usage: {vocab_score}/20"
        )

        st.write(
            f"📌 Grammar Accuracy: {grammar_score}/20"
        )

        st.write(
            f"📌 Sentence Structure: {structure_score}/10"
        )

        st.write(
            f"📌 Organization: {organization_score}/15"
        )

        st.write(
            f"📌 Essay Length: {length_score}/20"
        )

        st.metric(
            "Overall Score",
            f"{score}/100"
        )

        st.divider()

        st.subheader("💪 Strengths")

        strengths = []

        if vocab_ratio >= 0.60:
            strengths.append(
                "Strong vocabulary diversity."
            )

        if avg_sentence_length <= 20:
            strengths.append(
                "Balanced sentence structure."
            )

        if words >= 250:
            strengths.append(
                "Good content development."
            )

        if grammar_count <= 3:
            strengths.append(
                "Few grammar issues."
            )

        for item in strengths:
            st.write(f"✓ {item}")

        st.subheader("⚠ Areas for Improvement")

        weaknesses = []

        if words < 250:
            weaknesses.append(
                "Add more supporting evidence and examples."
            )

        if grammar_count > 3:
            weaknesses.append(
                "Reduce grammar errors."
            )

        if paragraph_count == 1:
            weaknesses.append(
                "Improve paragraph organization."
            )

        if repeated_words:
            weaknesses.append(
                "Reduce repeated vocabulary."
            )

        for item in weaknesses:
            st.write(f"• {item}")

        st.subheader("🤖 Recommendations")

        recommendations = [
            "Support arguments with examples.",
            "Use transitions between ideas.",
            "Review grammar carefully.",
            "Proofread before submission.",
            "Expand explanations where needed."
        ]

        for item in recommendations:
            st.write(f"• {item}")

        st.subheader("💡 Overall Feedback")

        if score >= 85:

            st.success(
                "Excellent essay. Strong organization, vocabulary usage, and grammar accuracy."
            )

        elif score >= 70:

            st.info(
                "Good essay. Some improvements in grammar and development could strengthen the writing."
            )

        elif score >= 50:

            st.warning(
                "Average essay. More detailed content, stronger organization, and grammar improvement are recommended."
            )

        else:

            st.error(
                "The essay requires substantial improvement across multiple writing areas."
            )