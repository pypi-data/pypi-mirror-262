![](Readme.assets\logo.jpg)

## 🔍 Streamlit Awesome Search

[![Downloads](https://static.pepy.tech/personalized-badge/streamlit-awesome-search?period=total&units=international_system&left_color=black&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/streamlit-awesome-search)


Streamlit Awesome Search is a component for the [Streamlit](https://streamlit.io/) library. It allows users to load a Pandas DataFrame and automatically generate Streamlit widgets in the expander. In addition, it also supports customization of search fields. These widgets trigger filtering events within the Pandas DataFrame.



## 🖊️ Support

Current support only exists for DataFrame columns with strings, numbers (int64 and float64) and datetimes(datetime64). **A future update will include support for advanced search function**.

By default, string data generates a text_input Streamlit widget, while numerical data creates sliders and datetime data creates date_input with ranges preset to the minimum and maximum values for that column. Users can pass a custom dictionary for handling specific types of data, where each key is the column in the DataFrame and the value is the streamlit widget type.

Sample of a custom column widget type dict:

```python
custom_column_widget_type = {"Name": "text",
                "Sex": "multiselect",
                "Embarked": "multiselect",
                "Ticket": "text",
                "loginDate": "date_input"
                "Pclass": "multiselect"}
```

The current version only supports: text, multiselect, date_input and select.



## 🚧 Installation

1. First, install Streamlit

`pip install streamlit`

2. Next, intall Pandas

`pip install pandas`

3. Install Streamlit Awesome Search

`pip install streamlit-awesome-search`

## 💻 Useage



```python
import streamlit as st
import pandas as pd

import streamlit-awesome-search.awesome_pandas as apd


@st.cache_data
def load_data():
    titan_df = pd.read_csv(file)
    return titan_df


file = "data/sample.csv"
df = load_data().astype({'loginDate': 'datetime64[s]'})

st.markdown("# Source Dataframe")
st.dataframe(df)

all_widgets = apd.create_widgets_expander(df, custom_column_widget_type={'loginDate':'date_input'})

if all_widgets:
    with st.spinner('Searching ...'):
        filter_df = apd.filter_df(df, all_widgets)
        st.markdown("# Result Dataframe")
        st.dataframe(filter_df)
```



This will generate the following app:

![](Readme.assets\demo.png)





## 🤗 Want to support my work?

Please give me a free little star, this will be the motivation for me to keep updating.