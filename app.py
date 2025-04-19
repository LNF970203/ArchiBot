import streamlit as st

from graph import helper_graph, PDF_NAME


IMAGE_ADDRESS = "https://media.licdn.com/dms/image/v2/D4D12AQH4I6ezcUeaQg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1736535209599?e=2147483647&v=beta&t=GsliN5hm8_ShOPMj9Li-q_sBHjOqy_-HJpKHejo-Rsk"


# application
st.title("Archi Bot")
st.image(IMAGE_ADDRESS)

# text input
st.header("Enter Your System Requirements")
texts = st.text_input("Please Enter Your System Requirements")

if not texts:
    st.error("Please Enter Some Requirements", icon = "🚨")
    st.stop()

# invoke the graph
with st.spinner("Designing.....", show_time=True):
    response = helper_graph.invoke({"requirements": texts})

# show th results
st.markdown(response["design"])

with st.sidebar:
    # Reading the PDF file as bytes
    with open(PDF_NAME, 'rb') as f:
        pdf_data = f.read()

    # Provide a download link
    st.subheader("Download the Design as a PDF")
    st.download_button(
        label="Download the Design",
        data=pdf_data,
        file_name="architecture_design.pdf",
        mime="application/pdf",
        on_click = "ignore"
    )
