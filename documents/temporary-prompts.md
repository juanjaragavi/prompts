# Prompt

Below I am pasting a markdown file. Your task is to convert the contents of the pasted Markdown file into a Typescript `.ts` file called `strings.ts`, based on the template that I am also inserting below.

## Original Markdown File

```markdown
# Find the Perfect Credit Card for You!

Let's discover the ideal credit card tailored to your unique lifestyle and financial goals.Take this quick quiz to receive personalized recommendations!

---

**Page 1 of 2**

**Progress:** [====........................] 50%

**Question 1:** What's your primary goal for getting a new credit card?

- **A)** Build Credit: Establish or improve my credit score.
- **B)** Earn Rewards: Maximize points, miles, or cash back on my spending.
- **C)** Save Money: Reduce interest payments or consolidate existing debt.
- **D)** Big purchases: Finance a large purchase.
- **E)** Other: I have another financial objective in mind.

---

**Page 2 of 2**

**Progress:** [====================] 100%

**Question 2:** How would you describe your usual monthly spending habits?

- **A)** Very Low: I rarely use credit cards and prefer to pay with cash or debit.
- **B)** Low: I use credit cards for small, occasional purchases.
- **C)** Moderate: I use credit cards for everyday expenses and pay off the balance monthly.
- **D)** High: I use credit cards frequently and may carry a balance from time to time.
- **E)** Very High: I use credit cards extensively for most purchases and may carry a significant balance.

```

## `strings.ts` File Template

Use the following file as a template for the structure and placement of the text strings extracted from the Markdown file above.

```typescript
export const step1Strings = {
  progress: "1 / 2",
  title: "Find your credit card",
  question: "What matters most to you when choosing a credit card?",
  options: [
    { id: "A", label: "High credit limit" },
    { id: "B", label: "Instant approval" },
    { id: "C", label: "No credit check required" },
    { id: "D", label: "No annual fee" },
    { id: "E", label: "Cashback rewards" },
    { id: "F", label: "Low or 0% APR" },
  ],
};

export const step2Strings = {
  progress: "2 / 2",
  title: "Find your credit card",
  question: "What is your monthly income?",
  options: [
    { id: "A", label: "Less than $2,500 USD" },
    { id: "B", label: "Between $2,500 and $5,000" },
    { id: "C", label: "Between $5,000 and $10,000" },
    { id: "D", label: "Between $10,000 and $15,000" },
    { id: "E", label: "Between $15,000 and $20,000" },
    { id: "F", label: "More than $20,000" },
  ],
};
```
