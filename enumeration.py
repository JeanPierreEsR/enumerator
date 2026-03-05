'''
This code enumerates items within text (depending on the desired format) such as
"following: i) Peru; ii) Colombia"

It accepts text separated by commas, semicolons, or newlines, and enumerates
each item automatically with Roman numerals in the chosen format.
'''
import re
import tkinter as tk
from tkinter import ttk, messagebox

_ROMAN_VALUES = [
    (1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'),
    (100,  'c'), (90,  'xc'), (50,  'l'), (40,  'xl'),
    (10,   'x'), (9,   'ix'), (5,   'v'), (4,   'iv'), (1, 'i'),
]


def to_roman(n):
    """Convert a positive integer to a lowercase roman numeral string."""
    result = ''
    for value, numeral in _ROMAN_VALUES:
        while n >= value:
            result += numeral
            n -= value
    return result


def roman_numerals(count, fmt):
    """Return a list of *count* roman numeral strings in the requested format."""
    if fmt == '(i)':
        return [f'({to_roman(i)})' for i in range(1, count + 1)]
    else:  # 'i)'
        return [f'{to_roman(i)})' for i in range(1, count + 1)]


def process_text():
    """Read input, split by chosen separator, enumerate, and display result."""
    raw = input_text.get('1.0', tk.END).strip()
    if not raw:
        messagebox.showwarning('Warning', 'Please enter some text.')
        return

    # Split input
    in_sep = input_separator.get()
    if in_sep == ',':
        items = re.split(r',\s*', raw)
    elif in_sep == ';':
        items = re.split(r';\s*', raw)
    else:  # newline
        items = raw.splitlines()

    items = [item.strip() for item in items if item.strip()]
    if not items:
        messagebox.showwarning('Warning', 'No items found after splitting.')
        return
    num = numbering.get()
    skip = num == 'none'
    roman = roman_numerals(len(items), num)
    last_sep = 'y' if spanish.get() else 'and'

    if lowercase_subsequent.get():
        items = [items[0]] + [item[0].lower() + item[1:] if item else item for item in items[1:]]

    out_sep = output_separator.get()
    if out_sep == '\n':
        join = '\n'
    else:
        join = f'{out_sep} '

    if skip:
        if len(items) == 1:
            result = items[0]
        else:
            result = join.join(items[:-1]) + join + f'{last_sep} {items[-1]}'
    elif len(items) == 1:
        result = f'{roman[0]} {items[0]}'
    else:
        parts = [f'{roman[i]} {item}' for i, item in enumerate(items[:-1])]
        last_part = f'{last_sep} {roman[len(items) - 1]} {items[-1]}'
        result = join.join(parts) + join + last_part

    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, result)


def copy_to_clipboard():
    """Copy the output text to the system clipboard."""
    result = output_text.get('1.0', tk.END).strip()
    if result:
        root.clipboard_clear()
        root.clipboard_append(result)
        root.update()


def clear_all():
    """Clear both input and output areas."""
    input_text.delete('1.0', tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)


# ── Main window ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Elements' Enumeration")
root.resizable(True, True)

PAD = {'padx': 8, 'pady': 4}

# ── Input area ─────────────────────────────────────────────────────────────────
input_frame = ttk.LabelFrame(root, text='Input Text', padding=8)
input_frame.grid(row=0, column=0, sticky='nsew', **PAD)

input_text = tk.Text(input_frame, height=6, width=64, wrap=tk.WORD)
input_text.pack(fill=tk.BOTH, expand=True)

# ── Options ────────────────────────────────────────────────────────────────────
options_frame = ttk.LabelFrame(root, text='Options', padding=8)
options_frame.grid(row=1, column=0, sticky='ew', **PAD)

# Input separator
ttk.Label(options_frame, text='Input separator:').grid(
    row=0, column=0, sticky='w', padx=4, pady=3)
input_separator = tk.StringVar(value=',')
for col, (lbl, val) in enumerate(
        [('Comma  ,', ','), ('Semicolon  ;', ';'), ('Newline  \\n', '\n')], start=1):
    ttk.Radiobutton(options_frame, text=lbl, variable=input_separator,
                    value=val).grid(row=0, column=col, padx=8, sticky='w')

# Output separator
ttk.Label(options_frame, text='Output separator:').grid(
    row=1, column=0, sticky='w', padx=4, pady=3)
output_separator = tk.StringVar(value=';')
for col, (lbl, val) in enumerate(
        [('Comma  ,', ','), ('Semicolon  ;', ';'), ('Newline  \\n', '\n')], start=1):
    ttk.Radiobutton(options_frame, text=lbl, variable=output_separator,
                    value=val).grid(row=1, column=col, padx=8, sticky='w')

# Numbering format
ttk.Label(options_frame, text='Numbering:').grid(
    row=2, column=0, sticky='w', padx=4, pady=3)
numbering = tk.StringVar(value='(i)')
ttk.Radiobutton(options_frame, text='(i)  →  (i), (ii), (iii)…',
                variable=numbering, value='(i)').grid(
    row=2, column=1, padx=8, sticky='w')
ttk.Radiobutton(options_frame, text='i)   →  i), ii), iii)…',
                variable=numbering, value='i)').grid(
    row=2, column=2, padx=8, sticky='w')
ttk.Radiobutton(options_frame, text='None  →  skip enumerators',
                variable=numbering, value='none').grid(
    row=2, column=3, padx=8, sticky='w')

# Spanish checkbox
spanish = tk.BooleanVar(value=False)
ttk.Checkbutton(options_frame, text='Spanish  (use "y" instead of "and")',
                variable=spanish).grid(
    row=3, column=0, columnspan=4, sticky='w', padx=4, pady=3)

# Lowercase subsequent checkbox
lowercase_subsequent = tk.BooleanVar(value=False)
ttk.Checkbutton(options_frame, text='Lowercase first letter of points (ii) onwards',
                variable=lowercase_subsequent).grid(
    row=4, column=0, columnspan=4, sticky='w', padx=4, pady=3)

# ── Buttons ────────────────────────────────────────────────────────────────────
btn_frame = ttk.Frame(root)
btn_frame.grid(row=2, column=0, pady=4)

ttk.Button(btn_frame, text='Enumerate', command=process_text).grid(
    row=0, column=0, padx=8)
ttk.Button(btn_frame, text='Copy to Clipboard', command=copy_to_clipboard).grid(
    row=0, column=1, padx=8)
ttk.Button(btn_frame, text='Clear', command=clear_all).grid(
    row=0, column=2, padx=8)

# ── Output area ────────────────────────────────────────────────────────────────
output_frame = ttk.LabelFrame(root, text='Result', padding=8)
output_frame.grid(row=3, column=0, sticky='nsew', **PAD)

output_text = tk.Text(output_frame, height=6, width=64, wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)

# ── Grid weights (allow resizing) ──────────────────────────────────────────────
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(3, weight=1)

root.mainloop()
