import base64
from pathlib import Path
import pandas as pd
import sel
import altair as alt
import streamlit as st


def streamlit_theme():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75  # noqa

    config = {
        "config": {
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "gridColor": grey_color,
                "domainColor": font_color,
                "tickColor": "#fff",
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


def streamlit_theme_alt():
    font = "IBM Plex Mono"
    primary_color = "#F63366"
    font_color = "#262730"
    grey_color = "#f0f2f6"
    base_size = 16
    lg_font = base_size * 1.25
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.75  # noqa

    config = {
        "config": {
            "view": {"fill": grey_color},
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "grid": True,
                "gridColor": "#fff",
                "gridOpacity": 1,
                "domain": False,
                # "domainColor": font_color,
                "tickColor": font_color,
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                "category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config


category_large = [
    "#f63366",
    "#0068c9",
    "#fffd80",
    "#7c61b0",
    "#ffd37b",
    "#ae5897",
    "#ffa774",
    "#d44a7e",
    "#fd756d",
]

alt.themes.register("streamlit", streamlit_theme)
alt.themes.enable("streamlit")

colnames_item = ['pid', 'b_name', 'title', 'size', 'og_price', 'new_price', 'sold_price', 'is_sold', 'old_date', 'new_date', '%p_change', 'Link']
colnames_seller = ['uname', 'ship_cost', 'amt_sold', 'amt_feedback', 'amt_listings', 'desc', 'amt_likes', 'prf_link', 'feed_link', 'size_desc', 'loc', 'amt_pics', 'Link']

colnames = {
    "pid": "Product ID",
    "b_name": "Brand Name",
    "title": "Title of Listing",
    "size": "Product Tag Size",
    "og_price": "Original Price of Listing",
    "new_price": "New Price of Listing",
    "sold_price": "Price if Listing Sold",
    "is_sold": "Boolean if Listing Sold",
    "old_date": "Original Date Listing was Created",
    "new_date": "Last Time Listing was Bumped",
    "%p_change": "Price Change (%) if Listing Lowered Prices",
    "link": "Original Link of Listing",
    "uname": "Username of Seller",
    "ship_cost": "Cost of Shipping",
    "amt_sold": "Total Number of Items Sold",
    "amt_feedback": "Total Number of Feedback Received",
    "amt_listings": "Total Number of Listings from Seller",
    "desc": "Full Text Description of Listing",
    "amt_likes": "Total Number of Favorites on Listing",
    "prf_link": "Link to Seller's Profile",
    "feed_link": "Link to Seller's Feedback",
    "size_desc": "Full Description to Listing's Size",
    "loc": "Location of Seller (where it's shipped from)",
    "amt_pics": "Number of Pictures in Listing"
}

##### CHARTS ####


def scatter(strain_data): #can convert to price by location
    data = strain_data.rename(columns=colnames)
    org_cts = data["Org Name"].value_counts()
    top_8_orgs = list(org_cts.nlargest(8).index)
    remaining = max(len(org_cts) - 8, 0)
    remaining_str = f"OTHER (n={remaining})"
    data["Supplier"] = data["Org Name"].where(
        data["Org Name"].isin(top_8_orgs), other=remaining_str
    )
    sort_order = top_8_orgs + [remaining_str]

    chart_base = alt.Chart(
        data, title="THC Measurements by Supplier", width=600, height=300
    )
    chart = chart_base.mark_circle(size=100, opacity=0.9).encode(
        x=alt.X("THC Max:Q"),
        y=alt.Y("Supplier", sort=sort_order),
        color=alt.Color(
            "Supplier",
            scale=alt.Scale(range=category_large),
            sort=sort_order,
            legend=None,
        ),
    )
    return chart



def line(strain_data): #price by date
    data = strain_data.rename(columns=colnames)
    chart_base = alt.Chart(
        data, title="THC Measurements by Date", width=600, height=300
    )
    chart = chart_base.mark_circle(strokeWidth=0, opacity=0.8).encode(
        x=alt.X("Test Date:T"), y=alt.Y("THC Max:Q"), color=alt.Color("THC Max:Q",),
    )
    line = (
        chart_base.mark_line(color="#0068c9", size=5, opacity=0.7)
        .transform_window(**{"Rolling Mean": "mean(THC Max)", "frame": [-30, 30]})
        .encode(x="Test Date:T", y="Rolling Mean:Q",)
    )
    return chart + line


def top_strain_suppliers(strain_data):
    top_suppliers = list(strain_data["org_name"].value_counts().head(8).index)
    cmap = dict(zip(top_suppliers, category_large))

    def supplier_colormap(supplier):
        c = cmap.get(supplier)
        if c:
            h = c.lstrip("#")
            r, g, b = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
            rgba = f"rgba({r}, {g}, {b}, 0.5)"
        return f"background-color: {rgba};" if c else "background-color: #fff"

    return supplier_colormap


def get_top_test_values(strain_data):
    top5_test = (
        strain_data.sort_values("thc_max", ascending=False)[
            ["org_name", "date_test", "thc_max"]
        ]
        .head(10)
        .assign(thc_max=lambda d: d["thc_max"].apply("{0:.1f}".format))
    )
    return top5_test


def get_top_test_table(strain_data):
    supplier_colormap = top_strain_suppliers(strain_data)
    top5_tests = get_top_test_values(strain_data)
    styled_table = top5_tests.style.applymap(supplier_colormap, subset=["org_name"])
    return styled_table


#######

#@st.cache
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

#@st.cache
def display_picture(link, length, width, is_sold):
    image_link = sel.get_image(link, is_sold)
    picture_html = f"<center><img src='{image_link}' class='img-fluid' width = '{width}' length = '{length}'></center>"
    st.markdown(picture_html, unsafe_allow_html=True)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
