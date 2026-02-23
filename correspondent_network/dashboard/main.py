import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8002")


class DashboardApp:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url

    def fetch_results(self, query: str, size: int) -> list:
        try:
            response = requests.get(
                f"{self.api_base_url}/search",
                params={"q": query, "size": size},
                timeout=10,
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except Exception as e:
            st.error(f"API error: {e}")
            return []

    def render(self):
        st.title("🕵️ Correspondent Network – Dashboard")
        st.markdown("Search and explore processed tweet images.")

        with st.sidebar:
            st.header("Search Options")
            query = st.text_input("Search query", placeholder="Enter keywords...")
            size = st.slider("Max results", 1, 50, 10)
            search_clicked = st.button("Search", type="primary")

        if search_clicked or query:
            results = self.fetch_results(query, size)
            st.subheader(f"Results ({len(results)} found)")

            if not results:
                st.info("No results found.")
            else:
                for item in results:
                    with st.expander(f"🖼️ image_id: {item.get('image_id', 'N/A')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Raw Text**")
                            st.text(item.get("raw_text", ""))
                        with col2:
                            st.markdown("**Clean Text**")
                            st.text(item.get("clean_text", ""))

                        analytics = item.get("analytics", {})
                        if analytics:
                            st.markdown("**Analytics**")
                            st.json(analytics)

                        metadata = item.get("metadata", {})
                        if metadata:
                            st.markdown("**Metadata**")
                            st.json(metadata)
        else:
            st.info("Enter a search query and click Search to explore results.")


if __name__ == "__main__":
    app = DashboardApp(API_BASE_URL)
    app.render()
