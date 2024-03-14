import os
import base64
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component("streamlit_listen", url="http://localhost:3001")
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_listen", path=build_dir)

def streamlit_listen(name="Listening component",
                     ready_prompt="Ready to listen",
                     recording_prompt="Recording",
                     start_prompt="Start",
                     stop_prompt="Stop",
                     width="200px",
                     start_icon="",
                     stop_icon="",
                     time_slice=3,
                     key=None):
    """Create a new instance of "my_component".

    Parameters
    ----------
    name="Listening component" :str 
    ready_prompt="Ready to listen" :str
    recording_prompt="Recording" :str
    start_prompt="Start" :str
    stop_prompt="Stop" :str
    width="100px" :str
    start_icon="" :str - path
    stop_icon="" :str - path
    time_slice=3 :int - seconds
    
    Returns
    -------
    recording :str base64

    """
    
    def img2data(path):
        if path:
            _, extension = os.path.splitext(path)
            with open(path, "rb") as f:
                contents = f.read()
                data_url = base64.b64encode(contents).decode("utf-8")
            
            return f'data:image/{extension};base64,{data_url}'
        else:
            return ''

    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(name=name,
                                      ready_prompt=ready_prompt,
                                      recording_prompt=recording_prompt,
                                      start_prompt=start_prompt,
                                      stop_prompt=stop_prompt,
                                      width=width,
                                      start_icon=img2data(start_icon),
                                      stop_icon=img2data(stop_icon),
                                      time_slice=time_slice,
                                      key=key,
                                      default=0)
    return component_value

def main():
    if 'chunks' not in st.session_state:
        st.session_state.chunks = []

    st.subheader(f":green[Running test from {__name__} file]")

    chunk = streamlit_listen()
    if chunk:
        st.session_state.chunks.append(chunk)

    st.write(f"No of chunks: {len(st.session_state.chunks)}")

    lenghts = [len(c['audio_base64']) for c in st.session_state.chunks]
    st.write(lenghts)

if __name__ == "__main__":
    main()