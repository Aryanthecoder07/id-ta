import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

st.title("🔍 Selenium Automation Framework (Optimized)")

# ------------------- Streamlit Inputs -------------------
url = st.text_input("Enter Website URL", "https://www.google.com")

st.subheader("➕ Define Test Cases")
num_cases = st.number_input("Number of Test Cases", min_value=1, max_value=10, value=1)

test_cases = []
for i in range(num_cases):
    st.markdown(f"#### Test Case {i+1}")
    element_id = st.text_input(f"Element ID (Test {i+1})", key=f"id_{i}")
    input_text = st.text_input(f"Input Text (Test {i+1})", key=f"text_{i}")
    action = st.selectbox(
        f"Action (Test {i+1})",
        ["Send Keys + Enter", "Click"],
        key=f"action_{i}"
    )
    test_cases.append({"id": element_id, "text": input_text, "action": action})

run = st.button("🚀 Run Test Suite")

# ------------------- Selenium Execution -------------------
if run:
    # URL validation
    if not url.strip():
        st.error("❌ URL cannot be empty.")
    else:
        if not url.startswith("http"):
            url = "https://" + url  # auto-fix missing protocol

        st.write("### Running Selenium Tests...")

        # Keep driver in session_state to reduce startup time
        if "driver" not in st.session_state:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.page_load_strategy = "eager"  # faster loading
            # options.add_argument("--headless")  # Uncomment if you don't need to see the browser
            st.session_state.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )

        driver = st.session_state.driver
        results = []

        try:
            driver.get(url)
            wait = WebDriverWait(driver, 10)

            for idx, tc in enumerate(test_cases, start=1):
                try:
                    elem = wait.until(EC.presence_of_element_located((By.ID, tc["id"])))
                    if tc["action"] == "Send Keys + Enter":
                        elem.clear()
                        elem.send_keys(tc["text"])
                        elem.send_keys(Keys.RETURN)
                    elif tc["action"] == "Click":
                        elem.click()

                    results.append((f"Test {idx}", "✅ PASS", driver.title))
                except Exception as e:
                    results.append((f"Test {idx}", f"❌ FAIL ({e})", ""))

        finally:
            # Optional: keep driver alive for next run
            pass  # don't quit driver here

        # Show results
        st.subheader("📊 Test Results")
        for r in results:
            st.write(f"**{r[0]}** → {r[1]}")
            if r[2]:
                st.caption(f"Page Title: {r[2]}")
