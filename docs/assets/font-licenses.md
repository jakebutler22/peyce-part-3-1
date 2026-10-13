# Local fonts: provenance and licenses

2026-10-13. The remote Google Fonts CSS import was replaced with local fonts. Existing `DM Sans` and `Playfair Display` family names and typography remain unchanged. No Google Fonts stylesheet or font CDN request is required at runtime.

## Official sources and included files

Official Google Fonts repository directories were inspected through the GitHub API ([DM Sans](https://api.github.com/repos/google/fonts/contents/ofl/dmsans), [Playfair Display](https://api.github.com/repos/google/fonts/contents/ofl/playfairdisplay)). The web renderer could not fetch the GitHub directory pages; no renderer success is claimed.

| Family/style | Local file | Official original download |
| --- | --- | --- |
| DM Sans variable normal | [DM-Sans-variable.ttf](../../frontend/public/assets/fonts/dmsans/DM-Sans-variable.ttf) | [DMSans[opsz,wght].ttf](https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf) |
| Playfair variable normal | [Playfair-Display-variable.ttf](../../frontend/public/assets/fonts/playfairdisplay/Playfair-Display-variable.ttf) | [PlayfairDisplay[wght].ttf](https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf) |
| Playfair variable italic | [Playfair-Display-italic-variable.ttf](../../frontend/public/assets/fonts/playfairdisplay/Playfair-Display-italic-variable.ttf) | [PlayfairDisplay-Italic[wght].ttf](https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf) |

Font bytes are unmodified; only local filenames were simplified. DM Sans provides `opsz` 9–40 and `wght` 100–1000. Both Playfair styles provide `wght` 400–900. These ranges were read from the downloaded TTF `fvar` tables with bundled Python binary parsing; no font library was installed.

## Attribution and licenses

- **DM Sans:** Copyright 2014 The DM Sans Project Authors ([upstream](https://github.com/googlefonts/dm-fonts)). SIL Open Font License 1.1; complete original notice/license included in [dmsans/OFL.txt](../../frontend/public/assets/fonts/dmsans/OFL.txt), downloaded from [official OFL.txt](https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/OFL.txt).
- **Playfair Display:** Copyright 2017 The Playfair Display Project Authors ([upstream](https://github.com/clauseggers/Playfair-Display)), with Reserved Font Name “Playfair Display.” SIL Open Font License 1.1; complete original notice/license included in [playfairdisplay/OFL.txt](../../frontend/public/assets/fonts/playfairdisplay/OFL.txt), downloaded from [official OFL.txt](https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt).

Font software remains under its included OFL license and is not relicensed by any project code license. Included notices/license text must travel with redistribution. No font modification, subset generation or reserved-name change was performed.

## CHECK → TAKE ACTION → VERIFY

**CHECK:** Inspected the existing import and family usage. Recorded commands before using scoped dependency authorization. Inspected official API directory listings to select files and capture expected Git blob hashes.

**TAKE ACTION:** Downloaded the three TTFs and two OFLs with `curl -fsSL` from the exact official URLs above. Replaced only the original first-line import in `frontend/src/style.css` with three local `@font-face` declarations using normal/italic styles, the actual weight ranges, and `font-display: swap`. No other CSS or typography was changed.

**VERIFY:** All five downloaded files match official Git blob SHA-1 hashes returned by the repository API. Actual TTF axes were checked. All local CSS paths point to existing files. Static inspection found no `fonts.googleapis.com` import in that stylesheet and three `font-display:swap` declarations. Actual browser loading, network behavior and final laptop/mobile typography are part of root-task QA; this asset subtask does not claim browser inspection.

| File | Bytes | Verified official Git blob SHA-1 | SHA-256 |
| --- | ---: | --- | --- |
| DM Sans normal | 240,164 | `c672f98060af9b2c85fca704ebd5ad9a8717c1df` | `8cd08d97e89c24d0aa92edd2f0f4c8ee6195eee9b7c9f154865a58b02f0c1c0d` |
| DM Sans OFL | 4,482 | `4430b85ac62998e2edb914360f9ebdfe43f4deaa` | `9af36190332437f5ecd09974de43c1f7c77a310a996cdd8ceb25628b458840e1` |
| Playfair normal | 300,724 | `7a09eb71f10622fd083134ac9ed46f59b21bee18` | `c40f2293766a503bc70cce9e512ef844a4ccb7cbcde792fe2ea31d191917d8d6` |
| Playfair italic | 278,688 | `94fae1f2853dd325b1a3602370780d154ffc8c89` | `a5e26dc5e2e77fb2803a0bf02fd4f81ee136ec8dea863ccdb0c59a263b21378b` |
| Playfair OFL | 4,449 | `13153890847ba9bde8a852596d1515261156e474` | `566be814f8e96e93dfa16101331557eb6b5467e9e03f627c0910fe93ca12300e` |

## Commands and environment

The local shell and `curl` ran in `/Users/jakebutler/Documents/ChatGPT/mental health vF`. Verification used bundled Python at `/Users/jakebutler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.

```sh
curl -fsSL 'https://api.github.com/repos/google/fonts/contents/ofl/dmsans'
curl -fsSL 'https://api.github.com/repos/google/fonts/contents/ofl/playfairdisplay'
mkdir -p frontend/public/assets/fonts/dmsans frontend/public/assets/fonts/playfairdisplay
curl -fsSL 'https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf' -o 'frontend/public/assets/fonts/dmsans/DM-Sans-variable.ttf'
curl -fsSL 'https://raw.githubusercontent.com/google/fonts/main/ofl/dmsans/OFL.txt' -o 'frontend/public/assets/fonts/dmsans/OFL.txt'
curl -fsSL 'https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf' -o 'frontend/public/assets/fonts/playfairdisplay/Playfair-Display-variable.ttf'
curl -fsSL 'https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/PlayfairDisplay-Italic%5Bwght%5D.ttf' -o 'frontend/public/assets/fonts/playfairdisplay/Playfair-Display-italic-variable.ttf'
curl -fsSL 'https://raw.githubusercontent.com/google/fonts/main/ofl/playfairdisplay/OFL.txt' -o 'frontend/public/assets/fonts/playfairdisplay/OFL.txt'
```

Hash verification reconstructed each Git blob header (`blob <byte length>\0`) and SHA-1, comparing it with the official API SHA. SHA-256 values were separately recorded for checked local files.
