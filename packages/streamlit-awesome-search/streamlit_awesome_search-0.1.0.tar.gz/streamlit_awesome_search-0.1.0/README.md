> Demo

```python
import streamlit as st
import streamlit_awesome_search.awesome_pandas as apd

all_widgets = apd.create_widgets_expander(df)

if all_widgets:
    with st.spinner('Searching ...'):
        filter_df = apd.filter_df(df, all_widgets)
```