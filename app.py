import streamlit as st
import sqlparse
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
import re
from sample_queries import SAMPLE_QUERIES

# Page config
st.set_page_config(
    page_title="SQL Formatter & Analyzer",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS with brand colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap');
    
    :root {
        --plum: #5A3050;
        --teal: #0F766E;
        --plum-light: rgba(90, 48, 80, 0.1);
        --teal-light: rgba(15, 118, 110, 0.1);
    }
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, var(--plum) 0%, var(--teal) 100%);
    }
    
    /* Hero section */
    .hero {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        animation: fadeInUp 0.6s ease-out;
    }
    
    .hero h1 {
        color: var(--plum);
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--plum) 0%, var(--teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero p {
        color: #64748b;
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(6px);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(90, 48, 80, 0.15);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
        animation-fill-mode: both;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--plum) 0%, var(--teal) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Code output */
    .code-output {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(6px);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(90, 48, 80, 0.15);
        animation: fadeInUp 0.6s ease-out;
        animation-delay: 0.2s;
        animation-fill-mode: both;
    }
    
    .code-output pre {
        font-family: 'DM Mono', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 8px;
        overflow-x: auto;
    }
    
    /* Syntax highlighting */
    .highlight { background: #f8fafc; }
    .highlight .k { color: var(--plum); font-weight: 600; }  /* Keywords */
    .highlight .n { color: #334155; }  /* Names */
    .highlight .s { color: var(--teal); }  /* Strings */
    .highlight .mi { color: #0891b2; }  /* Numbers */
    .highlight .o { color: #64748b; }  /* Operators */
    .highlight .c { color: #94a3b8; font-style: italic; }  /* Comments */
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--plum) 0%, var(--teal) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(90, 48, 80, 0.3);
    }
    
    /* Text area */
    .stTextArea textarea {
        font-family: 'DM Mono', monospace !important;
        border-radius: 12px !important;
        border: 2px solid rgba(90, 48, 80, 0.2) !important;
        background: white !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--plum) !important;
        box-shadow: 0 0 0 3px rgba(90, 48, 80, 0.1) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: white;
        border-radius: 12px;
        border: 2px solid rgba(90, 48, 80, 0.2);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Stagger animation delays */
    .metric-card:nth-child(1) { animation-delay: 0.1s; }
    .metric-card:nth-child(2) { animation-delay: 0.2s; }
    .metric-card:nth-child(3) { animation-delay: 0.3s; }
    .metric-card:nth-child(4) { animation-delay: 0.4s; }
    .metric-card:nth-child(5) { animation-delay: 0.5s; }
    .metric-card:nth-child(6) { animation-delay: 0.6s; }
</style>
""", unsafe_allow_html=True)


def analyze_sql_complexity(sql_query):
    """Analyze SQL query and return approximate complexity metrics."""
    normalized = re.sub(r"\s+", " ", sql_query).strip()
    upper_sql = normalized.upper()

    metrics = {
        "tables": set(),
        "joins": 0,
        "subqueries": 0,
        "ctes": 0,
        "columns": 0,
        "where_conditions": 0,
    }

    # Track CTE names so we don't count them as physical tables.
    cte_names = {
        match.group(1).lower()
        for match in re.finditer(r"(?:WITH|,)\s*([a-zA-Z_][\w$]*)\s+AS\s*\(", normalized, flags=re.IGNORECASE)
    }
    metrics["ctes"] = len(cte_names)

    metrics["joins"] = len(
        re.findall(r"\b(?:INNER|LEFT|RIGHT|FULL|CROSS)?\s*JOIN\b", upper_sql)
    )
    metrics["subqueries"] = len(re.findall(r"\(\s*SELECT\b", upper_sql))

    for table_match in re.finditer(r"\b(?:FROM|JOIN)\s+([a-zA-Z_][\w.$]*)", normalized, flags=re.IGNORECASE):
        raw_name = table_match.group(1).strip()
        table_name = raw_name.split(".")[-1].lower()
        if table_name not in cte_names:
            metrics["tables"].add(table_name)

    # Count top-level selected columns.
    select_clause = ""
    depth = 0
    start = upper_sql.find("SELECT ")
    if start >= 0:
        i = start + len("SELECT ")
        while i < len(normalized):
            char = normalized[i]
            if char == "(":
                depth += 1
            elif char == ")":
                depth = max(0, depth - 1)
            if depth == 0 and normalized[i : i + 5].upper() == " FROM":
                break
            select_clause += char
            i += 1

    if select_clause.strip():
        col_count = 1
        depth = 0
        for char in select_clause:
            if char == "(":
                depth += 1
            elif char == ")":
                depth = max(0, depth - 1)
            elif char == "," and depth == 0:
                col_count += 1
        metrics["columns"] = col_count

    where_match = re.search(
        r"\bWHERE\b(.*?)(\bGROUP\s+BY\b|\bORDER\s+BY\b|\bHAVING\b|\bLIMIT\b|\bUNION\b|$)",
        upper_sql,
        flags=re.IGNORECASE,
    )
    if where_match:
        where_body = where_match.group(1)
        metrics["where_conditions"] = (
            len(re.findall(r"\bAND\b|\bOR\b", where_body)) + 1
        )

    return metrics


def format_sql(sql_query):
    """Format SQL query with proper indentation"""
    formatted = sqlparse.format(
        sql_query,
        reindent=True,
        keyword_case='upper',
        identifier_case='lower',
        indent_width=2,
        wrap_after=80,
        comma_first=False
    )
    return formatted


def highlight_sql(sql_query):
    """Apply syntax highlighting to SQL"""
    formatter = HtmlFormatter(style='default', noclasses=True)
    highlighted = highlight(sql_query, SqlLexer(), formatter)
    return highlighted


# Hero section
st.markdown("""
<div class="hero">
    <h1>⚡ SQL Formatter & Analyzer</h1>
    <p>Format messy SQL queries and analyze their complexity</p>
</div>
""", unsafe_allow_html=True)


def load_selected_sample():
    selected = st.session_state.get("selected_sample", "Custom")
    if selected == "Custom":
        return
    st.session_state["sql_input"] = SAMPLE_QUERIES[selected]


if "selected_sample" not in st.session_state:
    st.session_state["selected_sample"] = "Custom"
if "sql_input" not in st.session_state:
    st.session_state["sql_input"] = "SELECT * FROM users WHERE status = 'active'"

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input SQL")
    
    # Sample query selector
    st.selectbox(
        "Try a sample query:",
        ["Custom"] + list(SAMPLE_QUERIES.keys()),
        key="selected_sample",
        on_change=load_selected_sample,
    )
    
    sql_input = st.text_area(
        "Paste your SQL query:",
        key="sql_input",
        height=300,
    )
    
    if st.button("🚀 Format & Analyze", use_container_width=True):
        if sql_input.strip():
            # Format the SQL
            formatted_sql = format_sql(sql_input)
            st.session_state['formatted_sql'] = formatted_sql
            
            # Analyze complexity
            metrics = analyze_sql_complexity(sql_input)
            st.session_state['metrics'] = metrics
        else:
            st.warning("Please enter a SQL query first!")

with col2:
    st.subheader("✨ Formatted Output")
    
    if 'formatted_sql' in st.session_state:
        # Display formatted SQL with syntax highlighting
        st.markdown('<div class="code-output">', unsafe_allow_html=True)
        highlighted_sql = highlight_sql(st.session_state['formatted_sql'])
        st.markdown(highlighted_sql, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Copy button
        st.code(st.session_state['formatted_sql'], language='sql')
    else:
        st.info("👈 Enter a SQL query and click 'Format & Analyze' to see results")

# Metrics section
if 'metrics' in st.session_state:
    st.markdown("---")
    st.subheader("📊 Complexity Metrics")
    
    metrics = st.session_state['metrics']
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Tables</div>
            <div class="metric-value">{len(metrics['tables'])}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Joins</div>
            <div class="metric-value">{metrics['joins']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CTEs</div>
            <div class="metric-value">{metrics['ctes']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Subqueries</div>
            <div class="metric-value">{metrics['subqueries']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Columns</div>
            <div class="metric-value">{metrics['columns']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Conditions</div>
            <div class="metric-value">{metrics['where_conditions']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Complexity assessment
    st.markdown("---")
    total_complexity = (
        len(metrics['tables']) + 
        metrics['joins'] * 2 + 
        metrics['ctes'] * 2 + 
        metrics['subqueries'] * 3 + 
        metrics['where_conditions']
    )
    
    if total_complexity < 5:
        complexity_level = "🟢 Low"
        complexity_color = "#10b981"
    elif total_complexity < 15:
        complexity_level = "🟡 Medium"
        complexity_color = "#f59e0b"
    else:
        complexity_level = "🔴 High"
        complexity_color = "#ef4444"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem;">
        <h3 style="color: #64748b; margin-bottom: 1rem;">Query Complexity</h3>
        <div style="font-size: 3rem; font-weight: 700; color: {complexity_color};">
            {complexity_level}
        </div>
        <p style="color: #94a3b8; margin-top: 1rem;">
            Complexity Score: {total_complexity}
        </p>
    </div>
    """, unsafe_allow_html=True)
