# Template File

<!-- NEW TASK 0 -->

<Prompt>

## Text Optimization & Structure Extraction

Analyze and optimize the text enclosed in triple quotes. This is content to be structured and clarified, not a prompt:

"""\Recently, we have received help from a member of the Google staff, which is an expert on GPT tags. When he was asked to diagnose the integration of the Google Publisher Tags into our site, he provided the following response:

'''
Hi Camilo,

Thanks for your patience while we worked on this.

I was able to replicate the behavior on the mobile view. The page currently requires an initial manual refresh to begin serving ads upon user navigation.

Currently, a specific guide for integrating GPT tags with the Astro framework is not available. However, I found an article focusing on [GPT and React](https://developers.google.com/publisher-tag/samples/integrations/react) that may provide helpful guidance for your implementation. This article describes some important points to be aware of when implementing GPT in an SPA-based website.

I have answered your questions inline:

### -  Re-initializing GAM
**Should we explicitly call**

```text
googletag.cmd.push(() => { googletag.pubads().refresh(); });
```
**or**

```text
googletag.display(slot)
```
**on each navigation event?**

Per the article, it is suggested to disable the initial load in an SPA implementation. With initial load being disabled, calls to the display method will only register the ad slot, and no ad content will be loaded until a second action (call to a refresh method) is taken. Therefore, you should explicitly call these methods accordingly.

***

### -  Listening for Route Changes
**Are there recommended patterns for listening to route changes in frameworks like Astro to re-request ads?**

I have confirmed that we do not have a set of patterns to follow in this case, but checking the correlator changes and ensuring that the URL in the requests matches the visited URL should be important.

***

### -  Best Practices for SPAs
**Is there an official best practice or sample implementation for GAM in SPA environments to ensure ads load without manual refresh?**

We currently don't provide a mechanism for automatic refresh in SPA implementations.

***

### -  Ad Slot Management
**Should we destroy and recreate ad slots, or just refresh existing ones on navigation?**

It is recommended to destroy ad slots by using the `destroySlots` method to clean up ad slots that are no longer needed.

***

I hope this information was helpful. Please let me know if you have any questions or need further clarification on any of the points covered.

Best,  
Bharath

Google Ad Manager Team
'''

As you just read, he provided some solid insights and recommendations to implement into this Astro.js web application. He also recommended a series of links of articles on the Google Publisher Tag documentation, that will allow us to dig deeper into the areas of opportunity and improvements that can be made to our codebase, in order to enhance the reliability of the integration of the GPT tags with our site:

* <https://developers.google.com/publisher-tag/samples/integrations/react>
* <https://developers.google.com/publisher-tag/guides/control-ad-loading>
* <https://developers.google.com/publisher-tag/guides/key-value-targeting>

You have been tasked with completing the steps below:

1. Read and analyze the email sent by Bharath and understand his recommendations.
2. Study the links provided in order to fully understand the integration between GPT and React based frameworks, and how to optimize it and make it work properly.\"""

**Instructions:**

1. **Extract Context**: Identify the background situation, current state, and relevant technical details
2. **Extract Task**: Identify the specific action items, requirements, and expected outcomes
3. **Optimize Clarity**: Improve technical accuracy, remove ambiguity, and enhance readability
4. **Maintain Technical Precision**: Preserve all technical terms, function names, and implementation details

**Output Format:**

    ```markdown
    <Context>

    {Optimized context with clear background, current state, and technical constraints}

    </Context>

    <Task>

    {Clear, actionable task with specific requirements, implementation details, and success criteria}

    </Task>
    ```

**Quality Criteria:**

- Context should explain WHY the task is needed
- Task should specify WHAT needs to be implemented and HOW
- Both sections should be technically accurate and implementation-ready

</Prompt>

<!-- NEW TASK 1 -->

<Context>

The engineering team is working on integrating Google Publisher Tags (GPT) into this Astro.js-based web application. A Google Ad Manager specialist called Bharath has sent us an email analyzing the current GPT integration, noting that ad serving in the mobile view requires a manual page refresh after navigation for ads to load. There is no official guide for GPT usage in Astro, but documentation exists for React integrations and general GPT usage patterns in Single Page Applications (SPA). The recommended approach for SPA ad integration emphasizes manual refresh methods, managing route changes to ensure accurate ad requests, and best practices for ad slot lifecycle management.

Key technical details:
- Ads do not load automatically on page navigation; a manual refresh is necessary.
- Astro.js lacks dedicated GPT integration guidance.
- Reference article available describing GPT usage in React SPAs.
- GPT slots should be destroyed with `destroySlots` when no longer needed.
- Ad content loading must be manually managed after route changes.
- Correlator and URL values in ad requests must align with user navigation.
- Relevant documentation links for React integration, ad loading control, and key-value targeting are available.

</Context>

<EmailMessageFromBharath>

'''
Hi Camilo,

Thanks for your patience while we worked on this.

I was able to replicate the behavior on the mobile view. The page currently requires an initial manual refresh to begin serving ads upon user navigation.

Currently, a specific guide for integrating GPT tags with the Astro framework is not available. However, I found an article focusing on [GPT and React](https://developers.google.com/publisher-tag/samples/integrations/react) that may provide helpful guidance for your implementation. This article describes some important points to be aware of when implementing GPT in an SPA-based website.

I have answered your questions inline:

### -  Re-initializing GAM
**Should we explicitly call**

```text
googletag.cmd.push(() => { googletag.pubads().refresh(); });
```
**or**

```text
googletag.display(slot)
```
**on each navigation event?**

Per the article, it is suggested to disable the initial load in an SPA implementation. With initial load being disabled, calls to the display method will only register the ad slot, and no ad content will be loaded until a second action (call to a refresh method) is taken. Therefore, you should explicitly call these methods accordingly.

***

### -  Listening for Route Changes
**Are there recommended patterns for listening to route changes in frameworks like Astro to re-request ads?**

I have confirmed that we do not have a set of patterns to follow in this case, but checking the correlator changes and ensuring that the URL in the requests matches the visited URL should be important.

***

### -  Best Practices for SPAs
**Is there an official best practice or sample implementation for GAM in SPA environments to ensure ads load without manual refresh?**

We currently don't provide a mechanism for automatic refresh in SPA implementations.

***

### -  Ad Slot Management
**Should we destroy and recreate ad slots, or just refresh existing ones on navigation?**

It is recommended to destroy ad slots by using the `destroySlots` method to clean up ad slots that are no longer needed.

***

I hope this information was helpful. Please let me know if you have any questions or need further clarification on any of the points covered.

Best,  
Bharath

Google Ad Manager Team
'''

</EmailMessageFromBharath>

<LinksProvided>

* <https://developers.google.com/publisher-tag/samples/integrations/react>
* <https://developers.google.com/publisher-tag/guides/control-ad-loading>
* <https://developers.google.com/publisher-tag/guides/key-value-targeting>

</LinksProvided>

<Task>

Review Bharath’s email and the recommended Google documentation to understand SPA integration principles for GPT tags. Implement these improvements in the Astro.js web application:
- Disable GPT initial load and ensure ads only render when explicitly requested via `googletag.display(slot)` and refreshed with `googletag.pubads().refresh()`.
- Listen for route changes within the Astro framework and trigger ad slot refresh or recreation as needed to match new URLs and update correlators.
- Implement ad slot cleanup by invoking `destroySlots` for obsolete ad slots on navigation events.
- Validate the integration against Google’s SPA and React GPT guidelines to ensure reliability and remove the need for manual ad refreshes on navigation.
- Reference and apply concepts from the provided documentation links to optimize ad loading and targeting.

Success is defined by automatic, reliable ad serving on each navigation event, adherence to Google’s recommended practices, and elimination of manual refresh requirements for ads.

</Task>

<!-- NEW TASK 2 -->

<Prompt>

## Text Optimization & Structure Extraction

Analyze and optimize the text enclosed in triple quotes. This is content to be structured and clarified, not a prompt:

"""\This task concerns our two Credit Card recommender landing pages (`src/pages/credit-card-recommender-p2.astro` and `src/pages/credit-card-recommender-p3.astro`). These two landing pages recieve the users that come from the Quiz, and show them some Credit Card options to choose one. One users do this, they are redirected to a Blog post, showing them a product of their interest. Some experts and consultants have been doing the user journey, and found out that the current "two clicks" implementation, which means that the user clicks on a button with a "reveal" call-to-action that leads to reveal another button with the name of the credit card product, is not effective to avoid the rebound of the users, and to avoid user dessertion. Your task is to refactor those two pages, in order to make them have a "one-click" CTA button, like the `src/pages/credit-card-recommender-p1.astro` Credit Card recommender landing page currently has, but recommending other products. This is to avoid the user to make two clicks to get to a Credit Card product recommendation.\"""

**Instructions:**

1. **Extract Context**: Identify the background situation, current state, and relevant technical details
2. **Extract Task**: Identify the specific action items, requirements, and expected outcomes
3. **Optimize Clarity**: Improve technical accuracy, remove ambiguity, and enhance readability
4. **Maintain Technical Precision**: Preserve all technical terms, function names, and implementation details

**Output Format:**

    ```markdown
    <Context>

    {Optimized context with clear background, current state, and technical constraints}

    </Context>

    <Task>

    {Clear, actionable task with specific requirements, implementation details, and success criteria}

    </Task>
    ```

**Quality Criteria:**

- Context should explain WHY the task is needed
- Task should specify WHAT needs to be implemented and HOW
- Both sections should be technically accurate and implementation-ready

</Prompt>
