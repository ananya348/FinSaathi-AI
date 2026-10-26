

import json
import re
from pathlib import Path

import pandas as pd
import streamlit as st

from src.retriever import retrieve
from src.watsonx_client import generate_answer


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FinSaathi AI",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. THEME
# =========================================================

NAVY = "#101D32"
EMERALD = "#16866A"
GOLD = "#D6B779"
IVORY = "#FBF9F3"

PROJECT_DIR = Path(__file__).resolve().parent
KNOWLEDGE_PATH = PROJECT_DIR / "data" / "financial_knowledge.json"
CHUNKS_PATH = PROJECT_DIR / "data" / "processed" / "chunks.json"

RBI_URL = (
    "https://www.rbi.org.in/commonman/images/"
    "FAME%20Booklet%20second%20edition/"
    "FAME%20Booklet%20English/FAME30072020.pdf"
)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {IVORY};
    }}

    [data-testid="stSidebar"] {{
        background-color: {NAVY};
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    .hero {{
        background: linear-gradient(120deg, {NAVY}, #1B3C50);
        padding: 28px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
    }}

    .hero h1 {{
        color: white;
        margin-bottom: 8px;
    }}

    .hero p {{
        color: #F2F0E8;
        font-size: 16px;
    }}

    .small-note {{
        color: #626B73;
        font-size: 13px;
    }}

    div.stButton > button[kind="primary"] {{
        background-color: {EMERALD};
        border-color: {EMERALD};
    }}

    div[data-testid="stMetric"] {{
        background-color: white;
        padding: 14px;
        border: 1px solid #E8E3D8;
        border-radius: 12px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

@st.cache_data
def load_knowledge():
    """Load the local JSON financial knowledge base."""
    if not KNOWLEDGE_PATH.exists():
        return []

    with open(KNOWLEDGE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("financial_knowledge.json must contain a list.")

    return data


def format_inr(amount):
    return f"₹{amount:,.2f}"


def find_json_matches(question, records, limit=2):
    """Find matching educational summaries in the JSON knowledge base."""
    stopwords = {
        "the", "is", "a", "an", "and", "or", "to", "of",
        "in", "for", "what", "how", "can", "i", "do",
        "my", "me", "it", "on", "with", "about", "should",
        "please", "tell", "explain", "does", "are", "be",
    }

    words = set(re.findall(r"[a-zA-Z0-9]+", question.lower()))
    words -= stopwords

    matches = []

    for record in records:
        keywords = {
            str(word).lower()
            for word in record.get("keywords", [])
        }

        topic_words = set(
            re.findall(
                r"[a-zA-Z0-9]+",
                record.get("topic", "").lower(),
            )
        )

        content_words = set(
            re.findall(
                r"[a-zA-Z0-9]+",
                record.get("content", "").lower(),
            )
        )

        score = (
            3 * len(words & keywords)
            + 2 * len(words & topic_words)
            + len(words & content_words)
        )

        if score > 0:
            matches.append((score, record))

    matches.sort(key=lambda item: item[0], reverse=True)

    return [
        {"score": score, **record}
        for score, record in matches[:limit]
    ]


def show_source_link(name, url):
    if url.startswith(("https://", "http://")):
        st.markdown(f"**Source:** [{name}]({url})")
    else:
        st.write(f"**Source:** {name}")


# =========================================================
# 4. SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("## 💚 FinSaathi AI")
    st.caption("Your financial literacy companion")
    st.divider()

    pages = [
        "Dashboard",
        "AI Assistant",
        "Scam Checker",
        "Budget Planner",
        "Knowledge Sources",
        "About Project",
    ]

    default_page = st.session_state.pop(
        "navigation_target",
        "Dashboard",
    )

    if default_page not in pages:
        default_page = "Dashboard"

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = default_page

    page = st.radio(
        "Navigate",
        pages,
        key="selected_page",
    )

    st.divider()
    st.caption("Learn. Plan. Stay Safe.")
    st.caption("Educational tool — not financial advice.")


# =========================================================
# 5. DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to FinSaathi AI 💚</h1>
            <p>
                Your beginner-friendly companion for financial literacy,
                digital payment safety, budgeting, and fraud awareness.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("What would you like to do today?")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("💬 Financial Assistant")
            st.write(
                "Ask about UPI safety, savings, budgeting, "
                "loans, and financial fraud."
            )

            if st.button(
                "Ask a Question",
                key="dashboard_assistant",
            ):
                st.session_state.navigation_target = "AI Assistant"
                st.rerun()

        with st.container(border=True):
            st.subheader("🛡️ Scam Checker")
            st.write(
                "Review suspicious messages and learn about common "
                "digital-payment scam warning signs."
            )

            if st.button(
                "Check a Message",
                key="dashboard_scam",
            ):
                st.session_state.navigation_target = "Scam Checker"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("💰 Budget Planner")
            st.write(
                "Track monthly expenses and compare your remaining "
                "balance with a savings goal."
            )

            if st.button(
                "Plan My Budget",
                key="dashboard_budget",
            ):
                st.session_state.navigation_target = "Budget Planner"
                st.rerun()

        with st.container(border=True):
            st.subheader("📚 Knowledge Sources")
            st.write(
                "Explore educational records and the official sources "
                "used by the prototype."
            )

            if st.button(
                "Explore Sources",
                key="dashboard_sources",
            ):
                st.session_state.navigation_target = "Knowledge Sources"
                st.rerun()

    st.info(
        "Safety reminder: Never share your UPI PIN, OTP, password, "
        "or CVV with another person."
    )


# =========================================================
# 6. FINANCIAL ASSISTANT — PDF RETRIEVAL + JSON
# =========================================================

elif page == "AI Assistant":

    st.title("💬 FinSaathi AI Financial Assistant")

    st.write(
        "Ask questions about digital payments, budgeting, loans, "
        "savings, investment safety, and financial fraud."
    )

    st.info(
        "FinSaathi AI retrieves relevant passages from the RBI FAME booklet "
        "and uses IBM watsonx.ai Granite to draft an answer grounded in those "
        "passages. Starter JSON records are shown as additional information. "
        "If the model is unavailable or its free usage limit is reached, the "
        "source passages remain available below."
    )

    question = st.text_input(
        "Your financial question",
        placeholder="Example: How can I stay safe when using UPI?",
        key="financial_question",
    )

    use_json = st.checkbox(
        "Also search the starter financial knowledge records",
        value=True,
    )

    if st.button("Search Financial Knowledge", type="primary"):

        if not question.strip():
            st.warning("Please enter a question.")

        else:
            try:
                pdf_results = retrieve(question, top_k=3)

                json_results = []

                if use_json:
                    records = load_knowledge()
                    json_results = find_json_matches(
                        question,
                        records,
                    )

                if not pdf_results and not json_results:
                    st.warning(
                        "No relevant information was found. Try rephrasing "
                        "your question using terms such as UPI, budgeting, "
                        "loan, investment, or fraud."
                    )

                else:
                    st.subheader("FinSaathi AI Answer")

                    if pdf_results:
                        with st.spinner(
                            "Generating an answer with IBM Granite..."
                        ):
                            answer, answer_sources = generate_answer(
                                question,
                                pdf_results,
                            )

                        st.markdown(answer)

                        if answer_sources:
                            with st.expander("Answer sources"):
                                for source in answer_sources:
                                    source_title = (
                                        f"[Source {source['number']}] "
                                        f"{source['source_name']} — page "
                                        f"{source['page']}"
                                    )
                                    source_url = source.get(
                                        "source_url",
                                        "",
                                    )

                                    if source_url.startswith(
                                        ("https://", "http://")
                                    ):
                                        st.markdown(
                                            f"- [{source_title}]"
                                            f"({source_url})"
                                        )
                                    else:
                                        st.markdown(f"- {source_title}")

                    else:
                        st.warning(
                            "No RBI PDF passages were retrieved, so an "
                            "AI-generated answer was not created. Review "
                            "the additional educational information below "
                            "and its linked sources."
                        )

                    st.subheader("Information from the RBI PDF")

                    if pdf_results:
                        for index, result in enumerate(
                            pdf_results,
                            start=1,
                        ):
                            with st.container(border=True):
                                st.markdown(
                                    f"**RBI passage {index} — "
                                    f"Page {result.get('page', 'N/A')}**"
                                )

                                st.write(result.get("text", ""))

                                st.caption(
                                    "Retrieval similarity score: "
                                    f"{result.get('score', 0):.4f}"
                                )

                                show_source_link(
                                    "RBI Financial Awareness Messages (FAME)",
                                    RBI_URL,
                                )
                    else:
                        st.write(
                            "No relevant passage was found in the RBI PDF."
                        )

                    if use_json:
                        st.subheader(
                            "Additional educational information"
                        )

                        if json_results:
                            for result in json_results:
                                with st.container(border=True):
                                    st.markdown(
                                        f"**{result.get('topic', 'Topic')}**"
                                    )

                                    st.write(result.get("content", ""))

                                    show_source_link(
                                        result.get(
                                            "source_name",
                                            "Educational source",
                                        ),
                                        result.get("source_url", ""),
                                    )
                        else:
                            st.write(
                                "No matching starter knowledge record "
                                "was found for this question."
                            )

                    st.caption(
                        "Retrieved information is educational and may "
                        "not cover every aspect of your question. Open "
                        "the official source and read the surrounding "
                        "context before relying on it."
                    )

            except (FileNotFoundError, ValueError, OSError) as error:
                st.error(f"Knowledge retrieval error: {error}")

            except Exception as error:
                st.error(
                    "An unexpected error occurred during retrieval. "
                    "Check the terminal for details."
                )
                st.caption(str(error))

    with st.expander("Explore supported topics"):
        st.write(
            "- UPI and electronic payment safety\n"
            "- Digital banking\n"
            "- Monthly budgeting\n"
            "- Responsible borrowing\n"
            "- Investment warning signs\n"
            "- Reporting cyber financial fraud"
        )

# =========================================================
# 7. SCAM CHECKER
# =========================================================

elif page == "Scam Checker":

    st.title("🛡️ Digital Scam Awareness Checker")

    st.write(
        "Review a suspicious message for common warning signs. "
        "This is a rule-based educational tool, not a definitive "
        "fraud detector."
    )

    st.warning(
        "Do not paste real OTPs, PINs, passwords, CVVs, full account "
        "numbers, card numbers, or other confidential information."
    )

    message = st.text_area(
        "Suspicious message",
        placeholder=(
            "Example: You won a reward! Scan this QR code and enter "
            "your UPI PIN to receive money."
        ),
        height=150,
    )

    if st.button("Analyse Warning Signs", type="primary"):

        if not message.strip():
            st.warning("Please enter a message.")

        else:
            text_message = message.lower()

            warning_patterns = {
                "Urgency or threats": [
                    "urgent",
                    "immediately",
                    "account blocked",
                    "account suspended",
                    "act now",
                    "last chance",
                ],
                "Confidential credential requests": [
                    "share otp",
                    "send otp",
                    "tell me your otp",
                    "share pin",
                    "tell me your pin",
                    "enter your pin",
                    "password",
                    "cvv",
                ],
                "Unexpected prizes or rewards": [
                    "you won",
                    "winner",
                    "prize",
                    "cashback",
                    "free gift",
                    "reward",
                ],
                "Suspicious payment requests": [
                    "scan this qr",
                    "scan qr",
                    "pay processing fee",
                    "send money to receive",
                    "receive money",
                ],
                "Suspicious links or verification requests": [
                    "click this link",
                    "verify your account",
                    "kyc expired",
                    "update kyc",
                    "unknown link",
                ],
                "Possible impersonation": [
                    "bank officer",
                    "police officer",
                    "digital arrest",
                ],
            }

            detected = []

            for category, phrases in warning_patterns.items():
                if any(
                    phrase in text_message
                    for phrase in phrases
                ):
                    detected.append(category)

            st.subheader("Review result")

            if detected:
                st.error(
                    "Potential warning signs found. Treat the message "
                    "cautiously and verify the sender independently."
                )

                for category in detected:
                    st.write(f"⚠️ {category}")

            else:
                st.info(
                    "No configured warning phrase was found. This "
                    "does not establish that the message is safe."
                )

            st.subheader("Safety recommendations")

            st.write(
                "- Never share your UPI PIN, OTP, password, or CVV."
            )
            st.write(
                "- Do not approve an unexpected payment or collect request."
            )
            st.write(
                "- Verify requests through the official bank or service app."
            )
            st.write(
                "- Avoid suspicious links and unknown remote-access apps."
            )

            st.subheader("If money has been lost")

            st.write(
                "In India, contact the cybercrime helpline **1930** "
                "promptly and report the incident at "
                "[cybercrime.gov.in](https://cybercrime.gov.in/). "
                "Notify your bank or payment provider immediately."
            )

            st.caption(
                "The checker cannot guarantee that a message is genuine "
                "or fraudulent."
            )


# =========================================================
# 8. MONTHLY BUDGET PLANNER
# =========================================================

elif page == "Budget Planner":

    st.title("💰 Monthly Budget Planner")

    st.write(
        "Enter your income and expenses to calculate your balance "
        "and see how your budget compares with your savings goal."
    )

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Monthly income (₹)",
            min_value=0.0,
            value=15000.0,
            step=500.0,
        )

    with col2:
        savings_goal = st.number_input(
            "Monthly savings goal (₹)",
            min_value=0.0,
            value=3000.0,
            step=500.0,
        )

    st.subheader("Monthly expenses")

    expense_categories = [
        ("Housing / Rent", 4000.0),
        ("Food / Groceries", 2500.0),
        ("Transport", 1000.0),
        ("Education", 1500.0),
        ("Bills / Utilities", 800.0),
        ("Healthcare", 500.0),
        ("Shopping", 500.0),
        ("Other expenses", 700.0),
    ]

    expenses = {}

    left_col, right_col = st.columns(2)

    for index, (category, default_amount) in enumerate(
        expense_categories
    ):
        target_col = left_col if index % 2 == 0 else right_col

        with target_col:
            expenses[category] = st.number_input(
                f"{category} (₹)",
                min_value=0.0,
                value=default_amount,
                step=100.0,
                key=f"expense_{index}",
            )

    total_expenses = sum(expenses.values())
    balance = income - total_expenses

    savings_rate = (
        balance / income * 100
        if income > 0
        else 0
    )

    st.divider()
    st.subheader("Your budget summary")

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Monthly income", format_inr(income))
    metric2.metric("Total expenses", format_inr(total_expenses))
    metric3.metric("Remaining balance", format_inr(balance))

    if balance < 0:
        st.error(
            f"Your expenses exceed your income by "
            f"{format_inr(abs(balance))}."
        )
    elif balance == 0:
        st.warning(
            "Your entire income is allocated to expenses. "
            "Consider reviewing your budget."
        )
    else:
        st.success(
            f"You have {format_inr(balance)} remaining after "
            "the entered expenses."
        )

    if income > 0:
        st.write(
            f"**Remaining balance as a share of income:** "
            f"{savings_rate:.1f}%"
        )

    if balance >= savings_goal:
        st.success(
            f"Your remaining balance meets your savings goal of "
            f"{format_inr(savings_goal)}."
        )
    else:
        st.info(
            f"You are {format_inr(savings_goal - balance)} below "
            "your savings goal based on the entered amounts."
        )

    st.subheader("Expense breakdown")

    expense_df = pd.DataFrame({
        "Category": list(expenses.keys()),
        "Amount (₹)": list(expenses.values()),
    })

    st.bar_chart(
        expense_df.set_index("Category"),
        y="Amount (₹)",
    )

    export_df = expense_df.copy()
    export_df.loc[len(export_df)] = [
        "Total expenses",
        total_expenses,
    ]
    export_df.loc[len(export_df)] = [
        "Monthly income",
        income,
    ]
    export_df.loc[len(export_df)] = [
        "Remaining balance",
        balance,
    ]
    export_df.loc[len(export_df)] = [
        "Savings goal",
        savings_goal,
    ]

    st.download_button(
        "📥 Download Budget as CSV",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name="finsaathi_monthly_budget.csv",
        mime="text/csv",
    )

    st.caption(
        "Calculations use only the values you enter. "
        "No bank account is connected."
    )

# =========================================================
# 9. KNOWLEDGE SOURCES
# =========================================================

elif page == "Knowledge Sources":

    st.title("📚 Financial Knowledge Sources")

    st.write(
        "Explore the starter educational records and the RBI booklet "
        "used by the current retrieval prototype."
    )

    st.markdown(
        f"**RBI Financial Awareness Messages (FAME):** "
        f"[Open booklet]({RBI_URL})"
    )

    if CHUNKS_PATH.exists():
        try:
            with open(
                CHUNKS_PATH,
                "r",
                encoding="utf-8",
            ) as file:
                chunks = json.load(file)

            st.success(
                f"RBI document passages available: {len(chunks)}"
            )

        except (json.JSONDecodeError, OSError) as error:
            st.error(
                f"Could not read the document passages: {error}"
            )
    else:
        st.warning(
            "The RBI document index is not built yet. Run "
            "`python build_knowledge.py` in your terminal."
        )

    if KNOWLEDGE_PATH.exists():
        try:
            records = load_knowledge()

            st.subheader("Starter knowledge records")

            for record in records:
                with st.container(border=True):
                    st.markdown(
                        f"**{record.get('topic', 'Financial topic')}**"
                    )
                    st.write(record.get("content", ""))

                    show_source_link(
                        record.get(
                            "source_name",
                            "Educational source",
                        ),
                        record.get("source_url", ""),
                    )

        except (
            json.JSONDecodeError,
            OSError,
            ValueError,
        ) as error:
            st.error(
                f"Could not load the JSON records: {error}"
            )

    st.subheader("Other official resources")

    st.markdown(
        "- [NPCI UPI FAQs]"
        "(https://www.npci.org.in/what-we-do/upi/faqs)"
    )
    st.markdown(
        "- [NPCI Fraud Awareness]"
        "(https://www.npci.org.in/fraud-awareness)"
    )
    st.markdown(
        "- [Reserve Bank of India](https://www.rbi.org.in/)"
    )
    st.markdown(
        "- [National Cyber Crime Reporting Portal]"
        "(https://cybercrime.gov.in/)"
    )


# =========================================================
# 10. ABOUT THE PROJECT
# =========================================================

elif page == "About Project":

    st.title("ℹ️ About FinSaathi AI")

    st.markdown(
        """
        ### Project overview

        FinSaathi AI is a financial-literacy prototype intended to help
        users understand basic financial concepts, plan monthly expenses,
        and recognise common digital-payment scam warning signs.

        ### Current modules

        - **Financial Assistant:** Retrieves relevant passages from the RBI
          FAME booklet, uses IBM watsonx.ai Granite to draft a grounded answer,
          and optionally searches starter JSON records.
        - **Scam Checker:** Highlights configured warning phrases.
        - **Budget Planner:** Calculates expenses, remaining balance,
          and savings-goal progress.
        - **Knowledge Sources:** Displays the available knowledge records
          and links to official resources.

        ### Technical stack

        - Python
        - Streamlit
        - Pandas
        - PyPDF
        - scikit-learn TF-IDF retrieval
        - Local JSON document storage

        ### Future improvements

        - Add more official financial-literacy documents.
        - Improve passage ranking and test retrieval accuracy.
        - Test generated answers for grounding and relevance.
        - Add English, Hindi, and Bengali answer support.
        - Add automated tests and deployment options.

        ### Important limitations

        The AI answer depends on retrieved passages and the availability of
        the configured IBM watsonx.ai model. It may be incomplete or incorrect;
        verify important details using the linked official sources. The scam
        checker is not a guaranteed fraud detector. This prototype is not a
        bank or a regulated financial advisory service.
        """
    )


# =========================================================
# 11. FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <p class="small-note" style="text-align:center;">
        💚 FinSaathi AI | Learn. Plan. Stay Safe.<br>
        Educational prototype. Verify important financial information
        through official sources.
    </p>
    """,
    unsafe_allow_html=True,
)
