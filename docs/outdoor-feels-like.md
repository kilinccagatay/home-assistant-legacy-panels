# Outside apparent temperature on both panel profiles

The optional secondary outside value comes from Open-Meteo's current
`apparent_temperature`, read by Home Assistant's REST integration. The main
outside temperature and conditions retain the existing weather entity, so two
providers can differ. It is a model-derived weather value, not an indoor sensor.

1. Copy [the REST example](../examples/weather/open-meteo-feels-like.yaml) into
   your private HA configuration and include the list under `rest:`. Merge into
   an existing REST list rather than adding a duplicate root key.
2. The example rounds `zone.home` coordinates to one decimal place before the
   request. This sends a regional location instead of precise home coordinates.
   No API key, account, calendar data or company information is sent.
3. Check HA configuration, then restart/reload the REST integration as appropriate
   for your setup. Confirm `sensor.panel_outdoor_feels_like` receives °C readings.
4. Set the private panel mapping `outdoorFeelsLike` to that sensor and rebuild
   each intended profile. The installer adds an explicit sensor subscription.
   Keep printer/lamp/default-tone/calendar mappings unchanged.

```json
{"outdoorFeelsLike": "sensor.panel_outdoor_feels_like"}
```

Both outside and inside sections use three aligned rows: large temperature,
condition or room label, then a small icon/value. Outside has a thermometer and
apparent temperature; inside has a droplet and relative humidity. There is no
visible “Hissedilen” label; the accessible name and tooltip retain that meaning.
The compact style applies only when the secondary outside sensor is configured.
Apparent temperature and humidity use matching 18 px Denver / 16 px Samsung
fonts. Each complete visible reading, including its sign, unit and leading symbol,
is centered under the weather/house symbol. Primary symbols have zero side
margin; the previous inherited 7 px right margin displaced their visual axis.
There are no positive/negative-specific offsets or invisible sign placeholders.

Negative values and zero are valid for both temperature readings. Missing,
unavailable, nonnumeric, disconnected or stale apparent data displays `—`, never
an invented zero. The REST sensor polls every 10 minutes with a 15-second timeout
and rejects invalid/future/older-than-30-minute sample timestamps. The panel also
checks the sample time before rendering. No JavaScript weather formula is used.

## Validation and limitations

The real installed sensor returned 1.3 °C during the review. DOM tests verify
−12.5 °C, 0 °C and positive temperatures for both readings, plus stale/missing
apparent data. Those synthetic values were never sent to the live sensor.
Actual Denver and Samsung captures were reviewed; the complete device checklist
still has outstanding physical/regression observations. See
[the combined review](three-day-agenda-review.md).

Sources: [Open-Meteo Weather API](https://open-meteo.com/en/docs),
[Home Assistant REST sensors](https://www.home-assistant.io/integrations/sensor.rest/).
