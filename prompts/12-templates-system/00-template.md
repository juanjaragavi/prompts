# Template File

\<Context\>

An audit by an external Google consultant has revealed a critical issue in our campaign tracking
system. Essential UTM parameters are being lost during the navigation flow from the initial ad-click
URL to the final landing page. Specifically, the `utm_source` parameter is being dropped, which
corrupts campaign performance data and attribution.

## Example of the Issue

- **Original URL (from the ad campaign):**

  ```text
  https://uk.topfinanzas.com/quiz?utm_source=adwords&utm_medium=cpc&utm_campaign=22524445886&utm_content=banner&utm_term=open
  ```

- **Final URL (on the landing page):**

  ```text
  https://uk.topfinanzas.com/credit-card-recommender-p1?utm_medium=cpc&utm_campaign=22524445886&utm_term=open&utm_content=banner
  ```

The discrepancy shows that `utm_source=adwords` is not being forwarded to the final destination,
which needs to be resolved to ensure data integrity.

\</Context\>

\<Task\>

Investigate the codebase to identify and resolve the root cause of the missing `utm_source`
parameter during URL redirection or client-side navigation.

### Requirements

1. **Code Audit**: Conduct a thorough review of the application's routing, redirection logic, and
   middleware. Pay close attention to any code that handles URL manipulation, especially server-side
   redirects (e.g., in Astro middleware) or client-side routing logic that might rebuild the URL's
   query string.
2. **Identify the Faulty Mechanism**: Pinpoint the exact function or configuration responsible for
   incorrectly forwarding or stripping the query parameters from the incoming request.
3. **Implement a Solution**: Modify the identified code to ensure that all original UTM parameters
   from the initial URL are preserved and correctly passed to the final destination page. The
   solution should be robust enough to handle all standard UTM parameters.
4. **Verification**: After implementing the fix, test the provided example URL to confirm that a
   user landing on the `/quiz` page is redirected to the `/credit-card-recommender-p1` page with the
   `utm_source` parameter and all other UTM parameters intact.

\</Task\>
