import streamlit as st


JS = """
export default function(component) {
    const { setTriggerValue,data,setStateValue } = component;
    const links = document.querySelectorAll('a[href="#"]');
    console.log(data)
    links.forEach((link) => {
        link.onclick = (e) => {
            setTriggerValue('clicked', link.innerHTML);
            setStateValue('state1', '123');
        };
    });
    return ()=>{
    console.log('aaaaa');
    };
    
}
"""

my_component = st.components.v2.component(
    "inline_links",
    js=JS,
)

def when_link_clicked():
    st.write("链接被点击了 — (callback 被触发)")

#result = my_component(data="hello world", on_clicked_change=lambda: None)
#result = my_component(data="hello world", on_clicked_change=when_link_clicked)
result = my_component(data="hello world")

print(result)

st.markdown(
    "Components aren't [sandboxed](#), so you can write JS that [interacts](#) with the main [document](#)."
)

if result.clicked:
    st.write(f"You clicked {result.clicked}!")
    st.write(f"You state {result.state1}!")