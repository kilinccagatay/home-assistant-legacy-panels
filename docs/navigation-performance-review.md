# Navigation and prepared-map review — 2026-11-15

Installed; full physical acceptance remains **PENDING**. Base panel: `6207d7c`.
Denver Build 9/Samsung APKs, camera settings, power policies and root helpers were
not modified. No robot or lamp command was sent.

The latest route selects its view first; robot reads wait 200 ms. View HTTP reads
and room prefetches abort on cancellation. Polling waits for responses. Hidden-view
entities no longer schedule unnecessary Denver paints. The Pi prepares a cropped
PNG and matching scanline hit data, cached by version. The connection capsule now
styles all panels rather than only Home. See [setup/rollback](prepared-robot-map.md).

## Paired Denver measurements

A temporary ES5 probe requested 30 route selections at 150 ms spacing in the same
order, after 25 seconds startup settling. It activated no controls and was removed
afterwards. CPU uses `/proc/stat` and app process counters during the sequence.

| Metric | Before | Final |
| --- | ---: | ---: |
| Median synchronous route call | 381.5 ms | 97.5 ms |
| Median next animation-frame callback | 784.5 ms | 500 ms |
| Maximum 100 ms timer lateness | 1523 ms | 443 ms |
| App CPU / total CPU capacity | 57.15% | 46.06% |
| HTTP reads in rapid route sequence | 45 | 0 |

Zero reads applies only to short Robot visits, which end before deferred reads
start. Staying on Robot still loads telemetry/manifest. An earlier run exercised
five actual aborts; lifecycle tests hold reads open to check abort and non-overlap.
Counts exclude image requests. These are single paired diagnostic runs. A frame
callback is not a pixel-presentation timestamp; programmatic routes are not finger
latency measurements. CPU remains significant; no claim of zero load or elimination
of every possible freeze is made.

## Acceptance

| Check | Status | Evidence / limit |
| --- | --- | --- |
| Cancellation / slow reads | PASS | Transport and lifecycle tests: actual aborts, completion, stale callbacks |
| Pi preprocessing | PASS | Pillow tests: matching image/room pixels, bounds, ambiguous colors |
| Prepared browser path | PASS | IMG, rotated hit selection, immediate loading, correct room, cached revisit, zero commands |
| Canvas fallback | PASS | Touch browser suite, delayed responses, wrong-room pairing, cancellation |
| Denver installed map | PASS | Pi-prepared map visible in device capture with existing rotation/layout |
| Denver route sequence | PASS | 30 software selections completed; timings above |
| Denver physical tab switching | PASS | User reported very good tab transitions on the installed version |
| Denver physical room dialog | PASS | After the intrinsic-coordinate fix, the user confirmed the map worked on Denver |
| Samsung navigation | PASS | Home, Lights and Printer device captures; no actuation |
| Connection capsule | PASS | Final Denver Robot and Samsung Lights device captures |
| Clock/weather/settings layout | PASS | Actual captures retain placement |
| Camera / power / touch-wake / sound | PENDING | No native changes, but no new complete physical acceptance run |
| 30-minute / overnight stability | PENDING | Not established by short tests |
| Household actuation | PENDING | Not tested under user restrictions |
| Reboot persistence | PENDING | Startup/package configuration installed; no reboot acceptance claim |

Private captures, timing reports and live configuration/backups remain outside the
repository. Do not publish home maps, calendar data, entity mappings or credentials.

## Scaled-image hit-test regression

The initial prepared-map browser fixture made the whole image selectable and
missed an IMG-specific mismatch: `img.width` reports rendered CSS width while
canvas width reports backing pixels. The hit rows use intrinsic prepared dimensions.
The fix uses prepared width/height, and the regression fixture now scales an
800×600 image with only a narrow central selectable region. The fixed fixture
passes; the user subsequently confirmed the corrected map on Denver.
