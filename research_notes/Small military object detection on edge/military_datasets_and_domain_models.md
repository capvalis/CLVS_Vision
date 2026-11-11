# Open-source datasets, pretrained models and published results for military object detection (aerial/satellite/SAR/thermal/ground), with emphasis on very small targets

Research date: 2026-11-10. Scope: only publicly accessible resources. License notes are from the original/official source wherever found; Roboflow/Kaggle re-uploads frequently re-label datasets as "CC BY 4.0" and should NOT be trusted over the original authors' terms (multiple examples below).

---

## Key Question 1 — Drone/UAV detection (counter-UAS): best open datasets and best-reported results on tiny drones (RGB and IR); edge-targeted detectors with code

### Takeaway
The IR anti-drone line (Anti-UAV300/410/600 -> 4th Anti-UAV 2025 -> CST Anti-UAV / TDTIV, ICCV 2025) is the only mature, public, tiny-target IR benchmark family; state-of-the-art state-accuracy on Anti-UAV410 is ~68% but collapses to ~36% on the tinier CST Anti-UAV, showing that few-pixel IR drones remain unsolved. In RGB, DUT Anti-UAV, Det-Fly, Drone-vs-Bird (most boxes < 32x32 px, DUA/non-commercial) and the new LRDDv2/v3 long-range sets (boxes down to 12 px area, paired 4K RGB + 640x512 IR in v3) are the right small-target test beds; cross-dataset generalization is poor (YOLO11m trained on Drone-vs-Bird gets only 0.484 mAP50 on Det-Fly). Several Jetson-class anti-UAV repos exist, but almost none ship weights trained on the standard benchmarks.

### Cited Findings

**Anti-UAV family (IR-centric, CVPR/ICCV workshop series)**
- Anti-UAV GitHub (ZhaoJ9014/Anti-UAV): Anti-UAV300 = RGB+IR, Anti-UAV410 = IR only, Anti-UAV600 = IR only (hosted as "3rd_Anti-UAV" on ModelScope); Full-HD video; per-frame visibility flags; repo released under MIT License; no baseline numbers in README — [Anti-UAV GitHub](https://github.com/ZhaoJ9014/Anti-UAV)
- Anti-UAV410: 410 mid-wave thermal IR sequences; SiamDT baseline (dual semantic reasoning + background suppression) scores 68.19 (test) / 71.65 (val); published IEEE TPAMI 46(6):2852–2865, 2024 — [Semantic Scholar entry](https://www.semanticscholar.org/paper/Anti-UAV410:-A-Thermal-Infrared-Benchmark-and-for-Huang-Li/7d3e80a592ab9e6bcce9cad1fb93ad983a15f516); average UAV size on Anti-UAV410 is 39x24 px, area ratio 0.35% — [MCATrack/TDTIV, ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_Tracking_Tiny_Drones_against_Clutter_Large-Scale_Infrared_Benchmark_with_Motion-Centric_ICCV_2025_paper.pdf)
- Tracker State Accuracy on Anti-UAV410 (from CST Anti-UAV comparison table): SiamDT 67.69, GlobalTrack 66.42, PrDiMP 59.31, Stark-ST 58.32, AiATrack 58.31, OSTrack-384 57.41, KYS 45.12 — [CST Anti-UAV (arXiv 2507.23473)](https://arxiv.org/pdf/2507.23473)
- CST Anti-UAV (ICCVW 2025): 220 thermal IR sequences, >240k boxes, size bins by box diagonal: tiny (0,10], small (10,30], normal (30,50], large (50,inf]; 78,224 tiny objects (4.5x prior large datasets); best of 20 SOT trackers reaches only 35.92% state accuracy vs 67.69% on Anti-UAV410; dataset "about to be publicly released", no license stated — [arXiv abs](https://arxiv.org/abs/2507.23473); [ICCVW PDF](https://openaccess.thecvf.com/content/ICCV2025W/Findings/papers/Xie_CST_Anti-UAV_A_Thermal_Infrared_Benchmark_for_Tiny_UAV_Tracking_ICCVW_2025_paper.pdf)
- TDTIV + MCATrack (ICCV 2025): large-scale infrared tiny-drone tracking benchmark; MCATrack reports >10% SA improvement over most competitors on Anti-UAV410 — [ICCV 2025 paper](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_Tracking_Tiny_Drones_against_Clutter_Large-Scale_Infrared_Benchmark_with_Motion-Centric_ICCV_2025_paper.pdf)
- 4th Anti-UAV Workshop & Challenge (CVPR 2025): three tracks, thermal IR, explicitly targets "fast-moving small UAVs" with distractors (kites, balloons, birds); training sets for all tracks released on the site — [anti-uav.github.io](https://anti-uav.github.io/); [submission page](https://anti-uav.github.io/submission/)
- 4th Anti-UAV Track 1 winner / Track 2 runner-up: "A Simple Detector with Frame Dynamics is a Strong Tracker" — global detection + frame-difference/optical-flow input encoding + trajectory-constraint filtering — [CVPRW 2025](https://openaccess.thecvf.com/content/CVPR2025W/Anti-UAV/html/Peng_A_Simple_Detector_with_Frame_Dynamics_is_a_Strong_Tracker_CVPRW_2025_paper.html)
- 4th Anti-UAV Track 3 winner: Dist-Tracker, MOTA 81.32% on official test set; detection AP50 93.9% and tracking MOTA 77.5% on Anti-UAV validation — [CVPRW 2025 PDF](https://openaccess.thecvf.com/content/CVPR2025W/Anti-UAV/papers/Wang_Dist-Tracker_A_Small_Object-aware_Detector_and_Tracker_for_UAV_Tracking_CVPRW_2025_paper.pdf)
- "The Power of Augmentations in IR Object Detection" (Track 2 entry) concludes that even with augmentation "the detection of small objects remains a challenge" — [CVPRW 2025 PDF](https://openaccess.thecvf.com/content/CVPR2025W/Anti-UAV/papers/Ustun_The_Power_of_Augmentations_in_IR_Object_Detection_CVPRW_2025_paper.pdf)
- UAUTrack (Dec 2025): unified multimodal anti-UAV tracker, local-tracking paradigm claimed lighter than SiamDT's global tracking; SOTA on Anti-UAV and DUT Anti-UAV — [arXiv 2512.02668](https://arxiv.org/pdf/2512.02668)
- Surveys: "Securing the Skies" (CVPRW 2025) and "Vision-Based Anti-UAV Technology" (2025) catalog benchmarks — [Securing the Skies](https://arxiv.org/html/2504.11967v1); [Vision-Based Anti-UAV](https://arxiv.org/pdf/2507.10006)

**RGB drone datasets**
- DUT Anti-UAV: 10,000 RGB images (5,200 train / 2,600 val / 2,200 test), 10,109 drone boxes, image sizes 240x160 to 5616x3744, plus 20 tracking videos — [Ultralytics blog](https://www.ultralytics.com/blog/drone-detection-dataset-yolo); official repo — [wangdongdut/DUT-Anti-UAV](https://github.com/wangdongdut/DUT-Anti-UAV)
- Det-Fly: 13,271 RGB images at 3840x2160, air-to-air views of a single DJI Mavic; micro UAVs at ~0.12% of frame — [Ultralytics blog](https://www.ultralytics.com/blog/drone-detection-dataset-yolo); repo listed MIT on GitHub, but whether MIT covers the images is unclear; a Roboflow re-upload disclaims commercial use — [Jake-WU/Det-Fly](https://github.com/Jake-WU/Det-Fly)
- Drone-vs-Bird challenge dataset: 77 training video sequences (as of ICASSP 2023), 85,904 annotated frames, drone sizes from 15 px to >1,000,000 px, "most annotated drones smaller than 32x32 pixels"; test set 30 unannotated videos — [SynDroneVision (arXiv 2411.05633)](https://arxiv.org/html/2411.05633v1); access by email to wosdetc@googlegroups.com with signed Data Usage Agreement, research-only — [wosdetc/challenge](https://github.com/wosdetc/challenge); dataset "openly available to the research community, for non-commercial purposes" — [ICASSP 2023 review (IEEE OJSP)](https://ieeexplore.ieee.org/abstract/document/10475518)
- Drone-vs-Bird at IJCNN 2025 (8th WOSDETC edition): summary paper DOI 10.1109/IJCNN64981.2025.11228314 — [Fraunhofer Publica](https://publica.fraunhofer.de/entities/publication/267aa1ec-a62d-4afa-99ad-cc369f57642b); top-3 entry WRN-YOLO (YOLOv5 with Wide-ResNet backbone + Roboflow synthetic data) has code but no weights and no license file — [yjwong1999/IJCNN2025-DvB](https://github.com/yjwong1999/IJCNN2025-DvB)
- LRDDv2 (Drexel, ISRR 2024): 39,516 images, "majority ... drones with 50 or fewer pixels in 1080p", range metadata for >8,000 images — [arXiv 2508.03331](https://arxiv.org/abs/2508.03331); access via https://research.coe.drexel.edu/ece/imaple/lrddv2/
- LRDDv3 (ICRA 2026): 13.3k 4K images (3840x2160), drones 0–200 m, box areas as small as 12 px total, paired 640x512 IR; mAP50 96.6% reported in-domain; cross-dataset: YOLO11m trained on Drone-vs-Bird -> 0.484 mAP50 on Det-Fly; trained on DUT Anti-UAV -> 0.431 — [arXiv 2605.25942](https://arxiv.org/pdf/2605.25942)
- Halmstad multi-sensor drone dataset: 650 videos (365 IR, 285 visible), 203,328 annotated frames, classes drone/bird/airplane/helicopter, 640x512 RGB and 320x256 IR, max drone range 200 m, CC BY 4.0 — [arXiv 2007.07396](https://arxiv.org/pdf/2007.07396); [repo](https://github.com/DroneDetectionThesis/Drone-detection-dataset)
- FL-Drones (EPFL): 14 videos, 38,948 frames, drone sizes min 9x9, mean 25.5x16.4, max 259x197 px at 640x480/752x480 — [Dogfight (arXiv 2103.17242)](https://arxiv.org/pdf/2103.17242)
- MIDGARD (CTU): ~8,776 auto-annotated images, 752x480, single MAV — [MRS MIDGARD page](https://mrs.fel.cvut.cz/midgard); [survey](https://www.mdpi.com/2504-446X/8/9/518)
- USC drone dataset: 30 one-minute 1920x1080 clips at 15 fps, single DJI Phantom, permissive MIT-style license — [USC MCL](https://mcl.usc.edu/mcl-drone-dataset/)
- SynDroneVision: synthetic RGB drone detection dataset (2024) — [arXiv 2411.05633](https://arxiv.org/pdf/2411.05633)

**Reported small-drone detection results (RGB)**
- DUT Anti-UAV: Eagle-YOLOv8-M 90.26% AP50 (lightweight variant 141 FPS) — [Drones 2026](https://doi.org/10.3390/drones10020112); SPAE-YOLOv8 mAP50 0.906 — [Sensors 2026](https://doi.org/10.3390/s26113424); ESMS-YOLOv7 mAP50 0.909 vs YOLOv7 0.819 — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2667241324000181)
- Det-Fly: YOLO-ADD +11.5% mAP50 over baseline, cross-validated on LRDDv2 and DUT Anti-UAV — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1568494626007957)
- Multi-scale/tiling for small drones: 4K frames resized to 640 px make distant drones fall below detection threshold; YOLO11m-p2 (extra P2 stride head) helps at higher compute; training with a bird class improved drone AP vs drone-only — [arXiv 2504.19347](https://arxiv.org/pdf/2504.19347)
- LMWP-YOLO (long-range small drones): +22.07% mAP over YOLO11n with 52.51% fewer params — [Sci. Reports 2025](https://www.nature.com/articles/s41598-025-95580-z)

**Edge anti-drone detectors with code**
- Prabhdeep1999/uav-detection: YOLOv5s on IR Anti-UAV challenge data, 99.91% mAP50 (in-domain), 37 FPS on Jetson TX2 — [GitHub](https://github.com/Prabhdeep1999/uav-detection)
- nvhuynh16/YOLO-applied-to-Anti-UAV: YOLOv8n-416 on Anti-UAV data, 79.5% mAP50-95, 140 FPS GPU / 25 FPS CPU, includes Anti-UAV -> YOLO converter, MIT code — [GitHub](https://github.com/nvhuynh16/YOLO-applied-to-Anti-UAV)
- samabbas19/YOLO26-Drone-Detection-Jetson-Orin-Nano: YOLO26n + TensorRT, 97% mAP50 on custom set, ~39–60 FPS on Orin Nano, no models included — [GitHub](https://github.com/samabbas19/YOLO26-Drone-Detection-Jetson-Orin-Nano)
- tau-adl/Detection_Tracking_JetsonTX2: YOLOv3 + GOTURN, 18 FPS detect / 28 FPS track on TX2 — [GitHub](https://github.com/tau-adl/Detection_Tracking_JetsonTX2)
- YOLOv9 on Jetson Nano: 24.12 FPS — [ResearchGate](https://www.researchgate.net/publication/385933819_Edge_Computing-Driven_Real-Time_Drone_Detection_Using_YOLOv9_and_NVIDIA_Jetson_Nano)

### Inferences
- For "smallest possible drone" evaluation, the most demanding public IR sets are CST Anti-UAV (when released) and Anti-UAV410; the most demanding RGB sets are Drone-vs-Bird (most boxes <32 px, but DUA) and LRDDv3 (12 px area objects, 4K + paired IR). FL-Drones (mean 25x16 px) remains a useful small legacy set.
- Reported mAP50 values of 90%+ on DUT Anti-UAV / Det-Fly are in-domain and misleading for deployment: the LRDDv3 cross-dataset numbers (0.43–0.48 mAP50) indicate large domain gaps; plan on training across several sets.
- Challenge-winning IR methods (frame dynamics, trajectory filtering, Dist-Tracker) are detector+temporal designs rather than single-frame YOLO — temporal cues appear essential for few-pixel IR drones.
- Edge repos generally train on single benchmarks and seldom release weights; a reusable open "anti-drone checkpoint" trained on the full union of public sets does not appear to exist.

### Gaps
- Per-team AP leaderboard numbers for Drone-vs-Bird IJCNN 2025 and the 4th Anti-UAV official leaderboard were not retrievable (summary paper/leaderboard behind IEEE/website; WRN-YOLO repo reports only "Top 3").
- CST Anti-UAV and TDTIV download URLs/licenses not yet published at time of research.
- Licenses for MIDGARD, FL-Drones, DUT Anti-UAV, LRDDv2/v3 were not found.
- No open model with weights trained on Anti-UAV410/CST was found on Hugging Face.

---

## Key Question 2 — Military vehicles: open datasets (satellite/aerial/ground), pretrained weights, and tiny-vehicle results in satellite imagery

### Takeaway
The large, well-curated overhead benchmarks (xView, DOTA, VEDAI, DIOR, FAIR1M, SIMD) contain only civilian vehicle classes and are mostly non-commercial; true "military vehicle" datasets are small community sets on Roboflow Universe/Kaggle (1k–27k images, mostly ground-level or oblique drone, mixed quality, often mislabeled CC BY) plus the Mendeley UAV set (CC BY 4.0) and MAR20 for military aircraft (CC BY-NC 4.0). For sub-16-pixel vehicle detection, AI-TOD/AI-TOD-v2 (mean 12.7–12.8 px) and xView small cars (median ~14 px) are the correct test beds; no peer-reviewed mAP for tank detection from satellite imagery was found.

### Cited Findings

**Overhead benchmarks (civilian vehicle classes, small objects)**
- xView: >1M instances, 60 classes, 0.3 m WorldView-3, ~3000x3000 px images, 847 labeled train images; license CC BY-NC-SA 4.0; vehicle taxonomy is civilian (Small Car, Pickup Truck, Cargo Truck, Engineering Vehicle...), no military class — [Ultralytics xView docs](https://docs.ultralytics.com/datasets/detect/xview); [xView paper](https://arxiv.org/pdf/1802.07856)
- xView small cars ~7 px on a side minimum, median 14 px; boxes typically 10x16 px — [Picterra baseline](https://medium.com/picterra/the-xview-dataset-and-baseline-results-5ab4a1d0f47f); [super-resolution study](https://arxiv.org/pdf/1812.04098); xView-vehicle subset mean size 14.1 px (range 8–33 px) — [arXiv 2104.11854](https://arxiv.org/pdf/2104.11854)
- DOTA: v1.0 2,806 images/188,282 instances/15 classes; v1.5 adds <10 px annotations, 403,318 instances; v2.0 11,268 images/1,793,658 instances/18 classes; only "small vehicle"/"large vehicle"; academic non-commercial only, Google Earth ToS — [Ultralytics DOTA docs](https://docs.ultralytics.com/datasets/obb/dota-v2); [DOTA CVPR 2018](https://openaccess.thecvf.com/content_cvpr_2018/papers/Xia_DOTA_A_Large-Scale_CVPR_2018_paper.pdf); license discussion — [ultralytics PR #27094](https://github.com/ultralytics/ultralytics/pull/27094)
- VEDAI: 1,246 images (1024 and 512 px), 12.5 cm GSD Utah AGRC imagery, RGB + IR, ~3,640 vehicle instances, 9 commonly used classes (car 62%) — [SuperYOLO (arXiv 2209.13351)](https://arxiv.org/pdf/2209.13351); [Multimodal RS detection](https://arxiv.org/pdf/2307.06724)
- DIOR: 23,463 images, 192,472 instances, 20 coarse classes (single "vehicle"), 0.5–30 m GSD; FAIR1M: 42,796 images, >1.02M OBB instances, 37 fine-grained classes incl. 10 vehicle sub-classes (all civilian) — [FAIR1M (arXiv 2103.05569)](https://arxiv.org/pdf/2103.05569); SIMD: 5,000 Google Earth images, 45,096 instances, 15 classes incl. 7 car types, 6 aircraft types — [Meta-review](https://arxiv.org/pdf/2309.06751)
- VME (2025, Nature Sci. Data) compares car-size distributions across xView, DOTA-v2, VEDAI, FAIR1M-2.0, DIOR — [VME](https://www.nature.com/articles/s41597-025-04567-y)
- AI-TOD: 28,036 images (800x800), 700,621 instances, 8 classes, mean object size ~12.8 px; AI-TOD-v2: 752,754 instances, mean 12.7 px, ~86% of instances <16 px; bins very tiny 2–8, tiny 8–16, small 16–32 px — [AI Review survey 2025](https://link.springer.com/article/10.1007/s10462-025-11150-9); [Similarity Distance label assignment](https://arxiv.org/pdf/2407.02394); SODA-A: 2,513 images, 872,069 OBB instances, avg 4761x2777 px, ~347 instances/image — [DyFrDet](https://arxiv.org/pdf/2608.02495)

**Military aircraft (satellite)**
- MAR20: 3,842 images, 20 military aircraft types, 22,341 instances, HBB + OBB, "research purposes only", CC BY-NC 4.0 — [Gong Cheng page](https://gcheng-nwpu.github.io/); Roboflow mirror re-labels as CC BY 4.0 (conflict) — [Roboflow MAR20](https://universe.roboflow.com/planes-omttb/mar20-bpxjm)
- MTARSI 2: 42 classes, CC BY (Zenodo) — [OpenAIRE](https://explore.openaire.eu/search/dataset?pid=10.5281/zenodo.5044950); MTARSI-INNAR: 27 train classes, CC BY 4.0 — [Zenodo](https://zenodo.org/records/10421449)
- HRPlanes: 3,092 Google Earth images 4800x2703, 18,477 aircraft incl. military, CC BY-NC 4.0 — [Zenodo](https://zenodo.org/records/14546832); HRPlanesv2: 2,120 images, 14,335 aircraft, CC BY-NC-ND 4.0 + Google Earth ToS, with YOLOv4/v5/v8 weight files — [GitHub](https://github.com/dilsadunsal/HRPlanesv2-Data-Set)
- Aircraft detection mAP context: YOLOv8 94% / RT-DETR 92.7% on curated aircraft sets; on DOTA, YOLOv5 mAP 0.567; on military MADAI dataset, TransEffiDet 86.6% — [Cinarer 2025](https://onlinelibrary.wiley.com/doi/10.1155/ijae/5599522); [FlightScope](https://arxiv.org/pdf/2404.02877)

**Military ground-vehicle datasets (community)**
- Roboflow Universe sets with hosted models: "military vehicles detection" (OJleHuHa) 1,994 images, APC/TANK/CAR/TRUCK/ART/MLRS, YOLOv8l model, CC BY 4.0 — [link](https://universe.roboflow.com/ojlehuha-aswwb/military-vehicles-detection-0jxhy/dataset/11); "military-vehicle" (Huyen Dinh) 10,218 images, 10 classes incl. tank/apc/bmp/artillery-gun — [link](https://universe.roboflow.com/huyen-dinh/military-vehicle-rstvv); "Military vehicles detection" (Robert Paulson) 9,962 images TRUCK/TANK/PERSON — [link](https://universe.roboflow.com/robert-paulson-fncbw/military-vehicles-detection-qwfnc); "military object detection" (yolo datasets) tank/military vehicle/soldier, CC BY 4.0 — [link](https://universe.roboflow.com/yolo-datasets-ymdve/military-object-detection-uxkcn); search pages — [class:apc](https://universe.roboflow.com/search?q=class%3Aapc), [class:military_vehicle](https://universe.roboflow.com/search?q=class%3Amilitary_vehicle), [class:soldier](https://universe.roboflow.com/search?q=class%3Asoldier)
- "Military Vehicle Recognition" (Roboflow): 1,245 drone reconnaissance images from the Russo-Ukrainian war (fighters, bombers, APCs, tanks, soldiers), YOLOv11 model mAP50 47.3%, precision 62.9% — [link](https://universe.roboflow.com/militaryvehiclerecognition/military-vehicle-recognition)
- Kaggle: Military Assets Dataset (12 classes, YOLOv8 format: tank, truck, vehicle, soldier, artillery, aircraft, warship...) — [link](https://www.kaggle.com/datasets/rawsi18/military-assets-dataset-12-classes-yolo8-format); UAV & Aerial View Battle Tank (synthetic, CC BY 4.0) — [link](https://www.kaggle.com/datasets/simuletic/uav-and-aerial-view-battle-tank-detection-dataset); AMAD-5 aerial military asset (5 classes incl. soldier, augmented) — [link](https://www.kaggle.com/datasets/rupankarmajumdar/amad-5-aerial-military-asset-detection-dataset); Oryx losses image set (ground photos, tabular) — [link](https://www.kaggle.com/datasets/piterfm/2022-ukraine-russia-war-equipment-losses-oryx)
- Mendeley "Multi-Class UAV Military Object Detection Dataset" (June 2026, JUST Jordan): 7,985 images / 14,018 instances — tank 4,990, drone 1,296, people 4,492, soldier 3,240; tank/drone/people sourced from Roboflow/Kaggle, soldier class entirely GTA5 synthetic; CC BY 4.0; YOLOv9c mAP50 89.6% — [Mendeley Data](https://data.mendeley.com/datasets/9z7yrcrpjk/1)
- GitHub ARMA-3 synthetic YOLOv5 weights (not real imagery) — [AlexandreSajus](https://github.com/AlexandreSajus/Military-Vehicles-Image-Recognition); [RsGoksel](https://github.com/RsGoksel/Military-Vehicles-Detection)
- Ukraine's "Universal Military Dataset" (labeled combat drone imagery; claims 70% of enemy equipment identified, 2.2 s/object) is shared with UK firms, not public — [The Decoder](https://the-decoder.com/ukraine-opens-its-massive-labeled-battlefield-dataset-to-british-firms-in-a-landmark-ai-weapons-partnership/)
- UAV military target pipeline (YOLOv11 + SPD-Conv small-target head; person/tank/IFV classes) — [CEUR-WS Vol-3963](https://ceur-ws.org/Vol-3963/paper2.pdf)

### Inferences
- "Military vehicle" open data is effectively a community-labeled Roboflow ecosystem: large overlap between projects (merges of the same sources), oblique/ground-level views dominate, and labels/licenses are unreliable. Use them for pretraining/domain exposure, not as benchmarks.
- For satellite-scale military vehicles (a tank at 0.3 m GSD is ~25x12 px; at 0.5 m ~14x7 px), xView small-car / AI-TOD protocols are the closest proxies; expect the same AP collapse seen on AI-TOD (very-tiny bin).
- MAR20 is the only curated, multi-class *military* overhead benchmark found, and it is non-commercial.

### Gaps
- No peer-reviewed mAP for tank/APC detection from *satellite* imagery was found (commercial systems like Maxar/Vantor Sentry do not publish metrics).
- Roboflow "military object detection" page returned HTTP 403; image count/model metrics taken from search snippet only.
- VEDAI, SIMD, DIOR, FAIR1M explicit license texts not found (DIOR/FAIR1M generally research-only per their portals; verify).
- MVRSD dataset (cited by the OKIYOLO HF card) — no primary source located.

---

## Key Question 3 — SAR imagery: datasets (SSDD, HRSID, SAR-Ship, SARDet-100K, MSAR, FUSAR-Ship, SAR-AIRcraft-1.0) and lightweight detectors with code

### Takeaway
SARDet-100K (NeurIPS 2024 spotlight; 116,598 images, 245,653 instances, 6 classes incl. tank/aircraft/ship; CC BY-NC 4.0) unifies 10 prior sets and ships MSFA pretrained checkpoints (best 56.4 mAP; newer foundation models reach 60–61 mAP). Ship datasets (SSDD 2,358 ships; HRSID 16,951 ships; SAR-Ship 59,535 ships) are saturated (97–98% AP50) and lightweight YOLO variants with code (LEAD-YOLO, AC-YOLO) reach near-baseline accuracy at roughly half the parameters. Chinese Journal-of-Radars datasets (MSAR, SAR-AIRcraft-1.0, FUSAR) require registration and are free for teaching/research only.

### Cited Findings
- SARDet-100K: 116,598 images, 245,653 instances, 6 categories (Aircraft, Ship, Car, Bridge, Tank, Harbor), 8:1:1 split, 10 source datasets; MSFA pretraining framework — [arXiv 2403.06534](https://arxiv.org/abs/2403.06534); [NeurIPS poster](https://neurips.cc/virtual/2024/poster/94539)
- SARDet-100K repo: license CC BY-NC 4.0; train 94,493 / val 10,492 / test 11,613 images (README says only train+val released so far); sources AIR_SARShip1/2, HRSID, MSAR, SADD, SAR-AIRcraft, ShipDataset, SSDD, OGSOD, SIVED; resolutions 0.1 m (SIVED) to 25 m; MSFA checkpoints for Faster/Cascade/Grid RCNN, RetinaNet, GFL, DenoDet, FCOS, DETR variants on R50–R152/ConvNeXt/VAN/Swin; Faster RCNN R50 49.0 -> 51.1 mAP with MSFA; ConvNeXt-B+MSFA 56.4 mAP; Faster RCNN R50+MSFA AP-small 45.2 — [GitHub zcablii/SARDet_100K](https://github.com/zcablii/SARDet_100K); weights — [Kaggle models](https://www.kaggle.com/models/greatbird/msfa); data — [Kaggle dataset](https://www.kaggle.com/datasets/greatbird/sardet-100k)
- SARDet-100K leaderboard: CoDe-MAE (HiViT-B) 61.1 mAP; SARVLMDet 60.2; SARMAE 57.9; SARATR-X 57.3; DenoDet v2 56.7; MSFA ConvNeXt-B 56.4; Deformable DETR 50.0 — [SOTA2 leaderboard](https://www.sota2.com/research/sota/object-detection-on-sardet-100k); DenoDet — [arXiv 2406.02833](https://arxiv.org/pdf/2406.02833); DenoDet V2 — [arXiv 2508.09392](https://arxiv.org/pdf/2508.09392)
- SSDD: 2,358 ship instances, official release — [Official-SSDD](https://github.com/TianwenZhang0825/Official-SSDD); HRSID: 5,604 images, 16,951 ships, 0.5/1/3 m — [HRSID](https://github.com/chaozhong2010/HRSID); SAR-Ship-Dataset: 59,535 ships, 256x256 chips — [CAESAR-Radi](https://github.com/CAESAR-Radi/SAR-Ship-Dataset)
- MSAR-1.0: 28,449 slices (HISEA-1 + GF-3, HH/HV/VH/VV), 4 classes (1,851 bridges, 39,858 ships, 12,319 oil tanks, 6,368 aircraft), 256x256 (bridges 2048x2048); free for teaching, commercial use requires contacting Journal of Radars; WeChat/email registration — [Journal of Radars](https://radars.ac.cn/web/data/getData?dataType=MSAR_en&pageType=en); [ScienceDB mirror](https://www.scidb.cn/en/detail?dataSetId=3f011a272c3f4c598843f1be94b9c58f)
- FUSAR-Ship v1.0: GF-3 UFS mode, 16,144 chips (6,252 AIS-matched ships, 15 categories/98 sub-categories, plus clutter/land/bridge negatives), 512x512, ~1.1–1.7 m resolution; "copyright Fudan University", no CC license — [Fudan EMW Lab](https://emwlab.fudan.edu.cn/67/05/c20899a222981/page.htm); [SCIS paper](https://link.springer.com/article/10.1007/s11432-019-2772-5)
- SAR-AIRcraft-1.0: GF-3 1 m, 4,368 images, 16,463 aircraft, 7 types (A220, A320/321, A330, ARJ21, B737, B787, other) — [Journal of Radars](https://radars.ac.cn/en/article/doi/10.12000/JR23043)
- Lightweight SAR detectors with code: LEAD-YOLO (YOLOv5 + FasterNet/RFCBAMConv/C3_CA; SSDD 97.7 AP vs 98.0 baseline with 56.5% fewer params; HRSID baseline 92.7; SAR-ship 98.1; Cambricon MLU220 deployment) — [GitHub](https://github.com/qingqing-zijin/LEAD-YOLO); AC-YOLO (YOLO11-based, -30% params, -15.6% FLOPs, +1.2 AP SSDD, +1.5 AP HRSID) — [PLOS ONE 2025](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0327362), code https://github.com/He-ship-sar/ACYOLO; DTKDP distillation+pruning for oriented SAR ships — [arXiv 2609.24872](https://arxiv.org/pdf/2609.24872); MC-ASFF-ShipYOLO (YOLO11, small/multi-scale, HRSID+SSDD) — [Sensors 2025 correction](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12846165/)
- Tooling: unified processor for HRSID/SAR-Ship/SSDD/SRSDD — [GitHub](https://github.com/egshkim/SAR-ShipDet-Dataset-Processor); curated lists — [Awesome-SAR-Detection](https://github.com/Sugeradi985/Awesome-SAR-Detection), [Ship datasets list](https://github.com/jasonmanesis/Satellite-Imagery-Datasets-Containing-Ships)
- SAR foundation model status (2025) — [arXiv 2509.21722](https://arxiv.org/pdf/2509.21722); SARATR-X — [arXiv 2405.09365](https://arxiv.org/pdf/2405.09365)

### Inferences
- SARDet-100K is the only multi-class SAR set with a "tank" category (storage tanks, from OGSOD — note: "tank" here means oil/storage tank, not armored vehicle; MSAR's "oil tanks" confirms the semantics). There is no open SAR dataset of military ground vehicles.
- Ship AP50 is saturated on SSDD/SAR-Ship; HRSID (92–93) and SARDet-100K small-object AP (~45) are the better discriminators for tiny-target work.
- Commercial use of nearly every SAR benchmark is blocked (CC BY-NC or Journal-of-Radars terms); any product model must be trained on licensed/own SAR data.

### Gaps
- Per-dataset small/medium/large ship histograms for SSDD/HRSID not retrieved (available in their papers).
- MSFA/SARDet-100K test split not yet released per README.
- No lightweight SARDet-100K detector with edge latency numbers found.

---

## Key Question 4 — Thermal/IR: HIT-UAV, FLIR ADAS, LLVIP, M3FD, KAIST, DroneVehicle, and infrared small target detection (ISTD) models that are edge-feasible

### Takeaway
HIT-UAV (2,898 thermal drone-view images, 60–130 m altitude, Person/Bicycle/Car/OtherVehicle; CC0 on Zenodo) and DroneVehicle (56,878 RGB-IR paired images, 953k vehicles, no explicit license) are the key aerial IR sets; LLVIP (non-commercial), FLIR-Aligned, M3FD and KAIST are ground-level fusion benchmarks where RGB-IR fusion adds ~10–15 mAP over RGB alone. ISTD benchmarks (SIRST 427 real, NUDT-SIRST 1,327 synthetic, IRSTD-1K 1,001 real; targets ~1–10 px, mean 11.9 px on IRSTD-1K) have a crowded 2025 field of lightweight models — LCMamNet (Jetson Orin NX benchmarked), BiisNet (binarized, ~10K params), WaveTD/IRST-RTDETR/TODENet (code+weights) — with IRSTD-1K IoU in the 67–74% range.

### Cited Findings

**Thermal aerial / paired datasets**
- HIT-UAV: 2,898 IR images from 43,470 frames; Person, Bicycle, Car, OtherVehicle; altitude 60–130 m, pitch 30–90 deg, day/night; 2,029/290/579 split; baselines mAP50: SSD-512 85.6%, YOLOv4 84.75%, YOLOv4-tiny 50.38% — [Sci. Data 2023](https://www.nature.com/articles/s41597-023-02066-6); [arXiv 2204.03245](https://arxiv.org/pdf/2204.03245); [GitHub](https://github.com/suojiashun/HIT-UAV-Infrared-Thermal-Dataset); Zenodo record 7633134 listed CC0-1.0 — [Ultralytics platform listing](https://platform.ultralytics.com/marco-milone/datasets/hit-uav); Kaggle YOLO-format mirror — [Kaggle](https://www.kaggle.com/datasets/pandrii000/hituav-a-highaltitude-infrared-thermal-dataset); EDet-YOLO +1.7 mAP50 over baseline on HIT-UAV — [EmergentMind summary](https://www.emergentmind.com/topics/hit-uav-dataset)
- DroneVehicle: 56,878 images, 953,087 vehicle instances, RGB-IR paired, day-to-night, OBB; mAP50 used; baselines Oriented R-CNN (RGB) 60.8, MBNet (RGB+IR) 71.9; GMD-YOLO 78.0 mAP50 — [UA-CMDet (arXiv 2003.02437)](https://arxiv.org/pdf/2003.02437); [C2Former (arXiv 2306.16175)](https://arxiv.org/pdf/2306.16175); [UA-CMDet repo, Apache-2.0 code](https://github.com/SunYM2020/UA-CMDet); no explicit data license; VisDrone family is "academic and non-commercial use only" — [VisDrone README mirror](https://github.com/Mhaiyang/VisDrone/blob/master/README.md)
- LLVIP: 15,488 aligned pairs (12,025 train / 3,463 test); official license: free for non-commercial purposes only, attribution, no redistribution — [LLVIP site](https://bupt-ai-cz.github.io/LLVIP/); [GitHub](https://github.com/bupt-ai-cz/LLVIP); SOTA: WaveMamba 98.3 mAP50 / 66.0 mAP; InfraNet 70.5–70.6 mAP; YOLOv8l RGB-only 91.9/54.0 — [WaveMamba ICCV 2025](https://arxiv.org/pdf/2507.18173); [InfraNet](https://arxiv.org/pdf/2607.03795)
- FLIR ADAS: 14,452 RGBT pairs; FLIR-Aligned subset 4,129 train / 1,013 test, only IR annotated; InfraNet RGB-IR 89.5 mAP50 / 55.1 mAP vs YOLOv8 RGB 66.3/28.2 — [InfraNet](https://arxiv.org/pdf/2607.03795); M3FD: 4,200 aligned pairs (3,360/840 split), PFDet 86.7 mAP50 — [Consensus/Discrepancy paper](https://arxiv.org/pdf/2604.11234)
- KAIST: 95,328 pairs, 103,128 pedestrian annotations; evaluated with log-average miss rate, GMD-YOLO MR 7.73% at 61.7 FPS — [UniRGB-IR](https://arxiv.org/pdf/2404.17360); [Consensus/Discrepancy paper](https://arxiv.org/pdf/2604.11234)
- MONET multimodal drone thermal dataset (rural) — [arXiv 2304.05417](https://arxiv.org/pdf/2304.05417); thermal drone detection with synthetic training — [arXiv 2608.17799](https://arxiv.org/pdf/2608.17799)

**ISTD datasets**
- NUAA-SIRST: 427 real images, ~10% multi-target, splits 341:86 or 224:96 — [ISTD review (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11207645/)
- NUDT-SIRST: 1,327 synthetic 256x256 images, 5 background types, ~37% multi-target, target sizes ~3x3–9x9 px (~0.015% of frame) — [Improved DNA-Net (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11819943/)
- IRSTD-1K: 1,001 real 512x512 images (drones, creatures, ships, vehicles), 800/201 split, target size 1x1–56x33; test split avg target 11.9 px (NUDT 31.4 px) — [Na-IRSTD](https://arxiv.org/pdf/2605.05804); [Deep IR small object segmentation survey](https://arxiv.org/html/2502.14168v1)
- Metrics: Pd (centroid within 3 px), Fa (false pixels / all pixels), IoU/nIoU — [MSDA-Net](https://arxiv.org/pdf/2406.02037)

**ISTD model results (IoU % / Pd % / Fa x1e-6, numbers vary by protocol)**
- DNA-Net: NUDT 82.17/98.93/23.65, IRSTD-1K 63.01/97.7/9.72, 4.69M params; MSHNet: NUDT 81.07/98.25/25.81, IRSTD-1K 64.51/97.8/12.37, 4.05M params — [Improved DNA-Net (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11819943/); MSHNet 24.43 GFLOPs, 20 FPS — [RDANet](https://arxiv.org/html/2608.20870v1)
- UIU-Net: 50.54M params; NUDT mIoU 94.11/Pd 97.98/Fa 0.74; IRSTD-1K 67.94/90.57/24.44; ACM 0.40M params IRSTD-1K 64.09 — [DATransNet](https://arxiv.org/pdf/2409.19599)
- Recent SOTA: RDANet IRSTD-1K IoU 73.82, NUDT 95.43; DGNet IRSTD-1K 72.72 (Fa 4.25), NUDT 95.78/Pd 99.37; MSCA-Net 78.43/94.56/67.08 on SIRST/NUDT/IRSTD-1K — [RDANet](https://arxiv.org/html/2608.20870v1); [DGNet](https://arxiv.org/pdf/2609.00666); [MSCA-Net](https://arxiv.org/pdf/2503.17193)
- Lightweight / edge ISTD: LCMamNet (Mamba; NUDT mIoU 95.58, Pd 99.47; latency measured on Jetson Orin NX 16G Super) — [arXiv 2607.24184](https://arxiv.org/pdf/2607.24184); BiisNet (binarized, "10K is enough") — [arXiv 2503.02662](https://arxiv.org/html/2503.02662v1); WaveTD (IRSTD-1K IoU 69.86/Pd 91.16/Fa 5.54; NUDT 93.30/99.30/1.42; weights released) — [GitHub](https://github.com/Fortuneteller6/WaveTD); IRST-RTDETR (4.68M params, -6.4 ms latency, code+weights) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1350449526000381), code https://github.com/amumu77-lang/IRST-RTDETR; TODENet (Pd 94.2% IRSTD-1K, code) — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1350449525003512); MDS-DWGANet (1.4M params, IRSTD-1K mIoU 67.04) — [Springer](https://link.springer.com/article/10.1007/s11760-025-04969-w); LCAE-Net 1.945M params / 4.86 GFLOPs / 70 FPS — [arXiv 2411.13260](https://arxiv.org/pdf/2411.13260); MiM-ISTD efficient Mamba — [arXiv 2403.02148](https://arxiv.org/pdf/2403.02148)
- Official code repos (from prior knowledge; verify): DNA-Net + NUDT-SIRST data https://github.com/YeRen123455/Infrared-Small-Target-Detection ; UIU-Net https://github.com/danfenghong/IEEE_TIP_UIU-Net ; MSHNet https://github.com/Lliu666/MSHNet ; SIRST https://github.com/YimianDai/sirst ; IRSTD-1K (ISNet) https://github.com/RuiZhang97/ISNet

### Inferences
- For "smallest thermal targets", ISTD sets (1–10 px targets) are far more demanding than HIT-UAV (people at 60–130 m are tens of px). ISTD models are segmentation networks at 256–512 px inputs with 1–5M params — edge-feasible, but they are single-class (target/no-target) and must be paired with a classifier/tracker.
- IRSTD-1K is the right real-data benchmark; NUDT-SIRST numbers (>93% IoU) are saturated synthetic results.
- Cross-paper ISTD numbers are inconsistent (e.g., AEDNet reports UIU-Net NUDT IoU 78.55 vs 94.11 elsewhere) — only compare within a single paper's table.

### Gaps
- No HIT-UAV result from a modern nano model with on-device latency was found (only community YOLOv8n/YOLO11s fine-tunes, no benchmark table).
- DroneVehicle has no explicit license from the authors; commercial status unclear.
- LCMamNet and BiisNet code links not verified.

---

## Key Question 5 — Personnel: TinyPerson, SeaDronesSee, Okutama-Action, camouflaged-person datasets, HERIDAL/SARD — what is reported for very small people from UAVs

### Takeaway
TinyPerson (median person size 13–15 px, ~20% under 8 px) is the canonical tiny-person benchmark; best reported AP50-tiny has risen from ~44 (2020) to ~59–61 (SSPNet/EFFM) while AP75-tiny stays single-digit. SeaDronesSee (54k frames, ~400k instances, CC0) and HERIDAL (1,647 images, 3,229 persons at 40–65 m, CC BY 3.0) are the permissively licensed SAR sets; soldier/camouflage datasets (CPD1K 1,000 images, MCAM, MSC1K, ACD1K, CPD-UAV) are small and mostly research-only, and real operational-UAV soldier imagery is essentially absent (the Mendeley set uses GTA5 synthetic soldiers).

### Cited Findings
- TinyPerson: 794 train / 816 test images (1920x1080, 3840x2160), seaside/maritime, median box size 13 px (train) / 15 px (test), ~1 in 5 under 8 px; eval ranges tiny [1,20], tiny1 [1,8], tiny2 [8,12], tiny3 [12,20], small [20,32]; Faster RCNN-FPN baseline 43.55 AP50-tiny, 47.29 with MSM pretraining — [Scale Match (WACV 2020)](https://arxiv.org/pdf/1912.10664); SSPNet 59.13 AP50-tiny (60.87 in repo) — [SSPNet](https://arxiv.org/pdf/2107.01548), [GitHub](https://github.com/MingboHong/SSPNet); WaveletPool+SSPNet 59.34 — [Anti-aliasing](https://arxiv.org/pdf/2310.14221); EFFM 60.72 AP (secondary report) — [search summary]; AP75-tiny ~5–9; data terms: no separate data license, research use, image rights remain with original owners — [HF mirror](https://huggingface.co/datasets/shijli/tinyperson); official repo (MIT for code) — [TinyBenchmark](https://github.com/Muqianli/TinyBenchmark)
- SeaDronesSee: >54,000 frames, ~400,000 instances, 5456x3632, 5–260 m altitude, 0–90 deg; code MIT, data CC0 1.0; MaCVi challenges WACV 2023–2025 — [WACV 2022 paper](https://openaccess.thecvf.com/content/WACV2022/papers/Varga_SeaDronesSee_A_Maritime_Benchmark_for_Detecting_Humans_in_Open_Water_WACV_2022_paper.pdf); [GitHub](https://github.com/Ben93kie/SeaDronesSee); anchor-box optimization for two-stage detectors on SeaDronesSee — [Sci. Reports](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10899653/); YOLOv8 modular optimization — [Sci. Reports 2024](https://www.nature.com/articles/s41598-024-75807-1)
- HERIDAL: 1,647 annotated 4000x3000 images (1,546 train / 101 test), 3,229 persons, 40–65 m altitude, ~2 cm GSD, Croatia/BiH; person ~0.1% of image; one method 68.89% precision / 94.65% recall; "only widely used public SAR-APD benchmark for land" — [Aerial Person Detection survey, J. Remote Sensing](https://spj.science.org/doi/10.34133/remotesensing.0474); license CC BY 3.0 Unported — [Accenture AIR README](https://github.com/Accenture/AIR/blob/master/README.md), [Aalto mirror](https://research.aalto.fi/en/datasets/heridal-dataset-in-keras-retinanet-pascal-voc-format)
- SARD: ~1,981 images, 6,532 boxes, 5–50 m, forest, oblique, pose attributes; ForestPersons (2026) cross-test: SARD-trained AP 23.2 / AP50 53.5 vs HERIDAL-trained 0.0/0.0 on real under-canopy MAV data — [ForestPersons](https://arxiv.org/html/2603.02541v1); [Person Recognition in Aerial Surveillance survey](https://arxiv.org/html/2511.17674v1)
- Okutama-Action: 43 videos (33 train / 10 test), 77,365 frames, 10–45 m, 45–90 deg, DJI Phantom 4, person boxes + actions; test GT not released; listed as non-commercial — [arXiv 1706.03038](https://arxiv.org/pdf/1706.03038); [HyperAI listing](https://hyper.ai/en/datasets/5714)
- Camouflage: CPD1K 1,000 soldier images from video (SPL 2018), worst cross-dataset generalization in SINet study — [SINet CVPR 2020](https://mmcheng.net/mftp/Papers/20CVPR_Camouflag.pdf); COD10K 10,000 images (5,066 camouflaged) but "only dozens" of camouflaged people — [COD page](https://dengpingfan.github.io/pages/COD.html), [Defence Technology 2021](https://www.sciencedirect.com/science/article/pii/S2214914721001586); CAMO 1,000 train / 250 test incl. military camouflage; MCAM (soldiers + supplies, pixel-level) — [ResearchGate](https://www.researchgate.net/publication/385748957_Military_camouflaged_object_detection_with_deep_learning_using_dataset_development_and_combination); MSC1K (2025) — [Sci. Reports](https://www.nature.com/articles/s41598-025-18886-y); CPD-UAV (Drones 2026) and MCODUAV — [Drones](https://doi.org/10.3390/drones10060447)
- Soldier UAV data: Mendeley set soldier class is GTA5-synthetic (982 images) due to "limited availability of open-source soldier images captured by operational UAV platforms" — [Mendeley](https://data.mendeley.com/datasets/9z7yrcrpjk/1); Roboflow "UAV-tank-soldier" 4,821 images CC BY 4.0 — [link](https://universe.roboflow.com/1-ukcc8/uav-tank-soldier-cjbmf)
- Zero-shot person detection in drone imagery with YOLO-World/GPT-4V on Okutama — [arXiv 2404.01571](https://arxiv.org/pdf/2404.01571)

### Inferences
- TinyPerson is the only personnel benchmark with a formal sub-20-px protocol; SeaDronesSee at 260 m altitude also yields very small swimmers and is the only large, CC0 set.
- HERIDAL's nadir high-altitude imagery transfers poorly to oblique/forest scenes (0.0 AP in ForestPersons) — domain mix is mandatory.
- There is no open benchmark for camouflaged/prone soldiers at long range from UAVs with meaningful scale; this is a genuine data gap.

### Gaps
- No per-size-bin results for SeaDronesSee or HERIDAL at sub-16 px found.
- Okutama-Action exact license text not found.
- Availability/licensing of MCAM, MSC1K, ACD1K, CPD-UAV not confirmed.

---

## Key Question 6 — Weapons: open firearm datasets (Mock Attack/USRT, UCF, Sohas, YouTube-GDD, Monash, CCTV-Gun, Roboflow) and lightweight models with code

### Takeaway
YouTube-GDD (5,000 images, 16,064 guns, YOLO format, built from scripts) is the most training-ready; the Seville Mock Attack/USRT set (5,149 Full-HD CCTV frames) is the realistic hard benchmark — raw training yields mAP ~0.09 because weapons are tiny, so tiling is standard; CCTV-Gun (MGD + USRT + UCF, Apache-2.0 code with mmdetection checkpoints) is the only benchmark with released trained models; no dedicated lightweight edge firearm detector with weights was found beyond Roboflow community models.

### Cited Findings
- YouTube-GDD: 343 HD videos -> 5,000 images, 16,064 gun + 9,046 person instances, YOLO labels, built via scripts; YOLOv5 baseline — [arXiv 2203.04129](https://arxiv.org/pdf/2203.04129); [GitHub](https://github.com/UCAS-GYX/YouTube-GDD)
- Mock Attack (Univ. of Seville, "Real-time gun detection in CCTV: An open problem"): 5,149 frames, 3 cameras, 1920 px wide; raw-image training mAP 0.092 per ACF paper — [ACF (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572610/); dataset page — [GitHub](https://github.com/Deepknowledge-US/US-Real-time-gun-detection-in-CCTV-An-open-problem-dataset/blob/gh-pages/index.md)
- ACF (Armed CCTV Footage): 8,319 images of armed pedestrians — [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9572610/)
- Sohas: 3,255 images, VOC format, 3,611 gun + 3,468 knife instances (secondary report) — [search summary; survey below]
- CCTV-Gun: curated from Monash Gun Dataset, USRT, UCF Crime; classes Person/Handgun; intra- and cross-dataset protocols; detectors Faster R-CNN, Swin-T, Deformable DETR, DetectoRS, ConvNeXt-T; trained models on Google Drive; Apache-2.0 — [arXiv 2303.10703](https://arxiv.org/abs/2303.10703); [GitHub](https://github.com/srikarym/CCTV-Gun)
- AI For Mankind gun-detection: merges YouTube-GDD + HGP + Seville data into one YOLOv5 training set — [GitHub](https://github.com/aiformankind/gun-detection)
- Firearm action+detection dataset for surveillance (2024) — [Data in Brief](https://www.sciencedirect.com/science/article/pii/S2352340924000040)
- Roboflow weapon-detection community model: 9,672 images, CC BY 4.0 — [link](https://universe.roboflow.com/yolov7test-u13vc/weapon-detection-m7qso)
- Survey "AI-Based Weapon Detection for Security Surveillance (2016–2025)" catalogs PDD, MAD, Weapon Vision AI etc. — [Electronics 2025](https://www.mdpi.com/2079-9292/14/23/4609); edge YOLOv5/v7/v8 on Sohas+COCO and SafeSchool YOLOv8 — [ReadyTensor](https://app.readytensor.ai/publications/safeschool-realtime-weapon-detection-using-yolov8-with-langchainbased-threat-analysis-agent-XLE3KDaNRIPq); distributed armed-robbery detection — [arXiv 2410.09731](https://arxiv.org/pdf/2410.09731)

### Inferences
- Handguns in wide-FOV CCTV are inherently a tiny-object problem (mAP <0.1 untiled); SAHI-style tiling or person-crop two-stage pipelines are the practical approach, which conflicts with edge latency budgets.
- Most weapon datasets are web/YouTube or staged; license terms are rarely explicit (YouTube-derived content has unclear redistribution rights).

### Gaps
- Exact CCTV-Gun image/instance counts and mAP tables not extracted (in paper PDF only).
- Sohas license and primary download page not located.
- No lightweight (<5M param) firearm detector with public weights and on-device latency found.

---

## Key Question 7 — Open multi-class "military object" pretrained checkpoints worth starting from (HF / Roboflow / GitHub): quality and license caveats

### Takeaway
Two Hugging Face checkpoints exist: OKIYOLO26X-DEFENSIVE (YOLO26x, 10 classes incl. tank/apc/artillery/military_vehicle/aircraft/helicopter/person; mAP50 75.8% on its own val split; AGPL-3.0) and spencercdz/YOLOv8m_defence (18 classes incl. Tank, Drone, Warship, Missile; mAP50-95 0.598 self-reported on a private dataset; Apache-2.0). Both are trained on aggregated Roboflow community data (or private data), with no small-object evaluation, and inherit Ultralytics AGPL / Roboflow-relabeling caveats — useful as warm starts, not as benchmarks.

### Cited Findings
- OKIYOLO26X-DEFENSIVE: classes person, car, bus, truck, tank, apc, artillery, military_vehicle, aircraft, helicopter; trained from YOLO26x COCO at imgsz 640 on Roboflow sets (Military Vehicles Detection, Military Tanks, Military-Civil-Vehicles, Russian-military-annotated, Army_vehicle_yolov8) + MVRSD; mAP50 75.8% / mAP50-95 59.8% (baseline 48.0/39.3), P 76.4, R 72.1; AGPL-3.0; card notes person detection weaker, APC vs military_vehicle ambiguity, "not a weapons system" — [HF card](https://huggingface.co/theokiGuyOKI/OKIYOLO26X-DEFENSIVE)
- spencercdz/YOLOv8m_defence: 18 classes (Cargo/Commercial/Light Aircraft, Drone, Fighter Jet, Fighter Plane, Helicopter, Missile, Truck, Car, Tank, Bus, Van, Cargo Ship, Yacht, Cruise Ship, Warship, Sailboat); private proprietary data; mAP50-95 0.598 measured on TensorRT-optimized version; Apache 2.0 — [HF card](https://huggingface.co/spencercdz/YOLOv8m_defence)
- Roboflow Universe hosted models: OJleHuHa yolov8l (6 classes) — [link](https://universe.roboflow.com/ojlehuha-aswwb/military-vehicles-detection-0jxhy/dataset/11); "Military Vehicle Recognition" YOLOv11 mAP50 47.3% on Ukraine drone footage — [link](https://universe.roboflow.com/militaryvehiclerecognition/military-vehicle-recognition); "vehicles-military-labels" model (148 images) — [link](https://universe.roboflow.com/yolomilitary/vehicles-military-labels)
- GitHub: gabrielyannarek04-max/military-object-detection (YOLOv8, 5 classes vehicles+personnel, weights via Releases) — [GitHub](https://github.com/gabrielyannarek04-max/military-object-detection); adityachintala/UAV-tracking-tank (YOLOv7 single-class tank, ~1,000 images, AP >90%) — [GitHub](https://github.com/adityachintala/UAV-tracking-tank)
- HRPlanesv2 YOLOv4/v5/v8 weights (aircraft only, CC BY-NC-ND data) — [GitHub](https://github.com/dilsadunsal/HRPlanesv2-Data-Set)
- SARDet-100K MSFA checkpoints (SAR, 6 classes, CC BY-NC 4.0 data) — [GitHub](https://github.com/zcablii/SARDet_100K)
- License caveats: Roboflow mirrors relabel MAR20 (CC BY-NC) and xView (CC BY-NC-SA) as CC BY 4.0 — [MAR20 official](https://gcheng-nwpu.github.io/), [xView docs](https://docs.ultralytics.com/datasets/detect/xview); Drone-vs-Bird copies on Roboflow conflict with its DUA — [wosdetc](https://github.com/wosdetc/challenge); Ultralytics position that DOTA restrictions apply to data not weights is "not independently confirmed" — [ultralytics PR #27094](https://github.com/ultralytics/ultralytics/pull/27094)

### Inferences
- Neither HF checkpoint was evaluated on small objects or on any standard benchmark; their validation splits come from the same Roboflow pools (likely near-duplicates across projects), so the 60–76% figures are optimistic.
- A clean, commercially usable multi-class military checkpoint does not exist: data provenance is Roboflow (uncertain rights), models are AGPL (Ultralytics) unless Apache (YOLOv8m_defence, but private data).
- Best practical starting points: OKIYOLO26X-DEFENSIVE (ground/aerial vehicles) + SARDet-100K MSFA (SAR) + an ISTD model (IR) as domain-specific backbones, re-trained on the user's own data.

### Gaps
- MVRSD dataset provenance/license not found.
- No HF checkpoint for anti-drone (Anti-UAV) or for military aircraft (MAR20) found.

---

## Key Question 8 — Which datasets have very small object sizes (median <32 px or <16 px) and are the right test beds for "smallest military objects"

### Takeaway
Confirmed sub-16-px benchmarks: AI-TOD/AI-TOD-v2 (mean 12.7–12.8 px, 86% <16 px), TinyPerson (median 13–15 px), xView small cars (median ~14 px, 10x16 px boxes), ISTD sets (IRSTD-1K avg 11.9 px, NUDT 3–9 px targets), and CST Anti-UAV tiny bin (box diagonal <=10 px). Sub-32-px: Drone-vs-Bird (most boxes <32x32), FL-Drones (mean 25x16), Anti-UAV410 (avg 39x24, borderline), LRDDv2 (most drones <=50 px at 1080p) and LRDDv3 (areas down to 12 px). DOTA-v1.5/v2 add <10 px annotations but have larger medians.

### Cited Findings
- AI-TOD mean 12.8 px; AI-TOD-v2 mean 12.7 px, ~86% <16 px — [AI Review 2025](https://link.springer.com/article/10.1007/s10462-025-11150-9); [arXiv 2407.02394](https://arxiv.org/pdf/2407.02394)
- TinyPerson median 13 px (train) / 15 px (test), ~20% <8 px — [WACV 2020](https://arxiv.org/pdf/1912.10664)
- xView small cars median 14 px, 10x16 px boxes at 0.3 m — [Picterra](https://medium.com/picterra/the-xview-dataset-and-baseline-results-5ab4a1d0f47f); [arXiv 1812.04098](https://arxiv.org/pdf/1812.04098)
- IRSTD-1K test avg target 11.9 px; NUDT-SIRST 3x3–9x9 px targets — [Na-IRSTD](https://arxiv.org/pdf/2605.05804); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11819943/)
- CST Anti-UAV tiny bin (0,10] diagonal, 78,224 tiny objects; Anti-UAV410 avg 39x24 px — [CST Anti-UAV](https://arxiv.org/pdf/2507.23473); [TDTIV/MCATrack](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_Tracking_Tiny_Drones_against_Clutter_Large-Scale_Infrared_Benchmark_with_Motion-Centric_ICCV_2025_paper.pdf)
- Drone-vs-Bird: most drones <32x32 px, min 15 px — [SynDroneVision](https://arxiv.org/html/2411.05633v1); FL-Drones mean 25.5x16.4, min 9x9 — [Dogfight](https://arxiv.org/pdf/2103.17242); LRDDv2 majority <=50 px at 1080p — [arXiv 2508.03331](https://arxiv.org/abs/2508.03331); LRDDv3 areas as small as 12 px — [arXiv 2605.25942](https://arxiv.org/pdf/2605.25942)
- DOTA-v1.5 adds annotations for objects <10 px; DOTA "small" bin is 10–50 px height — [Ultralytics DOTA](https://docs.ultralytics.com/datasets/obb/dota-v2); [DOTA paper](https://openaccess.thecvf.com/content_cvpr_2018/papers/Xia_DOTA_A_Large-Scale_CVPR_2018_paper.pdf)
- SODA-D (sibling) avg 20.31 px; SODA-A ~347 instances/image at 4761x2777 — [DyFrDet](https://arxiv.org/pdf/2608.02495)
- HERIDAL person ~0.1% of a 4000x3000 image — [J. Remote Sensing survey](https://spj.science.org/doi/10.34133/remotesensing.0474)
- SeaDronesSee altitude up to 260 m at 5456x3632 — [WACV 2022](https://openaccess.thecvf.com/content/WACV2022/papers/Varga_SeaDronesSee_A_Maritime_Benchmark_for_Detecting_Humans_in_Open_Water_WACV_2022_paper.pdf)

### Inferences
- Recommended "smallest military object" test-bed stack by modality: RGB satellite -> AI-TOD-v2 + xView small-vehicle subset (+ MAR20 for aircraft); IR -> IRSTD-1K (+ CST Anti-UAV when released, Anti-UAV410 now); RGB drone -> LRDDv3 + Drone-vs-Bird (if DUA acceptable) + FL-Drones; personnel -> TinyPerson + SeaDronesSee; SAR -> SARDet-100K AP-small and HRSID.
- Only SeaDronesSee (CC0), HIT-UAV (CC0 on Zenodo), HERIDAL (CC BY 3.0), Halmstad (CC BY 4.0), MTARSI (CC BY) and the Mendeley UAV set (CC BY 4.0) are clearly commercial-compatible among the sets above; nearly all tiny-object benchmarks (xView, DOTA, MAR20, SARDet-100K, LLVIP, Drone-vs-Bird, TinyPerson) are non-commercial.

### Gaps
- Median object sizes for SeaDronesSee, HERIDAL, HIT-UAV, DUT Anti-UAV, Det-Fly, DroneVehicle and the Roboflow military sets are not published in the sources found; they must be computed from annotations.
- AI-TOD license not retrieved.
