import streamlit as st
import datetime
import base64
import json
import io
from fpdf import FPDF

st.set_page_config(page_title="Crochet Companion", page_icon="🧶", layout="wide")

st.title("🧶 Crochet Companion")

# Sidebar Navigation
page = st.sidebar.radio("Go to", [
    "Stitch Counter", 
    "Pattern Library", 
    "Progress Tracker", 
    "Yarn Inventory",
    "Photos",
    "Dashboard",
    "Save & Load",
    "Print & PDF"
])

# ---------------- STITCH COUNTER ----------------
if page == "Stitch Counter":
    st.header("Stitch Counter")

    if 'rows' not in st.session_state:
        st.session_state.rows = []

    with st.form("Add Row"):
        row_label = st.text_input("Row Name (e.g. Row 1)")
        stitch_target = st.number_input("Stitches in this row", min_value=1, value=10)
        pattern_link = st.text_input("Linked Pattern (optional)")
        notes = st.text_area("Row Notes (optional)")
        if st.form_submit_button("➕ Add Row"):
            st.session_state.rows.append({
                "name": row_label,
                "target": stitch_target,
                "done": 0,
                "pattern": pattern_link,
                "notes": notes,
                "timestamp": str(datetime.datetime.now())
            })
            st.success(f"Added {row_label} with {stitch_target} stitches")

    if st.session_state.rows:
        st.subheader("Row Progress")
        sort_option = st.selectbox("Sort Rows By", ["Newest First", "Oldest First", "Alphabetical"])
        rows = st.session_state.rows.copy()

        if sort_option == "Newest First":
            rows.sort(key=lambda x: x['timestamp'], reverse=True)
        elif sort_option == "Oldest First":
            rows.sort(key=lambda x: x['timestamp'])
        else:
            rows.sort(key=lambda x: x['name'].lower())

        for idx, row in enumerate(rows):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{row['name']}** - {row['pattern'] if row['pattern'] else 'No linked pattern'}")
                st.caption(f"🕒 Added: {row['timestamp'][:19]}")
                if row['notes']:
                    st.info(f"📝 {row['notes']}")
                updated = st.slider(
                    f"Stitches Completed for {row['name']}",
                    min_value=0,
                    max_value=row['target'],
                    value=row['done'],
                    key=f"row_{row['name']}"
                )
                row['done'] = updated
                st.progress(updated / row['target'])
            with col2:
                if st.button("❌ Remove", key=f"remove_row_{row['name']}"):
                    st.session_state.rows = [r for r in st.session_state.rows if r['name'] != row['name']]
                    st.experimental_rerun()

        total_stitches = sum(r['done'] for r in st.session_state.rows)
        total_target = sum(r['target'] for r in st.session_state.rows)
        overall_progress = total_stitches / total_target if total_target > 0 else 0
        st.subheader("Overall Stitch Progress")
        st.progress(overall_progress)
        st.success(f"🧵 {total_stitches} stitches completed out of {total_target} total")
    else:
        st.info("Add a row to start tracking your stitches.")

# ---------------- PATTERN LIBRARY ----------------
elif page == "Pattern Library":
    st.header("📖 Pattern Library")

    if 'patterns' not in st.session_state:
        st.session_state.patterns = []

    new_name = st.text_input("Pattern Name")
    new_text = st.text_area("Pattern Instructions")
    if st.button("📌 Save Pattern") and new_name and new_text:
        st.session_state.patterns.append({
            "name": new_name,
            "text": new_text,
            "timestamp": str(datetime.datetime.now())
        })
        st.success("Pattern saved!")

    st.subheader("Your Patterns")
    for pattern in st.session_state.patterns:
        with st.expander(f"{pattern['name']} ({pattern['timestamp'][:10]})"):
            st.text(pattern["text"])

# ---------------- PROGRESS TRACKER ----------------
elif page == "Progress Tracker":
    st.header("🎯 Goal Tracker")

    if 'goals' not in st.session_state:
        st.session_state.goals = []

    goal_name = st.text_input("New Goal")
    goal_total = st.number_input("Target Count", min_value=1)
    if st.button("➕ Add Goal") and goal_name:
        st.session_state.goals.append({
            "goal": goal_name,
            "target": goal_total,
            "done": 0
        })

    for goal in st.session_state.goals:
        st.markdown(f"**{goal['goal']}**")
        progress = st.slider(
            f"Progress for {goal['goal']}", 
            min_value=0, 
            max_value=goal['target'], 
            value=goal['done'], 
            key=goal['goal']
        )
        goal['done'] = progress
        st.progress(progress / goal['target'])


# ... (previous code unchanged)

# ---------------- YARN INVENTORY ----------------
elif page == "Yarn Inventory":
    st.header("🧶 Yarn Stash")

    if 'yarn' not in st.session_state:
        st.session_state.yarn = []

    with st.form("yarn_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            yarn_type = st.text_input("Yarn Type")
        with col2:
            brand = st.text_input("Brand")
        with col3:
            color = st.text_input("Color")

        project = st.text_input("Allocated to Project")
        quantity = st.number_input("Amount (skeins)", min_value=0)
        notes = st.text_area("Notes")

        submitted = st.form_submit_button("➕ Add Yarn")
        if submitted:
            st.session_state.yarn.append({
                "type": yarn_type,
                "brand": brand,
                "color": color,
                "qty": quantity,
                "project": project,
                "notes": notes,
                "timestamp": str(datetime.datetime.now())
            })
            st.success("Yarn entry added!")

    st.subheader("Inventory")
    sort_option = st.selectbox("Sort Yarn By", ["Newest First", "Oldest First", "Brand", "Color"])
    yarn_list = st.session_state.yarn.copy()

    if sort_option == "Newest First":
        yarn_list.sort(key=lambda x: x['timestamp'], reverse=True)
    elif sort_option == "Oldest First":
        yarn_list.sort(key=lambda x: x['timestamp'])
    elif sort_option == "Brand":
        yarn_list.sort(key=lambda x: x['brand'].lower())
    elif sort_option == "Color":
        yarn_list.sort(key=lambda x: x['color'].lower())

    for idx, y in enumerate(yarn_list):
        with st.expander(f"{y['brand']} {y['type']} ({y['color']})"):
            st.write(f"**Quantity:** {y['qty']} skeins")
            st.write(f"**Allocated to:** {y['project'] or 'Unassigned'}")
            st.write(f"**Notes:** {y['notes']}")
            st.write(f"🕒 Added: {y['timestamp'][:19]}")
            if st.button("❌ Remove", key=f"remove_yarn_{idx}"):
                st.session_state.yarn = [item for item in st.session_state.yarn if item != y]
                st.experimental_rerun()

# ---------------- PHOTO UPLOADS ----------------
elif page == "Photos":
    st.header("📸 Project Photos")

    if 'photos' not in st.session_state:
        st.session_state.photos = []

    photo = st.file_uploader("Upload a project photo", type=["jpg", "jpeg", "png"])
    caption = st.text_input("Caption for this photo")
    tag = st.text_input("Tag/Project Name (optional)")

    if photo and st.button("📷 Save Photo"):
        b64 = base64.b64encode(photo.getvalue()).decode()
        st.session_state.photos.append({"img": b64, "caption": caption, "tag": tag})
        st.success("Photo saved!")

    st.subheader("Gallery")
    filter_tag = st.text_input("Filter by Tag (leave blank to show all)")
    for p in st.session_state.photos:
        if not filter_tag or filter_tag.lower() in (p.get("tag") or "").lower():
            st.image(base64.b64decode(p["img"]), caption=f"{p['caption']} - {p.get('tag', '')}", width=300)

# ---------------- DASHBOARD ----------------
elif page == "Dashboard":
    st.header("📊 Stats Dashboard")

    st.subheader("Total Stitches")
    total_stitches = sum(r['done'] for r in st.session_state.get('rows', []))
    st.metric("🧵 Stitches", total_stitches)

    # Award system
    st.subheader("🏅 Achievements")
    awards = []
    if total_stitches >= 10:
        awards.append("🥉 Novice Stitcher (10+ stitches)")
    if total_stitches >= 25:
        awards.append("📎 Consistent Crafter (25+ stitches)")
    if total_stitches >= 50:
        awards.append("🥈 Skilled Stitcher (50+ stitches)")
    if total_stitches >= 75:
        awards.append("🧷 Committed Crafter (75+ stitches)")
    if total_stitches >= 100:
        awards.append("🥇 Master Stitcher (100+ stitches)")
    if total_stitches >= 150:
        awards.append("🧶 Needle Ninja (150+ stitches)")
    if total_stitches >= 200:
        awards.append("🪡 Thread Tycoon (200+ stitches)")
    if total_stitches >= 250:
        awards.append("🏆 Legendary Crafter (250+ stitches)")
    if total_stitches >= 500:
        awards.append("🌟 Artisan of Yarn (500+ stitches)")
    if total_stitches >= 1000:
        awards.append("🌈 Fiber Enthusiast (1000+ stitches)")
    if total_stitches >= 5000:
        awards.append("🎖️ Precision Prodigy (5000+ stitches)")
    if total_stitches >= 10000:
        awards.append("🧵 Marathon Maker (10000+ stitches)")
    if total_stitches >= 25000:
        awards.append("🔱 Supreme Stitch Sorcerer (25,000+ stitches)")
    if total_stitches >= 50000:
        awards.append("👑 Crochet Commander (50,000+ stitches)")
    if total_stitches >= 100000:
        awards.append("🏅 Immortal Hook Hero (100,000+ stitches)")

    # Other achievement types
    total_goals = len(st.session_state.get('goals', []))
    total_photos = len(st.session_state.get('photos', []))
    total_yarns = len(st.session_state.get('yarn', []))
    total_rows = len(st.session_state.get('rows', []))
    completed_projects = sum(1 for g in st.session_state.get('goals', []) if g['done'] >= g['target'])

    if total_goals >= 5:
        awards.append("🎯 Goal Getter (5+ goals set)")
    if total_goals >= 10:
        awards.append("🎯 Focused Finisher (10+ goals set)")
    if completed_projects >= 1:
        awards.append("🏁 First Finish (1 project completed)")
    if completed_projects >= 5:
        awards.append("🏅 Project Champion (5 projects completed)")
    if completed_projects >= 10:
        awards.append("🎉 Achievement Addict (10 projects completed)")
    if total_rows >= 10:
        awards.append("📏 Row Rookie (10 rows tracked)")
    if total_rows >= 25:
        awards.append("📐 Pattern Pacer (25 rows tracked)")
    if total_rows >= 50:
        awards.append("📊 Precision Planner (50 rows tracked)")
    if total_rows >= 100:
        awards.append("📘 Structured Stitcher (100 rows tracked)")
    if total_rows >= 250:
        awards.append("📙 Routine Row Renegade (250 rows tracked)")
    if total_rows >= 500:
        awards.append("📗 Epic Row Engineer (500 rows tracked)")

    # Daily streak tracking (bonus achievement idea)
    if 'activity_log' not in st.session_state:
        st.session_state.activity_log = set()
    today = str(datetime.date.today())
    st.session_state.activity_log.add(today)
    streak = 1
    sorted_days = sorted(st.session_state.activity_log, reverse=True)
    for i in range(1, len(sorted_days)):
        prev_day = datetime.datetime.strptime(sorted_days[i-1], "%Y-%m-%d").date()
        current_day = datetime.datetime.strptime(sorted_days[i], "%Y-%m-%d").date()
        if (prev_day - current_day).days == 1:
            streak += 1
        else:
            break
    if streak >= 3:
        awards.append("🔥 3-Day Streaker")
    if streak >= 7:
        awards.append("💥 Weekly Warrior (7-day streak)")
    if streak >= 14:
        awards.append("⚡ Hook Habit Hero (14-day streak)")

    if total_photos >= 5:
        awards.append("📸 Snapshot Stitcher (5+ photos)")
    if total_photos >= 10:
        awards.append("📷 Crafting Chronicler (10+ photos)")
    if total_yarns >= 10:
        awards.append("🧺 Yarn Collector (10+ yarn types)")
    if total_yarns >= 20:
        awards.append("🎨 Palette Perfectionist (20+ yarn types)")

    if awards:
        for award in awards:
            st.success(award)
    else:
        st.info("No awards yet — keep stitching!")

    st.subheader("Goals Progress")
    if st.session_state.get('goals'):
        for g in st.session_state.goals:
            percent = int((g['done'] / g['target']) * 100) if g['target'] else 0
            st.write(f"{g['goal']}: {g['done']} / {g['target']} ({percent}%)")
            st.progress(g['done'] / g['target'])

    st.subheader("Yarn Types Tracked")
    if st.session_state.get('yarn'):
        yarn_types = list(set(y["type"] for y in st.session_state.yarn))
        st.write(", ".join(yarn_types))
        st.metric("Total Yarn Types", len(yarn_types))

    st.subheader("Photos Uploaded")
    st.metric("📷 Photos", len(st.session_state.get('photos', [])))