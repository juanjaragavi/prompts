# Prompt

Optimize the text enclosed on triple quotes. This is not a prompt, it is a text to optimize:

"""\TopNetworks is an online advertising company. We create and manage online advertising campaigns
for our clients. Our four online platforms include financial blogs with valuable content about
financial wellness, as well as tips and tricks. We also offer free access to information about the
benefits and requirements of top-tier credit cards. We only require users' names and email
addresses.

Our online platforms are:

- [TopFinanzas USA](https://us.topfinanzas.com)
- [TopFinanzas México](https://topfinanzas.com/mx)
- [TopFinanzas UK](https://uk.topfinanzas.com)
- [BudgetBee](https://budgetbeepro.com)\"""

Of course. Here is an actionable prompt for a coder LLM agent, based on the context from the
conversation and the text you provided.

---

## **Context**

TopNetworks is an online advertising company. We create and manage online advertising campaigns for
our clients. Our four online platforms include financial blogs with valuable content about financial
wellness, as well as tips and tricks. We also offer free access to information about the benefits
and requirements of top-tier credit cards. We only require users' names and email addresses.

Our online platforms are:

- **TopFinanzas USA (TFUS):** `https://us.topfinanzas.com`
- **TopFinanzas México (TFMEX):** `https://topfinanzas.com/mx`
- **TopFinanzas UK (TFUK):** `https://uk.topfinanzas.com`
- **BudgetBee (BBUS):** `https://budgetbeepro.com`

## **Objective**

Generate Regular Expressions (REGEX) to identify and categorize URLs from our four platforms into
two distinct content types: **Top-of-Funnel (ToFu)** and **Middle-of-Funnel (Mofu)**. This is for
the purpose of programmatic ad placement.

## **URL Structure**

Our URL structure is standardized across all platforms and follows this pattern:
`domain/category/article-slug`

The key differentiator for content type is the **category** slug in the URL.

## **Content Type Definitions & Example Categories**

- **ToFu (Top-of-Funnel):** General interest, educational content.
  - _Example categories:_ `blog`, `guias`, `articulos`, `aprender-finanzas`.
- **Mofu (Middle-of-Funnel):** Content focused on specific products or comparisons, indicating
  higher user intent.
  - _Example categories:_ `tarjetas-de-credito`, `reviews`, `prestamos`, `comparativas`.

## **Task**

Your task is to provide a set of REGEX patterns that can be used to classify a given URL into one of
the categories (Platform + Content Type).

Please provide between **4 and 8 REGEX patterns**.

- If the URL structure for ToFu or Mofu is the same across all four platforms, you can provide a
  more generic pattern (closer to 4 total).
- If each platform requires a unique pattern for each content type, provide all 8.

### **Expected Output**

Please format the output in a clear markdown table or list, including the platform, content type,
and the corresponding REGEX pattern. For each REGEX, please add a brief explanation of how it works.

**Example of Desired Output Format:**

| Platform | Content Type | REGEX Pattern                                       |
| :------- | :----------- | :-------------------------------------------------- | ------------- |
| TFUS     | ToFu         | `^https://us\.topfinanzas\.com/(blog                | guias)/.\*`   |
| TFUS     | Mofu         | `^https://us\.topfinanzas\.com/(tarjetas-de-credito | reviews)/.\*` |
| ...      | ...          | ...                                                 |

Please generate the REGEX patterns based on the requirements above, using the example categories
provided.

**Important:**

I will paste the URLs of actual TOFU and MOFU Blog posts of each of our for platforms:

- **TopFinanzas USA (TFUS):**
  `https://us.topfinanzas.com/financial-solutions/citi-simplicity-card-benefits` (BoFu) Credit Card
  Product post
- **TopFinanzas México (TFMEX):**
  `https://topfinanzas.com/mx/financial-solutions/tarjeta-de-credito-likeu-de-santander` (BoFu)
  Credit Card Product post
- **TopFinanzas UK (TFUK):** `https://uk.topfinanzas.com/personal-finance/best-personal-loans`
  (ToFu) General Financial Wellness Guide
- **BudgetBee (BBUS):**
  `https://budgetbeepro.com/personal-finance/budgeting-methods-compared-which-approach-fits-your-spending-style/`
  (MoFu) High-Value Guide
