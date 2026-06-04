"""Waste Ink Maintenance Counter Utility - single-file GUI for Windows (USB).

An open-source, maintenance-focused utility for selected compatible inkjet
printers. It reads approximate waste-ink maintenance counters, creates a local
backup, and can reset those counters *after the owner has physically inspected,
cleaned, replaced, or redirected the waste-ink pad/tank*. It does not perform any
physical maintenance and is not a way to avoid service requirements.

Independent implementation: a self-written USB + IEEE-1284.4 (D4) + control-channel
stack (epson_d4.py) with an embedded, EUPL-derived model database (model_db.py).

This project is not affiliated with, endorsed by, sponsored by, or approved by
Epson. Epson is a trademark of its respective owner. Product names are used only
to describe compatibility with selected printer models.

Usage:
    Double-click the .exe (or `python maintenance_counter_app.py`)  -> GUI
    `... --check`  -> headless read-only self-test (writes check_result.txt)
"""
import os
import sys
import json
import webbrowser

import printer_core
import eeprom_io
import operations
import oplog

APP_TITLE = "Waste Ink Maintenance Counter Utility"
VERSION = "1.0.0"
TERMS_VERSION = 2

WEBSITE_URL = "https://devmosman.github.io/MaintenanceCounterUtility"
DONATE_URL = "https://ko-fi.com/devmosman"


def open_url(url):
    try:
        webbrowser.open(url)
    except Exception:
        pass

NON_AFFILIATION = (
    "This project is not affiliated with, endorsed by, sponsored by, or approved "
    "by Epson. Epson is a trademark of its respective owner. Product names are "
    "used only to describe compatibility with selected printer models."
)

DISCLAIMER = (
    "TERMS OF USE — PLEASE READ CAREFULLY\n\n"
    "This is an open-source maintenance-counter utility. It is not an official "
    "Epson product. By using it you agree to ALL of the following:\n\n"
    "1. USE AT YOUR OWN RISK. Provided \"as is\", with NO warranty. The authors are "
    "not liable for any damage, data loss, voided warranty, or a non-working "
    "printer.\n\n"
    "2. SOFTWARE ONLY. A counter reset clears maintenance counters in printer "
    "memory. It does NOT clean, empty, repair, replace, or physically service the "
    "waste-ink pad or tank.\n\n"
    "3. PHYSICAL MAINTENANCE FIRST. Use the reset only after you have inspected, "
    "cleaned, replaced the waste-ink pad, or installed/verified an external waste-"
    "ink tank. Resetting without physical service may cause ink overflow, leakage, "
    "mess, or printer damage.\n\n"
    "4. LEGITIMATE MAINTENANCE ONLY. Use only for responsible owner maintenance or "
    "service. Do not reset low counters without a real maintenance/service reason.\n\n"
    "5. EXPERIMENTAL MODELS. Entries marked \"experimental\" are derived from "
    "community data and have not been verified on real hardware. Extra caution is "
    "required.\n\n"
    "6. LAWS VARY BY JURISDICTION. Anti-circumvention, repair, warranty, consumer-"
    "protection and product-liability rules differ by country. This is not legal "
    "advice; paid distribution should be reviewed by a qualified local lawyer.\n\n"
    "7. AUTHORIZATION. You confirm you own this printer or are authorized to "
    "maintain it.\n\n"
    + NON_AFFILIATION
)

SAFETY_SHORT = (
    "A counter reset is a maintenance-support step. It clears software counters "
    "only — the physical pad/tank must be serviced separately. Use only after "
    "physical maintenance."
)

# 8-point mandatory pre-reset warning
RESET_WARNING = (
    "Before resetting the maintenance counters, please understand:\n\n"
    "1. This software reset only clears maintenance counters.\n"
    "2. It does NOT clean, empty, repair, replace, or physically service the "
    "waste-ink pad.\n"
    "3. You must inspect, clean, or replace the waste-ink pad, or install/verify "
    "an external waste-ink tank, before continuing.\n"
    "4. Incorrect use may cause ink overflow, leakage, printer damage, data loss, "
    "or mess.\n"
    "5. Use this only for legitimate owner maintenance or service purposes.\n"
    "6. Do not reset low counters unless there is a real maintenance/service "
    "reason.\n"
    "7. Laws and warranty rules may vary by country.\n"
    "8. This tool is not affiliated with Epson."
)
ACK_PHYSICAL = ("I confirm that the waste ink pad has been inspected, cleaned, replaced, "
                "or an external waste ink tank is installed and functioning.")
ACK_RESPONSIBILITY = ("I understand this action modifies printer maintenance counters and I "
                      "accept full responsibility for ensuring physical maintenance has been "
                      "completed.")

USAGE_RENAME = {
    "Total print page counter": "Total printed pages",
    "Total scan counter": "Total scans",
    "Total print pass counter": "Print-head passes",
    "Manual cleaning counter": "Manual cleanings",
    "Timer cleaning counter": "Timer cleanings",
    "Power cleaning counter": "Power cleanings",
}


# ----------------------------- settings (persisted) ---------------------------
def load_settings():
    try:
        with open(eeprom_io.settings_path(), "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(s):
    try:
        with open(eeprom_io.settings_path(), "w", encoding="utf-8") as f:
            json.dump(s, f, indent=2)
    except Exception:
        pass


def terms_accepted():
    return load_settings().get("terms_accepted") == TERMS_VERSION


def accept_terms():
    s = load_settings(); s["terms_accepted"] = TERMS_VERSION; save_settings(s)


# ----------------------------- headless self-test -----------------------------
def check_mode():
    out = []
    try:
        with printer_core.UsbBackend() as be:
            st = be.read_state()
            out.append(f"OK model={st['model']} key={be.key} transport={st['transport']} "
                       f"experimental={st['experimental']} status={st['status']}")
            for name, raw, mx, pct in st["waste"]:
                out.append(f"  [{name}] {raw}/{mx} = {pct:.2f}%")
            for name, val in st["usage"]:
                out.append(f"  {USAGE_RENAME.get(name, name)}: {val}")
            out.append("  backup: " + os.path.basename(eeprom_io.backup(be, note="selftest")))
    except Exception as e:
        out.append(f"ERROR: {e!r}")
    text = "\n".join(out)
    try:
        with open("check_result.txt", "w", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        pass
    print(text)
    return 0 if out and out[0].startswith("OK") else 1


# --------------------------------- dialogs ---------------------------------
def _center(win, w, h):
    """Size and center a dialog, capping height to the screen so the bottom
    controls (checkbox/buttons) are always visible on small displays."""
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    h = min(h, sh - 90)
    w = min(w, sw - 40)
    x = max(0, (sw - w) // 2)
    y = max(0, (sh - h) // 2 - 20)
    win.geometry(f"{w}x{h}+{x}+{y}")
    win.minsize(min(w, 460), min(h, 320))
    # make sure the dialog is visible and on top (not hidden behind other windows)
    try:
        win.lift()
        win.focus_force()
        win.attributes("-topmost", True)
        win.after(250, lambda: win.attributes("-topmost", False))
    except Exception:
        pass


def _scrolled_text(parent, body):
    import tkinter as tk
    from tkinter import ttk
    frame = ttk.Frame(parent)
    sb = ttk.Scrollbar(frame); sb.pack(side="right", fill="y")
    txt = tk.Text(frame, wrap="word", yscrollcommand=sb.set, padx=10, pady=8)
    txt.insert("1.0", body); txt.config(state="disabled")
    txt.pack(side="left", fill="both", expand=True)
    sb.config(command=txt.yview)
    return frame


def _scroll_terms_dialog(root, title, body, accept_label, decline_label):
    import tkinter as tk
    from tkinter import ttk
    win = tk.Toplevel(root)
    win.title(title); win.transient(root); win.grab_set()
    result = {"ok": False}
    agreed = tk.BooleanVar(value=False)

    def ok():
        if agreed.get():
            result["ok"] = True; win.destroy()

    def no():
        result["ok"] = False; win.destroy()

    ttk.Label(win, text=title, font=("Segoe UI", 13, "bold")).pack(side="top", pady=(12, 6))
    # bottom-anchored controls FIRST so they are always visible
    bar = ttk.Frame(win); bar.pack(side="bottom", fill="x", padx=12, pady=10)
    ab = ttk.Button(bar, text=accept_label, command=ok); ab.pack(side="right", padx=4)
    ttk.Button(bar, text=decline_label, command=no).pack(side="right", padx=4)
    ttk.Checkbutton(win, variable=agreed,
                    text="I have read and accept these terms, and I take full responsibility."
                    ).pack(side="bottom", anchor="w", padx=16, pady=(8, 2))
    _scrolled_text(win, body).pack(side="top", fill="both", expand=True, padx=12)

    ab.state(["disabled"])
    agreed.trace_add("write", lambda *_: ab.state(["!disabled"] if agreed.get() else ["disabled"]))
    win.protocol("WM_DELETE_WINDOW", no)
    _center(win, 600, 560)
    root.wait_window(win)
    return result["ok"]


def show_terms(root):
    return _scroll_terms_dialog(root, f"{APP_TITLE} — Terms of Use", DISCLAIMER,
                                "Accept & Continue", "Decline & Exit")


def reset_consent(root):
    """Mandatory warning + physical-maintenance checkbox, then a required second
    confirmation. Returns True only if the user completes both steps."""
    import tkinter as tk
    from tkinter import ttk, messagebox
    win = tk.Toplevel(root)
    win.title(f"{APP_TITLE} — Before you reset"); win.transient(root); win.grab_set()
    ack = tk.BooleanVar(value=False)
    result = {"ok": False}

    def cont():
        if not ack.get():
            return
        # second, explicit confirmation
        if messagebox.askyesno(APP_TITLE, ACK_RESPONSIBILITY + "\n\nProceed with the reset?",
                               icon="warning", parent=win):
            result["ok"] = True
            win.destroy()

    def cancel():
        result["ok"] = False; win.destroy()

    ttk.Label(win, text="Maintenance reset — please confirm",
              font=("Segoe UI", 12, "bold")).pack(side="top", pady=(12, 6))
    # bottom-anchored controls FIRST so the checkbox + buttons are always visible
    bar = ttk.Frame(win); bar.pack(side="bottom", fill="x", padx=12, pady=10)
    cont_btn = ttk.Button(bar, text="Continue", command=cont); cont_btn.pack(side="right", padx=4)
    ttk.Button(bar, text="Cancel", command=cancel).pack(side="right", padx=4)
    chk = ttk.Checkbutton(win, variable=ack,
                          text="I confirm the statement above (physical maintenance completed).")
    chk.pack(side="bottom", anchor="w", padx=16, pady=(4, 2))
    ttk.Label(win, text=ACK_PHYSICAL, wraplength=560, foreground="#222"
              ).pack(side="bottom", anchor="w", padx=16, pady=(6, 0))
    ttk.Label(win, text="Tick the box below, then click Continue.",
              foreground="#444", font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=16)
    _scrolled_text(win, RESET_WARNING).pack(side="top", fill="both", expand=True, padx=12)

    cont_btn.state(["disabled"])
    ack.trace_add("write", lambda *_: cont_btn.state(["!disabled"] if ack.get() else ["disabled"]))
    win.protocol("WM_DELETE_WINDOW", cancel)
    _center(win, 600, 540)
    root.wait_window(win)
    return result["ok"]


def show_about(root):
    import tkinter as tk
    from tkinter import ttk
    win = tk.Toplevel(root); win.title("About"); win.transient(root); win.grab_set()
    ttk.Label(win, text=APP_TITLE, font=("Segoe UI", 12, "bold")).pack(side="top", pady=(12, 2))
    ttk.Label(win, text=f"Version {VERSION}  ·  open source (EUPL-1.2)").pack(side="top")
    body = (f"\n{NON_AFFILIATION}\n\n"
            f"Database: {printer_core.model_count()} compatible models (embedded).\n"
            "Connection: USB.\n\n"
            "A maintenance-support utility: it reads and can reset waste-ink "
            "maintenance counters after the owner performs physical pad/tank "
            "service. It does not perform physical maintenance and is not a way to "
            "avoid service requirements.\n\n"
            "Licensed under EUPL-1.2. See LICENSE.txt and NOTICE.txt. Not legal "
            "advice; laws vary by jurisdiction.")
    abar = ttk.Frame(win); abar.pack(side="bottom", pady=8)
    ttk.Button(abar, text="🌐 Website", command=lambda: open_url(WEBSITE_URL)).pack(side="left", padx=4)
    ttk.Button(abar, text="❤ Support on Ko-fi", command=lambda: open_url(DONATE_URL)).pack(side="left", padx=4)
    ttk.Button(abar, text="Close", command=win.destroy).pack(side="left", padx=4)
    _scrolled_text(win, body).pack(side="top", fill="both", expand=True, padx=12, pady=6)
    _center(win, 520, 420)
    root.wait_window(win)


# ---------------------------------- GUI ----------------------------------
def launch_gui():
    import tkinter as tk
    from tkinter import messagebox, ttk, filedialog

    root = tk.Tk()
    root.title(APP_TITLE)
    root.minsize(520, 720)
    try:
        ttk.Style(root).theme_use("vista")
    except Exception:
        pass

    selftest = os.environ.get("EWR_GUI_SELFTEST") == "1"
    # Bring the main window to the front first (avoids it/the dialog opening hidden
    # behind other windows on some Windows setups).
    try:
        root.update_idletasks()
        root.lift()
        root.attributes("-topmost", True)
        root.after(500, lambda: root.attributes("-topmost", False))
    except Exception:
        pass
    if not terms_accepted() and not selftest:
        # Do NOT withdraw the root: a modal whose parent is withdrawn can open
        # without a taskbar entry / behind other windows.
        if not show_terms(root):
            root.destroy(); return
        accept_terms()

    ttk.Label(root, text=APP_TITLE, font=("Segoe UI", 13, "bold")).pack(pady=(10, 0))
    ttk.Label(root, text="Maintenance-support utility · not an official Epson product",
              foreground="#666", font=("Segoe UI", 8)).pack()
    model_var = tk.StringVar(value="Not connected")
    ttk.Label(root, textvariable=model_var, font=("Segoe UI", 10, "bold")).pack(pady=(6, 0))
    badge_var = tk.StringVar(value="")
    badge = ttk.Label(root, textvariable=badge_var); badge.pack()
    status_var = tk.StringVar(value="")
    ttk.Label(root, textvariable=status_var, foreground="#a00").pack(pady=(0, 4))

    waste_frame = ttk.LabelFrame(root, text="Waste ink maintenance counters")
    waste_frame.pack(fill="x", padx=12, pady=4)
    bars, labels, names = [], [], []
    for i in range(3):
        r = ttk.Frame(waste_frame); r.pack(fill="x", padx=6, pady=2)
        nm = ttk.Label(r, text=f"Counter {i+1}", width=22, anchor="w"); nm.pack(side="left")
        bar = ttk.Progressbar(r, length=150, maximum=100); bar.pack(side="left", padx=6)
        lab = ttk.Label(r, text="--", width=18, anchor="w"); lab.pack(side="left")
        names.append(nm); bars.append(bar); labels.append(lab)
    ttk.Label(waste_frame, text="(counter names are approximate)",
              foreground="#888", font=("Segoe UI", 8)).pack(anchor="w", padx=6)

    usage_frame = ttk.LabelFrame(root, text="Usage counters")
    usage_frame.pack(fill="x", padx=12, pady=4)
    usage_body = ttk.Frame(usage_frame); usage_body.pack(fill="x", padx=6, pady=4)

    ttk.Label(root, text=SAFETY_SHORT, wraplength=480, foreground="#555",
              font=("Segoe UI", 8)).pack(padx=12, pady=(4, 4))

    btns = ttk.Frame(root); btns.pack(pady=8)
    state_cache = {"waste": []}

    def set_busy(b):
        root.config(cursor="watch" if b else ""); root.update_idletasks()

    def render(st):
        state_cache["waste"] = st["waste"]
        model_var.set(f"{st['model']}   —   {st['transport']}")
        if st["experimental"]:
            badge_var.set("⚠  EXPERIMENTAL model (community data, unverified)")
            badge.config(foreground="#b35900")
        else:
            badge_var.set("✔  Verified model"); badge.config(foreground="#207520")
        err = st["status"]
        status_var.set("" if ("IDLE" in err and "NONE" in err) else f"Status: {err}")
        for i in range(3):
            if i < len(st["waste"]):
                nm, raw, mx, pct = st["waste"][i]
                names[i]["text"] = nm; bars[i]["value"] = pct
                labels[i]["text"] = f"{raw} / {mx}  ({pct:.1f}%)"
            else:
                names[i]["text"] = ""; bars[i]["value"] = 0; labels[i]["text"] = "--"
        for c in usage_body.winfo_children():
            c.destroy()
        if st["usage"]:
            for row, (name, val) in enumerate(st["usage"]):
                ttk.Label(usage_body, text=USAGE_RENAME.get(name, name) + ":",
                          anchor="w", width=24).grid(row=row, column=0, sticky="w")
                ttk.Label(usage_body, text=("n/a" if val is None else f"{val:,}")
                          ).grid(row=row, column=1, sticky="w", padx=8)
        else:
            ttk.Label(usage_body, text="No usage counters for this model.").grid(row=0, column=0)

    def connect(fn):
        set_busy(True)
        try:
            with printer_core.UsbBackend() as be:
                return fn(be)
        except Exception as e:
            messagebox.showerror(APP_TITLE, str(e))
            model_var.set("Not connected / error"); badge_var.set(""); status_var.set(str(e))
            return None
        finally:
            set_busy(False)

    def refresh():
        r = connect(lambda be: be.read_state())
        if r:
            render(r)

    def backup_only():
        p = connect(lambda be: eeprom_io.backup(be, note="manual"))
        if p:
            oplog.log_event("manual_backup", path=p)
            messagebox.showinfo(APP_TITLE, f"Backup saved:\n{p}")

    def reset_action():
        st = connect(lambda be: be.read_state())
        if not st:
            return
        # low-counter caution (warn, do not block)
        if operations.counters_are_low(st["waste"]):
            if not messagebox.askyesno(
                APP_TITLE,
                "The current waste ink counters appear low. Resetting low counters is "
                "usually unnecessary unless you have a specific maintenance or service "
                "reason.\n\nContinue anyway?", icon="warning"):
                return
        if st["experimental"]:
            if not messagebox.askyesno(
                APP_TITLE, "This is an EXPERIMENTAL model (community data, not verified on "
                "hardware). Continue with extra caution?", icon="warning"):
                return
        # mandatory warning + physical-maintenance checkbox + second confirmation
        if not reset_consent(root):
            return

        def _run(be, override):
            return operations.perform_reset(
                be, acknowledged_physical=True, accepted_responsibility=True,
                override_backup_failure=override)

        # explicit handling so the backup-failure override path can be offered
        res = None
        set_busy(True)
        try:
            with printer_core.UsbBackend() as be:
                res = _run(be, False)
        except operations.BackupFailed as e:
            set_busy(False)
            if messagebox.askyesno(APP_TITLE, str(e) + "\n\nProceed WITHOUT a backup?",
                                   icon="warning"):
                set_busy(True)
                try:
                    with printer_core.UsbBackend() as be:
                        res = _run(be, True)
                except Exception as e2:
                    messagebox.showerror(APP_TITLE, f"Reset failed:\n{e2}")
            else:
                return
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Reset failed:\n{e}")
            return
        finally:
            set_busy(False)

        if res:
            refresh()
            bp = res.get("backup_path") or "(no backup — overridden)"
            messagebox.showinfo(
                APP_TITLE,
                "Maintenance counters reset.\n\n"
                f"Backup: {bp}\n\n"
                "Now POWER-CYCLE the printer (off with its power button, wait a few "
                "seconds, on) to commit the change.\n\n" + SAFETY_SHORT)

    def restore_action():
        path = filedialog.askopenfilename(
            title="Choose a backup to restore", initialdir=eeprom_io.backups_dir(),
            filetypes=[("Backup files", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            meta = eeprom_io.load_backup(path)
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Cannot read backup:\n{e}"); return
        if not messagebox.askyesno(
            APP_TITLE, f"Restore counters from backup?\n\nModel: {meta.get('model')}\n"
            f"Taken: {meta.get('timestamp')}\nBytes: {len(meta.get('eeprom', {}))}\n\n"
            "This writes the saved values back to the printer.", icon="warning"):
            return
        res = connect(lambda be: eeprom_io.restore(be, path))
        if res:
            oplog.log_event("restore", path=os.path.basename(path), bytes=res[0])
            messagebox.showinfo(APP_TITLE, f"Restored {res[0]}/{res[1]} bytes.\n"
                                           "Power-cycle the printer to commit.")
            refresh()

    ttk.Button(btns, text="Refresh", command=refresh).grid(row=0, column=0, padx=3)
    ttk.Button(btns, text="Backup", command=backup_only).grid(row=0, column=1, padx=3)
    ttk.Button(btns, text="Reset Maintenance Counters", command=reset_action).grid(row=0, column=2, padx=3)
    ttk.Button(btns, text="Restore…", command=restore_action).grid(row=0, column=3, padx=3)
    ttk.Button(btns, text="About", command=lambda: show_about(root)).grid(row=0, column=4, padx=3)

    # Website + donation (visible to the user)
    links = ttk.Frame(root); links.pack(pady=(0, 4))
    ttk.Button(links, text="🌐 Website", command=lambda: open_url(WEBSITE_URL)).pack(side="left", padx=4)
    tk.Button(links, text="❤ Support on Ko-fi", command=lambda: open_url(DONATE_URL),
              bg="#ff5e8a", fg="white", activebackground="#ff7aa0", activeforeground="white",
              relief="flat", padx=12, pady=3, cursor="hand2",
              font=("Segoe UI", 9, "bold")).pack(side="left", padx=4)

    foot = ttk.Frame(root); foot.pack(side="bottom", fill="x")
    ttk.Label(foot, text=NON_AFFILIATION, wraplength=500, foreground="#777",
              font=("Segoe UI", 7), justify="center").pack(pady=(2, 0))
    ttk.Label(foot, text=f"v{VERSION} · EUPL-1.2 · {printer_core.model_count()} models · USB",
              foreground="#999", font=("Segoe UI", 7)).pack(pady=(0, 4))

    root.after(250, refresh)
    if selftest:
        root.after(4000, root.destroy); print("GUI_SELFTEST: constructed OK")
    root.mainloop()
    if selftest:
        print("GUI_SELFTEST: closed cleanly")


def main():
    if "--check" in sys.argv:
        sys.exit(check_mode())
    try:
        launch_gui()
    except Exception:
        # In a windowed build the console is hidden; persist the traceback so a
        # startup failure can be diagnosed.
        import traceback
        try:
            with open(os.path.join(eeprom_io.app_dir(), "startup_error.log"),
                      "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
        except Exception:
            pass
        raise


if __name__ == "__main__":
    main()
