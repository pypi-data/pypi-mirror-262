# Streamlit Multi Menu
With streamlit_multi_menu you can create a multi-column menu widget (with google icons or background images on the buttons). It allows you to selected just one sub menu across the whole all columns.

## Installation instructions

```sh
pip install streamlit_multi_menu
```

## Usage instructions

```python
import streamlit as st
from streamlit_multi_menu import streamlit_multi_menu

### Define Menu
sub_menus = {"Finance":["Stock prediction","Turn around rate"],
             "Cars":["Drift","Garage"],
             "Food":["Ramen","Bubble Tea","Kitchen Design"]}

# Optinally you can supply google icons
sub_menu_icons = {
    "Finance": ["trending_up", "sync_alt"], 
    "Cars": ["directions_car", "garage"], 
    "Food": ["restaurant", "local_cafe", "kitchen"]
}

selected_menu = streamlit_multi_menu(menu_titles=list(sub_menus.keys()),
                              sub_menus=sub_menus,
                            sub_menu_icons = sub_menu_icons,
                            use_container_width=True)

if selected_menu != None:
    st.write("The selected menu is:",selected_menu)
```

## Use with images inside sub menu buttons
```python
### Define Menu
sub_menus = {"Finance":["Stock prediction","Turn around rate"],
             "Cars":["Drift","Garage"],
             "Food":["Ramen","Bubble Tea","Kitchen Design"]}

# Optinally you can supply google icons
sub_menu_icons = {
    "Finance": ["trending_up", "sync_alt"],
    "Cars": ["directions_car", "garage"],
    "Food": ["restaurant", "local_cafe", "kitchen"]
}

# Urls for images
list_of_finance_imgs = ["https://cdn1.vectorstock.com/i/1000x1000/09/30/stock-market-background-or-forex-trading-business-vector-29570930.jpg",
                        "https://thumbs.dreamstime.com/b/three-part-cycle-diagram-white-background-53987147.jpg"]

list_of_car_imgs = ["https://as1.ftcdn.net/v2/jpg/02/74/00/80/1000_F_274008098_hp9JCh3EM3UctN4ihEYarXY3c6wM7A0e.jpg",
                    "https://img.freepik.com/free-vector/empty-storehouse-warehouse-interior-factory_1441-3877.jpg?size=626&ext=jpg&ga=GA1.1.1224184972.1710201600&semt=ais"]

# Assign images to corresponding column
sub_menu_imgs = {"Finance":list_of_finance_imgs,
             "Cars":list_of_car_imgs}


selected_menu = streamlit_multi_menu(menu_titles=list(sub_menus.keys()),
                              sub_menus=sub_menus,
                            sub_menu_imgs=sub_menu_imgs,
                            sub_menu_icons = sub_menu_icons,
                             use_container_width=True)

```