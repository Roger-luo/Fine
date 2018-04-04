---
title: Fine
# subtitle: Roger's Fine Slide Generator
description: Roger's Fine Slide Generator
author: Roger

markdown:
  extensions:
  # more pymdownx extensions here:
  # https://facelessuser.github.io/pymdown-extensions/
    - pymdownx.magiclink
    - pymdownx.tasklist

reveal:
    # black/white/league/beige/sky/night/serif/simple/solarized
    theme: 'black'
    # full configuration see:
    # https://github.com/hakimel/reveal.js#configuration
    config:
        transition: 'fade'
...

---

# **F**{: style='color: #CD5C5C'} **I**{: style='color: orange'} **N**{: style='color: #4169E1'} **E**{: style='color: green'}

### **Roger**{: style='color: #696969'}'s Slide Generator {: style='color: #A9A9A9'}

---

# Header 1
## Header 2
### Header 3
#### Header 4

---

# MathJaX

$$
i\hbar\frac{\partial}{\partial t}\Psi = H\Psi
$$

---

# Code Block

```python
print('hello world!')
```

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

---

# Fragment

- first
{: .fragment}
- second
{: .fragment}

---

# More Fragment

---

### Grow

- one
{: .fragment .grow}
- two
{: .fragment .grow}
- three
{: .fragment .grow}

---

### Shrink

- three
{: .fragment .shrink}
- two
{: .fragment .shrink}
- one
{: .fragment .shrink}

---

### Fade Out

- one
{: .fragment .fade-out}
- two
{: .fragment .fade-out}
- three
{: .fragment .fade-out}

---

### Fade Up

- one
{: .fragment .fade-up}
- two
{: .fragment .fade-up}
- three
{: .fragment .fade-up}

---

### Current Visible

- one
{: .fragment .current-visible}
- two
{: .fragment .current-visible}
- three
{: .fragment .current-visible}

---

### HighLight `<Color>`

- one
{: .fragment .highlight-red}
- two
{: .fragment .highlight-green}
- three
{: .fragment .highlight-blue}

---

### Change Order

- two
{: .fragment data-fragment-index=2}
- one
{: .fragment data-fragment-index=1}
- three
{: .fragment data-fragment-index=3}

---

### Footnote

asd joi awm doa wmd sakdsa[^1]
dj ais djasd oasmd osam doks
amd oms adnn sandkjsa ndkjsan dks amd lkmwq
lkd nm lks alkd asdms alk dml ksam dlks aml
kdms ald ksam ldkamldksamdl ksamd

[^1]: This is a footnote

---

# Abbreviations

The HTML specification
is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]:  World Wide Web Consortium

---

# Smart Strong

Text with double__underscore__words.

__Strong__ still works.

__this__works__too__.

---

# Definition List

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

---

# Magic Link

http://rogerluo.me

---

Task List

- [X] item 1
    * [X] item A
    * [ ] item B
        more text
        + [x] item a
        + [ ] item b
        + [x] item c
    * [X] item C
- [ ] item 2
- [ ] item 3

---

# Table

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
