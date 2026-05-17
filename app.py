import streamlit as st
import pandas as pd
from datetime import datetime

# ตั้งค่าหน้าจอสำหรับมือถือ
st.set_page_config(page_title="Marketing Ticket System", page_icon="📈", layout="centered")

st.title("📈 Marketing Ticket System")
st.write("ระบบส่งงานและติดตามทิกเก็ท (สำหรับทุกคนที่ต้องการสั่งงานแผนกมาร์เก็ตติ้ง)")

# 1. ฐานข้อมูลจำลอง (อัปเดตการสะกดชื่อคุณ Gie เรียบร้อยค่ะ)
if 'marketing_tickets' not in st.session_state:
    st.session_state.marketing_tickets = [
        {"Ticket ID": "MKT-001", "ชื่องาน": "บรีฟกราฟิกป้ายโปรโมชั่นหน้าร้าน", "ผู้สั่งงาน (Requester)": "คุณเมย์ (Sales/ฝ่ายขาย)", "ผู้รับผิดชอบ (Assignee)": "🎨 P'Vicky (Graphic Designer)", "ความด่วน": "⚡ ด่วน (High)", "รายละเอียด": "ขอภาพกราฟิกขนาดพิมพ์ใหญ่สำหรับติดบอร์ดกิจกรรมหน้าร้าน", "สถานะ": "⏳ กำลังดำเนินการ", "กำหนดส่ง": "2026-05-22"},
        {"Ticket ID": "MKT-002", "ชื่องาน": "ทำคลิปสั้นไฮไลท์บรรยากาศงาน O.O.O. MARKET", "ผู้สั่งงาน (Requester)": "👩‍💻 Gie (Digital Marketer)", "ผู้รับผิดชอบ (Assignee)": "👩‍💻 Gie (Digital Marketer / Content Creator)", "ความด่วน": "🟢 ปกติ (Normal)", "รายละเอียด": "ตัดคลิปลง TikTok รีวิวบรรยากาศบูธในงาน", "สถานะ": "📌 รอดำเนินการ", "กำหนดส่ง": "2026-05-25"},
        {"Ticket ID": "MKT-003", "ชื่องาน": "อนุมัติงบโฆษณาแคมเปญใหม่", "ผู้สั่งงาน (Requester)": "👩‍💻 Gie (Digital Marketer)", "ผู้รับผิดชอบ (Assignee)": "👨‍💼 P'Turk (Marketing Manager)", "ความด่วน": "🔥 ด่วนที่สุด (Critical)", "รายละเอียด": "สรุปตัวเลขสถิติและงบ Ad สำหรับยิงสัปดาห์หน้าให้เซ็นผ่าน", "สถานะ": "👀 รอตรวจ/รออนุมัติ (Pending)", "กำหนดส่ง": "2026-05-20"},
        {"Ticket ID": "MKT-004", "ชื่องาน": "ประสานงานสถานที่จัดบอร์ดงานมาร์เก็ต", "ผู้สั่งงาน (Requester)": "👨‍💼 P'Turk (Marketing Manager)", "ผู้รับผิดชอบ (Assignee)": "🎪 P'Tom (Event Marketing Specialist)", "ความด่วน": "⚡ ด่วน (High)", "รายละเอียด": "ดีลกับ W District เรื่องพื้นที่วางโต๊ะและสปอตไฟ", "สถานะ": "⏳ กำลังดำเนินการ", "กำหนดส่ง": "2026-05-21"}
    ]

# รายชื่อและตำแหน่งในทีมมาร์เก็ตติ้ง (อัปเดตชื่อสากลของคุณ Gie ✨)
marketing_team_members = [
    "👨‍💼 P'Turk (Marketing Manager)",
    "🎪 P'Tom (Event Marketing Specialist)",
    "🎨 P'Vicky (Graphic Designer)",
    "👩‍💻 Gie (Digital Marketer / Content Creator)"
]

# สร้าง Tabs สำหรับการใช้งานบนมือถือ
tab1, tab2, tab3 = st.tabs(["📝 สั่งงานมาร์เก็ตติ้ง", "📊 ขั้นตอนและสถานะงานทั้งหมด", "🔄 อัปเดตสถานะงาน (เฉพาะทีม MKT)"])

# ---------------------------------------------------------
# TAB 1: หน้าสั่งงานสำหรับทุกคน (เห็นโหลดงานทีมทันทีที่เลือกชื่อ)
# ---------------------------------------------------------
with tab1:
    st.subheader("📝 สร้างทิกเก็ทส่งงานใหม่")
    selected_assignee = st.selectbox("🎯 มอบหมายงานให้ใครในทีมมาร์เก็ตติ้ง? (Assignee)", marketing_team_members)
    
    all_df = pd.DataFrame(st.session_state.marketing_tickets)
    current_tasks = all_df[(all_df["ผู้รับผิดชอบ (Assignee)"] == selected_assignee) & (all_df["สถานะ"] != "✅ เสร็จสิ้น/ดำเนินการแล้ว")]
    
    st.markdown(f"👀 **ตารางงานในมือปัจจุบันของ {selected_assignee.split(' ')[1]}:**")
    if not current_tasks.empty:
        st.warning(f"⚠️ ตอนนี้มีงานค้างอยู่ {len(current_tasks)} งานในระบบ:")
        st.dataframe(current_tasks[["Ticket ID", "ชื่องาน", "ความด่วน", "สถานะ"]], use_container_width=True)
    else:
        st.success("🟢 ตอนนี้คิวว่างอยู่ สามารถส่งงานใหม่ให้ได้เลยค่ะ!")
        
    st.markdown("---")
    
    with st.form(key='mkt_ticket_form', clear_on_submit=True):
        requester_info = st.text_input("👤 ชื่อผู้สั่งงาน และ แผนกของคุณ (เช่น คุณบี ฝ่ายขาย / Gie มาร์เก็ตติ้ง)")
        job_title = st.text_input("🎬 ชื่องานมาร์เก็ตติ้งที่ต้องการ")
        priority = st.selectbox("🚨 ระดับความด่วนของงาน", ["🟢 ปกติ (Normal)", "⚡ ด่วน (High)", "🔥 ด่วนที่สุด (Critical)"])
        deadline = st.date_input("📅 ต้องการงานภายในวันไหน? (Deadline)", datetime.now())
        detail = st.text_area("📝 รายละเอียดบรีฟงานโดยละเอียด")
        
        submit_button = st.form_submit_with_name("ส่งตั๋วงานเข้าสู่ระบบ 🚀")

    if submit_button:
        if requester_info and job_title and detail:
            new_id = f"MKT-{len(st.session_state.marketing_tickets) + 1:03d}"
            new_ticket = {
                "Ticket ID": new_id, "ชื่องาน": job_title, "ผู้สั่งงาน (Requester)": requester_info,
                "ผู้รับผิดชอบ (Assignee)": selected_assignee, "ความด่วน": priority, "รายละเอียด": detail,
                "สถานะ": "📌 รอดำเนินการ", "กำหนดส่ง": str(deadline)
            }
            st.session_state.marketing_tickets.append(new_ticket)
            st.success(f"ส่งทิกเก็ท {new_id} สำเร็จแล้ว!")
            st.rerun()

# ---------------------------------------------------------
# TAB 2: หน้าติดตามสถานะแบบแยกตารางดูรายบุคคลชัดเจน (อัปเดตชื่อคุณ Gie)
# ---------------------------------------------------------
with tab2:
    df = pd.DataFrame(st.session_state.marketing_tickets)
    
    st.subheader("📊 1. ตารางแยกภาระงานรายบุคคล (Individual Workload)")
    st.write("ดูสถานะงานแบบแยกตามรายชื่อผู้รับผิดชอบ เพื่อเช็กว่าใครกำลังทำอะไรอยู่บ้าง")
    
    for member in marketing_team_members:
        member_short_name = member.split(' ')[1] 
        member_tasks = df[(df["ผู้รับผิดชอบ (Assignee)"] == member) & (df["สถานะ"] != "✅ เสร็จสิ้น/ดำเนินการแล้ว")]
        
        st.markdown(f"### {member}")
        if not member_tasks.empty:
            st.dataframe(member_tasks[["Ticket ID", "ชื่องาน", "ผู้สั่งงาน (Requester)", "ความด่วน", "สถานะ", "กำหนดส่ง"]], use_container_width=True)
        else:
            st.caption(f"🟢 ตอนนี้ {member_short_name} ไม่มีงานค้างในระบบ (สเตตัสว่าง)")
        st.markdown("---")
        
    st.subheader("📋 2. ตารางรวมทุกงานในระบบ (All Tickets Summary)")
    filter_option = st.selectbox("🔍 ฟิลเตอร์เลือกกรองเฉพาะคนสำหรับตารางรวม:", ["ทุกคนในทีมมาร์เก็ตติ้ง"] + marketing_team_members)
    filtered_df = df if filter_option == "ทุกคนในทีมมาร์เก็ตติ้ง" else df[df["ผู้รับผิดชอบ (Assignee)"] == filter_option]
    st.dataframe(filtered_df[["Ticket ID", "ชื่องาน", "ผู้สั่งงาน (Requester)", "ผู้รับผิดชอบ (Assignee)", "ความด่วน", "สถานะ", "กำหนดส่ง"]], use_container_width=True)

# ---------------------------------------------------------
# TAB 3: หน้าอัปเดตสเตตัส (สำหรับทีม MKT เข้ามาเปลี่ยนสถานะงาน)
# ---------------------------------------------------------
with tab3:
    st.subheader("🔄 อัปเดตขั้นตอนการทำงาน (for Marketing Team)")
    ticket_ids = [t["Ticket ID"] for t in st.session_state.marketing_tickets]
    selected_id = st.selectbox("🎯 เลือก Ticket ID ที่ต้องการเปลี่ยนขั้นตอน", ticket_ids)
    
    mkt_status = ["📌 รอดำเนินการ", "⏳ กำลังดำเนินการ", "👀 รอตรวจ/รออนุมัติ (Pending)", "❌ ต้องแก้ไขงาน", "✅ เสร็จสิ้น/ดำเนินการแล้ว"]
    new_status = st.selectbox("🔄 เปลี่ยนสเตตัสงานเป็น", mkt_status)
    
    if st.button("บันทึกความคืบหน้าสเตตัส ✨"):
        for t in st.session_state.marketing_tickets:
            if t["Ticket ID"] == selected_id:
                t["สถานะ"] = new_status
                st.success(f"อัปเดตสเตตัสของ {selected_id} เป็น '{new_status}' เรียบร้อยแล้วค่ะ!")
                st.rerun()
                break