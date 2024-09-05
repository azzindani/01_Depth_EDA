import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pygwalker as pyg
#import ydata_profiling
import sweetviz as sv
import warnings
import streamlit.components.v1 as components

from pygwalker.api.streamlit import StreamlitRenderer
#from streamlit_pandas_profiling import st_profile_report
#from autoviz import AutoViz_Class
warnings.filterwarnings('ignore')

st.set_page_config(page_title = 'EDA', page_icon = ':1234:', layout = 'wide')
st.title('In-Depth Exploratory Data Analysis')

tab_1, tab_2 = st.tabs([
  'Chart Generation',
  'SweetViz',
])

if 'clicked' not in st.session_state:
  st.session_state.clicked = False

def click_button():
  st.session_state.clicked = True

def run_pywalker(df):
  pyg_app = StreamlitRenderer(df)
  pyg_app.explorer()

with st.sidebar:
  fl = st.file_uploader(':file_folder: Upload a file', type = (['csv', 'xlsx', 'xls']))

  title = st.text_input('Paste API URL', None)

  st.button('Use Data Sample', on_click = click_button)

  st.write(
    'Refresh the browser if you want to reset everything'
  )

with tab_1:
  if fl is not None:
    try:
      df = pd.read_csv(fl, encoding = 'ISO-8859-1')
    except:
      df = pd.read_excel(fl)
    run_pywalker(df)

  if title is not None:
    try:
      df = pd.read_csv(title, encoding = 'ISO-8859-1')
    except:
      df = pd.read_excel(title)

    run_pywalker(df)

  if st.session_state.clicked:
    df = pd.read_csv(
      'https://raw.githubusercontent.com/azzindani/00_Data_Source/main/Adidas_US_Sales.csv'
    )
    run_pywalker(df)

  else:
    print('Please upload your dataset')

with tab_2:
  try:
    report = sv.analyze(df)
    report.show_html()
    with open('SWEETVIZ_REPORT.html', 'r') as f:
      html_data = f.read()
    components.html(html_data, scrolling = True, height = 600)

    st.download_button(
      label = 'Download Full Report',
      data = html_data,
      file_name = 'SweetViz_Report.html'
    )
  except:
    pass
