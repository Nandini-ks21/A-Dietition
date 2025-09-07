#!/usr/bin/env python
# coding: utf-8

# In[22]:


from tkinter import *
from tkinter import messagebox
from random import choice, randint
import os

# -------------------- Theme / Utilities --------------------
PALETTE = {
    "bg_start": "#ffefba",  # soft peach
    "bg_end": "#ffffff",    # white
    "card_bg": "#ffffff",
    "header_bg": "#6a5acd",
    "accent": "#20c997",    # teal
    "accent2": "#ff6f61",   # coral
    "muted": "#6c757d",
}
FONT_HEADER = ("Segoe UI", 32, "bold")
FONT_SUB = ("Segoe UI", 14)
FONT_LABEL = ("Segoe UI", 12)


def _make_gradient(canvas, w, h, start, end):
    # simple vertical gradient by drawing many horizontal lines
    # start/end are hex colors like '#RRGGBB'
    def hex_to_rgb(hx):
        return tuple(int(hx[i : i + 2], 16) for i in (1, 3, 5))

    def rgb_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    start_rgb = hex_to_rgb(start)
    end_rgb = hex_to_rgb(end)
    for i in range(h):
        ratio = i / h
        curr = tuple(int(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * ratio) for j in range(3))
        canvas.create_line(0, i, w, i, fill=rgb_to_hex(curr))


def _on_hover(widget, enter_bg, leave_bg, enter_fg=None, leave_fg=None):
    def _enter(e):
        widget.config(bg=enter_bg)
        if enter_fg:
            widget.config(fg=enter_fg)

    def _leave(e):
        widget.config(bg=leave_bg)
        if leave_fg:
            widget.config(fg=leave_fg)

    widget.bind("<Enter>", _enter)
    widget.bind("<Leave>", _leave)


# -------------------- App Functions --------------------

def register(main):
    global reg_username_var, reg_pass_var, username_entry, password_entry
    reg_username_var = StringVar()
    reg_pass_var = StringVar()

    register_screen = Toplevel(main)
    register_screen.title("Register")
    register_screen.geometry("900x700")
    register_screen.configure(bg=PALETTE["bg_end"])

    # Header
    Label(register_screen, text="📝 Registration Form 📝", bg=PALETTE["header_bg"], fg="white",
          font=("Segoe UI", 26, "bold"), pady=15).pack(fill=X)

    Label(register_screen, text="Please enter your details", bg=PALETTE["bg_end"], fg="teal",
          font=("Segoe UI", 18, "bold"), pady=20).pack()

    form_frame = Frame(register_screen, bg=PALETTE["bg_end"])
    form_frame.pack(pady=10)

    # Full Name
    name = StringVar()
    Label(form_frame, text="Full Name", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=0, column=0, padx=20, pady=10)
    Entry(form_frame, textvariable=name, font=("Segoe UI", 14), bg="#fffafa", relief=GROOVE).grid(row=0, column=1, pady=10)

    # Phone
    phone = IntVar()
    Label(form_frame, text="Phone Number", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=1, column=0, padx=20, pady=10)
    Entry(form_frame, textvariable=phone, font=("Segoe UI", 14), bg="#fffafa", relief=GROOVE).grid(row=1, column=1, pady=10)

    # Registration ID
    registrationid = IntVar()
    Label(form_frame, text="Registration ID", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=2, column=0, padx=20, pady=10)
    Entry(form_frame, textvariable=registrationid, font=("Segoe UI", 14), bg="#fffafa", relief=GROOVE).grid(row=2, column=1, pady=10)

    # Gender
    gender_var = IntVar()
    Label(form_frame, text="Gender", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=3, column=0, padx=20, pady=10)
    Radiobutton(form_frame, text="Male", variable=gender_var, value=1, font=("Segoe UI", 12), bg=PALETTE["bg_end"]).grid(row=3, column=1, sticky="w")
    Radiobutton(form_frame, text="Female", variable=gender_var, value=2, font=("Segoe UI", 12), bg=PALETTE["bg_end"]).grid(row=3, column=1, sticky="e")

    # Email
    email = StringVar()
    Label(form_frame, text="Email", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=4, column=0, padx=20, pady=10)
    Entry(form_frame, textvariable=email, font=("Segoe UI", 14), width=30, bg="#fffafa", relief=GROOVE).grid(row=4, column=1, pady=10)

    # Username
    Label(form_frame, text="Username", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=5, column=0, padx=20, pady=10)
    username_entry = Entry(form_frame, textvariable=reg_username_var, font=("Segoe UI", 14),
                           bg="#fffafa", relief=GROOVE)
    username_entry.grid(row=5, column=1, pady=10)

    # Password
    Label(form_frame, text="Password", width=20, font=("Segoe UI", 14), anchor="w",
          bg=PALETTE["bg_end"], fg=PALETTE["muted"]).grid(row=6, column=0, padx=20, pady=10)
    password_entry = Entry(form_frame, textvariable=reg_pass_var, font=("Segoe UI", 14),
                           bg="#fffafa", show='*', relief=GROOVE)
    password_entry.grid(row=6, column=1, pady=10)

    # Submit button
    def register_user():
        u = reg_username_var.get().strip()
        p = reg_pass_var.get().strip()
        if not u or not p:
            messagebox.showwarning("Missing fields", "Username and password required.")
            return
        if u in os.listdir():
            messagebox.showerror("Error", "Username already exists.")
            return
        with open(u, "w") as f:
            f.write(u + "\n" + p)
        messagebox.showinfo("Success", "✨ Registration Successful!")
        register_screen.destroy()

    btn = Button(register_screen, text="✨ Register ✨", bg=PALETTE["accent2"], fg="white",
                 font=("Segoe UI", 16, "bold"), width=15, pady=8, relief=RAISED, command=register_user)
    btn.pack(pady=30)
    _on_hover(btn, "#ffd166", PALETTE["accent2"], enter_fg="#000000", leave_fg="white")

    
    def _do_register():
        u = reg_username_var.get().strip()
        p = reg_pass_var.get().strip()
        if not u or not p:
            messagebox.showwarning("Missing fields", "Please enter both username and password.")
            return
        # simple file-based storage (as original)
        if u in os.listdir():
            messagebox.showerror("Oops", "Username already exists. Choose another.")
            return
        with open(u, "w") as f:
            f.write(u + "\n" + p)
        messagebox.showinfo("Welcome", "Registration successful! 🎉")
        card.destroy()

    btn = Button(body, text="Register", bg=PALETTE["accent2"], fg="white", font=("Segoe UI", 14, "bold"), width=18, command=_do_register, relief=FLAT)
    btn.grid(row=3, column=1, pady=24)
    _on_hover(btn, "#ffd166", PALETTE["accent2"], enter_fg="#000000", leave_fg="white")


def login(main):
    global login_user_var, login_pass_var
    login_user_var = StringVar()
    login_pass_var = StringVar()

    card = Toplevel(main)
    card.title("Login")
    card.geometry("680x420")
    card.configure(bg=PALETTE["bg_end"])

    Label(card, text="Welcome back", bg=PALETTE["header_bg"], fg="white",
          font=("Segoe UI", 20, "bold"), pady=12).pack(fill=X)

    body = Frame(card, bg=PALETTE["card_bg"], padx=30, pady=20)
    body.pack(fill=BOTH, expand=True)

    Label(body, text="Username", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=0, column=0, sticky="w", pady=8)
    Entry(body, textvariable=login_user_var, font=FONT_SUB, bg="#fffafa", bd=2, relief=GROOVE, width=30).grid(row=0, column=1, pady=8)

    Label(body, text="Password", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=1, column=0, sticky="w", pady=8)
    Entry(body, textvariable=login_pass_var, font=FONT_SUB, bg="#fffafa", bd=2, relief=GROOVE, show='*', width=30).grid(row=1, column=1, pady=8)

    def _do_login():
        u = login_user_var.get().strip()
        p = login_pass_var.get().strip()
        if not u or not p:
            messagebox.showwarning("Missing fields", "Please fill both fields.")
            return
        if u in os.listdir():
            with open(u, 'r') as f:
                lines = f.read().splitlines()
            if p in lines:
                messagebox.showinfo("Success", "Login successful ✅")
                card.destroy()
                BMR_screen(main, u)
                return
            else:
                messagebox.showerror("Wrong", "Invalid password")
                return
        else:
            messagebox.showerror("Not found", "User not found")

    btn = Button(body, text="Login", bg=PALETTE["accent"], fg="white", font=("Segoe UI", 14, "bold"), width=14, command=_do_login, relief=FLAT)
    btn.grid(row=2, column=1, pady=18)
    _on_hover(btn, "#ffd166", PALETTE["accent"], enter_fg="#000000", leave_fg="white")


# -------------------- BMR & Meal Plan --------------------

def BMR_screen(root, username):
    win = Toplevel(root)
    win.title(f"Dietician — {username}")
    win.geometry("980x720")
    win.configure(bg=PALETTE["bg_end"])

    Label(win, text="Personalized Plan", bg=PALETTE["header_bg"], fg="white",
          font=("Segoe UI", 20, "bold"), pady=10).pack(fill=X)

    main_frame = Frame(win, bg=PALETTE["card_bg"], padx=20, pady=20)
    main_frame.pack(fill=BOTH, expand=True)

    # Left: inputs
    left = Frame(main_frame, bg=PALETTE["card_bg"])
    left.grid(row=0, column=0, sticky="nsew", padx=(0,20))

    Label(left, text="Weight (kg)", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=0, column=0, sticky='w')
    w_var = DoubleVar(value=70)
    Scale(left, variable=w_var, from_=30, to=180, orient=HORIZONTAL, length=300).grid(row=1, column=0, pady=8)

    Label(left, text="Height (cm)", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=2, column=0, sticky='w')
    h_var = DoubleVar(value=170)
    Scale(left, variable=h_var, from_=120, to=230, orient=HORIZONTAL, length=300).grid(row=3, column=0, pady=8)

    Label(left, text="Age", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=4, column=0, sticky='w')
    age_var = IntVar(value=30)
    Spinbox(left, from_=10, to=100, textvariable=age_var, width=6, font=FONT_LABEL).grid(row=5, column=0, pady=8, sticky='w')

    Label(left, text="Gender", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=6, column=0, sticky='w', pady=(12,0))
    gender_var = StringVar(value='Male')
    OptionMenu(left, gender_var, 'Male', 'Female').grid(row=7, column=0, sticky='w', pady=8)

    Label(left, text="Activity level", font=FONT_LABEL, bg=PALETTE["card_bg"], fg=PALETTE["muted"]).grid(row=8, column=0, sticky='w', pady=(12,0))
    activity_var = StringVar(value='Sedentary')
    activities = ['Sedentary','Lightly active','Moderately active','Very active','Super active']
    OptionMenu(left, activity_var, *activities).grid(row=9, column=0, sticky='w', pady=8)

    # Right: results & meal plan
    right = Frame(main_frame, bg=PALETTE["card_bg"], width=420)
    right.grid(row=0, column=1, sticky="nsew")

    result_lbl = Label(right, text="Your daily calorie need will appear here", wraplength=380, justify='left', bg=PALETTE["card_bg"], fg=PALETTE["muted"], font=FONT_LABEL)
    result_lbl.pack(pady=8)

    meal_frame = Frame(right, bg=PALETTE["card_bg"], bd=1, relief=GROOVE)
    meal_frame.pack(fill=BOTH, expand=True, padx=8, pady=8)

    # helper to compute
    def compute_and_show():
        try:
            w = float(w_var.get())
            h = float(h_var.get())
            age = float(age_var.get())
        except Exception:
            messagebox.showerror("Invalid", "Please enter valid numeric values")
            return
        gender = gender_var.get()
        act = activity_var.get()

        if gender == 'Male':
            bmr = 88.362 + (13.397 * w) + (4.799 * h) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * w) + (3.098 * h) - (4.330 * age)

        activity_factor = {
            'Sedentary': 1.2,
            'Lightly active': 1.375,
            'Moderately active': 1.55,
            'Very active': 1.725,
            'Super active': 1.9
        }[act]

        calories = int(bmr * activity_factor)
        result_lbl.config(text=f"Estimated daily calories: {calories} kcal")

        # produce a colorful meal plan
        for widget in meal_frame.winfo_children():
            widget.destroy()

        meals = _generate_meals(calories)
        for idx, (title, text) in enumerate(meals.items()):
            f = Frame(meal_frame, bg=("#f7fff7" if idx % 2 == 0 else "#fff7f7"), padx=8, pady=8)
            f.pack(fill=X, padx=6, pady=6)
            Label(f, text=title, font=("Segoe UI", 12, "bold"), bg=f['bg']).pack(anchor='w')
            Label(f, text=text, font=("Segoe UI", 11), bg=f['bg'], wraplength=360, justify='left').pack(anchor='w')

    compute_btn = Button(right, text="Calculate & Generate Plan", bg=PALETTE["accent"], fg="white", font=("Segoe UI", 12, "bold"), command=compute_and_show, relief=FLAT)
    compute_btn.pack(pady=12)
    _on_hover(compute_btn, "#ffd166", PALETTE["accent"], enter_fg="#000000", leave_fg="white")

    # make grid expand nicely
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)


# small meal generator
def _generate_meals(cal):
    proteins = ['Grilled chicken (100g)', 'Tofu (120g)', 'Greek yogurt (1 cup)', 'Salmon (90g)', 'Egg whites (4)']
    fruits = ['Apple', 'Banana', 'Mixed berries', 'Orange']
    veg = ['Steamed broccoli', 'Mixed salad', 'Sauteed spinach']
    grains = ['Brown rice (150g)', 'Quinoa (150g)', 'Whole wheat bread (2 slices)']
    extras = ['1 tbsp olive oil', 'Handful nuts', '1/2 avocado']

    # simple templates scaled by calories
    breakfast = f"{choice(proteins)} + {choice(fruits)} + {choice(grains)}"
    lunch = f"{choice(proteins)} + {choice(veg)} + {choice(grains)} + {choice(extras)}"
    snack = f"{choice(fruits)} + {choice(extras)}"
    dinner = f"{choice(proteins)} + 2 x {choice(veg)} + {choice(grains)}"

    return {
        'Breakfast': breakfast,
        'Lunch': lunch,
        'Snack': snack,
        'Dinner': dinner
    }


# -------------------- Main UI --------------------

def main_account_screen():
    root = Tk()
    root.geometry("1300x820")
    root.title("AI Dietician — Modern")
    root.resizable(False, False)

    # gradient background on a Canvas
    canvas = Canvas(root, width=1300, height=820, highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)
    _make_gradient(canvas, 1300, 820, PALETTE['bg_start'], PALETTE['bg_end'])

    # top header card
    hdr = Frame(root, bg=PALETTE['header_bg'], pady=16)
    hdr.place(relx=0.5, y=40, anchor='n', width=1100)
    Label(hdr, text="🥗 AI DIETICIAN — Modern UI", bg=PALETTE['header_bg'], fg="white", font=FONT_HEADER).pack()

    # center cards
    left_card = Frame(root, bg=PALETTE['card_bg'], bd=0)
    left_card.place(x=140, y=160, width=420, height=480)
    Label(left_card, text="Welcome", font=("Segoe UI", 18, "bold"), bg=PALETTE['card_bg']).pack(pady=12)
    Label(left_card, text="Already have an account?", font=FONT_LABEL, bg=PALETTE['card_bg'], fg=PALETTE['muted']).pack(pady=6)
    btn_login = Button(left_card, text="Login", bg=PALETTE['accent'], fg="white", font=("Segoe UI", 14, "bold"), width=18, height=2, command=lambda: login(root), relief=FLAT)
    btn_login.pack(pady=18)
    _on_hover(btn_login, "#ffd166", PALETTE['accent'], enter_fg="#000000", leave_fg="white")

    right_card = Frame(root, bg=PALETTE['card_bg'], bd=0)
    right_card.place(x=740, y=160, width=420, height=480)
    Label(right_card, text="New here?", font=("Segoe UI", 18, "bold"), bg=PALETTE['card_bg']).pack(pady=12)
    Label(right_card, text="Create account and get personalized plans", font=FONT_LABEL, bg=PALETTE['card_bg'], fg=PALETTE['muted']).pack(pady=6)
    btn_reg = Button(right_card, text="Register", bg=PALETTE['accent2'], fg="white", font=("Segoe UI", 14, "bold"), width=18, height=2, command=lambda: register(root), relief=FLAT)
    btn_reg.pack(pady=18)
    _on_hover(btn_reg, "#ffd166", PALETTE['accent2'], enter_fg="#000000", leave_fg="white")

    # Info card bottom
    info = Frame(root, bg=PALETTE['card_bg'])
    info.place(x=320, y=680, width=660, height=100)
    Label(info, text="Fast • Friendly • Personalised", font=("Segoe UI", 14, "bold"), bg=PALETTE['card_bg']).pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    main_account_screen()


# In[ ]:




