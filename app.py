import streamlit as st
import language_tool_python

st.title("📝 AI Essay Feedback System")

essay = st.text_area(
    "Paste your essay here:",
    height=250
)

if st.button("Analyze Essay"):

    if essay.strip() == "":
        st.warning("Please enter an essay.")

    else:

        words = len(essay.split())

        tool = language_tool_python.LanguageTool('en-US')

        matches = tool.check(essay)

        st.subheader("📊 Essay Statistics")

        st.write("Word Count:", words)

        st.subheader("✏ Grammar Feedback")

        if len(matches) == 0:
            st.success("No major grammar errors found.")

        else:

            st.write(f"Grammar Issues Found: {len(matches)}")

            for match in matches[:10]:

                st.write(f"• {match.message}")

        st.subheader("📚 Vocabulary Feedback")

        if words < 100:
            st.write(
                "Consider using more detailed explanations and richer vocabulary."
            )
        elif words < 250:
            st.write(
                "Vocabulary range is acceptable but could be expanded."
            )
        else:
            st.write(
                "Good vocabulary range and essay length."
            )