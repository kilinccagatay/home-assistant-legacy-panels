# Prepared robot maps and cancellable navigation

The browser owns touch feedback, navigation and drawing. A read-only worker in the
existing Advanced SSH addon prepares maps on the Pi. No camera settings, Android
APK or vacuum command implementation changes are required.

## Worker

Install `py3-pillow` in the SSH addon's persistent `packages` option. Copy
`examples/map-worker/prepare-map.py` and a private copy of `config.example.json`
to `/config/panel-map-worker/`. Preserve all existing addon options. Set the exact
map entity, configured room colors/IDs, LAN bind address, port and allowed dashboard
origin. Prefer the private `/config/panel-map-worker/cache` output directory.

Add to `init_commands` without replacing existing entries:

```sh
nohup python3 /config/panel-map-worker/prepare-map.py /config/panel-map-worker/config.json >/dev/null 2>&1 &
```

Start that same command once to activate without restarting Home Assistant. A file
lock prevents duplicate workers. The Supervisor credential comes from the addon
environment (or its existing s6 environment file), never browser configuration.
The worker performs GET requests only; it cannot initiate cleaning through its
HTTP endpoint, which serves only prepared map assets. Its LAN listener exposes
map data; do not expose the port to the Internet. CORS limits browser origins,
not network access or authentication. Use a trusted LAN, or an authenticated
reverse proxy when access control is required.

Every 15 seconds it checks the source version. It downloads and processes the
source image only after a version change. Pixel cropping and room-color scanning
run on the Pi. The manifest is small; the versioned PNG and scanline hit data are
immutable. They describe the same pixels and are published before the manifest.
Ambiguous colors and walls have no selectable room. Preparation failures leave
an old manifest which clients reject after 60 seconds. Restart retries safely.

Set `preparedRobotMap` in the private panel mapping to the worker's manifest URL.
The default example uses loopback deliberately: select the actual LAN bind address
only during deployment. Do not commit private entity maps or home map images.
HoaryDash's current proxy rejects `/local` paths; the small read-only listener
avoids modifying Core or loosening its proxy allowlist.

## Browser lifecycle

Navigation shows the latest selected view first and defers robot reads for 200 ms.
Leaving aborts outstanding view-owned reads and image loading. Completed reads
are removed; polling schedules its next iteration only after completion. Stale
callbacks remain guarded even if abort races a response. A first room tap starts
metadata preparation; expiry, another room, navigation or closing aborts it.
Double tap still opens the loading dialog immediately, before metadata arrives.
Already dispatched household commands are never cancelled or retried by routing.

The cached image and matching hit data survive navigation. An unchanged manifest
version causes no image download, pixel scan, canvas draw or hit-data download.
The installed prepared path uses an image element. The old canvas path remains
available for previews and installations without a worker.

Hidden browser views stop robot polling. Backlight-only darkness does not reliably
produce a matching wake event on Build 9; no new permanent dark-state latch is
added, because that could strand the map after camera wake. Native camera/power
policies remain unchanged. Legacy host compatibility callbacks also remain;
removing them requires a separate dependency audit.

## Verification and rollback

Run the JS tests (including `robot-cancellation.test.cjs`) and
`python3 tests/map-worker.test.py` in an environment with Pillow. The browser
room-selection suite covers immediate loading, delayed replies and cancellation.
Verify actual devices independently; synthetic navigation timings do not prove
physical touch latency, camera wake, sound, boot persistence or household actions.

To roll back, restore the backed-up dashboard YAML, remove only the worker startup
entry and stop only its process. Keep unrelated SSH options and all native camera,
display and watchdog settings. Cached private map files can then be removed.
