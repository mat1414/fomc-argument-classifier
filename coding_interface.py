# save as: fomc_arguments/coding_interface.py

"""
FOMC Argument Human Coding Interface
=====================================
Streamlit application for human validation of Claude-generated classifications
of FOMC meeting arguments for Inflation and Employment variables.

Following Mullainathan et al. (2024) framework for LLM output validation.

Usage:
    streamlit run coding_interface.py

Changelog:
    v1.0 - Initial web deployment version
         - Removed local file saving (download button only)
         - Session resume via CSV upload
         - Widget versioning for proper session resume
         - Locked coder name after first save
         - Inflation and Employment variables only
"""
import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
from pathlib import Path
import io


def get_script_directory():
    """Get the directory where this script is located."""
    return Path(__file__).resolve().parent


SCRIPT_DIR = get_script_directory()

# Page configuration
st.set_page_config(
    page_title="FOMC Argument Coding",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_categories():
    """Load argument and data category definitions."""
    arg_cat_path = SCRIPT_DIR / 'validation_samples' / 'production' / 'argument_categories.pkl'
    data_cat_path = SCRIPT_DIR / 'validation_samples' / 'production' / 'data_categories.pkl'

    arg_cat_df = pd.read_pickle(arg_cat_path)
    data_cat_df = pd.read_pickle(data_cat_path)

    return arg_cat_df, data_cat_df


@st.cache_data
def load_coding_data(variable):
    """Load the coding sample data for a specific variable."""
    coding_file = SCRIPT_DIR / 'validation_samples' / 'production' / f'coding_{variable.lower()}.csv'
    if coding_file.exists():
        return pd.read_csv(coding_file)
    return None


@st.cache_data
def load_coding_data_from_upload(file_content):
    """Load coding data from uploaded file."""
    return pd.read_csv(io.StringIO(file_content.decode('utf-8')))


def get_results_csv(results):
    """Convert results to CSV for download."""
    df = pd.DataFrame(results)
    return df.to_csv(index=False).encode('utf-8')


def get_previous_coding(coding_id, results):
    """Get previous coding values for a specific coding_id."""
    for result in results:
        if result.get('coding_id') == coding_id:
            return result
    return None


def validate_resume_csv(resume_df, coding_df):
    """
    Validate that a resume CSV is compatible with the current coding data.

    Returns:
        tuple: (is_valid, message, matching_ids)
    """
    required_cols = {'coding_id', 'coder_name', 'score'}
    if not required_cols.issubset(resume_df.columns):
        missing = required_cols - set(resume_df.columns)
        return False, f"Missing required columns: {missing}", set()

    resume_ids = set(resume_df['coding_id'].tolist())
    coding_ids = set(coding_df['coding_id'].tolist())

    matching_ids = resume_ids.intersection(coding_ids)
    unmatched_ids = resume_ids - coding_ids

    if len(matching_ids) == 0:
        return False, "No coding_ids in resume file match current data source", set()

    if len(unmatched_ids) > 0:
        return True, f"Warning: {len(unmatched_ids)} coding_ids in resume file not found in current data (will be ignored)", matching_ids

    return True, f"Successfully validated {len(matching_ids)} coded arguments", matching_ids


def initialize_session_state():
    """Initialize all session state variables."""
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'coded_ids' not in st.session_state:
        st.session_state.coded_ids = set()
    if 'widget_version' not in st.session_state:
        st.session_state.widget_version = 0
    if 'locked_coder_name' not in st.session_state:
        st.session_state.locked_coder_name = None
    if 'locked_variable' not in st.session_state:
        st.session_state.locked_variable = None


def main():
    st.title("FOMC Argument Human Coding Interface")
    st.markdown("**Human Validation of LLM Classifications**")
    st.markdown("---")

    # Initialize session state
    initialize_session_state()

    # Check for required files
    required_files = [
        'validation_samples/production/argument_categories.pkl',
        'validation_samples/production/data_categories.pkl'
    ]
    missing_files = [f for f in required_files if not (SCRIPT_DIR / f).exists()]

    if missing_files:
        st.error("Missing required files. Please ensure all data files are present.")
        st.stop()

    # Load categories
    try:
        arg_cat_df, data_cat_df = load_categories()
    except Exception as e:
        st.error(f"Error loading category files: {e}")
        st.stop()

    # Sidebar setup
    with st.sidebar:
        st.header("Coding Setup")

        # Coder identification
        if st.session_state.locked_coder_name is not None:
            st.text_input(
                "Your Name (locked)",
                value=st.session_state.locked_coder_name,
                disabled=True,
                help="Name is locked after first save to ensure consistency"
            )
            coder_name = st.session_state.locked_coder_name
        else:
            coder_name = st.text_input(
                "Your Name",
                placeholder="Enter your name",
                help="Used to identify your coding results. Will be locked after first save."
            )

        if not coder_name:
            st.warning("Please enter your name to begin")
            st.stop()

        # Variable selection
        if st.session_state.locked_variable is not None:
            st.selectbox(
                "Economic Variable (locked)",
                [st.session_state.locked_variable],
                disabled=True,
                help="Variable is locked after first save"
            )
            variable = st.session_state.locked_variable
        else:
            variable = st.selectbox(
                "Economic Variable",
                ["Inflation", "Employment"],
                help="Select which variable you're coding"
            )

        # Data source
        st.markdown("---")
        st.subheader("Data Source")

        data_source = st.radio(
            "Choose data source:",
            ["Use default sample", "Upload custom file"],
            help="Use the pre-loaded sample or upload your own CSV"
        )

        coding_df = None

        if data_source == "Use default sample":
            coding_df = load_coding_data(variable)
            if coding_df is None:
                st.error(f"Default coding file for {variable} not found.")
                st.stop()
            else:
                st.success(f"Loaded {len(coding_df)} {variable} arguments")
        else:
            uploaded_file = st.file_uploader(
                "Upload Coding File",
                type=['csv'],
                help="Upload a coding CSV file"
            )
            if uploaded_file:
                coding_df = load_coding_data_from_upload(uploaded_file.getvalue())
                st.success(f"Loaded {len(coding_df)} arguments")
            else:
                st.info("Please upload a coding file")
                st.stop()

    total_arguments = len(coding_df)
    current_index = st.session_state.current_index
    v = st.session_state.widget_version

    # Get variable-specific categories
    var_categories = arg_cat_df[arg_cat_df['variable'] == variable]

    # Progress tracking in sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("Progress")

        n_coded = len(st.session_state.coded_ids)
        progress_pct = n_coded / total_arguments if total_arguments > 0 else 0
        st.progress(progress_pct)
        st.write(f"Coded: {n_coded} / {total_arguments}")
        st.write(f"Current: Argument {current_index + 1}")
        st.write(f"Variable: {variable}")

        # Download results button
        st.markdown("---")
        st.subheader("Save Results")

        if st.session_state.results:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = coder_name.lower().replace(' ', '_')
            filename = f"coded_{safe_name}_{variable.lower()}_{timestamp}.csv"

            st.download_button(
                label="Download Results CSV",
                data=get_results_csv(st.session_state.results),
                file_name=filename,
                mime="text/csv",
                help="Download your coding results"
            )
            st.caption(f"{len(st.session_state.results)} arguments coded")
        else:
            st.info("Code some arguments to enable download")

        # Resume session
        st.markdown("---")
        st.subheader("Resume Session")

        resume_file = st.file_uploader(
            "Upload previous session",
            type=['csv'],
            key="resume_upload",
            help="Upload a previously downloaded results file to continue"
        )

        if resume_file:
            if st.button("Load Session"):
                try:
                    resume_df = pd.read_csv(resume_file)

                    is_valid, message, matching_ids = validate_resume_csv(resume_df, coding_df)

                    if not is_valid:
                        st.error(f"Cannot load session: {message}")
                    else:
                        if "Warning" in message:
                            st.warning(message)

                        valid_results = resume_df[resume_df['coding_id'].isin(matching_ids)].to_dict('records')

                        st.session_state.results = valid_results
                        st.session_state.coded_ids = set(r['coding_id'] for r in valid_results)

                        # Lock coder name and variable from resume file
                        if len(valid_results) > 0:
                            st.session_state.locked_coder_name = valid_results[0].get('coder_name', coder_name)
                            st.session_state.locked_variable = valid_results[0].get('variable', variable)

                        # Increment widget version
                        st.session_state.widget_version += 1

                        # Jump to first uncoded argument
                        found_uncoded = False
                        for idx in range(len(coding_df)):
                            if coding_df.iloc[idx]['coding_id'] not in st.session_state.coded_ids:
                                st.session_state.current_index = idx
                                found_uncoded = True
                                break

                        if not found_uncoded:
                            st.session_state.current_index = len(coding_df) - 1

                        st.success(f"Loaded {len(valid_results)} coded arguments")
                        st.rerun()

                except Exception as e:
                    st.error(f"Error loading session: {e}")

    # Main coding area
    if current_index < total_arguments:
        current_row = coding_df.iloc[current_index]
        coding_id = current_row['coding_id']
        quotation = current_row['quotation']
        description = current_row.get('description', None)
        explanation = current_row.get('explanation', None)

        is_coded = coding_id in st.session_state.coded_ids
        previous_coding = get_previous_coding(coding_id, st.session_state.results) if is_coded else None

        # Display quotation
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader(f"Quotation ({coding_id})")

            if is_coded:
                st.success("Already coded - you can update or skip")

            st.markdown(
                f"""<div style="background-color: #f0f2f6; padding: 20px;
                border-radius: 10px; min-height: 200px; font-size: 16px; line-height: 1.6;">
                {quotation}
                </div>""",
                unsafe_allow_html=True
            )

            if pd.notna(description) and str(description).strip():
                st.markdown("**Description:**")
                st.markdown(
                    f"""<div style="background-color: #e8f4f8; padding: 15px;
                    border-radius: 8px; font-size: 14px; line-height: 1.5; margin-top: 10px;">
                    {description}
                    </div>""",
                    unsafe_allow_html=True
                )

            if pd.notna(explanation) and str(explanation).strip():
                st.markdown("**Explanation:**")
                st.markdown(
                    f"""<div style="background-color: #fff4e6; padding: 15px;
                    border-radius: 8px; font-size: 14px; line-height: 1.5; margin-top: 10px;">
                    {explanation}
                    </div>""",
                    unsafe_allow_html=True
                )

        with col2:
            st.subheader("Coding Tasks")

            # 1. Score
            st.markdown("#### 1. Outlook Score")
            score_val = previous_coding.get('score', 0) if previous_coding else 0
            default_score = int(score_val) if isinstance(score_val, (int, float)) and not pd.isna(score_val) else 0

            score = st.number_input(
                f"{variable} Outlook (-3 to +3)",
                min_value=-3,
                max_value=3,
                value=default_score,
                step=1,
                key=f"score_{current_index}_v{v}",
                help=f"Score from -3 (strong negative {variable.lower()}) to +3 (strong positive {variable.lower()})"
            )

            st.caption("-3 (Strong Negative) ... 0 (Neutral) ... +3 (Strong Positive)")

            # 2. Information Citation
            st.markdown("#### 2. Information Source")
            cites_val = previous_coding.get('cites_data', 'No') if previous_coding else 'No'
            default_cites = cites_val if isinstance(cites_val, str) else 'No'

            cites_data = st.radio(
                "Does the speaker cite specific data or information?",
                ["Yes", "No"],
                index=0 if default_cites == "Yes" else 1,
                key=f"cites_data_{current_index}_v{v}",
                help="Look for references to statistics, reports, or specific observations"
            )

            # 2a. Data Categories (conditional)
            data_categories = []
            data_category_other = None

            data_cats_val = previous_coding.get('data_categories', '') if previous_coding else ''
            prev_data_cats = data_cats_val.split('; ') if isinstance(data_cats_val, str) and data_cats_val else []
            data_other_val = previous_coding.get('data_category_other', '') if previous_coding else ''
            prev_data_other = data_other_val if isinstance(data_other_val, str) else ''

            if cites_data == "Yes":
                st.markdown("##### Data Source Categories (check all that apply)")

                for idx, row in data_cat_df.iterrows():
                    default_checked = row['name'] in prev_data_cats

                    if st.checkbox(
                        row['name'],
                        value=default_checked,
                        key=f"data_cat_{idx}_{current_index}_v{v}",
                        help=row['description']
                    ):
                        data_categories.append(row['name'])

                default_other_checked = "Other / No Good Match" in prev_data_cats
                if st.checkbox(
                    "Other / No Good Match",
                    value=default_other_checked,
                    key=f"data_cat_other_{current_index}_v{v}"
                ):
                    data_categories.append("Other / No Good Match")
                    data_category_other = st.text_area(
                        "Please describe the data source:",
                        value=prev_data_other if prev_data_other else "",
                        max_chars=200,
                        key=f"data_category_other_text_{current_index}_v{v}"
                    )

            # 2b. Information Type
            information_type = None
            if cites_data == "Yes":
                st.markdown("##### Information Access")
                info_type_val = previous_coding.get('information_type', 'Public Information') if previous_coding else 'Public Information'
                prev_info_type = info_type_val if isinstance(info_type_val, str) else 'Public Information'

                information_type = st.radio(
                    "Information type:",
                    ["Public Information", "Private/Specialized Information"],
                    index=0 if prev_info_type == "Public Information" else 1,
                    key=f"information_type_{current_index}_v{v}",
                    help="Public = available to all; Private = special access or contacts"
                )

            # 3. Argument Category
            st.markdown("#### 3. Macroeconomic Category")

            category_options = var_categories['name'].tolist() + ["Other / No Good Match"]

            arg_cat_val = previous_coding.get('argument_category', category_options[0]) if previous_coding else category_options[0]
            prev_arg_cat = arg_cat_val if isinstance(arg_cat_val, str) else category_options[0]
            default_cat_index = category_options.index(prev_arg_cat) if prev_arg_cat in category_options else 0

            argument_category = st.selectbox(
                "Select the best category:",
                category_options,
                index=default_cat_index,
                key=f"argument_category_{current_index}_v{v}",
                help="Choose the category that best describes the economic argument"
            )

            argument_category_other = None
            if argument_category == "Other / No Good Match":
                arg_other_val = previous_coding.get('argument_category_other', '') if previous_coding else ''
                prev_arg_other = arg_other_val if isinstance(arg_other_val, str) else ''
                argument_category_other = st.text_area(
                    "Please describe why no category fits:",
                    value=prev_arg_other,
                    max_chars=200,
                    key=f"argument_category_other_{current_index}_v{v}"
                )

            # 4. Notes
            st.markdown("#### 4. Additional Notes (Optional)")
            notes_val = previous_coding.get('notes', '') if previous_coding else ''
            prev_notes = notes_val if isinstance(notes_val, str) else ''

            notes = st.text_area(
                "Any additional observations:",
                value=prev_notes,
                max_chars=500,
                key=f"notes_{current_index}_v{v}",
                help="Optional: flag any issues or ambiguities"
            )

        # Navigation
        st.markdown("---")
        col_prev, col_save, col_next, col_jump = st.columns([1, 2, 1, 2])

        with col_prev:
            if st.button("Previous", disabled=(current_index == 0), use_container_width=True):
                st.session_state.current_index -= 1
                st.rerun()

        with col_save:
            if st.button("Save & Continue", type="primary", use_container_width=True):
                # Lock coder name and variable on first save
                if st.session_state.locked_coder_name is None:
                    st.session_state.locked_coder_name = coder_name
                if st.session_state.locked_variable is None:
                    st.session_state.locked_variable = variable

                result = {
                    'coding_id': coding_id,
                    'coder_name': st.session_state.locked_coder_name,
                    'variable': st.session_state.locked_variable,
                    'score': score,
                    'cites_data': cites_data,
                    'data_categories': '; '.join(data_categories) if data_categories else None,
                    'data_category_other': data_category_other,
                    'information_type': information_type,
                    'argument_category': argument_category,
                    'argument_category_other': argument_category_other,
                    'notes': notes,
                    'coded_at': datetime.now().isoformat()
                }

                # Update or append
                existing_idx = None
                for i, r in enumerate(st.session_state.results):
                    if r['coding_id'] == coding_id:
                        existing_idx = i
                        break

                if existing_idx is not None:
                    st.session_state.results[existing_idx] = result
                else:
                    st.session_state.results.append(result)

                st.session_state.coded_ids.add(coding_id)

                st.success(f"Saved! ({len(st.session_state.results)} total)")

                if current_index < total_arguments - 1:
                    st.session_state.current_index += 1
                    st.rerun()

        with col_next:
            if st.button("Skip", disabled=(current_index == total_arguments - 1), use_container_width=True):
                st.session_state.current_index += 1
                st.rerun()

        with col_jump:
            jump_to = st.number_input(
                "Jump to:",
                min_value=1,
                max_value=total_arguments,
                value=current_index + 1,
                step=1,
                key=f"jump_{current_index}_v{v}"
            )
            if st.button("Go", use_container_width=True):
                st.session_state.current_index = jump_to - 1
                st.rerun()

    else:
        st.success("All arguments have been reviewed!")
        st.info(f"Total coded: {len(st.session_state.coded_ids)} / {total_arguments}")

        st.markdown("### Download your results:")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = coder_name.lower().replace(' ', '_')
        filename = f"coded_{safe_name}_{variable.lower()}_{timestamp}.csv"

        st.download_button(
            label="Download Results CSV",
            data=get_results_csv(st.session_state.results),
            file_name=filename,
            mime="text/csv",
            type="primary"
        )

        if st.button("Return to Start"):
            st.session_state.current_index = 0
            st.rerun()

    # Category reference panel
    with st.expander("Category Reference Guide"):
        tab1, tab2 = st.tabs(["Argument Categories", "Data Categories"])

        with tab1:
            st.subheader(f"{variable} Argument Categories")
            var_cats = arg_cat_df[arg_cat_df['variable'] == variable][['name', 'description']]
            for _, row in var_cats.iterrows():
                st.markdown(f"**{row['name']}**")
                st.markdown(f"*{row['description']}*")
                st.markdown("---")

        with tab2:
            st.subheader("Data Source Categories")
            for _, row in data_cat_df.iterrows():
                st.markdown(f"**{row['name']}**")
                st.markdown(f"*{row['description']}*")
                st.markdown("---")

    # Coding guidelines
    with st.expander("Coding Guidelines"):
        st.markdown("""
        ### Score Guidelines
        - **-3**: Strong negative outlook (expecting significant contraction/decline)
        - **-2**: Moderate negative outlook
        - **-1**: Slight negative outlook
        - **0**: Neutral/trend growth
        - **+1**: Slight positive outlook
        - **+2**: Moderate positive outlook
        - **+3**: Strong positive outlook

        ### What Counts as "Citing Data"?

        A quotation **"cites data"** if the speaker's argument relies on or references empirical information.

        **DOES cite data:**
        - Explicit references to statistics, reports, or indicators
        - Implicit references to measured phenomena (e.g., "inflation has accelerated")
        - Anecdotal evidence from specific sources (e.g., "contacts in my district report...")
        - References to trends or conditions requiring observational evidence
        - References to forecasts or projections based on data

        **DOES NOT cite data:**
        - Pure policy preferences without empirical support
        - Theoretical or conceptual arguments not grounded in observations
        - Procedural or process-oriented statements
        - Hypothetical scenarios without reference to actual conditions

        ### Information Type
        - **Public**: Data available to all (government statistics, market prices)
        - **Private/Specialized**: Internal Fed analysis, business contacts, special surveys
        """)


if __name__ == "__main__":
    main()
