import streamlit as st
import sidebar
import textPage

page = sidebar.show()

if page=="Text":
    textPage.renderPage()
