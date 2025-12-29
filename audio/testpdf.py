import streamlit as st

JS = """
export default function(component) {
    const { setTriggerValue, parentElement } = component;
    const btn = document.createElement("button");
    btn.innerText = "Click me!";
    parentElement.appendChild(btn);

    btn.onclick = () => {
        setTriggerValue("clicked", true);
    };
}
"""

my_button = st.components.v2.component(
    name="minimal_button",
    js=JS
)

res = my_button(on_clicked_change=lambda: None)

if res.clicked:
    st.write("按钮被点击了")
else:
    st.write("请点击按钮")
