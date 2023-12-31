import streamlit as st
from simpleicons.all import icons


class Link:
    BASE_URL = "https://img.shields.io/badge/"

    def __init__(self, label, color, message=None) -> None:
        self.label = label.strip().replace(" ", "_").replace('-','--')
        self.message = message.strip().replace(" ", "_").replace('-','--')
        self.color = color
        self.parameters = {}

    def config(self, key, value):
        self.parameters[key] = value
    
    def get(self, string):
        value = self.parameters.get(string, None)
        if value is not None:
            return value
        elif string == "label":
            return self.label
        elif string == "message":
            return self.message
        elif string == "color":
            return self.color

    def __str__(self):
        link_parts = [self.BASE_URL, f"{self.label}-{self.message}-{self.color}" if self.message else f"{self.label}-{self.color}"]
        if self.parameters:
            link_parts.append("?")
            link_parts.extend([f"{key}={value}&" for key, value in self.parameters.items() if value is not None])
        return "".join(link_parts).rstrip("&")
st.markdown('''# Badge Generator
This web app creates personalized badges for your upcoming project by generating HTML and Markdown code. It utilizes the shields.io API for crafting these badges.
            
To know how exactly it generates them, go to [github.com/abdbbdii/markdown-badge-generator](https://github.com/abdbbdii/markdown-badge-generator).
            
To know how the API works, go to [shields.io/badges](https://shields.io/badges).''')
with st.container(border=True):
    st.markdown("### Add elements")

    label = st.text_input("Label", placeholder="Label", value="Label")
    if not label:
        st.error("Label cannot be empty.")
    message = st.text_input("Message", placeholder="Message")
    link = Link(label=label,message=message, color="ffffff")

    logoInc=st.checkbox("Include a logo?")
    if logoInc:
        logo = st.selectbox("Logo", icons)
        link.config('logo', logo)
    else:
        logo = st.selectbox("Logo", icons, disabled=True)


with st.container(border=True):
    st.markdown("### Customize badge")
    link.config("style", st.selectbox("Style", ("flat", "flat-square", "plastic", "for-the-badge", "social")))
    columns1 = st.columns(2)
    columns2 = st.columns(2)
    if logoInc:
        icon = icons.get(link.get("logo"))
        color = columns1[0].color_picker("Badge Color", value="#"+icon.__dict__["hex"])[1:]
        if columns1[1].button("Get logo color", key="btn1"):
            color = icon.__dict__["hex"]

        logoColor = columns2[0].color_picker("Logo Color", value="#ffffff")[1:]
        if columns2[1].button("Get logo color", key="btn2"):
            logoColor = icon.__dict__["hex"]

        link.config('logoColor', logoColor)
    else:
        color = columns1[0].color_picker("Badge Color", value="#ffffff")[1:]
        columns1[1].button("Get logo color", disabled=True, key="btn1")
        columns2[0].color_picker("Logo Color", value="#ffffff", disabled=True)
        columns2[1].button("Get logo color", disabled=True, key="btn2")
    
    link.config('color', color)

with st.container(border=True):
    md=f"![{link.get('label')}]({link})"
    if (link.get("label")):
        st.markdown(md)
        st.code(md, "None")


st.write("Made with ❤️ by abd")
