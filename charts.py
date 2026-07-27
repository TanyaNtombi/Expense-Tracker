import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show_category_chart(category_data):
    """Display the spending by category bar chart."""

    if not category_data:
        st.info("No expense data available.")
        return

    chart_df = pd.DataFrame(
        category_data,
        columns=[
            "Category",
            "Total Spending"
        ]
    )

    st.bar_chart(
        chart_df.set_index("Category")
    )


def show_pie_chart(category_data):
    """Display the expense distribution pie chart."""

    if not category_data:
        st.info("No expense data available for the pie chart.")
        return

    pie_df = pd.DataFrame(
        category_data,
        columns=[
            "Category",
            "Total Spending"
        ]
    )

    fig, ax = plt.subplots(figsize=(5, 5))

    values = pie_df["Total Spending"]

    def fmt(pct):
        return f"{pct:.1f}%" if pct >= 5 else ""

    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        autopct=fmt,
        startangle=90,
        pctdistance=0.65,
        counterclock=False,
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 1
        },
        textprops={
            "fontsize": 9
        }
    )

    ax.axis("equal")

    total = values.sum()

    labels = [
        f"{category} — {amount / total * 100:.1f}%"
        for category, amount in zip(
            pie_df["Category"],
            values
        )
    ]

    ax.legend(
        wedges,
        labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    ax.set_title("Expense Distribution")

    plt.tight_layout()

    st.pyplot(fig)


def show_monthly_chart(monthly_data):
    """Display monthly summary and line chart."""

    if not monthly_data:
        st.info("No monthly spending data available.")
        return

    monthly_df = pd.DataFrame(
        monthly_data,
        columns=[
            "Month",
            "Total Spending (R)"
        ]
    )

    st.dataframe(
        monthly_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("## 📈 Monthly Spending Trend")

    monthly_df = monthly_df.set_index("Month")

    st.line_chart(monthly_df)