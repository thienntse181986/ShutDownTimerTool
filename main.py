import os
import time
import threading
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import sys
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

# ================== CÁC BIẾN TOÀN CỤC ==================
timer_thread = None
cancel_flag = False
tray_icon = None

# ================== SYSTEM TRAY ==================
def create_tray_icon():
    # simple flat icon with rounded corner look
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    bg = (22, 120, 204, 255)
    draw.rectangle((6, 6, size - 6, size - 6), fill=bg, outline=None)
    # small white glyph
    draw.rectangle((22, 20, 42, 44), fill=(255, 255, 255, 255))
    return image

def on_show_window(icon, item):
    root.deiconify()

def on_quit_app(icon, item):
    icon.stop()
    root.destroy()
    os._exit(0)

def run_tray():
    global tray_icon
    tray_icon = pystray.Icon(
        "Shutdown Timer",
        create_tray_icon(),
        "Shutdown Timer Tool",
        menu=pystray.Menu(
            item('Hiện cửa sổ', on_show_window),
            item('Thoát', on_quit_app)
        )
    )
    tray_icon.run()

def minimize_to_tray():
    root.withdraw()
    threading.Thread(target=run_tray, daemon=True).start()

# ================== CHỨC NĂNG HẸN GIỜ ==================
def countdown_and_shutdown(total_seconds, action):
    global cancel_flag
    cancel_flag = False

    start = time.time()
    for remaining in range(total_seconds, 0, -1):
        if cancel_flag:
            progress_var.set(0)
            return
        mins, secs = divmod(remaining, 60)
        label_status.configure(text=f"⏳ Còn lại: {mins:02d} phút {secs:02d} giây")
        # update progress bar
        elapsed = int(time.time() - start)
        try:
            progress = min(100, int((elapsed / total_seconds) * 100)) if total_seconds > 0 else 100
        except Exception:
            progress = 0
        progress_var.set(progress)
        time.sleep(1)

    progress_var.set(100)
    if action == "shutdown":
        os.system("shutdown /s /t 1")
    elif action == "restart":
        os.system("shutdown /r /t 1")
    elif action == "logoff":
        os.system("shutdown /l")

def start_timer():
    global timer_thread
    action = action_var.get()

    try:
        if mode_var.get() == "minute":
            minutes_text = entry_minutes.get().strip()
            if not minutes_text:
                raise ValueError("empty")
            minutes = int(minutes_text)
            if minutes <= 0:
                raise ValueError("non-positive")
            total_seconds = minutes * 60
            target_time = datetime.now() + timedelta(seconds=total_seconds)
        else:
            h_text = entry_hour.get().strip()
            m_text = entry_minute.get().strip()
            if not h_text or not m_text:
                raise ValueError("empty")
            h = int(h_text)
            m = int(m_text)
            if not (0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError("out-of-range")
            now = datetime.now()
            target_time = now.replace(hour=h, minute=m, second=0, microsecond=0)
            if target_time <= now:
                target_time += timedelta(days=1)
            total_seconds = int((target_time - now).total_seconds())

        timer_thread = threading.Thread(target=countdown_and_shutdown, args=(total_seconds, action), daemon=True)
        timer_thread.start()
        messagebox.showinfo("Hẹn giờ thành công", f"💻 Máy sẽ {action} lúc {target_time.strftime('%H:%M:%S')}")
        label_status.configure(text=f"🕒 Đã hẹn lúc: {target_time.strftime('%H:%M:%S')}")
        # visually reflect start
        progress_var.set(0)
        btn_start.configure(state="disabled")
        btn_cancel.configure(state="normal")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập giá trị hợp lệ!")

def cancel_timer():
    global cancel_flag
    cancel_flag = True
    os.system("shutdown /a")
    label_status.configure(text="⛔ Đã hủy hẹn giờ.")
    progress_var.set(0)
    btn_start.configure(state="normal")
    btn_cancel.configure(state="disabled")

def switch_mode():
    # show/hide frames using grid to avoid mixing geometry managers
    if mode_var.get() == "minute":
        try:
            frame_clock.grid_remove()
        except Exception:
            pass
        frame_minute.grid(row=1, column=0, sticky='ew', pady=(0,6))
    else:
        try:
            frame_minute.grid_remove()
        except Exception:
            pass
        frame_clock.grid(row=1, column=0, sticky='ew', pady=(0,6))

# ================== GIAO DIỆN ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("🕒 Hẹn giờ tắt máy - Windows")
# increase height slightly to avoid clipping on some displays
root.geometry("520x650")
root.resizable(False, False)

# Main container with padding and subtle border
container = ctk.CTkFrame(root, fg_color="#0f1720")
container.pack(fill="both", expand=True, padx=14, pady=14)

# Header
header = ctk.CTkFrame(container, height=90)
header.pack(fill="x", pady=(0, 12))
# ensure header keeps the specified height
header.pack_propagate(False)

# Center container inside header
center_frame = ctk.CTkFrame(header)
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title (centered) with color
title_label = ctk.CTkLabel(center_frame, text="Shutdown Timer", font=ctk.CTkFont(size=20, weight="bold"), text_color="#48c9b0")
title_label.pack(anchor="center")
# Subtitle with limited width so it wraps instead of overflowing
subtitle_label = ctk.CTkLabel(center_frame, text="Giữ an toàn cho công việc của bạn — đặt lịch tắt máy dễ dàng", font=ctk.CTkFont(size=11), wraplength=380, justify="center", text_color="#bfc9ce")
subtitle_label.pack(anchor="center", pady=(6,0))

# Content area (no scrollbar - larger window)
content = ctk.CTkFrame(container)
content.pack(fill="both", expand=True, padx=6, pady=(6,14))
content.grid_columnconfigure(0, weight=1)

# --- Chọn chế độ ---
frame_mode = ctk.CTkFrame(content)

mode_var = ctk.StringVar(value="minute")
ctk.CTkLabel(frame_mode, text="Chọn chế độ hẹn giờ:", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky='w', padx=10, pady=5)
ctk.CTkRadioButton(frame_mode, text="⏲ Hẹn sau X phút", variable=mode_var, value="minute", command=switch_mode).grid(row=1, column=0, sticky='w', padx=20, pady=2)
ctk.CTkRadioButton(frame_mode, text="🕰 Hẹn theo giờ cụ thể", variable=mode_var, value="clock", command=switch_mode).grid(row=2, column=0, sticky='w', padx=20, pady=2)

# --- Hẹn theo phút ---
frame_minute = ctk.CTkFrame(content)
ctk.CTkLabel(frame_minute, text="Nhập số phút:", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky='w', padx=6, pady=(8,4))
entry_minutes = ctk.CTkEntry(frame_minute, width=300, placeholder_text="Số phút (ví dụ: 30)")
entry_minutes.grid(row=1, column=0, sticky='ew', padx=6, pady=4)
frame_minute.grid_columnconfigure(0, weight=1)


# --- Hẹn theo giờ ---
frame_clock = ctk.CTkFrame(content)
ctk.CTkLabel(frame_clock, text="Nhập giờ hẹn (24h):", font=ctk.CTkFont(size=13)).grid(row=0, column=0, sticky='w', padx=6, pady=(8,4))
frame_time = ctk.CTkFrame(frame_clock)
entry_hour = ctk.CTkEntry(frame_time, placeholder_text="Giờ (0-23)")
entry_minute = ctk.CTkEntry(frame_time, placeholder_text="Phút (0-59)")
# Layout using grid so the entries share width
frame_time.columnconfigure(0, weight=1)
frame_time.columnconfigure(2, weight=1)
entry_hour.grid(row=0, column=0, sticky='ew', padx=(4,2))
ctk.CTkLabel(frame_time, text=":", font=ctk.CTkFont(size=16)).grid(row=0, column=1, padx=2)
entry_minute.grid(row=0, column=2, sticky='ew', padx=(2,4))
frame_time.grid(row=1, column=0, sticky='ew', padx=6, pady=4)
frame_clock.grid_columnconfigure(0, weight=1)

# --- Hành động ---
frame_action = ctk.CTkFrame(content)
frame_action.grid_columnconfigure(0, weight=1)
frame_action.grid(row=3, column=0, sticky='ew', padx=8, pady=6)
ctk.CTkLabel(frame_action, text="Hành động khi đến giờ:", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=0, sticky='w', padx=10, pady=(6,6))

action_var = ctk.StringVar(value="shutdown")
ctk.CTkRadioButton(frame_action, text="Tắt máy", variable=action_var, value="shutdown").grid(row=1, column=0, sticky='w', padx=20)
ctk.CTkRadioButton(frame_action, text="Khởi động lại", variable=action_var, value="restart").grid(row=2, column=0, sticky='w', padx=20)
ctk.CTkRadioButton(frame_action, text="Đăng xuất", variable=action_var, value="logoff").grid(row=3, column=0, sticky='w', padx=20)

# --- Nút chức năng ---
frame_button = ctk.CTkFrame(content)
frame_button.grid(row=4, column=0, sticky='ew', pady=8)
frame_button.grid_columnconfigure(0, weight=1)
btn_start = ctk.CTkButton(frame_button, text="✅ Bắt đầu hẹn giờ", command=start_timer, fg_color="#2ecc71", width=220, height=40)
btn_start.grid(row=0, column=0, padx=(40,12), sticky='w')
btn_cancel = ctk.CTkButton(frame_button, text="❌ Hủy hẹn giờ", command=cancel_timer, fg_color="#e74c3c", width=160, height=40)
btn_cancel.grid(row=0, column=1, padx=(6,40), sticky='e')
btn_cancel.configure(state="disabled")

# --- Trạng thái ---
progress_var = ctk.IntVar(value=0)
progress = ctk.CTkProgressBar(content, variable=progress_var)
progress.set(0)
progress.grid(row=5, column=0, sticky='ew', padx=12, pady=(8,6))

label_status = ctk.CTkLabel(content, text="⌛ Chưa đặt hẹn giờ", font=ctk.CTkFont(size=13))
label_status.grid(row=6, column=0, pady=8)

# Place frames into the content using grid (avoid pack/grid mixing)
frame_mode.grid(row=0, column=0, sticky='ew', padx=8, pady=6)
# show the right frame for the current mode
if mode_var.get() == "minute":
    frame_minute.grid(row=1, column=0, sticky='ew', pady=(0,6))
else:
    frame_clock.grid(row=1, column=0, sticky='ew', padx=8, pady=6)

frame_action.grid(row=3, column=0, sticky='ew', padx=8, pady=6)
frame_button.grid(row=4, column=0, sticky='ew', pady=8)
progress.grid(row=5, column=0, sticky='ew', padx=12, pady=(8,6))
label_status.grid(row=6, column=0, pady=8)

# footer
footer = ctk.CTkFrame(container)
footer.pack(fill="x", pady=(8,0))
ctk.CTkLabel(footer, text="Minimize to tray will keep the timer running.", font=ctk.CTkFont(size=10)).pack(side="left", padx=8)

# --- Khi bấm X hoặc minimize ---
def on_close():
    try:
        cancel_timer()
    except Exception:
        pass

    try:
        if tray_icon is not None:
            try:
                tray_icon.stop()
            except Exception:
                pass
    except NameError:
        pass

    try:
        root.destroy()
    except Exception:
        pass

    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()