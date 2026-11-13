#importing
import pandas as pd
import random
import numpy as np
import streamlit as st
from gtts import gTTS
import subprocess
text = 'I need help'
electrodes = ["Fp1", "Fp2", "F3", "F4", "C3", "C4", "P3", "P4", "O1", "O2"]
live = st.toggle("Live readings (refresh every 5 seconds)")
st.title("Welcome to BCI device manager.")
st.write("This app is created to manage BCI devices to help human beings, especially disabled people.")

@st.fragment(run_every="5s" if live else None)
def display_readings():
    if not live:
        st.info("Turn on live readings to start.")
        return

    random_data = [random.uniform(0.5, 5.0) for _ in electrodes]
    readings = pd.DataFrame(
        {
            "Signal Value": [round(value, 2) for value in random_data],
        },
        index=electrodes,
    )
    readings.index.name = "Electrode"

    st.write("Latest electrode readings:")
    st.dataframe(readings)
    st.line_chart(readings)

    filtered = readings[readings["Signal Value"] > 2.5]
    st.write("Filtered data (Signal Value > 2.5):")
    st.dataframe(filtered)
    if np.mean(filtered["Signal Value"]) > 4.5:
        tts = gTTS(text=text, lang='en')
        tts.save("alert.mp3")
        subprocess.run(["cmd", "/c", "start", "", "alert.mp3"], check=False)  # For Windows
        # os.system("afplay alert.mp3")  # For macOS
        # os.system("mpg321 alert.mp3")  # For Linux    
display_readings()
