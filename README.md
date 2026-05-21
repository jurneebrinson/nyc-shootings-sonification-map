# NYC Shootings Sonification Map

An interactive **sonification and geospatial visualization system** exploring NYC shooting incidents over time. This project translates public safety data into a combined audiovisual experience using Mapbox GL JS and Tone.js, allowing users to both see and hear patterns in urban violence.

👉 **Live Demo:** https://nyc-shootings-sonification.netlify.app/

---

## Overview

This project explores how **sonification can reveal temporal and spatial patterns in urban data** that are often difficult to perceive through static visualization alone.

Monthly shooting incidents across New York City are mapped spatially and translated into sound in real time. Each borough is assigned a distinct synthesized instrument, creating a layered audio representation of geographic variation.

As the timeline progresses, both the visual map and audio evolve together, forming an interactive audiovisual archive of incident data.

---

## Key Features

- Interactive Mapbox GL JS visualization of NYC shooting incidents
- Real-time audio generation using Tone.js
- Temporal playback of monthly aggregated data
- Borough-specific sound design (distinct synth per borough)
- Dynamic centroid tracking to represent spatial density over time
- Threshold-based “shell hit” percussion when incidents exceed baseline (~50/month)
- Timeline scrubbing and BPM control for temporal exploration
- Combined visual + auditory encoding of magnitude and distribution

---

## Sonification Design

- **Pitch mapping:** Monthly incident counts are mapped to musical pitch (higher counts → higher pitch)
- **Borough sound palette:**
  - Manhattan → Made from a tone synth with a triangle oscillator that has fairly sharp attack and release, Manhattan's sonification is bright, dense, and fairly structured to mirror Manhattan's density and structure of people, as it is one of the main hubs of the city with many desirable places to work, eat, and be entertained.
  - Bronx → The Bronx is represented sonically by a membrane synth, giving the location's sound a percussive, and punchy quality.  This is meant to represent the borough's deep-rooted history within hip hop and breakbeat culture.
  - Brooklyn → Brooklyn's sonification is sounded by an FM synth with added harmonicity to give it an unstable FM texture.  This lack of stability in the sonic identity is representative of the widespread gentrification displacement that is highly prevalent within this borough.
  - Queens → Queens is sounded by an AM synth with a small amount of added harmonicity and a generous release time.  This results in an airy, less dense sound, representative of how this borough is geographically broad and culturally diffuse.
  - Staten Island → Staten Island's sonic identity is defined by a tone synth with a sine oscillator that has a more generous attack and release.  Accompanied by a high pass filter and reverb, the sonification is very muted and isolated to represent Staten Island's separation from the rest of the inner city.
- **Threshold event (“shell hit”):**
  When monthly incident counts exceed ~50, a percussive noise burst is triggered. The amplitude scales with how far the value exceeds the threshold, emphasizing periods of unusually high activity.

---

## Data

- NYPD Shootings (2006-Present) Dataset
- Source: NYPD / NYC Open Data  
  https://data.cityofnewyork.us/Public-Safety/Shootings-2006-Present-/5ucz-vwe8/about_data

---

## Tech Stack

- **JavaScript** — application logic
- **Mapbox GL JS** — interactive geospatial rendering
- **Tone.js** — Web Audio synthesis and scheduling
- **Turf.js** — spatial analysis
- **GeoJSON** — data storage format

---

## Project Structure

```
/data/
  NYPD_Shootings_Data_Dictionary.xlsx
  Shootings_(2006-Present)_20260417.csv
  boroughs.geojson
  shootings.geojson
  shootings_monthly.geojson
  shootings_normalized.csv
  shootings_weekly.geojson
  shootings_yearly.geojson
  boroughs.geojson
/scripts/
  NYC Shootings Data Cooking.py
  /index.html
```

---

## How to Run Locally

Because this project loads local GeoJSON files, it must be served through a local server:

```bash
npx serve
```

Then open:

```
http://localhost:3000
```

---

## Controls

- **Play / Pause** — start or pause temporal playback  
- **Timeline slider** — scrub through months  
- **Borough selection** — click to filter spatial data  
- **Reset** — return to full NYC view  
- **About** — open project description modal  

---

## Author

**Jurnee Brinson**  
University of Oregon  
Focus: Music Production, Data Science, Creative Coding
