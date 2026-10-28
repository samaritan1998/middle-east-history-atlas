# Third-party content and data

## Historical boundary data

Source: [Historical boundaries of world countries and cultural regions](https://github.com/aourednik/historical-basemaps), maintained by Andre Ourednik and contributors.

The upstream repository includes the GNU General Public License, version 3. A verbatim copy is provided in [docs/historical-basemaps-LICENSE.txt](docs/historical-basemaps-LICENSE.txt).

Historical features from the 1500, 1600, 1880, 1914, 1920 and 1930 datasets are embedded in `data/events.json` and the generated `index.html`. This project selects features for the Middle East / North Africa / Balkans view, normalizes property names and distinguishes Ottoman core and dependent features. These adaptations were prepared in April 2026; the presentation was subsequently updated in October 2026. The data remain approximate and retain their upstream license.

## Modern map data

Source: [topojson/world-atlas](https://github.com/topojson/world-atlas), using Natural Earth 1:110m boundaries. The Natural Earth geographic data are in the public domain. Converted country features are embedded in `data/events.json` and `index.html`.

## Podcast and transcripts

Source: [中东往事](https://www.xiaoyuzhoufm.com/podcast/66abf8b07349f7a5572afaf2), 加州 101.

The episode text is an automatic speech-recognition transcription of the first chapter, included as reference material for the timeline. The podcast and its transcribed expression belong to their original rights holders; the historical-map dataset license does not relicense that material. Names and quotations in the transcription have not all been manually corrected.

The repository does not include the original audio recordings.
