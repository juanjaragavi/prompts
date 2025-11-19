# Document

- remove or comment the adzep script, so we can test the new script all by itself
- ⁠we need to improve the logic when calling the topAds.spa function. when the offerwall opens, it
  changes the path on the browser, and next.js detects this change and activates topAds.spa, even
  though it’s not a page change, it’s just the offerwall being shown. the best way would be to
  remove any logic that depends on the current pathname to detect if a page has changed
- ⁠you can also remove the “autoStart: false” from the config
- ⁠and the image for the offerwall is returning a 404

- We need to remove or comment out the Adzep script so that we can test the new script
  independently.
- We need to improve the logic when calling the topAds.spa function because opening the offer wall
  changes the browser's path. Next.js detects this change and activates topAds.spa, even though
  showing the offerwall does not constitute a page change. The best solution would be to remove any
  logic that depends on the current pathname to detect a page change.
- You can also remove "autoStart: false" from the configuration.
- The offerwall image is returning a 404 error.
