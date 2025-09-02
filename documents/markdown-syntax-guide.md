```python
print("Written by `claude-3-opus-20240229`")
```

# Markdown Syntax Guide

## Headers

# H1

## H2

### H3

#### H4

##### H5

###### H6

## Emphasis

_Italic text_ _Italic text_

**Bold text** **Bold text**

**_Bold and Italic text_** **_Bold and Italic text_**

~~Strikethrough text~~

## Lists

### Unordered List

- Item 1
- Item 2
  - Subitem 1
  - Subitem 2
- Item 3

### Ordered List

1. First item
2. Second item
3. Third item
   1. Indented item
   2. Indented item
4. Fourth item

## Links

[Link Text](https://www.example.com)

[Link with Title](https://www.example.com 'Link Title')

## Images

![Alt Text](https://www.example.com/image.jpg)

![Alt Text with Title](https://www.example.com/image.jpg 'Image Title')

## Code

Inline `code` has `back-ticks around` it.

```javascript
var example = 'This is a code block';
console.log(example);
```

## Blockquotes

> This is a blockquote.
>
> It can span multiple lines.

## Horizontal Rules

---

---

---

## Tables

| Column 1      | Column 2      | Column 3      |
| ------------- | ------------- | ------------- |
| Row 1, Cell 1 | Row 1, Cell 2 | Row 1, Cell 3 |
| Row 2, Cell 1 | Row 2, Cell 2 | Row 2, Cell 3 |

## Task Lists

- [x] Completed task
- [ ] Incomplete task
  - [x] Subtask 1
  - [ ] Subtask 2

## Footnotes

Here's a sentence with a footnote reference.[^1]

[^1]: This is the footnote.

## Escaping Characters

To escape characters that have special meaning in Markdown, use a backslash (\\) before the
character. For example, \*this\* will not be italicized.
