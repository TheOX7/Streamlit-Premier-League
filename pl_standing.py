import pandas as pd
import streamlit as st

# Membaca data dari file CSV
pl_standings = pd.read_csv('D:\GitHub\Streamlit-PL\Streamlit\PL 22-23 Standings.csv')

# Membuat fungsi untuk memberikan warna pada baris
def highlight_row(row):
    if row == 1 or row == 2 or row == 3 or row == 4:
        return ['background-color: lightblue'] * len(row)
    elif row == 5 or row == 6:
        return ['background-color: orange'] * len(row)
    elif row == 7:
        return ['background-color: green'] * len(row)
    elif row >= 18:
        return ['background-color: red'] * len(row)
    else:
        return [''] * len(row)
    
st.dataframe(pl_standings.style.apply(lambda x: highlight_row(x['Position']), axis=1), use_container_width=True)

