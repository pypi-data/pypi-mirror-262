import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
from pandas.core.frame import DataFrame


def create_widgets_expander(df, custom_column_widget_type={}, page_id=''):
    """
    This function will create all the widgets from your Pandas DataFrame and return them.
    Of course, you can free to customize the output widgets.

    df => a Pandas DataFrame
    custom_column_widget_type => [Optional] Widgets type for customizing manually specified fields
        supported: - multiselect, select, text
    page_id => When multiple pages are used, 
        the ID of the page is identified to prevent the session_state of key conflicts when the table field's names are duplicated between different pages.
    """
    return __create_widgets(df, custom_column_widget_type, st, page_id=page_id)


def __text_widget(df, column, ss_name, container_widget: DeltaGenerator, page_id=''):
    container_widget.text_input(f"{column.title()}", key=page_id+ss_name)
    all_widgets.append((ss_name, "text", column))


def __number_widget(df, column, ss_name, container_widget: DeltaGenerator, page_id=''):
    df = df[df[column].notna()]
    max = float(df[column].max())
    min = float(df[column].min())
    container_widget.slider(f"{column.title()}", min, max, (min, max), key=page_id+ss_name)
    all_widgets.append((ss_name, "number", column))


def __number_widget_int(df, column, ss_name, container_widget: DeltaGenerator, page_id=''):
    df = df[df[column].notna()]
    max = int(df[column].max())
    min = int(df[column].min())
    container_widget.slider(f"{column.title()}", min, max, (min, max), key=page_id+ss_name)
    all_widgets.append((ss_name, "number", column))


def __create_select(df, column, ss_name, container_widget: DeltaGenerator, multi=False, page_id=''):
    df = df[df[column].notna()]
    options = df[column].unique()
    options.sort()
    if multi == False:
        container_widget.selectbox(f"{column.title()}", options, key=page_id+ss_name)
        all_widgets.append((ss_name, "select", column))
    else:
        container_widget.multiselect(f"{column.title()}", options, key=page_id+ss_name)
        all_widgets.append((ss_name, "multiselect", column))


def __create_widgets(df: DataFrame, custom_column_widget_type: dict[str, str], container_widget: DeltaGenerator, page_id: str):
    global all_widgets
    all_widgets = []

    column_names = df.columns.tolist()

    with container_widget.expander("Advance Search"):
        with st.form(key='filter_form'):
            options = st.multiselect(
                'filter columns',
                column_names,
                []
            )

            if st.form_submit_button(label='Select'):
                st.session_state.selected_columns = options

    if 'selected_columns' in st.session_state :
        with container_widget.expander("Filter Condition", expanded=True):
            selected_columns = st.session_state.selected_columns
            ignore_columns = [col for col in df.columns if col not in selected_columns]
            for column in ignore_columns:
                df = df.drop(column, axis=1)            
            
            for ctype, column in zip(df.dtypes, df.columns):
                # Manually specify the field type and select the appropriate widget type
                if column in custom_column_widget_type:
                    if custom_column_widget_type[column] == "text":
                        __text_widget(df, column, column.lower(), container_widget, page_id=page_id)
                    elif custom_column_widget_type[column] == "select":
                        __create_select(df, column, column.lower(), container_widget, multi=False, page_id=page_id)
                    elif custom_column_widget_type[column] == "multiselect":
                        __create_select(df, column, column.lower(), container_widget, multi=True, page_i=page_id)
                # Automatically analyze the field type and select the appropriate widget type base on it
                else:
                    if ctype == "float64":
                        __number_widget(df, column, column.lower(), container_widget, page_id=page_id)
                    elif ctype == "int64":
                        __number_widget_int(df, column, column.lower(), container_widget, page_id=page_id)
                    elif ctype == "object":
                        if str(type(df[column].tolist()[0])) == "<class 'str'>":
                            __text_widget(df, column, column.lower(), container_widget, page_id=page_id)

    return all_widgets


def __filter_string(df, column, selected_list):
    final = []
    df = df[df[column].notna()]
    for idx, row in df.iterrows():
        if row[column] in selected_list:
            final.append(row)
    res = pd.DataFrame(final)
    return res


def filter_df(df, all_widgets):
    """
    This function will take the input dataframe and all the widgets generated from
    Streamlit Pandas. It will then return a filtered DataFrame based on the changes
    to the input widgets.

    df => the original Pandas DataFrame
    all_widgets => the widgets created by the function create_widgets().
    """
    res = df
    for widget in all_widgets:
        ss_name, ctype, column = widget
        data = st.session_state[ss_name]
        if data:
            if ctype == "text":
                if data != "":
                    res = res.loc[res[column].str.contains(data)]
            elif ctype == "select":
                res = __filter_string(res, column, data)
            elif ctype == "multiselect":
                res = __filter_string(res, column, data)
            elif ctype == "number":
                min, max = data
                res = res.loc[(res[column] >= min) & (res[column] <= max)]
    return res


def get_session_state_map():
    """
    Retrieve the current session state map from Streamlit's session_state.
    
    Returns:
        state_map (dict): The current session state map.
    """
    state_map = {}
    for key, value in st.session_state.items():
        state_map[key] = value
    return state_map