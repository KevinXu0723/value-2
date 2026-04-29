import streamlit as st

PAGES = {
    "home": {"path": "app.py", "label": "🏠 首页"},
    "valuation": {"path": "pages/app_streamlit.py", "label": "📈 估值工具"},
    "peer": {"path": "pages/peer-analysis.py", "label": "🧭 同行分析"},
    "growth": {"path": "pages/growth.py", "label": "📈 增长率计算器"},
}


def render_top_nav(current: str | None = None):
    # 保险：current 不存在时不高亮任何按钮
    current = current if current in PAGES else None

    cols = st.columns(len(PAGES), gap="small")
    for i, (key, meta) in enumerate(PAGES.items()):
        with cols[i]:
            is_current = key == current

            clicked = st.button(
                meta["label"],
                key=f"top_nav_{key}",
                use_container_width=True,
                type="primary" if is_current else "secondary",
                disabled=is_current,
            )

            if clicked and not is_current:
                st.switch_page(meta["path"])

    st.divider()
