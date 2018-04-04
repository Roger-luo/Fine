from fine.parser import Presentation

text = """
---
...

---
data:
    transition: zoom
transition:
    speed: fast

background:
    color: '#8B0000'
note: This is a speaker note.
...

# Frame YAML

---
background:
    image: /media/background.jpg
...

# Backgronud Image
"""

pre = Presentation(text)
