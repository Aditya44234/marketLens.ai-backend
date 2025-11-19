import re

def extract_locations(query, all_locations):
    return [loc for loc in all_locations if loc in query.lower()]

def extract_years(query):
    m = re.search(r'last (\d+) year', query.lower())
    return int(m.group(1)) if m else None

def determine_query_type(query, all_locations):
    q = query.strip().lower()
    locs = extract_locations(q, all_locations)
    years = extract_years(q)
    if 'compare' in q and len(locs) == 2:
        return "compare", locs, years
    elif 'price growth' in q and locs and years:
        return "growth", locs, years
    elif len(locs) == 1:
        return "single", locs, years
    return None, locs, years

def generate_chart(filtered_df, analysis_type, locations, years):
    if not filtered_df.empty:
        if analysis_type == "compare":
            chart_df = (
                filtered_df.groupby(['final location', 'year'])['total sold - igr']
                .sum().reset_index()
            )
            return {
                "labels": chart_df['year'].astype(str).unique().tolist(),
                "datasets": [
                    {
                        "label": f"{loc.title()} Total Sold (IGR)",
                        "data": chart_df[chart_df['final location'] == loc]['total sold - igr'].tolist()
                    } for loc in chart_df['final location'].unique()
                ]
            }
        else:
            chart_df = filtered_df.groupby('year')['total sold - igr'].sum().reset_index()
            return {
                "labels": chart_df["year"].astype(str).tolist(),
                "datasets": [
                    {
                        "label": f"Total Sold (IGR) - {locations[0].title()}",
                        "data": chart_df["total sold - igr"].tolist()
                    }
                ]
            }
    return {"labels": [], "datasets": []}

def build_prompt(user_query, filtered_df, analysis_type, locations, years):
    prompt_df = filtered_df.copy()
    if len(prompt_df) > 30:
        prompt_df = prompt_df.head(30)
    if analysis_type == "compare":
        return (
            f"User question: {user_query}\n"
            f"Here is the relevant real estate data for comparison:\n"
            f"{prompt_df.to_string(index=False)}\n"
            "Compare the demand/sales trends between the two places and return a summary for a real estate stakeholder.Respond in concise and correct way , short summary about 1 para of 4-6 lines"
        )
    elif analysis_type == "growth":
        return (
            f"User question: {user_query}\n"
            f"Here is the price data for {locations[0].title()} over the last {years} years:\n"
            f"{prompt_df.to_string(index=False)}\n"
            "Give insights on price growth and trend over this recent period for a stakeholder.Respond in concise and correct way , short summary about 1 para of 4-6 lines "
        )
    else:
        return (
            f"User question: {user_query}\n"
            f"Here is the relevant real estate data for {locations[0].title()}:\n"
            f"{prompt_df.to_string(index=False)}\n"
            "Please analyze the market trends and return a concise summary for a real estate stakeholder.Respond in concise and correct way , short summary about 1 para of 4-6 lines"
        )
