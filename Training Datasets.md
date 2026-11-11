# Training Datasets: what we will use, for what, and how

Written 11 November 2026. Companion to `Project Context.md` (section 4b gave the first version of this plan) and `Architecture.md`. This file supersedes section 4b where they differ.

Every dataset on the shortlist was re-checked at its original source on 11 November 2026 (official repositories, Zenodo or figshare records, primary papers, GitHub issues). No archives were downloaded. The local Kaggle set was inspected directly on disk. Items marked **unverified** could not be confirmed from a primary source.

---

## 1. Headline conclusions

1. **Four public drone-view sets are clean enough for a product:** HIT-UAV (thermal), SeaDronesSee (visible, maritime), HERIDAL (visible, land, people), and Halmstad (visible plus thermal, drones and birds). Together they teach "what people, vehicles and drones look like from 40 to 260 metres". None of them has a single military label.
2. **No drone-view military vehicle or soldier dataset exists anywhere with a credible commercial licence.** Every candidate is either research-only, re-uploaded from unknown sources with a licence tag the uploader cannot grant, gated to US government users, or gated to Ukrainian and allied firms.
3. **The local Kaggle set is class exposure only, and only for research builds.** It has byte-identical images across its train, validation and test splits, is made of news, stock and Telegram photos, and its CC BY 4.0 claim cannot cover those. It is also not drone-view: the median tank box is 165 by 115 pixels.
4. **The military class names for the product will therefore come from three places we control:** our own flights, synthetic imagery we render ourselves, and possibly purchased synthetic data. Public data gives the drone-view foundation; our data gives the military meaning.
5. **DSIAC is not available to us.** The request form is for US government employees, military personnel and US government contractors.
6. **TNO and TRICLOBS have no annotations.** They remain useful only for testing the camera alignment and the day-plus-thermal fusion step.

---

## 2. The shortlist, by role

### Tier A. Product-safe, used for training the drone-view foundation

| Dataset | What it gives | Licence (owner's own statement) | Size | Capture | Caveats to handle |
|---|---|---|---|---|---|
| **HIT-UAV** | Thermal drone view of people, cars, bicycles, other vehicles. The thermal foundation. | CC0 on Zenodo v1.2.1; CC BY 4.0 in the GitHub LICENSE file. Attribute, which satisfies both. | 2,898 images at 640x512, 8-bit, from 43,470 frames sampled every 15 frames. 24,899 boxes. Person 12,312, Car 7,311, Bicycle 4,980, OtherVehicle 148, DontCare 148 (per-class counts from a third-party mirror, unverified against the paper). | DJI Matrice 210 V2 with Zenmuse XT2 (FLIR LWIR, 25 mm). Altitude 60 to 130 m in 10 m steps, camera tilt 30 to 90 degrees, day and night, no rain. Schools, parking lots, roads, playgrounds. Location not stated. | Split is 70/20/10 with no statement that it is by scene; rebuild our own split by grouping filenames (they encode day/night, altitude, angle, weather, serial). The COCO JSON has a known box-offset bug (issue #6); use the VOC XML and the repo's converter. Ignore the DontCare class. Average person height about 21 pixels. |
| **SeaDronesSee** | Visible drone view of people and boats in water, down to a few pixels. The strongest "tiny person from height" set. Also 10 Hz metadata per frame (altitude, gimbal pitch, roll, pitch, yaw, GPS), useful later for testing our geolocation step. | README states "dataset is CC0 1.0". No LICENSE file in the repo; the README is the only statement. | Detection v2: 14,227 RGB images (8,930 train, 1,547 val, 3,750 test) at 3840x2160, 5456x3632 and 1229x934. MOT: 22 clips, 54,105 frames, 403,192 boxes. Multispectral subset: 432 images. | DJI Matrice 100 and 210, Mavic 2 Pro, Trinity F90+. Altitude 5 to 260 m, gimbal 0 to 90 degrees. Lake Constance. | **Test labels are withheld**; scoring is through the MaCVi server, three uploads a day, account needed. We score on the validation split and the MOT clips instead. Splits are random by frame and by cut video, not by flight. v1 download share is reported unavailable; v2 is the one to request. Known ID-label and metadata errors in the MOT set. Heavy class imbalance toward boats. |
| **HERIDAL** | Visible, straight-down drone view of people on land at 40 to 65 m. Person about 0.1 percent of the frame. | CC BY 3.0 Unported, stated by the authors on the University of Split page (quoted from a Wayback capture, since the live host was down on 11 November 2026). Explicitly allows commercial use. | 1,647 annotated 4000x3000 JPEGs (1,546 train, 101 test), 3,229 person boxes, VOC XML. | Several drones and cameras, Mediterranean wilderness of Croatia and Bosnia. About 2 cm per pixel. | Official host down; use the Zenodo mirror 5662351 (8.3 GB, open). A few test images are 4000x2250 while their XML says 4000x3000; fix on import. Straight-down only, so it transfers poorly to oblique forest scenes (a 2026 study measured 0.0 AP under canopy). Use it for tiny-person tiles and copy-paste chips, not as the only person source. |
| **Halmstad drone detection** | Visible and thermal video of drones, birds, airplanes and helicopters out to 200 m. Gives us the "other drone" danger class and the "bird" distractor class. | CC0 1.0 in the GitHub LICENSE file, authors' own. Zenodo lists "Other (Open)". | 650 ten-second clips: 365 thermal, 285 visible; 203,328 annotated frames. Visible 640x512, thermal 320x256. Clips binned close, medium, distant by target pixel width. | FLIR Breach thermal, Sony HDR-CX405 visible. Drones: Hubsan H107D+, DJI Phantom 4 Pro, DJI F450. Daylight only, ground-to-air. | **Exclude the 49 airplane and helicopter clips taken from a YouTube channel** (11 airplane, 38 helicopter, flagged in the description spreadsheet). Labels are MATLAB groundTruth objects; use the mcos-decoder tool to convert. No official split; split by clip. Thermal resolution is half of ours. |

### Tier B. Research builds only, pending a legal view

| Dataset | What it gives | Why it is not product-safe | How we use it |
|---|---|---|---|
| **Military Assets, Kaggle v5 (local copy, D43)** | The only large set with the 12 military class names: tank, soldier, camouflaged soldier, weapon, artillery, truck, vehicle, aircraft, warship, trench, civilian, civilian vehicle. | Measured on disk: 482 images byte-identical between train and val, 314 between train and test, 54 between val and test. Headers carry Dreamstime, Getty and Wikimedia Commons traces; samples include a news photo, a stock photo, a sales advert and a Telegram war clip with a channel watermark. The uploader's CC BY 4.0 cannot cover these. Likely upstream is a Roboflow project "army-vehicles" with the same 12 classes and 23,400 images (unverified; page blocked). | Research-only builds: teach the model the class names so we can test the pipeline end to end. Deduplicate across splits first. Never report accuracy on its test split. Do not ship weights trained on it until a lawyer has looked. |
| **Military and Civilian Vehicles, Mendeley v1 (D42)** | Six classes: military truck, tank, aircraft, helicopter; civilian car, aircraft. 6,772 images, 130 negatives, 11,528 boxes. Published by DRDO's Institute for System Studies and Analyses; paper title is "Edge device based Military Vehicle Detection and Classification from UAV". | Page says only "we created our own dataset"; image origin and whether images are aerial are not stated on the page. A 2026 survey tabulates it as "ground and aerial" (unverified). | Worth a direct conversation with the authors, since it is Indian-origin and may be partly drone-view. Until then, same treatment as the Kaggle set. |
| **Multi-Class UAV Military Object Detection, Mendeley (Jordan, June 2026)** | 7,985 images: tank, drone, people, soldier. | Authors re-collected tank, drone and people images from unnamed Roboflow and Kaggle sets; they cannot grant CC BY on those. The 982 soldier images are GTA5 renders with their own terms. | Do not use. |

### Tier C. Testing the fusion and geometry steps only, no training

| Dataset | What it gives | Licence | Why no training |
|---|---|---|---|
| **TNO Image Fusion (D28)** | About 261 registered visible, near-infrared and thermal pairs at 768x576, people and vehicles, night. | CC BY 4.0, figshare v2. | No annotations exist, from the authors or anyone else. Use to test our alignment and decision-level fusion code. |
| **TRICLOBS (D29)** | 16 staged scenario clips, 56,865 frames, visible plus NIR plus LWIR packed into one BMP, 640x480, plus weather files. About 40 GB. | CC BY 4.0, figshare. | No annotations. Channels are not frame-synchronised. Use for fusion testing and as a tiny seed of scene descriptions. |

### Tier D. Request-only or closed

| Dataset | Status | Decision |
|---|---|---|
| **DSIAC ATR database (D26)** | US government employees, military personnel or US government contractors with a contract number and certifying official. | Not available to us. Drop. |
| **Military Vehicles in Low-FPS UAV Footage (D34, Ukraine)** | Author-reviewed request, purpose-limited, no redistribution or retraining without authorisation. 119 online videos, 5 FPS, three coarse classes, track IDs. | Request for validation of the tracker and vehicle classes only, if the authors accept a commercial applicant. Never train product weights on it. |
| **Ukrainian battlefield data (Brave1, Enabled Intelligence)** | Gated to vetted Ukrainian and allied firms. | Not open data. Drop. |

### Tier E. Rejected, with the reason

| Dataset | Reason |
|---|---|
| Roboflow Universe military sets (UAV-tank-soldier, Aerial Asset Recognition, air_to_ground, Detection-System-Military, soldiers with soldier_ru and soldier_ua classes, and others) | No provenance statements, hashed filenames, one reports 100 percent accuracy, one is plainly Telegram war footage. Roboflow lets any uploader pick any licence tag. |
| VEDAI | Owner's terms: research and non-commercial only. Mirrors' CC BY tags are not the owner's. |
| UAVDT | "For research purpose only" at the official site. |
| VisDrone, DroneVehicle | CC BY-NC-SA 3.0 and no licence respectively. |
| MVRSD | CC BY-NC-ND 4.0 on Science Data Bank; satellite view anyway. |
| Simuletic UAV tank set | Synthetic, sample is non-commercial, full set is sold at 590 USD per 1,000 images. Kept as a purchase option, not a dataset. |
| Satellite, radar, camouflage, caption and change sets from the 56-entry review | Wrong sensor or viewpoint, or research-only. See `Understanding/`. |

---

## 3. Where the military labels will come from

Since nothing public is clean, the product's military classes come from three sources we control. All three are needed; none alone is enough.

| Source | What it supplies | Cost and effort | Evidence it works |
|---|---|---|---|
| **Own flights** | The only honest data: our sensor pair, our heights, our terrain, real targets or stand-ins (vehicles, people in uniform, equipment). Also the only honest test set. | Flight time, targets, labelling. Model-assisted labelling cuts the labelling cost after the first few hundred frames. | Every cross-dataset study in the research notes shows accuracy collapses on new sensors and scenes; the edge report says the honest test set is "one you capture with your own sensor at operational range". |
| **Synthetic rendering we generate** | Unlimited drone-view images of tanks, trucks, artillery, soldiers, trenches with perfect boxes, any height, angle, season, day or night, thermal or visible. | Build a scene pipeline in Gazebo or Unreal with military vehicle models. Sauron already plans a Gazebo simulator profile, so the tooling overlaps. | Jeong et al. 2025 (D45) trained on 14,944 synthetic instances rendered in Unreal and validated on real military targets. RarePlanes showed synthetic plus few real samples works for aircraft. The TNO 2026 study (D39) combined simulated data, foundation models and few real samples for military vehicles. |
| **Purchased synthetic** | A quick start before our own pipeline exists. | Simuletic sells 3,000 UAV-view tank images for about 1,770 USD. Check terms allow training commercial models. | Same evidence as above; a stopgap only. |

What synthetic cannot fix: the gap between rendered and real appearance (domain gap). The research says the answer is a small amount of real data mixed in, which is why own flights are mandatory.

---

## 4. Training stages, revised

| Stage | Data | Purpose | Build type |
|---|---|---|---|
| **1. Drone-view foundation** | HIT-UAV (thermal), SeaDronesSee val plus MOT (visible), HERIDAL (visible), Halmstad minus YouTube clips (visible plus thermal) | Teach the model what people, vehicles, boats, drones and birds look like from height, especially at under 32 pixels. Separate RGB and thermal branches. | Product-safe |
| **2a. Military class names, research build** | Kaggle D43 (deduplicated), Mendeley D42 | Prove the pipeline end to end with the 12 class names on recorded footage. Produces numbers for internal comparison only. | Research only |
| **2b. Military class names, product build** | Synthetic renders plus own flights, with copy-paste of real target chips onto empty drone frames from stage 1 sets | The weights that ship. | Product-safe |
| **3. Day-plus-thermal fusion** | Halmstad pairs for training the fusion rule; TNO and TRICLOBS for testing alignment | Decision-level fusion of the two detectors. | Product-safe |
| **4. Own data fine-tune** | Own flights, split by flight | Final accuracy. | Product-safe |
| **5. Evaluation** | Own held-out flights first. Then HIT-UAV test (rebuilt split), SeaDronesSee val, HERIDAL test (public labels), Halmstad held-out clips. D34 only if access is granted. | The scorecard. | |

---

## 4b. Target class list (adopted 11 November 2026)

The class list is the fixed set of names the detector may answer with. Every label from every dataset is translated into one of these names before training. It can still be changed before the first real training run; after that, changes mean retraining.

### The list

| Name | Meaning | Training examples come from | Used by the danger rules for |
|---|---|---|---|
| person | Any human, any clothing | HIT-UAV Person and Bicycle; SeaDronesSee swimmer, floater, swimmer-on-boat, floater-on-boat; HERIDAL person; Kaggle soldier, camouflage_soldier, civilian; own flights | Counting, zones, distance rules |
| soldier | Person in military dress or carrying arms. Subtype of person. | Kaggle soldier, camouflage_soldier; own flights; synthetic | Threat rules |
| weapon | Handheld firearm or launcher | Kaggle weapon; own flights | "Armed person" rule |
| vehicle | Any civilian ground vehicle | HIT-UAV Car, OtherVehicle; Kaggle civilian_vehicle; Mendeley civilian car; own flights | Baseline traffic |
| military_vehicle | Any military ground vehicle. Subtypes: tank, truck, artillery. | Kaggle military_tank, military_truck, military_vehicle, military_artillery; Mendeley military truck, tank; synthetic; own flights | Convoy and approach rules |
| aircraft | Plane or helicopter | Kaggle military_aircraft; Mendeley aircraft, helicopter; Halmstad airplane, helicopter | Air activity |
| drone | Another UAV | Halmstad drone; own flights | Counter-drone alert |
| bird | Distractor. Never alerted. | Halmstad bird | Prevents false drone alarms |
| boat | Any vessel. Subtype: warship. | SeaDronesSee boat; Kaggle military_warship | Maritime rules |
| trench | Dug fortification | Kaggle trench (4 examples only); own flights; synthetic | Static-threat mapping |

Ten names, three with subtypes. A subtype is used only when the model is confident; otherwise the parent name is reported. This is the parent-fallback convention xView and HRSC2016 use.

Deliberately excluded: a separate "civilian" class. From 100 metres a model cannot tell a civilian from an off-duty soldier, and labelling it would teach guessing. The rules layer treats "person without soldier or weapon" as the civilian case.

Classes to drop from source datasets rather than map: HIT-UAV DontCare; SeaDronesSee life jacket, jetski, buoy and ignored regions (jetski could map to boat if useful); Kaggle civilian maps to person.

### How the list relates to the 56-dataset catalogue in `Understanding/`

The catalogue holds several hundred class names. The list is not their union; it is what a drone camera must find for the danger rules. Coverage:

| Class family in the catalogue | Example datasets | In our list? | Reason |
|---|---|---|---|
| Broad people, vehicles, aircraft, ships, drones | DIOR, DOTA, xView, DroneVehicle, M3FD, Anti-UAV sets, Kaggle | Yes, as person, vehicle, military_vehicle, aircraft, boat, drone | What a drone camera sees. |
| Military vehicle subtypes | D34 coarse groups; MSTAR and SAMPLE model names; TNO 15-class; MVRSD | Partly: tank, truck, artillery | Coarse subtypes are readable at 100 m; exact models are not, and those sets are radar or unavailable. |
| Fine aircraft types | MAR20, MTARSI, Kaggle aircraft 114 types, RarePlanes roles | No, only aircraft | Satellite or spotter view, research-only, not needed by a rule. Can be added as subtypes later. |
| Fine ship types | FGSC-23, FGSD, HRSC2016, ShipRSImageNet, FUSAR, OpenSARShip | No, only boat with warship subtype | Satellite and radar, research-only. |
| Infrastructure and land use | DOTA facilities, xView buildings, fMoW functions, FAIR1M roads | No | Fixed infrastructure belongs to the map layer, not the detector. |
| Radar targets, oil tanks, bridges | SARDet-100K | No | Not our sensor. |
| Camouflaged foreground | CAMO, COD10K | Folded into soldier | Camouflage is an appearance, not a thing. Non-commercial sets anyway. |
| Infrared small spots | IRSTD-1k, NUDT-SIRST, SIRST | No separate class | A spot becomes a named class once large enough. An "unknown small target" class can be added if we fly very high. |
| Damage, change, captions, questions | xBD, LEVIR, RSICD, RSVQA, FSAR-Cap, SARChat | No | Not object names. Scene text comes from the vision-language layer in Sauron. |
| Trench, weapon, bird | Kaggle, Halmstad | Yes | Direct. |

## 5. Practical handling notes

- **Splits.** Every public set is split by frame or by random cut, not by flight. Rebuild splits ourselves: HIT-UAV by filename group, SeaDronesSee by clip, Halmstad by clip, HERIDAL keep the fixed test set. Our own data is split by flight from day one.
- **Formats.** HIT-UAV: use VOC XML, not the COCO JSON. Halmstad: MATLAB groundTruth, convert with mcos-decoder. SeaDronesSee: COCO JSON for detection, MOT-challenge text for tracking. HERIDAL: VOC XML with a size mismatch on a few files. Kaggle: YOLO text with no trailing newline on the last line, which breaks naive counting.
- **Class mapping.** Use the adopted list in section 4b. Every importer maps source labels to those ten names and three subtypes, and drops the listed ignore classes.
- **Attribution file.** Keep a NOTICE file listing HIT-UAV (CC BY 4.0 or CC0), HERIDAL (CC BY 3.0, University of Split), SeaDronesSee (CC0), Halmstad (CC0), TNO and TRICLOBS (CC BY 4.0). Attribution is cheap and makes every licence reading safe.
- **Thermal resolution.** HIT-UAV matches our 640x512 plan. Halmstad thermal is 320x256; upscale during training or weight it lower.
- **Download status (11 November 2026, evening).**
  - HIT-UAV: downloaded, MD5 verified, extracted to `Dataset/HIT-UAV/extracted/...`. Class counts match the published ones exactly (Person 12,312; Car 7,311; Bicycle 4,980; OtherVehicle 148; DontCare 148). 105 scene groups from the filename pattern. Built as `vision/datasets/hit_uav_v1` (2,316 / 265 / 317 images, all frames kept, split by scene). 7,698 person boxes are under 32 pixels.
  - Halmstad: downloaded, MD5 verified, extracted. Labels decoded from MATLAB with mcos-decoder (one box per frame or none). Frames exported at every third frame with `vision/tools/halmstad_export.py`: 67,983 frames, 1.4 GB. The 49 YouTube-sourced clips are listed in `Dataset/Halmstad/internet_clips.txt` and excluded by the importer. 17 clips have a frame-count mismatch of more than two between video and labels (listed in `export_summary.json`); boxes beyond the label length are treated as absent. Built as `vision/datasets/halmstad_v1` (50,075 / 6,376 / 6,377 frames, split by clip). Thermal is 320x256, visible 640x512.
  - TNO Image Fusion: downloaded, MD5 verified, extracted (536 BMP, 19 TIF, no labels). Fusion testing only.
  - HERIDAL: downloading from the Zenodo mirror (8.3 GB), in progress.
  - Mendeley DRDO vehicles: **not downloaded**. The API lists only 100 files per call with no working pagination and the "Download All" button needs a browser. The file names show the images are web photos: AFP photo IDs (`000_14M0LD`), US DoD photo IDs (`010205-F-1631A-001`), a New York Times image (`03helicopters2-span-articleLarge`), car-review sites (`01-honda-civic-si-sedan`). Ground-level, not UAV, and not rights-cleared. Same tier as the Kaggle set.
  - SeaDronesSee: **not downloaded**; needs a request through the project site and a MaCVi account in a person's name.
  - TRICLOBS: skipped for now (40 GB, no labels).

---

## 6. Measured facts about the local Kaggle set (D43), 11 November 2026

| Fact | Value |
|---|---|
| Images | 21,978 train, 2,941 val, 1,396 test; 23,860 unique by file hash across all splits |
| Exact duplicates | 1,544 within train, 529 within val, 382 within test; 482 train-val, 314 train-test, 54 val-test cross-split pairs |
| Train boxes per class | tank 17,454; aircraft 7,337; soldier 6,502; camouflaged soldier 4,477; warship 2,134; military vehicle 1,963; truck 1,245; weapon 1,210; civilian vehicle 519; artillery 439; civilian 52; trench 4 |
| Median box size, pixels | tank 165x115; aircraft 378x171; warship 497x407; soldier 62x113; camouflaged soldier 224x381; civilian vehicle 64x47 |
| Boxes under 32 pixels | soldier 17 percent, civilian vehicle 23 percent, truck 11 percent, all others under 7 percent |
| Images with no boxes | 294 train, 273 val, 127 test |
| Image sizes | mostly 640x640, some 1280x720, 1920x1080, 2048x1365 |
| Provenance traces in headers | Dreamstime, Getty, Wikimedia Commons; one sample carries a Telegram channel watermark; one is a sales advert with a price in roubles; one has baked-in noise augmentation |
| Test split gaps | no warship or weapon examples at all |

---

## 7. Actions this creates

1. Legal view on the Kaggle and Mendeley sets before any weights trained on them leave the research environment.
2. Contact the DRDO authors of the Mendeley vehicles set about provenance and view type.
3. Decide the synthetic pipeline (Gazebo, Unreal, or purchase first) since it is now on the critical path for the product build.
4. Request SeaDronesSee v2 and create a MaCVi account.
5. Target class list: done, section 4b (adopted 11 November 2026).
6. Plan the first own-data flights to match the public sets: 40 to 130 m, oblique, day and night, RGB plus thermal.
