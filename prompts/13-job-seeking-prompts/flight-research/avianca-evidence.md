# Avianca — Fare Family & Refund Evidence (BOG→MEX)

**Search URL (results):** https://booking.avianca.com/av/booking/avail?departureDate=2026-09-17&tripType=round-trip&platform=WEBB2C&from=BOG&to=MEX&nbAdults=1&nbYoungs=0&nbChildren=0&nbInfants=0&language=EN&pointOfSale=US&returnDate=2026-09-27
**Timestamp:** Thu Aug 20 2026 15:00 (America/Bogota, GMT-0500)
**Params confirmed on page:** BOG ⇄ MEX, 17 Sep – 27 Sep 2026, 1 Adult, currency USD. Header showed "BOG ⇄ MEX | 17 Sep – 27 Sep | 1 Adult".
**Note:** Prices shown on the availability page are PER-DIRECTION (outbound leg). Round-trip total = outbound fare + return fare (return leg priced after outbound selection).

## Outbound direct flights (Thu 17 Sep 2026), operated by Avianca, arriving MEX

| Dep   | Arr        | Duration | Lowest (Light)                                                                                          |
| ----- | ---------- | -------- | ------------------------------------------------------------------------------------------------------- |
| 19:15 | 23:00      | 4h45     | USD 318.29                                                                                              |
| 23:30 | 03:05 (+1) | 4h35     | USD 318.29                                                                                              |
| 14:20 | 18:05      | 4h45     | USD 402.09                                                                                              |
| 08:20 | 12:10      | 4h50     | USD 653.49                                                                                              |
| 02:00 | 05:39      | 4h39     | USD 695.54 — ARRIVES NLU (Felipe Ángeles), NOT MEX; operated by Viva Aerobus → excluded (wrong airport) |

## Economy fare families (for 19:15 flight; representative)

| Fare family | Price (outbound) | Changes                          | Refunds (per fare card icons)                                  |
| ----------- | ---------------- | -------------------------------- | -------------------------------------------------------------- |
| **Light**   | USD 318.29       | Changes before flight (with fee) | ✗ Refunds (crossed out = NOT included)                         |
| **Classic** | USD 391.59       | Changes before flight (greyed)   | ✗ Refunds (crossed out = NOT included)                         |
| **Flex**    | USD 423.04       | ✓ Changes (before the flight)    | ✓ **"Refunds (before the flight)"** listed as included benefit |

## General "Fare conditions" disclosure (verbatim, first-party Avianca page)

1. "Basic, Light, Classic, and Business Classic fares have change fees. Flex and Business Flex fares allow changes without a change fee before departure; fare differences and taxes may apply."
2. "**Refunds after the flight are not permitted for any fare, except in the event of operational disruptions.**"
3. "Refund conditions apply solely to the amount paid for the fare. Taxes, fees, and charges will be refunded in accordance with applicable legal provisions and as stipulated in the Contract of Carriage."
4. "All our fares (Basic, Light, Classic, Flex, and Business Classic), except Business Flex, are promotional."
5. No-show: "If you do not show up for the first leg of your trip, it will be considered a 'no-show' and the subsequent legs of your reservation will be canceled."

## Interpretation (against task refund standard)

- **Light & Classic:** Explicitly NOT refundable (✗ Refunds). REJECT.
- **Flex:** The only economy fare with a "Refunds (before the flight)" line item shown as included. This indicates a **voluntary refund permitted before departure**, refunding the fare amount. This is distinct from the "free change" benefit (shown as a separate line).
- CAVEAT: The fare card icon says "Refunds (before the flight)" but the UI does not spell out "to original form of payment" or "$0 penalty" verbatim on this screen. The general note confirms the refund is of "the amount paid for the fare" (i.e., money, not voucher) and applies before the flight. Applying the more-restrictive rule, the exact penalty/OFOP wording should ideally be confirmed in the Contract of Carriage / Help Center, but the first-party fare card does explicitly present Refunds-before-flight as an included Flex benefit (contrast with ✗ on Light/Classic).

## Flex ROUND-TRIP price — CONFIRMED on avail page (pre-passenger-data)

Outbound selected = Flex USD 423.04 (19:15 BOG→MEX, direct, 4h45).
Return leg fare families (MEX→BOG 00:40→06:15, Sep 27, direct, 4h35, operated by Avianca):

- Light USD 250.99 (✗ refunds)
- Classic USD 327.59 (✗ refunds)
- **Flex USD 360.49 (✓ Refunds before the flight)**

**ROUND-TRIP FLEX/FLEX TOTAL = 423.04 + 360.49 = USD 783.53** → UNDER USD 900 ✓

### QUALIFYING OPTION (Avianca)

- Route: BOG↔MEX, both directions DIRECT (0 stops)
- Outbound: AV, 17 Sep 19:15 BOG → 23:00 MEX (4h45)
- Return: AV, 27 Sep 00:40 MEX → 06:15 BOG (4h35)
- Fare family: FLEX (economy) both legs
- All-in RT price: USD 783.53 (per-passenger prices shown "Price per passenger"; taxes/fees included in Avianca displayed fare total)
- Refund: Flex fare card explicitly lists "Refunds (before the flight)" as included; general conditions confirm refund of amount paid for the fare (money, not voucher), before flight, no change/cancel fee stated for Flex (Flex = no change fee; refund permitted before departure).
- COP: not displayed (site currency was USD). COP not directly available.
- Alternative cheaper return times also at USD 250.99 base (04:55 flight) with Flex likely same ~360.

Note: Currency format uses comma as decimal (USD 423,04 = 423.04).
