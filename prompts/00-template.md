## **Context**

TopNetworks is a company that helps people advertise on the internet. We create and manage online advertising campaigns for our clients. We have four online platforms. They include financial blogs with valuable content about financial wellness, as well as tips and tricks. We also offer free information about the benefits and requirements of the best credit cards. We only need users' names and email addresses.

Our online platforms are:

- **TopFinanzas USA (TFUS):** `https://us.topfinanzas.com`
- **TopFinanzas México (TFMEX):** `https://topfinanzas.com/mx`
- **TopFinanzas UK (TFUK):** `https://uk.topfinanzas.com`
- **BudgetBee (BBUS):** `https://budgetbeepro.com`

We will make a new Astro.js project. It will be a blog about financial wellness, similar to the ones above. The new site will be called MejoresFinanzas and will have the same content strategy and business model as our existing financial wellness blogs, above.

## **Task**

Generate an executive report about MejoresFinanzas, detailing the description of the site, the target audience, and other important information about the site.
This new site, will be based on two existing projects, located on the following local directories: `/Users/macbookpro/Github/budgetbee` and `/Users/macbookpro/Github/uk-topfinanzas-com`. Browse those projects to obtain extra context about what we want for MejoresFinanzas.

## **Output Structure**

Deliver your output as a JSON object.

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

Refine your report:
  
1. Include only the following topics
  - Project Overview
  - Target Audience
  - Competitive Advantages
2. The site will have native ENGLISH content, not Spanish. The Spanish version is coming later this year.
