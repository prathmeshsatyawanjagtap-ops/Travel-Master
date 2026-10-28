import streamlit as st
import plotly.express as px

from planner import (
    recommend_destinations,
    generate_itinerary
)

from budget import (
    calculate_budget,
    allocate_budget
)


st.set_page_config(
    page_title="Travel Master",
    page_icon="✈️",
    layout="wide"
)


# -----------------------------
# PAGE STYLING
# -----------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: #f8fafc;
}

h1, h2, h3 {
    color: #f8fafc;
}

[data-testid="stMetric"] {
    background-color: #172337;
    padding: 18px;
    border-radius: 12px;
}

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    min-height: 45px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HEADER
# -----------------------------

st.title("✈️ Travel Master")

st.markdown(
    "### Your AI-powered personal trip planner"
)

st.write(
    "Plan smarter trips using your budget, "
    "available time and travel preferences."
)

st.divider()


# -----------------------------
# SIDEBAR INPUTS
# -----------------------------

st.sidebar.title("🧳 Plan Your Trip")

origin = st.sidebar.text_input(
    "Starting location",
    value="Pune"
)

budget = st.sidebar.number_input(
    "Total budget (₹)",
    min_value=500,
    max_value=1000000,
    value=5000,
    step=500
)

days = st.sidebar.slider(
    "Available days",
    min_value=1,
    max_value=14,
    value=2
)

travelers = st.sidebar.number_input(
    "Number of travelers",
    min_value=1,
    max_value=20,
    value=1
)

interest = st.sidebar.selectbox(
    "Travel interests",
    [
        "nature",
        "adventure",
        "beach",
        "culture",
        "food",
        "history",
        "mountains",
        "relaxation"
    ]
)

transport = st.sidebar.selectbox(
    "Preferred transport",
    [
        "Any",
        "Train",
        "Bus",
        "Car",
        "Bike"
    ]
)

accommodation = st.sidebar.selectbox(
    "Accommodation preference",
    [
        "Budget",
        "Standard",
        "Premium"
    ]
)

generate = st.sidebar.button(
    "✨ Generate My Trip",
    type="primary"
)


# -----------------------------
# MAIN DASHBOARD
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Your Budget",
    f"₹{budget:,.0f}"
)

col2.metric(
    "Available Time",
    f"{days} days"
)

col3.metric(
    "Travelers",
    int(travelers)
)


st.divider()

st.subheader("🌍 Your Personalized Trip Plan")


if generate:

    if not origin.strip():
        st.error(
            "Please enter your starting location."
        )

    else:

        recommendations = recommend_destinations(
            budget=budget,
            travelers=int(travelers),
            days=days,
            interest=interest
        )

        if not recommendations:

            st.warning(
                "No destinations match the current "
                "budget and duration estimates. "
                "Try changing your budget, duration "
                "or number of travelers."
            )

        else:

            st.success(
                f"Found {len(recommendations)} "
                "potential destinations!"
            )

            st.caption(
                "Estimates use sample destination data. "
                "Live transport and accommodation prices "
                "are not currently checked."
            )

            for index, destination in enumerate(
                recommendations
            ):

                with st.container(border=True):

                    st.subheader(
                        f"📍 {destination['name']}, "
                        f"{destination['state']}"
                    )

                    st.write(
                        destination["description"]
                    )

                    a, b, c = st.columns(3)

                    a.metric(
                        "Estimated Cost",
                        f"₹{destination['estimated_cost']:,.0f}"
                    )

                    a.caption(
                        "Illustrative estimate for the trip"
                    )

                    b.metric(
                        "Remaining Budget",
                        f"₹{budget - destination['estimated_cost']:,.0f}"
                    )

                    c.metric(
                        "Interest Match",
                        (
                            "Yes"
                            if destination["interest_match"]
                            else "Partial"
                        )
                    )

                    if st.button(
                        "View Itinerary",
                        key=f"itinerary_{index}"
                    ):

                        st.session_state[
                            "selected_destination"
                        ] = destination["name"]

            selected = st.session_state.get(
                "selected_destination"
            )

            if selected:

                st.divider()

                st.subheader(
                    f"🗓️ Itinerary for {selected}"
                )

                itinerary = generate_itinerary(
                    selected,
                    days
                )

                for item in itinerary:

                    with st.expander(
                        f"Day {item['day']}"
                    ):

                        st.write(
                            f"🌅 Morning: {item['morning']}"
                        )

                        st.write(
                            f"☀️ Afternoon: {item['afternoon']}"
                        )

                        st.write(
                            f"🌆 Evening: {item['evening']}"
                        )

                budget_split = allocate_budget(
                    budget
                )

                st.subheader("💰 Budget Breakdown")

                fig = px.pie(
                    names=list(budget_split.keys()),
                    values=list(budget_split.values()),
                    hole=0.5,
                    title="Suggested Budget Allocation"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.download_button(
                    label="Download Budget Plan",
                    data=(
                        f"Travel Master Trip Plan\n"
                        f"Starting location: {origin}\n"
                        f"Destination: {selected}\n"
                        f"Budget: ₹{budget}\n"
                        f"Duration: {days} days\n"
                        f"Travelers: {travelers}\n"
                        f"Interest: {interest}\n"
                        f"Preferred transport: {transport}\n"
                        f"Accommodation: {accommodation}\n"
                    ),
                    file_name="travel_master_plan.txt",
                    mime="text/plain"
                )

else:

    st.info(
        "Enter your trip preferences in the sidebar "
        "and click Generate My Trip to begin."
    )

    st.markdown("""
    #### ✨ What Travel Master can help you do

    - Find destinations that fit your estimated budget.
    - Compare potential travel destinations.
    - Generate a basic daily itinerary.
    - Understand your budget allocation.
    - Download your trip plan.
    """)