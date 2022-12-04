from collections import OrderedDict

import streamlit as st

# TODO : change TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

# TODO : you can (and should) rename and add tabs in the ./tabs folder, and import them here.
from tabs import intro, second_tab, third_tab, fourth_tab, fifth_tab, sixth_tab, seventh_tab


st.set_page_config(
    page_title=config.TITLE,
    page_icon="assets/favicon.png",
)

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


# TODO: add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (second_tab.sidebar_name, second_tab),
        (third_tab.sidebar_name, third_tab),
        (fourth_tab.sidebar_name, fourth_tab),
        (fifth_tab.sidebar_name, fifth_tab),
        (sixth_tab.sidebar_name, sixth_tab),
        (seventh_tab.sidebar_name, seventh_tab),
    ]
)


def run():
    st.sidebar.image(
        "assets/logo-pybike.png",
        width=200,
    )
    tab_name = st.sidebar.radio("Sommaire", list(TABS.keys()), 0)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}")

    st.sidebar.markdown("### Membres de l'équipe :")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
