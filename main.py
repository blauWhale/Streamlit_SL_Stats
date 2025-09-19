import streamlit as st
import pandas as pd
import altair as alt

# Load your CSV data
df = pd.read_csv('data.csv', sep=';')

# Prepare data
data = pd.DataFrame({
    'Squad': df['Squad'],
    'Sh/90': df['Sh/90'],
    'Sh A /90': df['Sh A /90']
})

# Calculate the averages
avg_x = data['Sh/90'].mean()
avg_y = data['Sh A /90'].mean()

# Define zoom window around the averages
x_margin = 5
y_margin = 5

x_min = max(0, avg_x - x_margin)
x_max = avg_x + x_margin
y_min = max(0, avg_y - y_margin)
y_max = avg_y + y_margin

# Create base scatter plot with zoomed axes
chart = alt.Chart(data).mark_circle(size=100).encode(
    x=alt.X('Sh/90', scale=alt.Scale(domain=[x_min, x_max])),
    y=alt.Y('Sh A /90', scale=alt.Scale(domain=[y_min, y_max])),
    tooltip='Squad'
)

# Add labels to points
text = chart.mark_text(
    align='left',
    dx=5,
    fontSize=10
).encode(
    text='Squad'
)

# Lines at the average point
vlines = alt.Chart(pd.DataFrame({'x': [avg_x]})).mark_rule(
    color='gray', strokeDash=[5, 5]
).encode(x='x')

hlines = alt.Chart(pd.DataFrame({'y': [avg_y]})).mark_rule(
    color='gray', strokeDash=[5, 5]
).encode(y='y')

# Combine all
full_chart = (chart + text + vlines + hlines).properties(
    title='Zoomed into Average Point'
).interactive()

st.altair_chart(full_chart, use_container_width=True)


####
# Liste der CSV-Dateien (du kannst die Namen später anpassen)
csv_files = {
    'FCZ': 'xG_data.csv',
    'GC': 'xG_data_gc.csv',
    'Winti': 'xG_data_winti.csv'
}

# Dropdown Menü für die Auswahl
selected_club = st.selectbox('Wähle einen Verein:', list(csv_files.keys()))

# Die gewählte CSV laden
data = pd.read_csv(csv_files[selected_club], sep=';')

# Linien für xG
line_xG = alt.Chart(data).mark_line(color='blue', point=True).encode(
    x='Spieltag',
    y='xG'
)

# Linien für xG Conceded
line_xG_conceded = alt.Chart(data).mark_line(color='red', point=True).encode(
    x='Spieltag',
    y='xG_Conceded'
)

# Linien zusammenlegen, gleiche y-Achse
chart = alt.layer(line_xG, line_xG_conceded).resolve_scale(
    y='shared'
).properties(
    title=f'{selected_club} - Entwicklung von xG und xG Conceded pro Runde'
)

st.altair_chart(chart, use_container_width=True)