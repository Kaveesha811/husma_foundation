import streamlit as st
from database.operations import get_donation_analytics, get_monthly_donation_trend, get_donor_ranking


def generate_donation_report():
    """Generate comprehensive donation report"""
    analytics = get_donation_analytics()
    monthly_trend = get_monthly_donation_trend()
    donor_ranking = get_donor_ranking()

    report = {
        'summary': analytics,
        'monthly_trend': monthly_trend,
        'donor_ranking': donor_ranking
    }

    return report


def display_analytics_dashboard():
    """Display analytics dashboard in Streamlit"""
    report = generate_donation_report()

    st.subheader("📊 Donation Analytics Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Donations",
            f"LKR {report['summary'].get('total_amount', 0):,.2f}"
        )

    with col2:
        st.metric(
            "Average Donation",
            f"LKR {report['summary'].get('average_donation', 0):,.2f}"
        )

    with col3:
        st.metric(
            "Unique Donors",
            report['summary'].get('unique_donors', 0)
        )

    with col4:
        st.metric(
            "Largest Donation",
            f"LKR {report['summary'].get('largest_donation', 0):,.2f}"
        )

    # Monthly Trend
    if report['monthly_trend']:
        st.subheader("📈 Monthly Donation Trend")
        for month_data in report['monthly_trend']:
            st.write(
                f"**{month_data['month']}:** "
                f"LKR {month_data['monthly_total']:,.2f} "
                f"({month_data['donation_count']} donations)"
            )

    # Donor Ranking
    if report['donor_ranking']:
        st.subheader("🏆 Top Donors")
        for i, donor in enumerate(report['donor_ranking'], 1):
            st.write(
                f"{i}. **{donor['name']}** - "
                f"LKR {donor['total_donated']:,.2f} "
                f"({donor['donation_count']} donations)"
            )