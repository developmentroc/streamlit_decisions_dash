import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components


def main():
    st.title("🧠 Decision Intelligence Dashboard")

    with open("index.html", "r", encoding='utf-8') as f:
        html_str = f.read()

    st.html(html_str)


if __name__ == "__main__":
    main()
