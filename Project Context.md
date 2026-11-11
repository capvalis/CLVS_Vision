# Project Context: Multi-Drone Danger Detection with Real-Time AR for a Ground Station

Written 10 November 2026. Plain-language working document. Update it as decisions change.

This file sits next to `Understanding/` (the 56-dataset review), `Dataset/` (the local Kaggle set), `reports/` and `research_notes/` (the model and hardware survey). Dataset IDs such as D43 refer to the entries in `Understanding/Dataset Research Report.md`.

---

## 1. What we are building

Several drones fly over an area and feed one system. The system must:

1. **Detect any danger** in what the drones see.
2. **Analyse the conditions and the scenario** (what is happening, under what conditions).
3. **Combine many kinds of data** from many drones into one picture.
4. **Deliver an AR (augmented reality) view in real time** to an authorised person, plus any extra understanding or data that person asks for.

The vision model is the first stage of this product, not the whole product.

### Decisions already made

| Question | Decision | What it changes |
|---|---|---|
| Who receives the AR view? | A **ground station** operator, not a soldier in the field. | The heavy computing can run at the ground station. Drones can send video or send only results. Latency budget is "feels live on a screen", roughly under one second, not headset-grade. |
| Demo or product? | A **deployable product**. | Only commercially clean data and models may end up in the shipped system. AGPL models (all Ultralytics YOLO) and research-only datasets (DOTA, xView, MAR20, VisDrone, LLVIP and others) are off limits for the final product unless licensed or replaced. |
| What data do the drones collect? | See Section 3. **Recommendation: paired visible (RGB) video plus thermal (LWIR) video, time-synced, with drone telemetry attached to every frame.** | Drives sensor purchase, data collection, and which public datasets are useful. |

---

## 2. The six layers of the system

| Layer | Plain meaning | Public data support (from the review) |
|---|---|---|
| 1. Sensing | Cameras and sensors on each drone, plus where the drone is and where the camera points. | Not a data question. Engineering. |
| 2. Perception | Find and name objects in each frame: vehicles, people, weapons, aircraft, drones, trenches. | **Good.** Many labelled sets exist, though most are research-only and objects are often tiny. |
| 3. Tracking | Follow each object across frames and across drones so one truck is not counted five times. | **Partial.** Drone-as-target tracking sets (D30 to D33) and ordinary-vehicle sets (D35) exist. The one military vehicle tracking set (D34) is request-only. |
| 4. Fusion | Merge all drones and all sensors into one shared map. | **Weak.** Day plus thermal pairs exist (D25, D27, D28, D29) but only civilian scenes. No public multi-drone dataset at all. |
| 5. Understanding and danger | Turn "three vehicles moving toward a building" into a flagged threat with a confidence. | **None.** No public dataset labels intent, threat, or "what is happening". Caption and question sets (D48 to D55) describe only what is visible, often from templates. |
| 6. Delivery | Draw results on the ground station's AR view, only for authorised users, with a record of what was claimed and why. | Not a data question. Engineering. |

**Consequence for layer 5.** "Danger" must be defined by people with domain knowledge as rules on top of detections and tracks. Later, the system can learn from the ground station operators' own decisions on recorded footage. A vision-language model can help describe scenes in words but must not be the judge of threat on its own.

---

## 3. What type of data the drones should collect

### How this was decided

I looked at every drone-view dataset in the review and research notes, noted what sensor, resolution, altitude and frame rate each used, and looked for the overlap. The overlap is the "common ground": the data type that lets us reuse the most public data and matches what drones in this domain actually carry.

### Evidence table: drone-view datasets and their sensors

| Dataset | Sensor and resolution | Altitude and angle | Frame rate | Licence for a product |
|---|---|---|---|---|
| HIT-UAV | Thermal (LWIR) only, 640x512 | 60 to 130 m, camera tilt 30 to 90 degrees, day and night | Stills from video | **CC0, clean** |
| DroneVehicle (D25) | RGB + thermal pairs, 640x512 image area | Urban roads, day and night | Stills | No licence stated, unsafe |
| VTUAV (D35) | RGB 1920x1080 + thermal 640x480 native, DJI Matrice 300 with Zenmuse H20T | Two cities, day and night | 30 FPS | No licence stated, unsafe |
| Military Vehicles Low-FPS UAV (D34) | RGB video, 480p to 4K, online footage | Varied, oblique | 5 FPS | Request-only, no redistribution |
| SeaDronesSee | RGB 5456x3632 | 5 to 260 m, 0 to 90 degrees | Video | **CC0, clean** |
| HERIDAL | RGB 4000x3000, about 2 cm per pixel | 40 to 65 m, looking straight down | Stills | **CC BY 3.0, clean** |
| Okutama-Action | RGB, DJI Phantom 4 | 10 to 45 m, 45 to 90 degrees | Video | Non-commercial |
| Halmstad drone set | RGB 640x512 + thermal 320x256 | Ground-to-air, range to 200 m | Video | **CC BY 4.0, clean** |
| LRDDv3 | RGB 4K + thermal 640x512 pairs | Long-range drone targets | Video | Not found |
| Anti-UAV family (D30 to D32) | Thermal 640x512, some RGB pairs | Ground-to-air | 25 FPS | MIT code, data terms unclear |
| M3FD (D27) | RGB 1024x768 + thermal 640x512, registered | Ground level, roads | Stills | Code GPL, data unclear |
| TNO and TRICLOBS (D28, D29) | Visible + near-infrared + thermal | Ground level, staged | Video | **CC BY 4.0, clean** |
| Military Assets, Kaggle (D43, local copy) | RGB web photos, mostly 640x640, ground and oblique | Mixed | Stills | CC BY 4.0 claimed, upstream rights unverified |
| Mendeley UAV military set | RGB, soldiers are GTA5 synthetic | Drone view | Stills | CC BY 4.0 |

### The common ground

Four things repeat across almost every drone-view dataset and almost every drone payload in this domain:

1. **A visible-light (RGB) camera at 1080p or higher.** Every RGB set is at least 1080p; the strongest small-object sets are 4K. Small targets need pixels, so the sensor should record at its full resolution even if the model later looks at crops.
2. **A thermal (LWIR) camera at 640x512.** This exact size appears in HIT-UAV, DroneVehicle, Anti-UAV, M3FD, LRDDv3 and the common commercial thermal cores (DJI Zenmuse H20T/H30T, FLIR Boson). It is the industry default. Thermal is what makes night and camouflage work; the research notes show day-plus-thermal fusion adds roughly 10 to 15 mAP over RGB alone at ground level and most of the gain comes at night.
3. **Oblique viewing from roughly 40 to 130 m.** HIT-UAV, HERIDAL, Okutama and SeaDronesSee all sit in this band with the camera tilted 30 to 90 degrees. This is also where a person is still tens of pixels tall in thermal, which is detectable. Much higher and people become single-pixel blobs.
4. **Video at 25 to 30 frames per second**, labelled at a lower rate. VTUAV and Anti-UAV record at 25 to 30 FPS. The Ukrainian military set used 5 FPS and still supported tracking. Record full rate, label sparsely, let the tracker fill gaps.

### Recommendation

Collect **paired RGB and thermal video, time-synchronised, with a telemetry record attached to every frame.**

| Item | Recommended | Why |
|---|---|---|
| RGB camera | 4K sensor if the payload allows, 1080p minimum, 25 to 30 FPS | Tiny targets. Allows tiling and zoom-in later without a second flight. |
| Thermal camera | Uncooled LWIR, 640x512, 25 to 30 Hz | Matches the public data, the commercial cores, and the night-time need. Note: thermal cores above 9 Hz are export-controlled in some countries. Check procurement rules early. |
| Mounting | Both cameras on one gimbal, boresighted (pointing the same way) | Makes day-thermal pairing possible without heavy software alignment. The DJI H20T-class payloads do this out of the box. |
| Telemetry per frame | GPS position, altitude above ground, gimbal pitch/yaw/roll, camera zoom and intrinsics, precise timestamp, drone ID | Without this, a detection is only a pixel position. The AR view needs a ground position. A laser rangefinder (present on H20T-class payloads) gives direct target range. |
| Flight profile for collection | 40 to 130 m, oblique 30 to 90 degrees, day and night, several seasons and terrains | Matches the public data so pretraining transfers, and covers the conditions the product will face. |
| Storage | Raw full-resolution video, not compressed crops; keep the two streams and telemetry in one container or with a shared clock | Labels can be added or changed later. Compression destroys the tiny targets we care about. |

### What to leave out, for now

- **Radar (SAR) and satellite imagery.** Eight SAR sets and sixteen satellite sets exist in the review, but they are a different sensor family, a different viewpoint, and mostly research-only. Not what a tactical drone carries.
- **Near-infrared (NIR) as a third camera.** Only the TNO sets use it. No model or dataset pipeline depends on it. Add later if a specific need appears.
- **Audio, radio, and other non-image sensors.** Useful for fusion later, but nothing in the current research supports them, and they do not change the vision model choice.

---

## 4. Which public datasets are usable for a product

Commercially clean drone-relevant sets (from the review and notes). Each still needs a licence re-check before use:

| Dataset | What it gives | Licence |
|---|---|---|
| HIT-UAV | Thermal drone view, people and vehicles, 60 to 130 m | CC0 |
| SeaDronesSee | RGB drone view, people in water, 5 to 260 m, 54k frames | CC0 |
| HERIDAL | RGB drone view, people on land, 40 to 65 m | CC BY 3.0 |
| Halmstad | RGB + thermal, drones versus birds and aircraft | CC BY 4.0 |
| TNO and TRICLOBS (D28, D29) | Visible + thermal fusion, ground level, military-style staged scenes | CC BY 4.0 |
| Mendeley vehicles (D42) | Military and civilian vehicle photos | CC BY 4.0 (upstream photo rights not traced) |
| Military Assets, Kaggle (D43) | 12 military classes, ground and oblique photos, our local copy | CC BY 4.0 claimed, upstream rights not traced |
| MTARSI (D19) | Satellite aircraft chips | CC BY 4.0, but satellite view |
| RarePlanes (D22) | Satellite aircraft, real and synthetic | CC BY-SA 4.0 (share-alike clause), satellite view |

Not usable in the shipped product without a licence: DOTA, xView, MAR20, VisDrone and DroneVehicle, SARDet-100K, LLVIP, TinyPerson, Drone-vs-Bird, COD10K, CAMO, fMoW, LEVIR-CD. They can still inform research and evaluation if their terms allow it.

**The practical reading:** public data gives class exposure and pretraining. The product's accuracy will come from our own collection with the sensor pair above. The research notes say this directly: cross-dataset drone detection drops to 0.43 to 0.48 mAP50, and the honest test set is the one you capture with your own sensor at operational range.

### 4b. Dataset roles: which set does what, and how it is used

**Superseded on 11 November 2026 by `Training Datasets.md`**, which re-checked every set at its source. Main changes: DSIAC is unavailable to non-US-government users; TNO and TRICLOBS have no annotations and are for fusion testing only; the Kaggle set has cross-split duplicates and uncredible licensing; no public drone-view military set is commercially clean, so military labels come from own flights and synthetic rendering. The table below is kept as the earlier snapshot.

Training happens in stages. Each stage uses a different group of datasets for a different reason.

| Stage | Datasets | Why these | How they are used |
|---|---|---|---|
| **1. Teach "drone view and tiny objects"** | SeaDronesSee (CC0), HERIDAL (CC BY 3.0), HIT-UAV (CC0, thermal) | Only large, clean sets filmed from a drone at product-like heights. They teach the model what a person or vehicle looks like at 40 to 260 m, which no ground-photo set can. | Pretrain the RGB detector on SeaDronesSee plus HERIDAL tiles (people), and the thermal detector on HIT-UAV (people, vehicles). Train on 640 or 1280 px tiles with overlap. These become the base weights. |
| **2. Teach the military class names** | Military Assets D43 (local copy), Mendeley Vehicles D42 | The only clean-licensed sets with tank, soldier, weapon, artillery, warship, aircraft labels. D42 adds the military-versus-civilian vehicle distinction and 130 negative images. | Fine-tune on top of stage 1 with mixed batches so drone-view skills are not forgotten. Cut object chips out of D43 and paste them onto empty drone frames (copy-paste augmentation) to give the military classes a drone-like background. Rebalance: tank is 40 percent of boxes, trench has 3 examples, civilian has 43. Never report accuracy on D43's own test split; it is web photos, not drone view, and has no warship or weapon examples. |
| **3. Teach day-plus-thermal fusion** | TNO Image Fusion and TRICLOBS D28/D29 (CC BY 4.0), Halmstad (CC BY 4.0) | TNO sets are registered visible/NIR/thermal of people and vehicles in staged military-style scenes. Halmstad pairs RGB and thermal for drone, bird, aircraft and helicopter targets. | TNO: validate the camera alignment step and the late-fusion rule (merge the RGB and thermal detections). We would have to draw boxes ourselves; the release has no boxes. TRICLOBS' 16 one-line scenario briefs are a tiny seed for scene descriptions. Halmstad: adds "other drone" as a danger class and "bird" as a distractor class so the model does not flag every bird. |
| **4. Our own flights (the main source)** | Own RGB + thermal video with telemetry | Every public set is either civilian, web photos, or research-only. Nothing public shows military targets from our sensor at our heights. | Fly the collection profile in Section 3. Label with model-assisted labelling: the stage 2 model proposes boxes, humans correct them. Split by flight, never by frame, so the test set is truly unseen. This is the only honest accuracy number for the product. |
| **5. Evaluation only** | Own held-out flights first; then SeaDronesSee and HIT-UAV test splits; D34 Ukrainian UAV military vehicles if access is granted | D34 is the only real drone footage of military vehicles with track IDs, but it is request-only and purpose-restricted. | D34: request access for validation of the tracker and the vehicle classes only. Do not train product weights on it or redistribute it. |

**Not used, and why**

| Group | Datasets | Reason |
|---|---|---|
| Radar | D01 to D08 (SAR) | A different sensor the drone does not carry. The military ones (MSTAR, SAMPLE) are 1990s test-range radar chips. |
| Satellite | D09 to D24 | Straight-down view from space at 0.3 to 30 m per pixel. Different from oblique drone video. Mostly research-only. MAR20 and RarePlanes know aircraft types but the view does not transfer and RarePlanes' share-alike clause is a product risk. |
| Infrared small spots | D36 to D38 | Single-class 1 to 10 pixel blobs. Only relevant if we fly very high. Licence terms unclear. |
| Camouflage | D46, D47 | Non-commercial. Mostly animals; only dozens of camouflaged people. |
| Scene, change, language | D48 to D56 | Satellite view, template text, research licences. fMoW's licence forbids commercial sharing. xBD is natural-disaster damage. |
| Community mirrors | D41 (Kaggle aircraft), D44 (HF mirror), D40 (milair) | Licence Unknown or a mirror of restricted data; video frames with unknown rights. |
| Paper-only | D39, D45 | No public release exists. |
| Non-commercial drone sets | VisDrone, DroneVehicle D25, LLVIP, TinyPerson, Drone-vs-Bird, Okutama, Anti-UAV family D30 to D33, VTUAV D35 | Research-only or no licence. Whether weights trained on them inherit the restriction is legally unsettled, so they stay out of product weights. |
| Request-based archive | DSIAC D26 | The only real military vehicle visible-plus-thermal archive. Worth a formal request, but distribution is at DSIAC's discretion and reuse terms are not a licence. Treat as a possible bonus, not a plan. |

**One legal check before shipping.** D43 and D42 declare CC BY 4.0 but neither traces the rights of the original web photos. Get this reviewed before weights trained on them go into the product.

---

## 5. Facts about our local dataset (D43, measured 10 November 2026)

- YOLO format, 12 classes, 21,978 train / 2,941 val / 1,396 test images. Mostly 640x640 JPEG, some 1080p and 2K.
- Heavily imbalanced. Train boxes: military_tank 9,013; soldier 4,534; military_aircraft 3,333; military_vehicle 1,287; camouflage_soldier 1,070; military_truck 826; weapon 587; civilian_vehicle 460; military_warship 297; military_artillery 200; civilian 43; trench 3.
- 294 train, 273 val, 127 test images have empty label files.
- About a quarter of boxes cover under 1 percent of the image area, so small targets are common.
- The test split has no warship or weapon examples at all.
- Source photos are web images, ground and oblique, not drone-view. Treat it as class exposure, not as the benchmark.

---

## 6. Model and hardware direction (from `reports/Small military object detection on edge.md`)

Because the operator is at a ground station, computing can sit there. Two placements remain open:

- **Drone-side detection, ground-side fusion.** A small detector on each drone (Jetson Orin Nano class) sends tracks, not video. Saves bandwidth. Needs a model that fits a 7 to 25 W box.
- **Ground-side everything.** Drones stream video, the ground station runs larger models on one GPU. Simpler models, heavier radio link.

Either way the survey's advice holds: spend compute on image resolution and video context, not on bigger networks. Train on tiles, use a stride-4 (P2) head or a high-resolution teacher, run the detector sparsely with a tracker in between, and escalate to zoom-in only when something is found.

Licence-clean model families: D-FINE, DEIM v1, RT-DETR (Baidu upstream), RF-DETR Nano to Large, LW-DETR, YOLOX, NanoDet, PP-YOLOE, DAMO-YOLO (all Apache-2.0). Avoid: every Ultralytics YOLO (AGPL), DEIMv2 (custom licence, contact authors), YOLO-NAS (non-commercial), LEAF-YOLO (GPL).

---

## 6b. Sauron: the telemetry engine we already have (checked 10 November 2026)

Sauron lives at `Capvalis/sauron` (Rust engine, Git remote rahulyadav-2004/sauron). In plain words: it takes readings from many machines, keeps the original bytes, converts approved fields into exact common values with their own timestamps and clock uncertainty, keeps live state, allows corrections without rewriting history, and delivers results to authorised subscribers and a dashboard. It also has an "intelligence" track that captures camera frames, runs a detector, asks a vision-language model to describe the scene, and joins those with device readings.

**What Sauron already covers for this project**

| Need | Status in Sauron |
|---|---|
| Drone position (lat, lon, height above home, speed) | Done. MAVLink position pair, DJI Mini 3 SRT subtitle file, CSV and JSON. Exact numbers, exact source time, UTC only when the clock relation is proven. |
| Battery | Done for MAVLink battery percentage (held until a frame-bound time exists). |
| Keeping originals, corrections, withdrawals, replay, durable delivery, authentication | Done. This is Sauron's core strength (G1 to G3 accepted for bounded profiles). |
| Camera frames tied to a source clock, stored immutably with hashes | Done for simulator PNGs and browser JPEG samples. RTSP exists but a real camera was never run. |
| Object detection and tracking | A bounded path exists: Ultralytics YOLO26n on EC2 CPU at 320 px with ByteTrack, fixed camera only. Sauron's own docs call this a pilot, not production. |
| Scene description in words | Luna (surroundings) and Terra (environment) prompts on an Azure model, 2 to 4 seconds per answer. |
| Joining camera results with device readings into one situation record | I4.2 and I4.3 implemented in bounded form. |
| Map | MapLibre with OpenStreetMap. Shows drone positions as markers. Does not place detected objects. |
| Multiple drones | Planned (five-drone ArduPilot/Gazebo profile). Gateway currently rejects more than eight sources. |

**What Sauron does not have yet, which the vision model needs**

| Gap | Why it matters | Sauron's own words |
|---|---|---|
| Drone attitude and gimbal angles per frame | Without camera pointing direction, a detection stays a pixel position and cannot be put on the map. | "No attitude/IMU/barometer/magnetometer/range family is registered." Attitude is a planned variant only. Gimbal is not mentioned anywhere. |
| Camera intrinsics and zoom for real cameras | Needed for the pixel-to-ground ray. Only the Webots simulator camera has a frozen calibration. | "Locating an object in its image requires separately qualified calibration/depth/geometry." |
| Pixel-to-ground projection with terrain | The actual AR placement step. Terrain data is listed as a future direction. | "A drone's GPS describes the drone; it does not locate every image box on the map." |
| Thermal video stream | The data plan needs paired RGB and thermal. Sauron has one image stream per camera, visible only. | No thermal mention. |
| Moving-camera tracking | ByteTrack is tuned for fixed cameras. | "For a moving drone, qualify BoT-SORT with camera-motion compensation ... planned, not silently activated." |
| Real drone video input | RTSP positive case, drone SDK and GPU runtime are untested. | "Positive RTSP, drone/simulator devices and sustained decode buffering remain untested." |
| Edge placement | Everything runs on EC2 CPU. A ground station needs local compute. | "The currently authorized processing host is EC2." |
| Product-safe detector | Sauron's YOLO is Ultralytics, AGPL. | "The applicable license and notices must be recorded before shipping a proprietary production package." |
| DJI SRT dialect | Only the Mini 3 five-line format is parsed. Enterprise payloads (H20T class) have a different SRT dialect with gimbal fields, and the real path is the DJI SDK, not subtitles. | "It is not a general SRT/HTML parser or an MP4/KLV extractor." |

**Verdict.** Sauron is the right backbone for the ground station: ingestion, exact time, provenance, corrections, delivery, dashboard. It answers "where is each drone and when was this frame taken". It does not yet answer "where on the ground is the thing the camera saw". Closing that needs five additions inside Sauron: an attitude and gimbal telemetry family, a camera calibration record per real camera, a frame-to-telemetry time join for real video, a geolocation step (camera ray to ground or terrain), and a thermal stream. The detector itself should be replaced with an Apache-licensed model when the product path is built.

## 7. Open questions

1. Which drone platform and payload will be used, so the sensor pair can be confirmed against it.
2. Expected radio bandwidth per drone, which decides drone-side versus ground-side detection.
3. The first list of "danger" rules, written by domain experts, so layer 5 has something to run.
4. Whether any existing in-house footage exists to start labelling.
5. Export-control status of thermal cores above 9 Hz in the deployment country.

---

## 7b. Proposed order of work (discussed 10 November 2026, not yet agreed)

Principle: build one thin line from drone footage to the ground-station screen first, using recordings and one drone, then make each link stronger. Do not build the vision model alone for months and bolt AR on at the end. The AR view is thin from day one and grows with every step.

| Step | What we build | Why this order | Needs the drone decision? |
|---|---|---|---|
| 0. Decide drone and payload | Pick the platform, camera pair and how telemetry comes out (MAVLink or DJI SDK). | Gates steps 3 and 6. Everything else can start without it. | This is the decision. |
| 1. Scorecard | A fixed test set of drone footage with labels (CC0 sets plus any own footage), split by flight, and a script that scores small-object accuracy and speed on the target hardware. | Without a scorecard we cannot choose a model or know if a change helped. The edge report says to spend the first week on this. | No |
| 2. Eyes on recordings | An Apache-licensed detector (D-FINE or DEIM class) trained in the stages of Section 4b, plus a tracker, run on recorded drone video through Sauron's existing frame path. Replaces the AGPL YOLO. Boxes and tracks land in Sauron's ledger and show on the existing video view. | Proves the vision model on real footage with no hardware risk. Reuses Sauron's capture, storage and display. | No |
| 3. Geometry | Attitude, gimbal and camera calibration into Sauron; a pixel-to-ground step; validate with markers at known positions on the ground. | This is what turns "a box in the picture" into "a dot on the map". The first real AR moment. | Yes |
| 4. Danger rules, version one | Domain experts write the first rule list (what counts as danger, at what distance, in which zone). Implemented as ordinary code over tracks and positions, with each alert linked to its evidence. | No dataset teaches danger, so people must define it. Can be drafted in parallel with step 2; needs step 3 to compute distances. | No for drafting, yes for distances |
| 5. Ground-station view | Grow Sauron's dashboard: boxes on video (exists), then object markers on the map (after 3), then alerts with reasons (after 4), then the operator's "ask for more" actions. | Each step adds one visible thing. Operators can give feedback early. | No |
| 6. Live, one drone | Swap recordings for a live stream from the chosen drone. Move the detector to ground-station hardware. Measure real delay end to end. | Only after the recorded path works. Exposes radio, decode and timing problems in isolation. | Yes |
| 7. Thermal | Add the thermal stream, train the thermal branch, fuse at decision level. | Night capability. Comes after the visible path is stable so problems are not confused. | Yes |
| 8. Many drones | Raise Sauron's source limit, merge tracks across drones on the shared map, de-duplicate. | Hardest fusion problem. Only sensible once one drone is solid. | Yes |
| 9. Learn from operators | Record operator decisions on alerts and use them to tune or train the danger layer. | Turns the rule list into something that improves with use. | No |

Steps 1, 2, 4 (drafting) and 5 (first part) can start now. Steps 3, 6, 7 and 8 wait for the drone decision.

## 8. Glossary

- **RGB**: an ordinary colour camera.
- **LWIR / thermal**: a camera that sees heat, works at night, 640x512 is the standard size.
- **NIR**: near-infrared, not heat, just beyond visible red. Different from thermal.
- **SAR**: radar imaging from satellites or aircraft. Not a camera.
- **Oblique**: camera tilted forward rather than pointing straight down.
- **Telemetry**: the drone's position, height, and camera pointing data.
- **mAP, AP50**: accuracy scores for detectors; higher is better, 50 means the box only needs to half-overlap the truth.
- **P2 head**: a detector setting that keeps a finer image grid so tiny objects are not lost.
- **Tiling**: cutting a big frame into pieces so small objects stay large enough to see.
- **Tracker**: software that follows an object from frame to frame.
- **AGPL**: a licence that forces you to release your source code if you serve the model over a network. Not product-friendly.
- **CC0 / CC BY**: licences that allow commercial use (CC BY needs credit).
