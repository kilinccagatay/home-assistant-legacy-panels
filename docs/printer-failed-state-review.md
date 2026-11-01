# Retained failed-job state review — 2026-11-01

Observed live: printer last-job status `failed`, current stage `idle`, print error
`off` and HMS errors `off`. The previous panel always translated `failed` into
Baskı hatası. The new display-only resolver shows Hazır only with all three
explicit corroborating readings. Other failure/unknown combinations keep the
error state. Raw Home Assistant state and history are not changed.

Samsung remains native Build 16. Only office JavaScript, the installer and three
read-only office subscriptions changed; Denver deployment is unchanged. The
configuration, installer, JavaScript and mapping were privately backed up; a
failed deployment restores all original files. Rollback restores those backups.
No printer job, power, light or firmware command was sent for verification.

Existing office tests cover ready recovery, active print/HMS faults, unavailable
error and unknown stage, plus resumed printing and power-off dominance. Installer
tests verify the new subscriptions, domain validation and Denver isolation. ES5
parse passed. Real hardware faults were not induced. Before the final device capture, the
printer began a new job and correctly showed Yazdırılıyor; it was not cancelled
for this test. Live post-cancellation Ready observation therefore remains pending.

| Check | Status | Evidence / remaining work |
| --- | --- | --- |
| D01 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D02 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D03 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D04 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D05 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D06 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D07 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D08 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D09 | N/A | Samsung has no battery overlay; Denver assets unchanged. |
| D10 | N/A | Samsung has no battery overlay; Denver assets unchanged. |
| D11 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D12 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D13 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| D14 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U01 | N/A | Office profile omits the Denver layout, robot and all-house countdown. |
| U02 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U03 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U04 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U05 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U06 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U07 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| U08 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H01 | N/A | Office profile omits the Denver layout, robot and all-house countdown. |
| H02 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H03 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H04 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H05 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H06 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H07 | N/A | Office profile omits the Denver layout, robot and all-house countdown. |
| H08 | N/A | Office profile omits the Denver layout, robot and all-house countdown. |
| H09 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H10 | PENDING | Not repeated on this final deployment; no full general-feature acceptance claim. |
| H11 | PENDING | The observed failed/idle/no-fault combination passes fixtures. A new real job started before final capture; live post-cancel Ready confirmation remains pending. |
| E01 | PASS | Office DOM suite, six installer tests and ES5 parse passed. |
| E02 | PASS | Served resolver and three mapping keys verified. Actual Samsung captured a new running print; no cancellation/ready claim from that capture. |
| E03 | PASS | Only intended source/tests/guides published; private mappings/configuration and work-calendar captures excluded. |
| E04 | PASS | Guides and intended changes committed/pushed; other physical checks remain pending. |

Overall: PENDING for the complete general-feature gate.
