# Local development

One-time install for **hot reload** (browser refreshes when you save):

```bash
pip3 install -r requirements.txt
```

Then start the server:

```bash
./dev
```

Open **http://localhost:3000**. Edit any HTML/CSS and save — the browser reloads automatically.

---

Without the install, `./dev` still runs a plain server (no hot reload). You can also run `python3 -m http.server 3000` directly.
