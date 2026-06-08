import streamlit as st
import textstat

st.title("📝 AI Essay Feedback System")

st.write(
    "Analyze vocabulary, readability, and overall quality of English essays."
)

essay = st.text_area(
    "Paste your essay here:",
    height=250
)

if st.button("Analyze Essay"):

    if essay.strip() == "":
        st.warning("Please enter an essay.")

    else:

        words = len(essay.split())

        readability = textstat.flesch_reading_ease(essay)

        st.subheader("📊 Essay Statistics")

        st.write("Word Count:", words)

        st.write(
            "Readability Score:",
            round(readability, 2)
        )

        st.subheader("📚 Vocabulary Feedback")

        if words < 100:
            st.warning(
                "Consider adding more detailed explanations and richer vocabulary."
            )

        elif words < 250:
            st.info(
                "Vocabulary range is acceptable but can still be improved."
            )

        else:
            st.success(
                "Good vocabulary range and essay length."
            )

        st.subheader("💡 Overall Feedback")

        if readability > 60:
            st.success(
                "The essay is generally easy to read and understand."
            )

        else:
            st.warning(
                "The essay may be difficult to read. Consider simplifying some sentences."
            )