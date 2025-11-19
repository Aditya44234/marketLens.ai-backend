from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.ai import get_gemini_summary
from .utils.query_helpers import extract_locations, extract_years, determine_query_type, generate_chart, build_prompt
import pandas as pd

@api_view(['POST'])
def analyze_view(request):
    uploaded_file = request.FILES.get('file')
    user_query = request.data.get('query')
    if not uploaded_file:
        return Response({"error": "No file uploaded."}, status=400)
    try:
        df = pd.read_excel(uploaded_file)
        df = df.fillna("")
    except Exception as e:
        return Response({"error": f"Could not parse Excel: {str(e)}"}, status=400)

    all_locations = df['final location'].str.lower().unique()
    analysis_type, locations, years = determine_query_type(user_query, all_locations)

    # Filter data according to analysis_type
    filtered_df = pd.DataFrame()
    if analysis_type == "compare":
        filtered_df = df[df['final location'].str.lower().isin(locations)]
    elif analysis_type == "growth":
        location = locations[0]
        max_year = df['year'].max()
        min_year = max_year - years + 1
        filtered_df = df[
            (df['final location'].str.lower() == location) &
            (df['year'] >= min_year)
        ]
    elif analysis_type == "single":
        filtered_df = df[df['final location'].str.lower() == locations[0]]

    table_data = filtered_df.to_dict(orient='records')
    chart_data = generate_chart(filtered_df, analysis_type, locations, years)

    if not filtered_df.empty:
        prompt = build_prompt(user_query, filtered_df, analysis_type, locations, years)
        ai_summary = get_gemini_summary(prompt)
        summary = ai_summary if ai_summary else f"{user_query}: Unable to get AI summary."
    else:
        summary = f"No data found for '{user_query}'. Check spelling or try another location."

    return Response({
        "summary": summary,
        "chart": chart_data,
        "table": table_data
    })
