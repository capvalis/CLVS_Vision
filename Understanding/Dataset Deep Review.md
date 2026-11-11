# Dataset Deep Review

**56 dataset/release profiles · Evidence checked 10 November 2026**

This companion reviews how each catalogue entry was collected, labelled, partitioned and evaluated. It adds primary-method evidence and explicitly identifies corrections to the earlier catalogue. **A review is not an archive validation:** most findings come from papers, creator documentation and public metadata. Targeted file/annotation checks are named wherever performed. No complete visual-quality audit of the 56 image/video archives was conducted.

The central finding is that these resources represent different kinds of evidence: selected object crops, scene boxes, foreground masks, sensor pairs, temporal tracks, before/after changes and text generated from existing labels. Neither a large sample count nor the presence of sentences establishes broad scenario understanding. The profiles explain what is actually observed or annotated, without ranking datasets for military deployment or prescribing a recognition system.

The original report, workbook and `catalogue.json` remain as the earlier snapshot. Where this companion records a correction or stronger source, use the updated evidence here. The companion JSON contains the same 56 profiles with structured sources. Model compatibility, model licences, runtime performance and hardware comparisons remain outside this dataset review.

## How to interpret the evidence

| Evidence type | What it establishes | What it does not establish |
|---|---|---|
| Primary paper or creator documentation | What the authors report collecting, labelling and evaluating | That a current download exactly matches the paper or has no annotation errors |
| File-tree or directory metadata | Existence and names of returned files, sometimes complete path counts | Correct image content, correct class labels or absence of visual duplicates |
| Parsed annotation manifest | Actual record counts, schemas and the particular structural checks performed | Correctness of the depicted object or completeness of the annotations |
| Reported annotation review | A documented checking process | A residual error rate unless an appropriately described audit measures one |
| Benchmark result | Agreement with a specified annotation and evaluation protocol | General performance across unrelated environments or causes/intent not labelled by the data |

Unknown means the evidence was not established in this review. It does not automatically mean that a property is absent or that a dataset is poor. Author-reported quality controls and this review’s direct checks are deliberately distinguished. No numerical quality ranking has been invented.

## Main findings and corrections

| Finding | Evidence and consequence |
|---|---|
| **56 entries are not 56 independent source collections.** | [FGSC-23](#d15) reuses about 1,600 HRSC2016 chips; [FSAR-Cap](#d48) derives from FAIR-CSAR; [SARChat](#d55) derives from SARDet-100K; [LEVIR-CC](#d50) mainly crops LEVIR-CD imagery. Versions, mirrors and new labels can reuse the same observations. |
| **CAMO and CAMO-COCO have different denominators.** | The original paper calls the 1,250 camouflage-positive images CAMO. Adding 1,250 ordinary COCO images with zero camouflage masks creates CAMO-COCO, totalling 2,500. This corrects the earlier combined count under CAMO. [D46](#d46) |
| **Original HRSC2016 differs from a widely repeated count.** | Its original paper reports 1,061 labelled images and 2,976 objects, plus 610 separate unannotated images. Which later package produced the commonly repeated 1,070 figure was not resolved. [D17](#d17) |
| **milair’s image and class-occurrence counts differ.** | The checked untruncated Git tree has 374 image paths and 374 paired XML paths. The README class-occurrence counts sum to 660. [D40](#d40) |
| **RSICD’s five caption records rarely mean five different sentences.** | Direct JSON inspection found repeated caption strings within 10,197 of 10,921 images; only 724 images have five distinct trimmed strings. This measures repetition, not caption incorrectness. [D52](#d52) |
| **HRSID’s checked-in manifest is older than its linked release.** | The 2019 JSON contains 3,573 images, 9,870 annotations and 215 annotation-empty image records. It does not validate the complete later published release. [D02](#d02) |
| **Some published sources disagree internally.** | Examples include M3FD counts, COD10K’s background/noncamouflage descriptions, DIOR-R object totals, RSVQA-HR resolution wording and xBD split percentages. Each profile retains the discrepancy instead of silently choosing a number. [D27](#d27), [D47](#d47), [D10](#d10), [D53](#d53), [D56](#d56) |
| **Not every visible object is necessarily labelled.** | FUSAR labels a chip’s central ship; fMoW labels selected functional regions; xBD deliberately ignores post-event buildings without transferred pre-event polygons. Unmarked regions are therefore not universally reliable negatives. [D01](#d01), [D49](#d49), [D56](#d56) |
| **Language supervision has identifiable construction limits.** | FSAR-Cap combines templates, human refinement and language-model standardization; SARChat mainly expands existing annotation geometry; LEVIR-CC uses a fixed five-sentence set for no-change pairs. These are different sources of language evidence. [D48](#d48), [D55](#d55), [D50](#d50) |
| **High QA accuracy can reflect answer patterns.** | In the original RSVQA experiments, random reassignment of images still produced approximately 73–74% overall accuracy. This is an author-reported control demonstrating substantial language/answer bias. [D53](#d53), [D54](#d54) |
| **Access and rights are release-specific.** | FGSC-23’s full paper supplies non-profit academic-use terms; FSAR-Cap now has a creator-linked V1 release; Jeong’s paper still promises a future release and SARChat’s README has a placeholder dataset link. A repository or article licence does not settle all constituent image rights. [D15](#d15), [D48](#d48), [D45](#d45), [D55](#d55) |

## Why the dataset types need separate interpretations

| Dataset/annotation type | The labelled question | Main interpretation limit |
|---|---|---|
| Object-centred classification chips | Which listed category belongs to this selected object? | Selection can remove empty scenes and much of the original context. |
| Boxes or instance masks | Where are annotated objects, and what listed class do they have? | Visibility exclusions, size rules and incomplete category coverage define what may be unlabelled. |
| Foreground/camouflage masks | Which pixels belong to the specified foreground? | A binary mask does not provide identity, activity or cause. |
| Paired sensors / fusion collections | What corresponding observations do the sensors provide? | Registration, synchronization and modality visibility differ; an attractive fused preview is not an extra sensor or ground-truth label. |
| Tracking sequences | Where is the specified object over time, including absence if annotated? | Initialization rules, annotation cadence and absence scoring change what a score measures. |
| Before/after change masks or captions | What defined change is visible between these dates? | Two dates rarely identify when, why or through which intermediate events the change occurred. |
| Captions and question–answer records | What reference language or mapped answer accompanies the image? | Text can be templated, repeated, map-derived or generated from boxes; fluent output does not prove visual grounding. |

## Direct checks performed

The following are deliberately limited checks of public metadata or annotations. Their conclusions do not imply an image-quality audit.

- **HRSID (D02):** parsed the older public COCO JSON; counted image/annotation records, checked selected structural properties and compared file history. See its profile for the exact scope.
- **SAMPLE (D05):** compared MAT filename counts in original data-addition and current Git trees. No image arrays were inspected.
- **Anti-UAV410 (D31):** inspected annotation-directory listings and evaluation/loader code; an adjacent-looking filename pair is a concern requiring investigation, not proof of split leakage.
- **milair (D40):** counted 374 image paths and 374 XML paths in an untruncated tree; basename sets matched. XML contents were not audited.
- **RSICD (D52):** parsed 10,921 image records, 54,605 caption records and exact string repetition; image pixels and semantic correctness were not checked.
- **Public release listings (D44, D48, D49, D50 and others as indicated):** established visible files or release pointers. Incomplete pagination was not treated as a complete inventory.

For RSICD and the root file-list checks, the reproducible script and recorded results are in `research/dataset_catalogue/deep_metadata_checks.py` and `research/dataset_catalogue/evidence/deep_metadata_checks.json`. RSICD’s checked JSON SHA256 is `5e342037d469d074711676bdb9c02b6942a624530b1959d24d2734e68af9cede`. milair’s checked tree SHA is `93d91400fa5b606df32fe030c2b167a45cb9fcff`. Source URLs and locators accompany every dataset below.

## Dataset index

### SAR imagery

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D01](#d01) | FUSAR-Ship / FUSAR-Ship1.0 | A 512×512 amplitude chip labelled by its central marine object; chip, ship identity and parent scene are different units. |
| [D02](#d02) | HRSID | An 800×800 image tile with ship polygons/boxes; repository filenames also encode apparent parent-scene identifiers and crop windows. |
| [D03](#d03) | MSTAR | Depending on subcollection, an aspect-dependent target chip, a replicate physical target, or a full clutter scene. There is no verified unified chip denominator. |
| [D04](#d04) | OpenSARShip (original release) | Original paper: 11,346 SAR ship chips associated with AIS. This does not count unique vessels, parent scenes or negative backgrounds. |
| [D05](#d05) | SAMPLE | A measured observation and matched simulated counterpart. Alternative MAT/PNG representations and paired domains are not independent physical exemplars. |
| [D06](#d06) | SAR-AIRcraft-1.0 | Detection images contain multiple aircraft; recognition examples are separate crops extracted using the labelled boxes. Neither is a unique-airframe count. |
| [D07](#d07) | SARDet-100K | A standardized source image or overlapping patch, plus repeated image-local object annotations; not necessarily an independent scene or unique object. |
| [D08](#d08) | SSDD / Official SSDD | An image with ship instances; box, rotated-box and polygon labels represent different geometry for those instances, not three independent observations. |

### Overhead optical imagery

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D09](#d09) | DIOR | 23,463 RGB images, each 800×800 pixels, containing multiple objects. The original paper reports 192,472 instances; the current creator page reports 192,518. |
| [D10](#d10) | DIOR-R | The same 23,463 images used by DIOR, with oriented annotations. AOPG's dataset paragraph reports 192,518 instances, while its introduction reports 192,512; original DIOR reported 192,472. |
| [D11](#d11) | DOTA v1.0 | 2,806 variable-sized images with 188,282 annotated instances in 15 classes. Original source images are the counting unit; downstream tiles are additional representations of those images. |
| [D12](#d12) | DOTA v1.5 | The same 2,806 images and image partitions as v1.0, with denser labels and 16 categories. The current site reports 403,318 instances; the inspected paper's Table V reports 402,089. |
| [D13](#d13) | DOTA v2.0 | 11,268 source images containing 1,793,658 instances in 18 categories, including airport and helipad. Counts include earlier-version material and additional images, not an entirely independent second corpus. |
| [D14](#d14) | FAIR1M (original paper release) | 15,266 images and approximately 1.02 million annotated instances, organized into 37 fine categories under five broad groups. This is an image-and-instance detection collection, not a set of independent object identities. |
| [D15](#d15) | FGSC-23 | 4,052 object-centred image chips across 23 categories: 22 ship categories and one ship-like non-ship category. The paper reports class imbalance, with class 11 containing only 27 examples. |
| [D16](#d16) | FGSD | 2,612 selected labelled images, each 930×930 pixels, drawn from 4,736 collected pictures. The paper counts 5,634 ships and separately 1,366 docks; neither number is the image count. |
| [D17](#d17) | HRSC2016 | The original paper reports 1,061 labelled images with 2,976 ships, plus 610 separate unannotated images. Of labelled images, 70 contain sea-only backgrounds and 991 sea-land backgrounds; both groups contain ships. |
| [D18](#d18) | MAR20 | The creator reports 3,842 images containing 22,341 aircraft instances across 20 types. The distinction between images and objects is explicit; these totals do not enumerate unique physical aircraft. |
| [D19](#d19) | MTARSI (original 2019 deposit) | 9,385 single-aircraft chips in 20 categories, described as manually expanded. Each chip contains one complete aircraft; image totals are not counts of independent scenes or physical aircraft. |
| [D20](#d20) | MTARSI 2 (separate 2021 derivative) | Aircraft image chips assigned to 42 reclassified categories. The inspected deposit description does not give a verified total image count, so the original MTARSI total of 9,385 is not transferred. |
| [D21](#d21) | MVRSD | The README reports 3,000 images of 640×640 pixels with 32,626 instances, plus three additional large unlabelled images. The unlabelled images should not be counted as annotated examples or verified negatives. |
| [D22](#d22) | RarePlanes | The paper distinguishes 253 real scenes, 112 locations, 14,707 real aircraft and 629,551 synthetic annotations across 50,000 renders. Tiled products and source scenes are different units and must remain separately counted. |
| [D23](#d23) | ShipRSImageNet (paper counts; repository currently V1.1) | The README reports 3,435 images and 17,573 instances, with 50 leaf labels across four hierarchy levels. The leaf inventory includes Dock, so '50 ship types' is an imprecise shorthand. |
| [D24](#d24) | xView (2018 detection dataset) | More than one million annotated objects in 60 categories across approximately 1,415 km² of WorldView-3 imagery. The review does not select among conflicting secondary image counts without an official manifest. |

### Visible and thermal imagery

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D25](#d25) | DroneVehicle | 28,439 RGB/infrared pairs, or 56,878 individual images, with 953,087 modality-specific quadrilateral annotations. Boxes do not count unique physical vehicles. |
| [D26](#d26) | DSIAC ATR Algorithm Development Image Database / historical SENSIAC lead | The official 206 GB figure is archive size, not an image, frame or sequence total. A later paper's 2,595 images and eight classes describe its study subset. |
| [D27](#d27) | M3FD | The published introduction says 4,177 pairs/23,635 objects, while Table 1 and section 4 say 4,200/33,603. The current README reports 34,407 labels and an additional 300 fusion pairs. |
| [D28](#d28) | TNO Image Fusion Dataset | The reviewed official release does not establish a complete homogeneous image/sequence total. The 2017 TNO Multiband Image Collection is an umbrella of three datasets, not a countable synonym for this entry. |
| [D29](#d29) | TRICLOBS Dynamic Multiband Image Dataset | Sixteen motion scenarios at three sites occupy 4/4/8 scenario folders. Published frame counts sum to 56,865 multiband frames; this is arithmetic from Table 1, not a file count. |

### Video tracking

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D30](#d30) | Anti-UAV original / later Anti-UAV300 label | The original paper reports 318 unaligned RGB/infrared video pairs and about 585,900 box annotations. The later 'Anti-UAV300' label is a release name, not the exact original count. |
| [D31](#d31) | Anti-UAV410 | The README reports 410 infrared videos and over 438,000 manually annotated boxes. Directory listings contain 200/90/120 train/validation/test .txt files; these are metadata counts, not verified video counts. |
| [D32](#d32) | AntiUAV600 | Six hundred thermal sequences contain over 723,000 densely annotated frames. The paper gives approximately 337,000/56,000/330,000 frames in train/validation/test. |
| [D33](#d33) | DUT Anti-UAV | The detection subset has 10,000 images and 10,109 boxes. A separate tracking subset has twenty videos, averaging 1,240 frames. Table object totals must not be read as image counts. |
| [D34](#d34) | Military Vehicles in Low-FPS UAV Footage validation benchmark | The benchmark comprises 119 videos, 18,421 frames and 58,897 boxes. The request form states all recordings are 5 FPS; these units do not count unique vehicles across online sources. |
| [D35](#d35) | VTUAV / DUT-VTUAV | Five hundred sequences contain 1,664,549 RGB-T pairs. Manual boxes every ten frames total 326,961 across modalities; 24,464 masks occur at 1 FPS in 100 clips. |

### Infrared small spots

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D36](#d36) | IRSTD-1k | The paper describes 1,000 real 512×512 infrared images, while the current official README says 1,001. The discrepancy remains unresolved without a versioned file manifest. |
| [D37](#d37) | NUDT-SIRST | The release describes 1,327 synthetic 256×256 images. Approximately 37% contain multiple targets; image count is not target count or a count of independent real acquisitions. |
| [D38](#d38) | SIRST (often called NUAA-SIRST in later papers) | The original release contains 427 representative images and 480 target instances. One selected image per source sequence is the stated design; SIRST v2 is a separate release. |

### Web and synthetic imagery

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D39](#d39) | 15-class RGB military-vehicle collection described by TNO studies | 959 RGB images representing 15 vehicle classes. This is the reused real-image collection, not a count of the synthetic images in the later experiment. |
| [D40](#d40) | milair-dataset | 374 image paths and 374 XML paths with matching basename sets in the untruncated public tree. The README class-occurrence sum is 660, a different counting unit. |
| [D41](#d41) | Military Aircraft Detection Dataset (Kaggle v105) | Images, annotated object boxes and derived crops are distinct units. A verified current unique-image total could not be established from the inspected owner description. |
| [D42](#d42) | Military and Civilian Vehicles Classification (Mendeley v1) | 6,772 images: 6,642 positive and 130 negative, with 11,528 annotated objects according to the depositor. Object count is not image count. |
| [D43](#d43) | Military Assets Dataset (Kaggle v5) | 26,315 author-reported labelled images: 21,978 train, 2,941 validation and 1,396 test. These are split image totals, not independently verified distinct scenes. |
| [D44](#d44) | Military-Aircraft-Detection (Illia56 mirror) | The card describes 43 aircraft types; a verified unique-image or instance total is unavailable. Crop folders, annotated samples and full-image files are separate representations, not necessarily distinct observations. |
| [D45](#d45) | RGB military-target collection described by Jeong et al. (2025) | Table 2 gives 14,944 synthetic training instances, 1,267 real training instances and 514 real validation instances. These are explicitly object-instance totals, not image totals. |

### Camouflage segmentation

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D46](#d46) | CAMO | The paper distinguishes CAMO: 1,250 camouflage-positive images, from CAMO-COCO: those 1,250 plus 1,250 COCO negatives, totalling 2,500. The earlier catalogue used the combined count under CAMO. |
| [D47](#d47) | COD10K | 10,000 total images with a 6,000/4,000 train/test split. The main camouflage segmentation evaluation uses 2,026 camouflage-positive test images, not all 4,000 test images. |

### Scene, change and language

| ID | Dataset / release | Sample unit and accounting |
|---|---|---|
| [D48](#d48) | FSAR-Cap | 14,480 source images and 72,400 caption associations: five descriptions per image. Images derive from FAIR-CSAR and are not a new independent sensor acquisition. |
| [D49](#d49) | Functional Map of the World (fMoW) | The headline exceeds one million images, but temporal sites and paired pansharpened/multispectral products are distinct units. Reported unique boxes are 83,412 train, 14,241 validation, 16,948 test and 18,115 seq. |
| [D50](#d50) | LEVIR-CC | 10,077 before/after image pairs and 50,385 caption records, five per pair. Published counts separate 5,038 changed and 5,039 no-change pairs; multiple captions are not independent visual observations. |
| [D51](#d51) | LEVIR-CD (original release) | 637 original 1024×1024 image pairs at 0.5 m/pixel, with 31,333 changed-building instances according to the creator. Later 256×256 tiles are derivatives of these original pairs. |
| [D52](#d52) | RSICD | Verified 10,921 image records with 10,921 distinct filenames and 54,605 sentence records, exactly five per image. Five records do not imply five distinct texts. |
| [D53](#d53) | RSVQA-HR | 10,659 image patches and 1,066,316 question–answer pairs from 161 source tiles. Many questions reuse each patch. |
| [D54](#d54) | RSVQA-LR | 772 image patches and 77,232 question–answer pairs from nine source tiles. The QA total does not represent 77,232 independent visual scenes. |
| [D55](#d55) | SARChat-2M / SARChat-Bench | 2,063,548 dialogue samples: 1,836,912 training and 226,636 test. They reuse SARDet-100K imagery and labels rather than introducing two million independently acquired images. |
| [D56](#d56) | xBD | 22,068 pre/post images across 19 disasters; 850,736 polygon annotations. The damage-class counts sum to 425,368, consistent with pre/post representation, so 850,736 must not be called unique buildings. |

## Individual reviews

<a id="d01"></a>

### D01 · FUSAR-Ship / FUSAR-Ship1.0

**Evidence inspected.** Read primary full paper Sections 2–5, Tables 2/4/5, Figure 15, supplement Table S1, and current journal release/use guide. Findings are author-reported unless explicitly described as arithmetic or document comparison.

**What a sample represents.** A 512×512 amplitude chip labelled by its central marine object; chip, ship identity and parent scene are different units.

**Collection and selection.** The authors processed 126 Gaofen-3 scenes using sea/land separation, candidate extraction and SAR/AIS matching. This selects observations through an annotation pipeline rather than an exhaustive census.

**Labels and negatives.** AIS and associated vessel-type information supply ship labels; difficult dense nearshore matches require manual correction. Section 5 admits residual category errors and chips containing several ship types but labelled only by the central ship. Six explicitly constructed non-ship categories include strong false alarms, bridges/coastlines, coastal land/islands, wave clutter, ordinary sea and land.

**Partitions and independence.** Section 5 reports a random 70/30 division and four randomly selected scene demonstrations; it does not establish a parent-scene or vessel-disjoint test. Multiple observations can share scenes, vessels and background. Four demonstration scenes are not documented as independent of the chip pool.

**Quality evidence.** Authors describe manual correction and consistent crop/box conventions, but acknowledge registration errors. Independent label-accuracy measurement was not performed here.

**What evaluation means.** The reported preliminary experiment groups samples into eight categories, including false alarms; it is not evaluation across every node of the 15/98-category hierarchy.

**Interpretation.** The release combines informative AIS-linked labels with documented selection and label ambiguity. Current portal totals should remain release-specific; the smaller paper population must not be silently substituted.

**New findings in this review:**

- Primary Section 4.2 says 10,125 chips; Figure 15 and the current portal say 16,144. Table 2 also contains the smaller experimental population. No explicit version mapping reconciles them.
- Central-object-only labels and AIS mismatches are acknowledged by the authors, not merely hypothetical audit concerns.

**Still unresolved:**

- Relationship between the 10,125-chip paper population and 16,144-chip release.
- Per-class correction/error rates; vessel- and scene-disjoint partitions.

**Sources and exact evidence:**

- [Primary FUSAR full paper](https://scis.scichina.com/en/2020/140303.pdf) — Sections 2–5; pp. 3–6, 8–16; Tables 2,4,5; Figure 15. Describes candidate/AIS label generation, manual correction, negative categories, smaller population, random split, and central-ship/misregistration limitations.
- [Current journal FUSAR release](https://radars.ac.cn/web/data/getData?dataType=FUSAR) — FUSAR-Ship1.0 description and chip-category totals. Reports 16,144 chips including 6,252 AIS-matched ship chips; contrasts with primary paper Section 4.2.
- [Primary supplementary material](https://static-content.springer.com/esm/art%3A10.1007%2Fs11432-019-2772-5/MediaObjects/11432_2019_2772_MOESM1_ESM.pdf) — Table S1. Identifies specific demonstration acquisitions; does not supply a full scene-disjoint partition manifest.

<a id="d02"></a>

### D02 · HRSID

**Evidence inspected.** Read official README and commit histories; independently parsed the single checked-in COCO annotation JSON in memory. No imagery/archive downloaded. Original paper full text was unavailable from IEEE; paper-release claims remain distinct.

**What a sample represents.** An 800×800 image tile with ship polygons/boxes; repository filenames also encode apparent parent-scene identifiers and crop windows.

**Collection and selection.** The README describes varied high-resolution SAR sources. The inspected JSON contains 136 distinct filename prefixes, consistent with multiple tiles per source; prefix interpretation is metadata evidence, not verified geolocation.

**Labels and negatives.** Independently checked schema includes image_id, category_id/name, polygon segmentation, area, bbox and iscrowd; every listed category is ship. The inspected file has 215 image records without annotations. These are annotation-empty records, not independently confirmed ship-free scenes. The README separately offers 400 background images.

**Partitions and independence.** The file named train2017.json contains 3,573 images and 9,870 annotations. Its only recorded upload is 24 November 2019, preceding 2020 README/download updates. It is not the published 3,642-image derivative training partition. Only one annotation partition is checked into this repository. Cross-split parent-scene overlap cannot be tested; 136 prefixes within training do not prove leakage.

**Quality evidence.** Checks found unique annotation IDs, positive box dimensions and iscrowd=0 throughout. These structural checks do not establish polygon accuracy, label completeness or image validity.

**What evaluation means.** Detection and segmentation assess different geometry. The published 5,604/16,951 release totals cannot be validated by treating this older training file as the complete dataset.

**Interpretation.** HRSID documentation supports a useful distinction between published dataset totals, linked packages and an older repository artifact. Structural validity should not be described as a full annotation-quality audit.

**New findings in this review:**

- The old checked-in annotation file and linked release are materially different documented artifacts.
- 215 annotation-empty records qualify any blanket claim that the repository contains only positive tiles.
- The 16,951 versus SARDet's 16,969 instance difference remains unresolved; the older JSON does not explain it.

**Still unresolved:**

- Exact correspondence between old JSON and current download packages.
- Original annotation adjudication and source-scene partition rules.

**Sources and exact evidence:**

- [Official HRSID annotation file](https://raw.githubusercontent.com/chaozhong2010/HRSID/master/annotations/train2017.json) — Top-level categories/images/annotations; independently counted on 2026-11-10. 3,573 images, 9,870 annotations, 215 unreferenced image IDs, 136 filename prefixes; polygons, boxes and structural checks.
- [Annotation-file commit history](https://api.github.com/repos/chaozhong2010/HRSID/commits?path=annotations/train2017.json&per_page=5) — Commit e098068b9e7d5391f5392ea2d109ca33049f9d88. Only listed annotation upload dated 2019-11-24.
- [Official HRSID README](https://github.com/chaozhong2010/HRSID) — Dataset statistics, download versions and supplementary background images. 5,604/16,951 headline release; distinct JPG/PNG and background packages.
- [README history](https://api.github.com/repos/chaozhong2010/HRSID/commits?path=README.md&per_page=5) — July 2020 updates. Later updates include changed dataset download links; repository annotation upload predates them.

<a id="d03"></a>

### D03 · MSTAR

**Evidence inspected.** Read official archive overview, public targets, clutter, T-72 variants, mixed targets and conversion-tool descriptions; reread SAMPLE Sections 1/2.1/2.3 for documented use of original collection records.

**What a sample represents.** Depending on subcollection, an aspect-dependent target chip, a replicate physical target, or a full clutter scene. There is no verified unified chip denominator.

**Collection and selection.** Official pages describe separate 1995/1996 collections, multiple scenes and STARLOS/Sandia acquisition conditions. The variant and mixed-target collections span a broader condition set than the initial public-target page.

**Labels and negatives.** Known collection targets and replicate identities provide labels; SAMPLE describes historical photographs, configuration notes and image-header metadata. This is curated collection truth, not evidence of independently adjudicated labels in every redistributed chip package. The official archive includes 100 separate rural/urban clutter scenes. Their existence does not establish that a particular ten-class classification subset includes negatives or exhaustive detection annotations.

**Partitions and independence.** Official sections group data by collection, scene and acquisition condition; they do not define one universal train/test partition. A paper's subset protocol cannot be substituted for archive-level documentation. Different views can share the same physical target, scene and conditions. SAMPLE explicitly notes shared operating conditions as a limitation of MSTAR-derived evaluations.

**Quality evidence.** Collection provenance and known target configurations are documented. Archive-wide duplicate, missing-file and label-error checks were not performed.

**What evaluation means.** Closed-label chip classification measures discrimination among selected historical exemplars. It does not by itself measure background rejection, unseen-identity recognition or full-scene detection.

**Interpretation.** MSTAR should be described as an archive family with protocol-dependent subsets. Reporting target-type, physical-exemplar and image counts separately is necessary to interpret published results.

**New findings in this review:**

- Variant/mixed-target pages directly demonstrate collection and scene heterogeneity omitted by a single ten-class summary.
- SLICY is a known engineering reflector target, not an additional ordinary vehicle class.
- The program name alone does not establish motion tracks or temporal ground truth.

**Still unresolved:**

- Complete manifest and annotation completeness for each public subcollection.
- Which replicate identities and source scenes overlap within any specific published split.

**Sources and exact evidence:**

- [Official MSTAR archive overview](https://www.sdms.afrl.af.mil/index.php?collection=mstar) — September 1995 and November 1996 collection descriptions. Different target-type and physical-target populations; no single chip total.
- [Official public targets](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=targets) — Target table and SLICY paragraph. Replicate identities and engineered reflector purpose.
- [Official variant collection](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=variants) — Collection #2, Scenes 1–3. Variant collection has multiple scenes/acquisition conditions.
- [Official mixed-target collection](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=mixed) — Collection #1 Scene 1; Collection #2 Scenes 1–3. Mixed-target scope differs from the initial public-target subset.
- [Official clutter collection](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=clutter) — Clutter table. 100 rural/urban full scenes, separate from classification chip lists.
- [SAMPLE author manuscript](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/sample_public.pdf) — Sections 1,2.1,2.3. Historical photographs/notes/metadata and shared-operating-condition limitation.

<a id="d04"></a>

### D04 · OpenSARShip (original release)

**Evidence inspected.** Read original and 2.0 author abstracts through OpenAlex indexing, current SJTU project/detail/download pages, FUSAR's comparison paragraph and the secondary EasySAR reader README. Original full methods text was not recovered.

**What a sample represents.** Original paper: 11,346 SAR ship chips associated with AIS. This does not count unique vessels, parent scenes or negative backgrounds.

**Collection and selection.** Original abstract establishes Sentinel-1/AIS integration. FUSAR's later comparison reports 41 Sentinel-1 scenes, five Asian ports and concentrated ship-type populations; these details are secondary, not independently reconstructed.

**Labels and negatives.** AIS-associated information supplies reported type/metadata. Original matching, manual review and exclusion procedures remain unverified. The later 2.0 abstract explicitly adds interference labels and type levels. An interference-labelled chip is not necessarily a ship-free negative. Neither accessible abstract provides a count or exhaustive policy for empty/background scenes.

**Partitions and independence.** No authoritative original split manifest was inspected. Image count alone cannot establish vessel-, acquisition- or port-disjoint evaluation. Repeated acquisitions and alternative patch representations can inflate apparent sample diversity; exact identity linkage and duplication could not be checked.

**Quality evidence.** Author claims of reliability were not reproduced. The EasySAR tool README identifies Ship.xml, Metedata.xml and several patch representations, but is secondary documentation rather than the original schema specification.

**What evaluation means.** The original paper describes ship interpretation and imagery-quality assessment. The 2.0 abstract illustrates geometric-parameter extraction. These are different questions from open-scene detection with measured false alarms.

**Interpretation.** Original and expanded releases require separate catalogue identities. Current portal text is insufficient to infer the original matching quality or evaluation partitions.

**New findings in this review:**

- SJTU currently reports 34,528 chips; the 2.0 author abstract reports exactly 34,528. This resolves the count as an expanded version, not a correction to original 11,346.
- Version 2.0 explicitly adds interference labelling and type levels, so its labels cannot be assumed identical to the original.
- Download suffixes _1/_2 are not proven publication-version identifiers.

**Still unresolved:**

- Original full annotation/matching method and exact XML semantics.
- Per-version negative policy, unique-vessel counts and partition independence.

**Sources and exact evidence:**

- [Original author abstract, indexed retrieval](https://api.openalex.org/works/https://doi.org/10.1109/JSTARS.2017.2755672) — abstract_inverted_index; original DOI 10.1109/JSTARS.2017.2755672. 11,346 AIS-integrated chips and imagery-quality/interpretation purpose; secondary retrieval of author abstract.
- [OpenSARShip 2.0 author abstract, indexed retrieval](https://api.openalex.org/works/https://doi.org/10.1109/BIGSARDATA.2017.8124929) — Abstract. 34,528 chips; upgraded volume, interference labels and type levels.
- [SJTU OpenSAR detail page](https://opensar.sjtu.edu.cn/openSAR.html) — OpenSARShip description. Current institutional count 34,528 corroborates expanded-version abstract.
- [SJTU download page](https://opensar.sjtu.edu.cn/DataAndCodes.html) — Package links and both original/2.0 citations. Multiple package representations; suffix-to-version mapping not supplied.
- [FUSAR primary paper, secondary OpenSARShip comparison](https://scis.scichina.com/en/2020/140303.pdf) — Section 1, p.2. Reports original 41 scenes, five ports, 17 types and strong cargo concentration.
- [EasySAR reader documentation (secondary)](https://github.com/luckight/OpenSARShipFilter) — README, Run section. Names Ship.xml, Metedata.xml and Patch/Patch_Cal/Patch_RGB/Patch_Uint8; not a primary schema guarantee.

<a id="d05"></a>

### D05 · SAMPLE

**Evidence inspected.** Reread manuscript Sections 2/4.1, Tables 1/4/5 and public verify.py; independently counted MAT paths in original data-addition and current Git trees. No image arrays inspected.

**What a sample represents.** A measured observation and matched simulated counterpart. Alternative MAT/PNG representations and paired domains are not independent physical exemplars.

**Collection and selection.** Authors restrict selection to ten vehicle/serial combinations with satisfactory historical CAD models and compatible collection records. Models were manually compared with photographs/notes; simulation backgrounds were not matched to measured ground planes.

**Labels and negatives.** Known vehicle identity and measured-source metadata determine class/pair labels. Per-pair registration changes measured-image alignment; filename fields permit correspondence without reading arrays. The public release consists of labelled target chips. Background pixels within a chip are not an independently labelled clutter-only negative set.

**Partitions and independence.** Paper protocols hold out an acquisition condition, but the same small set of physical exemplars remains represented. This is not evidence of an unseen-vehicle-identity partition. Many views share one serial per category; synthetic and measured members share intended geometry. Registration and repeated representations create additional dependencies.

**Quality evidence.** Authors report repeated manual CAD checking. verify.py checks file families, metadata keys and permitted condition ranges, and can rewrite MAT metadata; its presence is not proof an untouched archive passed a read-only audit.

**What evaluation means.** Comparisons concern a narrow paired measured/simulated domain and closed class list. Better matching does not establish physical fidelity for unrepresented configurations or environments.

**Interpretation.** The history narrows, but does not solve, the count mismatch. Report manuscript and public-manifest denominators separately, without inventing missing samples or treating one pair as two independent examples.

**New findings in this review:**

- The first data-addition commit, dated 27 September 2019, already has 1,345 measured and 1,345 synthetic MAT paths.
- Later listed commits modify README only. Thus later repository deletion does not explain the manuscript's 1,366-pair Table 5; discrepancy predates public upload.
- Paper explicitly distinguishes matched targets from unmatched ground/background.

**Still unresolved:**

- Why manuscript Table 5 exceeds both public Git trees by 21 pairs.
- Image-level corruption, exact alignment residuals and release-specific metadata completeness.

**Sources and exact evidence:**

- [Primary SAMPLE manuscript](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/sample_public.pdf) — Sections 2.1–2.3,4.1; Tables 1,4,5; pp.3–5,8–9. Fixed serial selection, manual model checking, alignment, unmatched ground planes and paper count.
- [Original public data tree](https://api.github.com/repos/benjaminlewis-afrl/SAMPLE_dataset_public/git/trees/bc3a10cbef849440413d4b87b9eeb98187575763?recursive=1) — Untruncated MAT path inventory. Independent count: 1,345 real and 1,345 synth files already in initial data upload.
- [Current public data tree](https://api.github.com/repos/benjaminlewis-afrl/SAMPLE_dataset_public/git/trees/1bae4156afcba7ad9c9f2eb743ed20675ed14fb1?recursive=1) — Untruncated MAT path inventory. Current counts match original public upload.
- [Official commit history](https://api.github.com/repos/benjaminlewis-afrl/SAMPLE_dataset_public/commits?per_page=50) — September 2019 data addition and subsequent README commits. No later data-changing commit appears in the returned complete short history.
- [Official verify.py](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/verify.py) — Target-key handling and assertions. Script validates composition/ranges and may rewrite metadata; reviewed, not executed.

<a id="d06"></a>

### D06 · SAR-AIRcraft-1.0

**Evidence inspected.** Retrieved primary full HTML through the journal page's own read endpoint; read Sections 2.1/2.2,4.1–4.3 and Tables 1/3. No dataset package or model code executed.

**What a sample represents.** Detection images contain multiple aircraft; recognition examples are separate crops extracted using the labelled boxes. Neither is a unique-airframe count.

**Collection and selection.** Section 2.1 specifies 1 m, single-polarization Gaofen-3 spotlight imagery selected primarily from three named civil airports across multiple times, with four image sizes.

**Labels and negatives.** Section 2.2 explicitly describes horizontal Pascal VOC XML boxes: image size, aircraft name and xmin/ymin/xmax/ymax. This resolves the previous schema uncertainty; the described release schema is not a scattering-keypoint annotation specification. The paper describes background facilities and false detections but does not enumerate aircraft-free images or an exhaustive negative-selection rule.

**Partitions and independence.** Section 2.2 reports 7:1:2 training/validation/test image division. Section 4.2 separately reports 13,513/2,950 cropped-instance recognition partitions. The previous object-count table must not stand in for image split counts. The paper reports multiple times/viewpoints, primarily at three named airports, but does not establish airport-, date- or airframe-disjoint splitting.

**Quality evidence.** The source describes representation and labelled examples, but gives no verified annotator agreement/error rate in reviewed sections. No independent label checks were performed.

**What evaluation means.** Detection, crop recognition accuracy and joint type-plus-localization evaluation are distinct. Recognition results assume ground-truth cropping; they do not include the preceding localization failure rate.

**Interpretation.** This is a geographically concentrated civil-type image benchmark with separate evaluation units. Published crop recognition and detection scores cannot be interpreted as one interchangeable measure.

**New findings in this review:**

- Full methods resolve primary sensor/mode, civil-airport scope, XML schema and validation-split existence.
- Table 3 belongs specifically to box-cropped recognition, explaining why its units differ from the 7:1:2 image protocol.
- Other denotes aircraft outside the six named classes, not a background class.

**Still unresolved:**

- Exact image manifests and assignment by airport/date/parent acquisition.
- Annotator process, uncertain-type handling and aircraft-free image counts.

**Sources and exact evidence:**

- [Primary SAR-AIRcraft full article](https://radars.ac.cn/article/doi/10.12000/JR23043?viewType=HTML) — Sections 2.1,2.2,4.1–4.3; Table 3. Three civil airports/multiple times; Gaofen-3 spotlight; VOC XML; 7:1:2 image split; box-cropped recognition counts and metrics.
- [Journal full-text read endpoint](https://radars.ac.cn/article/htmlContent) — Read-only POST id=17f21be5-c367-42c8-9e32-d7a01e667aba,pageType=cn. Returned htmlContent successfully; source of full methods text absent from initial page HTML.
- [SARDet current paper](https://arxiv.org/html/2403.06534v3) — Table 1 and Appendix A.2. SAR-AIRcraft derivative uses overlapping patches, explaining why aggregate counts are not original image/instance counts.

<a id="d07"></a>

### D07 · SARDet-100K

**Evidence inspected.** Read paper Tables 1/2 and Appendix A.2, official README, dataset parser SAR_Det.py and base SARDet_100k configuration. Code was inspected statically, not run.

**What a sample represents.** A standardized source image or overlapping patch, plus repeated image-local object annotations; not necessarily an independent scene or unique object.

**Collection and selection.** Ten existing datasets are assembled. Larger images from three sources are cropped with overlap; existing partitions are retained where available, otherwise image partitions are created.

**Labels and negatives.** Annotation formats are converted to COCO and broad categories reconciled. The described standardization is not a documented reannotation of every image for every category. The inspected base training configuration enables empty-ground-truth filtering. The parser preserves test-mode image records; therefore raw image totals do not automatically equal the images admitted during training.

**Partitions and independence.** Paper reports three partitions. Final base-config assignments reference separate val.json and test.json, although README still contradicts itself about test-download availability. Configuration paths do not prove those files are publicly downloadable. Overlap can repeat one object across patches; aggregate data also overlap constituent benchmarks. Source-scene leakage and cross-category annotation completeness were not independently tested.

**Quality evidence.** Parser asserts unique annotation IDs and excludes ignored, nonintersecting, nonpositive-area/tiny or out-of-category annotations. Structural filtering is not verification of class correctness or exhaustive labels.

**What evaluation means.** The inspected configuration uses COCO bounding-box metrics, including classwise test output. Optional mask fields in the parser do not make those reported results segmentation evaluations.

**Interpretation.** The benchmark standardizes representation and reporting, while inheriting heterogeneous annotation and sampling assumptions. Its size is a patch/annotation denominator, not a new independent acquisition population.

**New findings in this review:**

- Static code establishes negative-image and invalid-annotation handling beyond the paper's headline counts.
- The final test configuration is distinct from validation; an earlier alias is overwritten and should not be misread as the final setting.
- Current parser/config provide no explanation for the HRSID 18-instance or SSDD 131-instance count differences.

**Still unresolved:**

- Public test-package status and source-to-derived annotation provenance.
- Deduplication, parent-scene partitioning and complete six-category coverage per image.

**Sources and exact evidence:**

- [Primary SARDet paper](https://arxiv.org/html/2403.06534v3) — Tables 1–2; Appendix A.2. Ten-source construction, source counts, overlapping crops and partition policy.
- [Official dataset parser](https://raw.githubusercontent.com/zcablii/SARDet_100K/main/MSFA/msfa/datasets/SAR_Det.py) — load_data_list, parse_data_info, filter_data. Unique-ID assertion, annotation exclusions, optional masks and test-mode filtering behavior.
- [Official base dataset configuration](https://raw.githubusercontent.com/zcablii/SARDet_100K/main/MSFA/configs/_base_/datasets/SARDet_100k.py) — train_dataloader filter_cfg; final val/test dataloaders and evaluators. Empty-ground-truth training filter, separate final test path, bbox metrics.
- [Official README](https://github.com/zcablii/SARDet_100K) — Dataset download section and source-statistics table. Conflicting test-release text and unresolved derivative counts.

<a id="d08"></a>

### D08 · SSDD / Official SSDD

**Evidence inspected.** Read primary 2021 paper Sections 1.4,3.1–3.3,4,6.1–6.3, Table 6/7 and test-set descriptions; compared SARDet's derivative statistics. No archive annotation files inspected.

**What a sample represents.** An image with ship instances; box, rotated-box and polygon labels represent different geometry for those instances, not three independent observations.

**Collection and selection.** The official release revisits heterogeneous multi-sensor imagery and corrects the initial annotation version. It is not described as a fresh independent sensor campaign.

**Labels and negatives.** The paper describes drawing polygons with LabelMe and deriving horizontal and minimum-area rotated boxes from polygon outlines. This establishes the documented geometric relationship; released annotation variants were not compared file by file. The paper describes three stored image channels repeating one grayscale channel, not three radar measurements. Polygon masks define background outside ships. That does not establish an enumerated, independently verified ship-free image subset; no such count was found in reviewed sections.

**Partitions and independence.** Table 6 fixes 928 training and 232 test images using final filename digits; no unique validation set is supplied. The 232 test images comprise 46 inshore and 186 offshore images. A deterministic filename split improves repeatability but does not establish parent-scene, acquisition-date or vessel independence. Derived annotation types are correlated.

**Quality evidence.** Authors identify and correct missing/false labels and loose boxes. They do not report an independently reproduced post-correction error rate here.

**What evaluation means.** Inshore means the image contains land, not proof a particular ship is moored. Section 6.3 defines size using label-type-specific pixel-area thresholds; this is not a uniform physical vessel-size classification.

**Interpretation.** Version, geometric annotation task and partition must accompany reported numbers. Three-channel storage, multiple label types and repeated crops should not be counted as added sensor diversity or independent data.

**New findings in this review:**

- Primary full text resolves exact official split and confirms absent unique validation set.
- Inshore/offshore is image-context labelling; size definitions vary between box, rotated-box and polygon tasks.
- Original 2,456 versus SARDet 2,587 remains unresolved: paper discusses corrections, but the reviewed text does not provide a 131-instance reconciliation ledger.

**Still unresolved:**

- Exact corrected object inventory and provenance of the 131-instance difference.
- Negative-only inventory, annotator agreement and acquisition-disjoint split evidence.

**Sources and exact evidence:**

- [Primary official SSDD paper](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-13-03690/article_deploy/remotesensing-13-03690.pdf) — Sections 1.4,3.1–3.3,4,6.1–6.3; pp.6,15–18,27–29; Tables 6–7. Correction motivation, grayscale replication, LabelMe polygons/derived boxes, fixed 928/232 split, land-containing definition and task-specific size bins.
- [Official SSDD repository](https://github.com/TianwenZhang0825/Official-SSDD) — 2021 release citation and download links. Identifies the revised official release; repository does not contain a reviewed annotation-difference ledger.
- [SARDet primary aggregate paper](https://arxiv.org/html/2403.06534v3) — Table 1; Appendix A.2. Derivative SSDD contribution: 1,160 images/2,587 annotations and separate three-way partition context.

<a id="d09"></a>

### D09 · DIOR

**Evidence inspected.** Independently read the original paper's dataset and evaluation sections and compared its totals with the current creator page. Collection and annotation procedures below are author-reported; no image archive or annotation sample was audited.

**What a sample represents.** 23,463 RGB images, each 800×800 pixels, containing multiple objects. The original paper reports 192,472 instances; the current creator page reports 192,518.

**Collection and selection.** Earth-observation interpretation experts selected Google Earth imagery from more than 80 countries, deliberately varying weather, season, quality, scale and appearance. Reported spatial resolution is 0.5–30 m. This is curated coverage, not probability sampling of geography.

**Labels and negatives.** Annotators manually drew horizontal boxes with LabelMe for 20 broad categories. Class selection combined categories shared by earlier benchmarks with literature and application considerations. Ships and vehicles dominate instance counts; the ontology mixes objects and larger facilities. The reviewed construction section does not establish a separately enumerated negative-only image set or an exhaustive background sampling rule. Unannotated pixels should not be treated as independently verified absence of every object type.

**Partitions and independence.** The paper reports random image-level splits: 5,862 training, 5,863 validation and 11,738 test images. Train plus validation is 11,725. The stated goal is similar distributions; no location, capture-date or physical-object holdout is established. Multiple categories can coexist in one image, so per-category image counts cannot be added into unique-image totals. Google Earth source-scene overlap and repeated observations were not audited.

**Quality evidence.** Expert collection and manual annotation are documented. The reviewed sections do not specify an independent second-pass audit, inter-annotator agreement or measured annotation-error rate.

**What evaluation means.** Paper AP/mAP evaluates class-labelled horizontal detections with more than 50% box overlap. It measures the chosen categories and geometry, not fine aircraft/ship subtype recognition.

**Interpretation.** DIOR is a broad detection benchmark with deliberately diverse imagery. Its published scale is credible as an author-reported release description; geographic diversity alone does not establish independent evaluation.

**New findings in this review:**

- Recovered exact original split counts.
- Identified the 46-instance difference between original-paper and current-page totals.

**Still unresolved:**

- Release manifest explaining the instance-count change.
- Negative-only coverage and location-level split correspondence.

**Sources and exact evidence:**

- [Original DIOR paper](https://arxiv.org/pdf/1909.00133) — §4.1–4.2 and §5.1; PDF pp.10–13. Reports collection, LabelMe horizontal boxes, 23,463 images, 192,472 instances and random image split counts.
- [Creator dataset page](https://gcheng-nwpu.github.io/) — DIOR dataset section. Current page gives 192,518 instances and CC BY-NC 4.0 research-use terms.

<a id="d10"></a>

### D10 · DIOR-R

**Evidence inspected.** Independently read the AOPG paper's DIOR-R description and compared it with the creator page and original DIOR paper. This is a documentation review, not verification of released files.

**What a sample represents.** The same 23,463 images used by DIOR, with oriented annotations. AOPG's dataset paragraph reports 192,518 instances, while its introduction reports 192,512; original DIOR reported 192,472.

**Collection and selection.** The paper explicitly reuses DIOR imagery rather than describing a newly acquired image collection. Its Google Earth provenance and deliberately varied scenes therefore derive from DIOR; oriented relabelling does not add independent scenes.

**Labels and negatives.** Authors say they annotate oriented bounding boxes for every instance across the same 20 broad classes. The inspected DIOR-R paragraph does not provide an annotator workforce, calibration procedure, adjudication rule or detailed difficult-object policy. No separate negative-image collection or revised background-coverage rule is established. Existing DIOR image content is inherited, but identical object inclusion cannot be assumed given the conflicting instance totals.

**Partitions and independence.** AOPG reports using the trainval set for training and the test set for evaluation. The paper establishes image reuse; an independently checked mapping of DIOR-R release filenames to DIOR's original splits was not obtained. DIOR and DIOR-R substantially share observations by construction. They must not be counted as independent image corpora, nor does an image-level split prove location or object identity separation.

**Quality evidence.** The existence and intended oriented geometry are confirmed by both paper and creator documentation. Neither establishes a measured annotation error rate. Added orientation is not itself evidence of improved category correctness.

**What evaluation means.** The benchmark tests oriented object localisation and broad-category classification. Horizontal DIOR results and oriented DIOR-R results have different geometric matching conditions and are not interchangeable measurements.

**Interpretation.** Treat DIOR-R as an annotation variant with useful orientation information and inherited sampling limitations. Attach the exact release and annotation task to any reported result.

**New findings in this review:**

- The primary paper itself contains two DIOR-R totals, 192,512 and 192,518.
- The exact same-image relationship is explicit in the dataset paragraph.

**Still unresolved:**

- Canonical instance count and released split mapping.
- Oriented-box checking process and ambiguous-object conventions.

**Sources and exact evidence:**

- [Anchor-Free Oriented Proposal Generator for Object Detection](https://arxiv.org/html/2110.01931) — Introduction; Experiments, Datasets paragraph; Results on DIOR-R. Introduction gives 192,512; dataset paragraph gives 192,518 and explicitly states shared DIOR images and oriented relabelling.
- [DIOR and DIOR-R creator page](https://gcheng-nwpu.github.io/) — DIOR-R section. Describes oriented boxes and points to the AOPG paper and downloads.

<a id="d11"></a>

### D11 · DOTA v1.0

**Evidence inspected.** Independently checked current creator documentation and the later comprehensive DOTA paper, whose version tables identify v1.0. Annotation procedures are the authors' retrospective account, not an external audit of the 2018 archive.

**What a sample represents.** 2,806 variable-sized images with 188,282 annotated instances in 15 classes. Original source images are the counting unit; downstream tiles are additional representations of those images.

**Collection and selection.** The later source table assigns the shared v1.0/v1.5 images to 2,375 Google Earth and 431 GF/JL images. It gives no aerial/CycloMedia images for this set; the current generic source list should not be applied retroactively.

**Labels and negatives.** Oriented quadrilaterals carry category and difficult flags. The common pipeline uses expert examples to train volunteers; initial labels from the plain group are checked by senior volunteers and authors. Failed images return for correction. The paper describes Google Earth collection as foreground-rich. It acknowledges tiny missed objects and subsequently adds sub-10-pixel instances in v1.5. Thus unlabelled small objects in v1.0 are not necessarily true negatives.

**Partitions and independence.** Authors and creator page report approximately one-half training, one-sixth validation and one-third test. Version tables give 98,990, 28,853 and 60,439 instances, respectively. Geographic, temporal and physical-object disjointness is not established by these proportions. v1.5 reuses these images and v2.0 contains earlier material. Version totals cannot be summed as independent scenes. Tiling may create correlated observations; the archive was not audited for duplicates.

**Quality evidence.** Repeated review is documented, but the statement that missed objects are negligible is an author claim without an independent error estimate in the inspected material.

**What evaluation means.** Horizontal-box and oriented-box detection are separate tasks. The comprehensive paper specifies VOC2007 mAP; quadrilateral overlap changes the localisation criterion. Generic plane and ship labels do not encode fine subtypes.

**Interpretation.** Use v1.0 as a historically specific annotation release. Its count, geometry and coverage policy must travel together when interpreting benchmark results.

**New findings in this review:**

- Corrected the earlier attribution of CycloMedia imagery to v1.0.
- Established that later tiny-object coverage changes the meaning of unlabelled background.

**Still unresolved:**

- Exact source-scene and split overlap.
- Version-specific annotation omissions and archive fidelity.

**Sources and exact evidence:**

- [DOTA comprehensive benchmark paper](https://arxiv.org/html/2102.12219) — §III; §IV-A/Table III; §IV-G/Table V; §V-A. Documents annotation review, sources of shared earlier images, version totals and separate HBB/OBB evaluation.
- [Official DOTA dataset specification](https://captain-whu.github.io/DOTA/dataset.html) — Annotation format and terms. Specifies eight-coordinate quadrilaterals, class and difficult fields; academic-only/noncommercial terms.
- [Official DOTA version overview](https://captain-whu.github.io/DOTA/) — DOTA-v1.0. Confirms 2,806 images, 188,282 instances and split proportions.

<a id="d12"></a>

### D12 · DOTA v1.5

**Evidence inspected.** Independently compared the comprehensive DOTA paper's version tables with the current official page. This establishes a documentation discrepancy; no archive-level recount was performed.

**What a sample represents.** The same 2,806 images and image partitions as v1.0, with denser labels and 16 categories. The current site reports 403,318 instances; the inspected paper's Table V reports 402,089.

**Collection and selection.** No new image acquisition is claimed for v1.5. The comprehensive paper attributes these images to Google Earth and GF/JL satellites, with zero aerial/CycloMedia images in its source table.

**Labels and negatives.** The release adds extremely small instances, described as less than 10 pixels, and the container-crane category. It retains oriented quadrilateral annotations. The paper's common workflow uses expert examples, trained volunteers, senior checking and author review. Small objects omitted in v1.0 can become positives in v1.5. This directly changes annotation completeness and evaluation background; the increase in object totals should not be interpreted as more independent imagery.

**Partitions and independence.** The authors explicitly preserve v1.0 image splits. The paper gives 210,631 training, 69,565 validation and 121,893 test instances, summing to its 402,089 total, not the current site's total. This is a reannotation of v1.0 observations. Cross-version comparisons must account for label coverage and taxonomy changes, and separate versions cannot serve as independent source evidence.

**Quality evidence.** The review workflow is documented but no independent measured residual-error rate is supplied. Version-table consistency can be checked arithmetically; it cannot resolve what the current downloadable archive contains.

**What evaluation means.** Detection remains broad-category classification plus horizontal or oriented localisation under the specified task. Added tiny objects and a new class change the denominator and difficulty of reported results.

**Interpretation.** Preserve both cited totals with their versions rather than silently choosing one. v1.5 primarily deepens annotation coverage and cannot be counted as a new image collection.

**New findings in this review:**

- Table V resolves the paper's 402,089 as an overall total; its container-crane row is 237.
- Current official total differs by 1,229 instances, with no inspected change log resolving it.

**Still unresolved:**

- Manifest or correction explaining 402,089 versus 403,318.
- Location-level and date-level partition independence.

**Sources and exact evidence:**

- [DOTA comprehensive benchmark paper](https://arxiv.org/html/2102.12219) — §IV-A/Table III; §IV-G.2/Table V. Same images/splits, tiny-object addition, 237 container cranes, and 402,089 total including split arithmetic.
- [Current official DOTA overview](https://captain-whu.github.io/DOTA/) — DOTA-v1.5 section. Reports 403,318 total instances and re-use of v1.0 images.
- [Official DOTA annotation and terms](https://captain-whu.github.io/DOTA/dataset.html) — Annotation format and use terms. Quadrilateral/class/difficult annotation specification and academic/noncommercial restrictions.

<a id="d13"></a>

### D13 · DOTA v2.0

**Evidence inspected.** Independently read construction, source, version and evaluation sections of the comprehensive paper and checked official counts. Collection quality and residual annotation accuracy remain author-reported.

**What a sample represents.** 11,268 source images containing 1,793,658 instances in 18 categories, including airport and helipad. Counts include earlier-version material and additional images, not an entirely independent second corpus.

**Collection and selection.** Table III separates 10,186 Google Earth, 516 GF/JL and 566 aerial images. Google Earth selection is foreground-rich, while larger satellite/aerial images contribute more background. GF/JL panchromatic imagery is converted from 10-bit to 8-bit.

**Labels and negatives.** Experts supply examples; trained volunteers create quadrilateral labels; senior volunteers and authors check them and return failures. Plane nose, wingtips and tail guide boxes; corner order encodes heading where discernible. Ambiguous direction and tiny objects remain annotation challenges. More low-foreground imagery broadens background coverage, but the paper does not establish that all unannotated content is negative. Missed tiny objects are acknowledged, and difficult flags are part of the format.

**Partitions and independence.** Official splits are 1,830 training, 593 validation, 2,792 test-dev and 6,053 test-challenge images, with 268,627, 81,048, 353,346 and 1,090,637 instances. These independently sum to the headline totals. Mixed sensors, incomplete GSD/date metadata and inherited images limit claims about independent distribution coverage. The much larger test portion is a benchmark design choice, not a representative geographic sample.

**Quality evidence.** The review process is documented; a negligible miss proportion is an author assessment, not an independently verified error rate. GSD is available for only about 30% of images; acquisition dates are incomplete and geolocations are not released.

**What evaluation means.** The paper uses separate horizontal and oriented tasks with VOC2007 mAP and evaluates on test-dev. Hidden labels reduce direct test-label access but do not demonstrate geographic independence.

**Interpretation.** A large, well-documented broad-object benchmark whose source mixture and incomplete metadata should accompany aggregate performance claims.

**New findings in this review:**

- Source counts distinguish the aerial imagery introduced beyond the earlier versions.
- Paper-era test-image access wording differs from current challenge-specific availability.

**Still unresolved:**

- Source-scene overlap across partitions.
- Current test-challenge availability and version-specific access conditions.

**Sources and exact evidence:**

- [DOTA comprehensive benchmark paper](https://arxiv.org/html/2102.12219) — §III; §IV-A/B/G, Tables III/V; §V-A. Construction/QC, per-source counts, incomplete metadata, release relationships and evaluation semantics.
- [Official DOTA overview](https://captain-whu.github.io/DOTA/) — DOTA-v2.0 split table and download notes. Gives image and instance totals for four partitions and challenge-specific access notes.
- [Official annotation specification](https://captain-whu.github.io/DOTA/dataset.html) — Annotations and copyright. Oriented corners, difficult flag and research-use restrictions.

<a id="d14"></a>

### D14 · FAIR1M (original paper release)

**Evidence inspected.** Independently read the original paper's construction, annotation and benchmark sections. The record is tied to that release; later challenge packages were not treated as identical.

**What a sample represents.** 15,266 images and approximately 1.02 million annotated instances, organized into 37 fine categories under five broad groups. This is an image-and-instance detection collection, not a set of independent object identities.

**Collection and selection.** Authors collected Google Earth and Gaofen imagery at 0.3–0.8 m resolution over more than 100 airports, harbours and cities. Gaofen preprocessing includes cloud/noise rejection, block adjustment, orthorectification, pansharpening and hue adjustment.

**Labels and negatives.** Ordered oriented boxes encode class and direction, with occlusion or uncertain-direction information. The ontology combines named civil aircraft models with functional ship/vehicle classes, courts and roads. Other-airplane, other-ship and other-vehicle absorb unlisted types. The paper states a 16-pixel annotation threshold, but its example says ships longer than 13 m need not be labelled at 0.8 m resolution. That example is internally difficult to reconcile; no corrected rule was established. Small unlabelled objects cannot automatically be treated as verified negatives.

**Partitions and independence.** The original paper reports training/validation/test proportions of one-half, one-sixth and one-third, with test labels withheld for server evaluation. It does not establish geographic or date-disjoint selection in the inspected split description. Multitemporal and multisource imagery can cover the same region. Preprocessing alignment and broad geographic coverage do not demonstrate independent partitions.

**Quality evidence.** Authors describe paired independent reannotation and merging, supervisor checks of location/category/orientation, and expert inspection. No external error-rate or agreement audit was performed here.

**What evaluation means.** Besides ordinary AP, the paper introduces FIoU and confidence-sensitive fine-grained mAP_F, with a 0.5 FIoU threshold. These are distinct from plain IoU-based mAP and require their metric name.

**Interpretation.** Its detailed taxonomy and review procedure are documented strengths of construction, while mixed category granularity and metric differences limit simple cross-dataset comparisons.

**New findings in this review:**

- Recovered original split proportions and the distinct mAP_F definition.
- Identified contradictory wording in the size-threshold example.

**Still unresolved:**

- Corrected annotation-size rule.
- Release-specific file counts, geographic split independence and dataset licence.

**Sources and exact evidence:**

- [FAIR1M primary paper](https://arxiv.org/html/2103.05569) — §3 dataset construction/annotation; §4 benchmark metrics. Source preprocessing, taxonomy, 16-pixel rule, three review stages, split proportions and FIoU/mAP_F definitions.
- [FAIR1M journal record](https://doi.org/10.1016/j.isprsjprs.2021.12.004) — Published article identity. Identifies the journal version separately from later challenge releases.

<a id="d15"></a>

### D15 · FGSC-23

**Evidence inspected.** Independently retrieved and read the publisher's full PDF, extending the earlier abstract-only review. Construction and experiment details below are author-reported; neither the chip archive nor individual labels were inspected.

**What a sample represents.** 4,052 object-centred image chips across 23 categories: 22 ship categories and one ship-like non-ship category. The paper reports class imbalance, with class 11 containing only 27 examples.

**Collection and selection.** Sources are Google Earth and GF-2 panchromatic imagery at 0.4–2 m resolution; approximately 1,600 chips explicitly derive from HRSC2016. Crops align the object centre with the image centre and include panchromatic and composite-colour appearances.

**Labels and negatives.** Humans assign chip categories plus integer aspect ratio in the range 1–13 and axis angle from 0–180 degrees. Attributes are encoded in filenames. This angle represents undirected axial orientation, not a complete directed bow heading. The negative category contains non-ship objects resembling ships. It provides a specific confusion class, not evidence of systematic sampling across all background conditions or full-scene false-positive behaviour.

**Partitions and independence.** The experiment randomly selects 20% within each category for testing, except class 11, where 10 examples are test and 17 training. The paper describes augmentation of the training subset after this split. Source-image or physical-ship grouping is not established. HRSC2016 reuse is explicitly documented. Multiple chips may share source imagery or vessel identity; a random chip split does not resolve this relationship.

**Quality evidence.** The paper documents human labels and attribute conventions, but the reviewed construction section does not describe independent adjudication, agreement statistics or a measured error rate.

**What evaluation means.** Per-class accuracy, overall accuracy and confusion matrices evaluate classification of centred chips. Overall accuracy reflects the imbalanced class frequencies. The special small-class split makes a blanket 80/20 description incomplete.

**Interpretation.** FGSC-23 has more verifiable methodological detail than its abstract alone conveyed. Its negative category and shape attributes should be interpreted within a cropped classification task.

**New findings in this review:**

- Established approximately 1,600-chip HRSC2016 dependency.
- Recovered the smallest-class split exception, filename attributes and non-profit academic-use restriction.

**Still unresolved:**

- Source-chip manifest and duplicate/identity correspondence.
- Complete label-name mapping and independent annotation audit.

**Sources and exact evidence:**

- [FGSC-23 full publisher paper](https://www.cjig.cn/zh/article/doi/10.11834/jig.200261/) — Linked full PDF: §1, p.2339; §2, p.2340; §3, pp.2340–2341 (PDF pp.7–9). Reports HRSC2016-derived chips, source resolution, negative category, filename attributes, non-profit academic terms, download link, 20% test rule and class-11 exception.
- [FGSC-23 DOI](https://doi.org/10.11834/jig.200261) — Journal of Image and Graphics 26(10), 2337–2345 (2021). Establishes the original publication identity; archive accessibility was not tested.

<a id="d16"></a>

### D16 · FGSD

**Evidence inspected.** Independently read the original full paper's collection, hierarchy, annotation and baseline sections. Numerical totals and conventions are primary-source reports; no public archive or individual label was audited.

**What a sample represents.** 2,612 selected labelled images, each 930×930 pixels, drawn from 4,736 collected pictures. The paper counts 5,634 ships and separately 1,366 docks; neither number is the image count.

**Collection and selection.** Authors used current and historical Google Earth imagery from 17 ports in four countries, reporting 0.12–1.93 m resolution. They shifted and rotated map views while collecting samples and retained port ID, resolution and Google Earth layer information.

**Labels and negatives.** There are 43 ship types plus a separate dock class, with a multilevel ship hierarchy. Both horizontal and rotated boxes are supplied. Heading uses a centre-to-bow vector represented through direction signs, rather than treating a box angle alone as full ship heading. The labelled subset is selected from collected imagery; the paper does not give a negative-only image inventory or explain why every excluded picture was rejected. Dock is an explicitly labelled class, not a synonym for background.

**Partitions and independence.** Training contains 1,917 images/3,964 ships, validation 268/590 and test 427/1,080. These sum to the stated labelled totals. The inspected paper does not establish a randomization algorithm or port/date/physical-ship holdout. Map shifts, rotations and historical observations may create related views of the same place or vessel. This is a plausible dependence mechanism, not a measured duplicate rate. ShipRSImageNet explicitly reuses FGSD.

**Quality evidence.** The paper defines label geometry and metadata but does not document a staged independent annotation audit or measured error rate. Those omissions should remain unknown rather than be filled from later papers.

**What evaluation means.** Two baseline tasks predict category with horizontal or rotated boxes, reported through AP and mAP. The inspected baseline description does not pin down all matching and averaging settings, so scores require their exact protocol.

**Interpretation.** FGSD documents rich label structure but restricted port sampling. Its public paper alone does not verify a current downloadable release or independent test population.

**New findings in this review:**

- Clarified heading encoding beyond the rotated box.
- Separated collected pictures, labelled images, ships and docks.

**Still unresolved:**

- Current creator-controlled archive and dataset licence.
- Annotation adjudication, negative sampling and split independence.

**Sources and exact evidence:**

- [FGSD original paper](https://arxiv.org/html/2003.06832) — §2.1–2.3; §3 and Table 1. Collection and selected totals, split counts, 43 ship types plus docks, heading representation, metadata and AP/mAP baseline tasks.
- [ShipRSImageNet creator repository](https://github.com/zzndream/ShipRSImageNet) — Image collection/source description. Explicitly identifies FGSD as a source; corroborates reuse without establishing a standalone FGSD archive.

<a id="d17"></a>

### D17 · HRSC2016

**Evidence inspected.** Independently read the original publisher PDF, especially §2 and its partition algorithm. This resolves the original-paper count; it does not establish which later archive produced the frequently repeated 1,070 figure.

**What a sample represents.** The original paper reports 1,061 labelled images with 2,976 ships, plus 610 separate unannotated images. Of labelled images, 70 contain sea-only backgrounds and 991 sea-land backgrounds; both groups contain ships.

**Collection and selection.** Google Earth current/historical imagery was collected from six harbours at 0.4–2 m resolution. Images containing ships were saved with random rotation. Harbour, source, date, scale and approximate coordinates were recorded; the authors warn about shifted Google Earth coordinates.

**Labels and negatives.** Labels form ship/category/type levels. Uncertain leaf types fall back to the second-level category. Horizontal boxes, rotated boxes and V-shaped bow points are described. Pixel-based segmentation masks are supplied only for test images; the sea-separation evaluation uses both ground-truth sea and ship regions. Collection explicitly selects images if ships are present. Sea-only means background composition, not negative imagery. The 610 unannotated images are not documented as verified ship-free examples.

**Partitions and independence.** Original splits are 436/181/444 images and 1,207/541/1,228 ships for training/validation/test. Algorithm 1 assigns source images using randomized, hierarchy-aware class processing; this is not a harbour, date or vessel-identity holdout. Small harbour coverage and historical/rotated observations permit correlated images. The authors' 'Unbiasedness' section describes partition construction, not population-representative sampling.

**Quality evidence.** The paper acknowledges difficult subtype recognition and the cost of expert hiring. Its proposed citizen-scientist approach should not be read as proof that every original label received independent expert adjudication.

**What evaluation means.** The paper separates sea-land separation fitness from class/localisation detection evaluation. Sea separation considers sea overlap and retained ship integrity. One-class ship mAP does not measure fine ship-type accuracy.

**Interpretation.** HRSC2016 is a multi-task, hierarchical research collection. Release provenance is essential when later literature changes its count or collapses the label hierarchy.

**New findings in this review:**

- Resolved the original labelled total as 1,061, not 1,070.
- Recovered exact splits, fallback labels and the separately unannotated collection.

**Still unresolved:**

- Origin of the later 1,070-image count.
- Dataset-specific licence and current release-manifest fidelity.

**Sources and exact evidence:**

- [Original HRSC2016 paper](https://www.scitepress.org/Papers/2017/61206/61206.pdf) — §2.1–2.2/Algorithm 1, published pp.326–327; §3.1/3.3, pp.327–329. 1,061 labelled and 610 unannotated images; exact splits; positive-image collection; hierarchy fallback; mask and head-point scope; separate evaluation tasks.
- [Original publisher record](https://www.scitepress.org/Link.aspx?doi=10.5220/0006120603240331) — ICPRAM 2017, pp.324–331. Establishes paper identity; article copyright is not a dataset-image licence.

<a id="d18"></a>

### D18 · MAR20

**Evidence inspected.** Independently checked the creator's dataset description and publisher record. The journal full-text route was gated, so collection, checking and split procedures could not be established from the accessible primary material.

**What a sample represents.** The creator reports 3,842 images containing 22,341 aircraft instances across 20 types. The distinction between images and objects is explicit; these totals do not enumerate unique physical aircraft.

**Collection and selection.** Accessible documentation identifies a remote-sensing aircraft-recognition dataset but does not provide a verified complete sensor, imagery-provider, geographic or acquisition-date inventory. Sources from other datasets hosted on the same creator page must not be transferred to MAR20.

**Labels and negatives.** The creator explicitly states that instances have both horizontal and oriented bounding boxes. It does not specify, in that description, an annotator workforce, disagreement handling, unknown-type convention or object-size threshold. A negative-only image subset, rules for partly visible objects and minimum annotation size were not established. The presence of boxes does not demonstrate exhaustive annotation of all visible aircraft.

**Partitions and independence.** No exact original split counts or partition construction method were verified. Any later implementation's split should be identified as such rather than described as an audited canonical release. The absence of source-scene, date and object-identity metadata in the inspected description leaves dependence unresolved. Large object counts do not establish independent observations.

**Quality evidence.** The source supports the existence of dual annotation geometry and the reported totals. It does not substantiate an independent error rate, expert consensus or geographic coverage audit.

**What evaluation means.** The labels concern aircraft type and localisation. Horizontal and oriented detections need distinct geometry-aware interpretation; the accessible evidence does not justify reproducing a specific scoring protocol.

**Interpretation.** MAR20 is a creator-documented detection asset with specific annotation and licence statements, but its deeper methodological evidence remains incomplete.

**New findings in this review:**

- Separated creator citation year 2022 from journal publication in 2023, volume 27(12), pp.2688–2696.
- Confirmed explicit CC BY-NC 4.0 and research-purpose wording on the creator page.

**Still unresolved:**

- Accessible primary methods and complete taxonomy.
- Canonical split, annotation adjudication and source-scene independence.

**Sources and exact evidence:**

- [MAR20 creator description](https://gcheng-nwpu.github.io/) — MAR20 dataset section. 3,842 images, 20 types, 22,341 instances; HBB and OBB; CC BY-NC 4.0; citation dated 2022.
- [MAR20 journal record](https://www.ygxb.ac.cn/zh/article/doi/10.11834/jrs.20222139/) — Bibliographic record and abstract. Identifies published journal version, 2023, 27(12), 2688–2696; full-text methods were not accessible in this review.

<a id="d19"></a>

### D19 · MTARSI (original 2019 deposit)

**Evidence inspected.** Independently read creator-deposited DataCite metadata and the abstract of a later external quality study indexed by OpenAlex. The original archive and that study's full text were not accessible; detailed error counts were therefore not inferred.

**What a sample represents.** 9,385 single-aircraft chips in 20 categories, described as manually expanded. Each chip contains one complete aircraft; image totals are not counts of independent scenes or physical aircraft.

**Collection and selection.** The deposit describes Google Earth imagery from 36 airports. Manual expansion is explicit, but the inspected metadata does not specify a parent-image manifest, exact expansion transformations or independent acquisition dates.

**Labels and negatives.** Seven interpretation specialists labelled the images. The taxonomy combines specific aircraft types with a broad Boeing class, so category granularity is uneven. No box geometry or adjudication protocol is established by the deposit description. The one-complete-aircraft rule makes this a positive, object-centred classification set. A documented background or no-aircraft category was not established; chip accuracy therefore does not evaluate scene-wide false positives.

**Partitions and independence.** The original canonical split and any grouping of expanded siblings were not verified. The later study's reported validation results are its experimental evidence, not documentation of a universally fixed dataset split. Manual expansion, airport-specific backgrounds and cropped views can correlate samples. No duplicate or split audit was performed, and MTARSI 2 explicitly derives from this collection.

**Quality evidence.** Specialist annotation is author-reported. Gao et al.'s independent study reports labelling errors and limited complexity/heterogeneity, alongside weak results on its adopted external samples despite near-perfect internal validation. Only the abstract was inspected, so the scope and sample selection remain limited.

**What evaluation means.** Classification accuracy measures assignment among the chosen chip labels. The external study demonstrates that internal validation can differ from external-sample performance; it does not establish a universal failure rate for every reuse.

**Interpretation.** The deposit is identifiable and licensed CC BY 4.0, but its count should not be interpreted as independent coverage or its chip task as full-scene detection.

**New findings in this review:**

- Preserved the quality study's abstract-only evidence boundary.
- Separated specialist labelling claims from external observations about generalization.

**Still unresolved:**

- Original split and augmentation lineage.
- Full-text quality-study protocol and verified per-label corrections.

**Sources and exact evidence:**

- [Original MTARSI deposit metadata](https://api.datacite.org/dois/10.5281/zenodo.3464319) — Descriptions, creators and rights fields. 9,385 manually expanded chips, 20 types, 36 airports, one complete aircraft per chip, seven specialists and CC BY 4.0.
- [Gao et al. external quality study](https://doi.org/10.1109/ACCESS.2022.3231327) — Abstract, inspected via OpenAlex indexed record. Reports limited complexity/heterogeneity, labelling errors and poor performance on adopted external samples despite high internal validation.
- [OpenAlex abstract record](https://api.openalex.org/works/https://doi.org/10.1109/ACCESS.2022.3231327) — abstract_inverted_index and locations. Provides the inspected study abstract; listed IEEE full-text PDF returned HTTP 418 during this review.

<a id="d20"></a>

### D20 · MTARSI 2 (separate 2021 derivative)

**Evidence inspected.** Independently checked the creator-deposited DOI metadata. This supports derivation, reclassification and declared rights; it does not substitute for inspection of archive contents or a methodological paper.

**What a sample represents.** Aircraft image chips assigned to 42 reclassified categories. The inspected deposit description does not give a verified total image count, so the original MTARSI total of 9,385 is not transferred.

**Collection and selection.** Richard Rudd-Orthner and Lyudmila Mihaylova's 2021 University of Sheffield deposit explicitly derives from the original MTARSI and adds augmentation. It is not documented as a newly acquired independent set of airports or source scenes.

**Labels and negatives.** The stated change is reclassification into 42 categories. The metadata does not provide a complete old-to-new label map, explicit unknown/ambiguous cases, annotator qualifications or an independently checked category-error estimate. No newly introduced no-aircraft/background class or negative-image sampling process is documented. The original's object-centred chip origin remains relevant, but each derivative file was not checked against that rule.

**Partitions and independence.** Training, validation and test counts and the timing of augmentation relative to splitting are not established. Grouping all variants from a parent image within a partition cannot be assumed. The original and derivative share source material by declaration. Additional variants increase file counts without necessarily increasing source-scene or aircraft-identity coverage.

**Quality evidence.** The explicit parent DOI is useful provenance evidence. A description of reclassification alone does not show that original label errors were all corrected or independently adjudicated. The deposit acknowledges uneven class frequencies and appearance variation.

**What evaluation means.** A 42-class classification result answers a different label question from the original 20-class task. Changes in category boundaries and augmentation also prevent attributing any score change solely to improved data quality.

**Interpretation.** Treat MTARSI 2 as a traceable reclassified/augmented derivative, with CC BY 4.0 deposit terms. Its methodological gaps remain explicit pending a manifest-level account.

**New findings in this review:**

- Established that the missing derivative count must remain unknown.
- Separated taxonomy refinement from new imagery and from verified label correction.

**Still unresolved:**

- Exact file count, complete label mapping and augmentation lineage.
- Canonical split, negative policy and independent QC evidence.

**Sources and exact evidence:**

- [MTARSI 2 creator-deposited metadata](https://api.datacite.org/dois/10.5281/zenodo.5044950) — Descriptions, creators, related identifiers and rights. 2021 Sheffield deposit; 42 reclassifications; added augmentation; parent MTARSI DOI and CC BY 4.0. No verified total count or split was found.
- [Original parent deposit](https://doi.org/10.5281/zenodo.3464319) — Parent identity cited by derivative. Establishes the original collection identity, not independence of the derivative.

<a id="d21"></a>

### D21 · MVRSD

**Evidence inspected.** Independently inspected the creator repository's README and public file listing. These document a claimed dataset and demo, but the demo archive and a full annotation release were not downloaded.

**What a sample represents.** The README reports 3,000 images of 640×640 pixels with 32,626 instances, plus three additional large unlabelled images. The unlabelled images should not be counted as annotated examples or verified negatives.

**Collection and selection.** Authors describe Google Earth imagery at 0.3 m resolution from more than 40 military scenarios across Asia, North America and Europe. The term 'scenario' is not defined as an independent scene, location, acquisition or physical-object unit.

**Labels and negatives.** The repository establishes an object-detection context but the inspected description does not provide a sufficiently complete class ontology, label geometry schema, annotator protocol or treatment of uncertain identities. Specific class detail should not be supplied from the dataset name alone. Neither a background-only subset nor rules for occlusion, truncation or minimum object size were established. Three unlabelled large images are described as extra material, not a negative class.

**Partitions and independence.** Canonical train/validation/test counts and partition construction are not documented in the inspected README. A geographically broad collection description does not establish geographic separation between partitions. Chip extraction, Google Earth source reuse and the relationship between the additional large images and labelled chips are unresolved. It is not possible to quantify unique scenes from the README.

**Quality evidence.** No repeat-labelling process, independent adjudication, measured label-error rate or duplicate analysis is described in the reviewed repository material. The reported counts remain creator claims rather than independently recounted data.

**What evaluation means.** Without a verified ontology, annotation schema and scoring protocol, the dataset's name and headline totals are insufficient to interpret a quantitative benchmark result precisely.

**Interpretation.** MVRSD has identifiable creator documentation but a shallow publicly verified methodological record. It should remain visibly less substantiated than entries with inspected primary methods.

**New findings in this review:**

- Distinguished the three unlabelled images from the reported annotated set.
- Identified that '40 scenarios' is not a documented independence unit.

**Still unresolved:**

- Complete released ontology/schema, split and provenance manifest.
- Data licence, negative-image policy and annotation QC.

**Sources and exact evidence:**

- [MVRSD creator repository](https://github.com/baidongls/MVRSD) — README dataset description and repository file listing. Reports 3,000 640×640 images, 32,626 instances, 0.3 m Google Earth imagery, over 40 scenarios and three unlabelled large images; inspected listing exposes README and demo archive.

<a id="d22"></a>

### D22 · RarePlanes

**Evidence inspected.** Independently read the primary paper's annotation, real-data and experimental-split sections and checked creator/AWS documentation. Reported quality checks were not independently replicated on image files.

**What a sample represents.** The paper distinguishes 253 real scenes, 112 locations, 14,707 real aircraft and 629,551 synthetic annotations across 50,000 renders. Tiled products and source scenes are different units and must remain separately counted.

**Collection and selection.** WorldView-3 scenes cover 22 countries and 2,142 km². Authors stratified large OpenStreetMap aerodromes in the US/Europe by climate, added seven manually chosen locations overlapping earlier datasets, and selected seasonal revisits. Panchromatic, multispectral and pansharpened RGB products have different resolutions.

**Labels and negatives.** Real aircraft are annotated as ordered nose–wing–tail–wing diamonds, supporting bounding boxes, length and wingspan. Ten visual attributes with 33 choices lead to broad role classes. Synthetic annotations come from simulation, and full instance masks are synthetic-only. Released 512×512 real tiles overlap by 20% and contain at least one aircraft. Full images are cropped to annotation extents. The positive-tile product is not a random sample of aircraft-free land.

**Partitions and independence.** The paper explicitly allows an airfield in both real training and test sets at different dates and includes at least one scene per country in both. Its synthetic experiment uses 45,000 renders and 5,000 cross-validation renders. Revisited airfields, overlapping tiles and manually selected overlap locations create explicit dependencies. Synthetic diversity is generated variation, not additional real observations.

**Quality evidence.** A professional service labels the real data and performs its own QC, followed by author QC. This is a reported two-round process; no independent residual-error estimate was calculated here.

**What evaluation means.** Diamond-derived detection geometry and attribute/role recognition differ from exact model identification or real silhouette segmentation. Real and synthetic labels have distinct production processes; combined headline counts do not describe one homogeneous measurement population.

**Interpretation.** RarePlanes provides unusually detailed construction metadata, but its documented partitions are not location-disjoint. CC BY-SA 4.0 and public AWS access are verified documentation claims.

**New findings in this review:**

- Confirmed positive-only tile construction and explicit same-airfield split overlap.
- Distinguished diamonds from synthetic silhouette masks and scenes from tiles.

**Still unresolved:**

- Archive-level correspondence of tiles, source scenes and releases.
- Independent annotation-error estimate.

**Sources and exact evidence:**

- [RarePlanes primary paper](https://arxiv.org/html/2006.02963v2) — §3 dataset annotation/real and synthetic data; §4.1 split preparation. Exact counts, diamond annotation, two QC rounds, climate-stratified collection, positive overlapping tiles and same-airfield split reuse.
- [RarePlanes creator page](https://www.cosmiqworks.org/rareplanes/) — Dataset description and access. Identifies real/synthetic products and dataset distribution.
- [AWS RarePlanes registry](https://registry.opendata.aws/rareplanes/) — License and access. CC BY-SA 4.0 and public S3 access without an AWS account.

<a id="d23"></a>

### D23 · ShipRSImageNet (paper counts; repository currently V1.1)

**Evidence inspected.** Independently reviewed the creator README, repository tree and stated evaluation tasks. The primary publisher paper and archive were not inspected; documentation arithmetic and source relationships were checked without recounting images.

**What a sample represents.** The README reports 3,435 images and 17,573 instances, with 50 leaf labels across four hierarchy levels. The leaf inventory includes Dock, so '50 ship types' is an imprecise shorthand.

**Collection and selection.** Authors report 532 ship-containing xView crops with 150-pixel overlap, 1,057 HRSC2016 images, 1,846 FGSD images, 21 Airbus images and 17 GF/JL images. These listed contributions total 3,473, conflicting with the headline 3,435.

**Labels and negatives.** The creators report expert categorisation, correction of wrong labels and added missed small ships. HBBs, OBBs and polygons are described, with COCO/VOC representations. 'Other' labels appear at multiple hierarchy levels. The xView component deliberately extracts images containing ships. A negative-only image inventory and inclusion policy for the other source components were not verified. Dock is a labelled object, not an implicit background category.

**Partitions and independence.** The current V1.1 notice adds a dedicated test set, but exact split sizes and source-disjoint selection are not given there. Earlier paper totals cannot automatically be assigned to the current release. Reuse of xView, HRSC2016 and FGSD is explicit, with additional overlap within xView crops. These are documented source dependencies, not independent new observations.

**Quality evidence.** Expert review and correction are creator claims without an inspected independent audit or measured residual-error estimate. The count conflict remains unresolved rather than being silently repaired.

**What evaluation means.** The README specifies COCO-style mAP/mAR, including mAP across IoU 0.50–0.95, and separates horizontal detection from 'segmentation with oriented bounding boxes'. That wording does not establish true silhouette masks; hierarchy level also changes the category task.

**Interpretation.** This is a derivative, relabelled collection whose source provenance is useful but whose count, mask meaning and current split need release-specific reconciliation.

**New findings in this review:**

- Verified that listed source counts sum to 3,473.
- Clarified metric range, hierarchy-specific evaluation and uncertain mask semantics.

**Still unresolved:**

- 3,435 versus 3,473 and current V1.1 totals.
- Mask geometry and split independence.
- Academic-only image terms versus final Apache-2.0 wording.

**Sources and exact evidence:**

- [ShipRSImageNet creator README](https://raw.githubusercontent.com/zzndream/ShipRSImageNet/main/README.md) — Description; What's New; Image Source and Usage License; Object Category; Models trained; License. Headline/source counts, explicit reuse, expert corrections, V1.1 test-set notice, hierarchy, COCO metric range and conflicting terms.
- [Creator repository tree](https://github.com/zzndream/ShipRSImageNet) — README and public dataset-related code listing. Confirms benchmark code and release links; no archive mask or split manifest was checked.

<a id="d24"></a>

### D24 · xView (2018 detection dataset)

**Evidence inspected.** Independently read primary paper sections on collection, annotation, QC and splits and checked official dataset terms. Numerical QC thresholds are author-reported acceptance criteria, not this review's measured label accuracy.

**What a sample represents.** More than one million annotated objects in 60 categories across approximately 1,415 km² of WorldView-3 imagery. The review does not select among conflicting secondary image counts without an official manifest.

**Collection and selection.** Authors identify candidate areas from open databases, confirm relevant objects visually, draw areas of interest and extract intersecting 1 km² UTM grid cells. Variation across continents, environments and capture conditions is deliberately sought; sampling is object-conditioned.

**Labels and negatives.** Workers use a QGIS plugin for horizontal boxes. Each labels a general category, using a child class when confident and falling back to its parent otherwise. Partly visible objects at approximately 20% visibility or less are excluded. The goal is exhaustive annotation within the selected classes, subject to visibility exclusion. Supervisory checks include empty tiles and incomplete annotation, but no independently verified negative-only distribution is established.

**Partitions and independence.** The public release splits per image, with 59.2%/20.0%/20.8% of objects in train/test/validation and at least five instances per category in each. The paper's separate baseline experiments use a 70/30 split; these protocols must not be conflated. Per-image splitting does not establish spatial separation of neighbouring grid cells. Authors acknowledge that tightly packed groups can be mistakenly labelled as one object; buildings and small cars dominate counts.

**Quality evidence.** Worker cross-review, supervisor checks and expert gold-standard checks are described. Experts label six 1 km² chips per batch; passing requires precision 0.75 and recall 0.95 at IoU 0.5. Failed batches are remediated, with Tomnod used for difficult chips.

**What evaluation means.** Box-detection AP concerns the chosen mixed object/facility ontology. QC acceptance thresholds do not mean every class or image reaches those values. Parent fallback and merged-object errors affect label interpretation.

**Interpretation.** xView has a substantive documented QC pipeline and CC BY-NC-SA 4.0 data terms, while sampling and split dependencies limit broad generalization claims.

**New findings in this review:**

- Recovered public split proportions separately from baseline splits.
- Established visibility exclusion, parent fallback and gold-standard sampling scope.

**Still unresolved:**

- Canonical image manifest and location-level partition independence.
- Residual class-specific annotation errors.

**Sources and exact evidence:**

- [xView primary paper](https://arxiv.org/html/1802.07856) — Dataset collection, Annotation, Quality Control, Dataset Splits and Experiments sections. AOI/grid construction, parent fallback, visibility exclusions, three QC stages, sampled acceptance thresholds and distinct public/baseline partitions.
- [Official xView dataset terms](https://xviewdataset.org/terms.html) — Dataset licence terms. Dataset-specific CC BY-NC-SA 4.0; distinct from the article licence.
- [Official xView site](https://xviewdataset.org/) — 2018 dataset overview. Identifies the 60-class detection benchmark and official access context.

<a id="d25"></a>

### D25 · DroneVehicle

**Evidence inspected.** Full author paper sections III-A–D and V-A3–4 and the official README were inspected. Images and individual annotation files were not audited.

**What a sample represents.** 28,439 RGB/infrared pairs, or 56,878 individual images, with 953,087 modality-specific quadrilateral annotations. Boxes do not count unique physical vehicles.

**Collection and selection.** UAV imagery covers roads, residential areas and parking lots by day and night. Distortion correction, affine transformation and cropping align most pairs; exact universal registration is not claimed.

**Labels and negatives.** Manual labels give four corner coordinates and one of five vehicle classes. The modalities deliberately have different totals because an object may be visible in only one. Four corners describe image geometry, not a segmentation mask or verified physical heading. No explicit target-free-image sampling rule, exhaustive background annotation policy or ignore-region specification was established in the reviewed sections.

**Partitions and independence.** Published train/validation/test partitions contain 17,990/1,469/8,980 pairs. Corresponding RGB box totals are 286,793/22,462/143,315; infrared totals are 316,411/24,490/159,616. The published partition counts do not establish separate flights, source videos, locations or vehicle identities. Paired modalities and repeated observations cannot be treated as independent physical instances.

**Quality evidence.** The paper reports removal of poor-quality or blurred images and manual checking of all image data. No independent error-rate or agreement measurement was performed here.

**What evaluation means.** Detection mAP uses an intersection-over-union threshold greater than 0.5. It evaluates class-labelled quadrilateral localization against visibility-dependent annotations, rather than object identity across images or scene interpretation.

**Interpretation.** The record supports paired ordinary-vehicle localization with qualified alignment and per-modality visibility. It does not document event, intent or affiliation labels.

**New findings in this review:**

- Visibility differences explain unequal modality annotation totals; equality is not the published goal.
- The README's 840×712 files include a 100-pixel border around a 640×512 image region.
- The deeper paper review establishes exact split and modality-specific box totals.

**Still unresolved:**

- Source-group separation across partitions; negative and ignored-object policies; independently measured registration and annotation error.

**Sources and exact evidence:**

- [DroneVehicle author paper, version 2](https://arxiv.org/html/2003.02437v2) — III-A–D; V-A3 Partition Protocol; V-A4 Evaluation Metric. Describes image curation, registration, quadrilateral labels, visibility-related annotation differences, exact partitions and IoU-based evaluation.
- [Official DroneVehicle release](https://github.com/VisDrone/DroneVehicle) — README dataset statistics and image/annotation notes. Documents five classes, per-modality statistics and the white-border convention; no image-level audit was conducted.

<a id="d26"></a>

### D26 · DSIAC ATR Algorithm Development Image Database / historical SENSIAC lead

**Evidence inspected.** The current DSIAC landing page and a later study's dataset section were inspected. The advertised seven-section user guide and archive schemas were unavailable publicly in the reviewed page.

**What a sample represents.** The official 206 GB figure is archive size, not an image, frame or sequence total. A later paper's 2,595 images and eight classes describe its study subset.

**Collection and selection.** US Army NVESD acquired visible and MWIR imagery using commercial cameras, covering military and civilian vehicles and people across recording conditions. The public page summarizes capture context without a complete acquisition manifest.

**Labels and negatives.** DSIAC advertises ground truth, target photographs, meteorology and target/background temperature differences, plus a viewer and user guide. The page does not reveal coordinate conventions, annotation cadence, visibility flags or the exact class ontology. Neither exhaustive negative coverage nor an explicit absent-target or ignored-object policy is established by the public summary.

**Partitions and independence.** No canonical train/validation/test assignment or evaluation protocol was found on the current page. The later study's selected images cannot supply a full-archive partition. Repeated target identities, viewpoints, acquisition runs and shared backgrounds cannot be quantified from the landing page. The historical SENSIAC name was not independently verified as a separate release.

**Quality evidence.** The availability of ground truth and environmental documentation is a publisher claim. No manual, label file, image sample or empirical annotation-quality audit was inspected.

**What evaluation means.** Archive contents support descriptive statements about object imagery and capture metadata. Scores from a paper-specific subset reflect that subset's selection and task, not an official archive-wide benchmark.

**Interpretation.** A documented military-origin image archive remains substantially opaque at schema level. No scene-narrative, intent or allegiance annotation set is established.

**New findings in this review:**

- The page's 2020 publication and 2026 modification timestamps describe the webpage, not acquisition dates.
- Distribution Statement A coexists with DSIAC's stated final-distribution discretion; no request was submitted.

**Still unresolved:**

- Complete counts, ontology, label cadence, negatives, source identities, official partitions and current archive-level reuse terms.

**Sources and exact evidence:**

- [DSIAC official archive page](https://dsiac.dtic.mil/databases/atr-algorithm-development-image-database/) — Database description, accompanying materials, access and distribution text; page metadata. Reports 206 GB and accompanying ground truth/context, advertises a seven-section guide, and directs prospective recipients to a request process.
- [Zero-Shot Scene Understanding for Automatic Target Recognition Using Large Vision-Language Models](https://arxiv.org/html/2501.07396v1) — IV-A, DSIAC dataset description. Describes 2,595 images and eight classes in the study; this is not evidence of the full archive's size or schema.

<a id="d27"></a>

### D27 · M3FD

**Evidence inspected.** The author preprint, published CVPR paper and current TarDAL README were inspected. No image pairs, YOLO label files or split manifests were audited.

**What a sample represents.** The published introduction says 4,177 pairs/23,635 objects, while Table 1 and section 4 say 4,200/33,603. The current README reports 34,407 labels and an additional 300 fusion pairs.

**Collection and selection.** Native optical 1024×768 and LWIR 640×512 streams undergo intrinsic/extrinsic calibration and homography into common 1024×768 coordinates. Four environment groups and ten sub-scenarios describe captured conditions.

**Labels and negatives.** The release documents manually assigned YOLO boxes for People, Car, Bus, Motorcycle, Lamp and Truck. The inspected release establishes a visible/infrared pair; mentioned future binocular-depth information is not confirmed released data. No explicit negative-image sampling, ignored-object rule or exhaustive visibility policy was verified. The README acknowledges missed and mislabelled objects.

**Partitions and independence.** Section 5 describes selections of 180 and 3,500 'multi-modality images' and their expansion into 24,000 and 151,000 patches for experiments. These are not established as a canonical source-independent partition. Cropped patches are derived observations, not additional independent captures. Source-video, location and object-identity exclusions across experimental selections were not established.

**Quality evidence.** Calibration and manual labelling are described, but the authors' known-error caveat remains material. No independent alignment check, inter-annotator agreement or label-error sampling was undertaken.

**What evaluation means.** Detection mAP at IoU 0.5 measures annotated object localization/classification. Fusion image-quality metrics assess a different outcome and do not independently validate object labels or establish a uniquely correct fused image.

**Interpretation.** M3FD provides ordinary-object boxes and environmental grouping across paired modalities. 'Multi-scenario' does not establish event narratives or intent annotations.

**New findings in this review:**

- Count discrepancies occur within the published paper as well as between paper and README.
- The separate 300-pair fusion set must remain distinct from the main detection count.
- No separate manually annotated mask product was verified.

**Still unresolved:**

- Reconciliation of three object-count claims; exact version manifests; source-independent partitions; released annotation completeness and pair-registration error.

**Sources and exact evidence:**

- [Published M3FD/TarDAL CVPR paper](https://openaccess.thecvf.com/content/CVPR2022/html/Liu_Target-Aware_Dual_Adversarial_Learning_and_a_Multi-Scenario_Multi-Modality_Benchmark_To_CVPR_2022_paper.html) — Introduction; Table 1; sections 4 and 5 of linked paper. The introduction and dataset table/body give conflicting pair/object totals; dataset and experiment sections describe sensors, registration, classes and derived patches.
- [Author preprint, version 1](https://arxiv.org/html/2203.16220v1) — Section 4 M3FD; section 5 experimental settings and evaluation. Describes six object classes, four condition groups, ten sub-scenarios and separate detection/fusion evaluations.
- [Official TarDAL dataset README](https://github.com/JinyuanLiu-CV/TarDAL) — M3FD description, data organization and labelling caveat. Reports 34,407 labels, a separate 300-pair fusion collection, YOLO text annotations and possible missing or incorrect labels.

<a id="d28"></a>

### D28 · TNO Image Fusion Dataset

**Evidence inspected.** The official versioned Figshare metadata and open 2017 data article were inspected. The ZIP was not downloaded; the article was read through PMC after a Figshare PDF retrieval failed.

**What a sample represents.** The reviewed official release does not establish a complete homogeneous image/sequence total. The 2017 TNO Multiband Image Collection is an umbrella of three datasets, not a countable synonym for this entry.

**Collection and selection.** The Image Fusion collection includes intensified visual 390–700 nm, NIR 700–1000 nm and LWIR 8–12 μm nighttime observations of people and vehicles from Netherlands urban/rural field trials.

**Labels and negatives.** Sensor signals are warped and subsampled for pixel correspondence. Camera descriptions and recording references accompany the imagery; no formal object-box, mask, track or timed-event annotation schema was established. No target-free sampling arm or exhaustive object-presence/background policy is defined. Scene content descriptions do not create negative labels.

**Partitions and independence.** No canonical train/validation/test partition was specified in the reviewed article or release metadata. Third-party selected subsets cannot establish the release's original partition. The umbrella contains distinct sensor collections, including the separately described TRICLOBS release. Repeated scenes, cameras and frames must not be combined as independent new datasets.

**Quality evidence.** The primary article documents sensor and registration procedures. Versioned release metadata and an explicit CC BY 4.0 license improve traceability, but do not measure residual alignment or annotation accuracy.

**What evaluation means.** Registered multiband inputs are the principal product. The sources do not establish one independent 'correct fused image' or a mandatory benchmark score; subsequent fusion metrics describe their own stated criteria.

**Interpretation.** This is a multiband imagery resource with acquisition documentation. Military-relevant scene descriptions do not establish a formal military event or identity ontology.

**New findings in this review:**

- The umbrella-versus-individual-dataset distinction prevents combining unrelated counts.
- BMP/TIF/MP4 formats are reported across the umbrella, not verified in every subset.
- Original v1 is from 2014; v2 is from 2022.

**Still unresolved:**

- Exact per-collection counts and manifests; residual registration errors; any additional task labels not documented in the inspected sources.

**Sources and exact evidence:**

- [TNO Multiband Image Collection data article](https://pmc.ncbi.nlm.nih.gov/articles/PMC5635205/) — Specifications Table; section 1 Data; section 2 Experimental design. Separates three datasets in the umbrella and describes spectral bands, nighttime acquisition, registration and formats.
- [TNO Image Fusion Dataset, version 2](https://doi.org/10.6084/m9.figshare.1008029.v2) — Official description, version history, files and license metadata. Provides the versioned individual release, ZIP/document listing and CC BY 4.0 metadata; archive contents were not inspected.
- [TNO Image Fusion Dataset, version 1](https://doi.org/10.6084/m9.figshare.1008029.v1) — Original version metadata. Establishes the 2014 original release separately from the 2022 update.

<a id="d29"></a>

### D29 · TRICLOBS Dynamic Multiband Image Dataset

**Evidence inspected.** The primary paper, its 16-row scenario table and official release metadata were inspected. Raw BMPs, preview MP4s and accompanying spreadsheets were not downloaded.

**What a sample represents.** Sixteen motion scenarios at three sites occupy 4/4/8 scenario folders. Published frame counts sum to 56,865 multiband frames; this is arithmetic from Table 1, not a file count.

**Collection and selection.** Field trials record staged people/vehicle actions with visible, NIR and LWIR sensors. Thermal 384×288 data are interpolated and visible/NIR cropped to common field of view; output is 640×480.

**Labels and negatives.** Raw sequential 24-bit BMPs encode visible in R, NIR in G and LWIR in B, each eight bits. Table 1 supplies one prose action description per scenario; reference colour photographs and atmospheric/lighting CSV/Excel data provide context. The scripted recordings have no verified object-detection present/absent schema or dedicated negative population. A prose clip description is not an exhaustive per-frame label.

**Partitions and independence.** No standard learning or evaluation split is specified. The three sites and sixteen scenarios are acquisition organization, not demonstrated independent train/test assignments. Many adjacent frames and repeated actions/sites occur within a small set of scripted recordings. Frame counts cannot be interpreted as independent scenarios or independent field trials.

**Quality evidence.** The paper explicitly documents unsynchronized channels with maximum timing difference below 9 ms, independent gain-related flicker, vignetting and limited environmental diversity. These are publisher-described limitations, not independently measured defects.

**What evaluation means.** The release supplies registered spectral observations for fusion-related study, without dense boxes, track identities, timed action ranges or an official mandatory task score. Scenario prose describes visible staged activity, not hidden intent.

**Interpretation.** TRICLOBS is a qualified exception with genuine clip-level action metadata, while its raw sensor product and presentation previews must remain distinct.

**New findings in this review:**

- MP4s are four-panel visualization previews containing a colour-remapped fusion; the paper says they are not intended for further processing.
- Spatial registration does not mean sensor synchronization.
- The raw BMP channel packing differs fundamentally from the preview product.

**Still unresolved:**

- Residual spatial/temporal registration measured on files; any annotation products beyond the inspected paper table; independent scene/source grouping.

**Sources and exact evidence:**

- [TRICLOBS primary paper](https://doi.org/10.1371/journal.pone.0165016) — Image registration; Registration sites and conditions; The TRICLOBS Data Set: Contents and Structure; Limitations. Documents raw BMP channel encoding, preview MP4 restrictions, resampling, timing mismatch, supplemental context and known sensor/environment limitations.
- [TRICLOBS scenario table](https://doi.org/10.1371/journal.pone.0165016.t001) — Table 1, all sixteen scenario rows. Provides per-clip action prose and frame totals; the counts sum to 56,865, without timed action boundaries.
- [Official TRICLOBS dataset](https://figshare.com/articles/dataset/The_TRICLOBS_Dynamic_Multiband_Image_Dataset/3206887) — Release description, files and license metadata. Establishes the separately versioned dynamic multiband release and CC BY 4.0 terms; files themselves were not audited.

<a id="d30"></a>

### D30 · Anti-UAV original / later Anti-UAV300 label

**Evidence inspected.** Original paper version 3 sections III-A–E, the correction README and the current version table were inspected. Individual videos and label files were not audited.

**What a sample represents.** The original paper reports 318 unaligned RGB/infrared video pairs and about 585,900 box annotations. The later 'Anti-UAV300' label is a release name, not the exact original count.

**Collection and selection.** Ground-based paired sensors record mainly DJI/Parrot consumer drones at 25 FPS under varied lighting and backgrounds. Modalities are explicitly unaligned.

**Labels and negatives.** The coarse stage labels every 25 frames. The paper then describes selecting 30 pairs for detailed per-frame annotation, corrections and 1,000-frame clips. This does not establish independently manual annotation of every released frame or complete interpolation provenance. An exist flag records presence/absence; an empty prediction represents absence. The paper calls its rectangle field get_rect and describes corner coordinates, which must not be silently equated with later xywh schemas.

**Partitions and independence.** The original train/validation/test allocation is 160/67/91 paired sequences. Training and validation use different clips from the same recordings; the paper describes test recordings as independent. Training and validation are not independent at recording level. Cross-version overlap and precise manual/derived label provenance across all release frames remain unaudited.

**Quality evidence.** Progressive annotation and manual correction are published claims. The original repository lists four start-frame corrections. Their existence supports version-sensitive review, without establishing a measured residual label-error rate.

**What evaluation means.** State accuracy combines bounding-box IoU on present-target frames with correctly predicted absence, averages within each clip, then across clips. It is neither ordinary classification accuracy nor a metric of event understanding.

**Interpretation.** The annotation semantics are UAV localization and visible existence. They do not establish military subtype, intent, threat, authorization or allegiance.

**New findings in this review:**

- The paper's detailed annotation stage explicitly names 30 selected video pairs.
- Seven challenge attributes describe visual/tracking difficulty rather than scenario narratives.
- Original field names and coordinate descriptions differ from the later 410 evaluator.

**Still unresolved:**

- Frame-level annotation provenance across the entire release; exact version manifests and overlap; independent audit of corrected start frames.

**Sources and exact evidence:**

- [Original Anti-UAV paper, version 3](https://arxiv.org/html/2101.08466v3) — III-A–E, acquisition, annotation, partition and evaluation descriptions. Documents unaligned modalities, coarse/detailed annotation stages, existence labels, original splits and sequence-averaged state accuracy.
- [Original Anti-UAV repository](https://github.com/ucas-vg/Anti-UAV) — README release and ground-truth correction notices. Publishes four start-frame correction notices; corrected dataset files were not inspected.
- [Anti-UAV umbrella repository](https://github.com/ZhaoJ9014/Anti-UAV) — Dataset/version table. Uses Anti-UAV300 for the RGB+IR release and distinguishes later infrared-only versions.

<a id="d31"></a>

### D31 · Anti-UAV410

**Evidence inspected.** The dedicated README, loader/evaluator code and GitHub annotation-directory listings were inspected. Publisher full text was unavailable; no video or annotation-file contents were audited.

**What a sample represents.** The README reports 410 infrared videos and over 438,000 manually annotated boxes. Directory listings contain 200/90/120 train/validation/test .txt files; these are metadata counts, not verified video counts.

**Collection and selection.** The release describes thermal UAV tracking under varied appearance, clutter, occlusion and out-of-view conditions. Detailed acquisition and paper-level review procedures were not established from accessible materials.

**Labels and negatives.** The loader finds IR_label.json, checks image/gt_rect count equality and a four-entry initial rectangle. The evaluator interprets rectangles as x,y,width,height. Ten sequence attributes are documented; the README explicitly says frame attributes are incomplete. Evaluation handles absence: empty or single-value predictions denote absent targets; present frames use box overlap. Some invalid or zero ground-truth cases may be skipped, so file conventions affect the scored population.

**Partitions and independence.** Listed annotation filenames total 410 across the three directories. Train contains 02_6319_0000-1499.txt and test contains 02_6319_1500-2999.txt, suggesting adjacent excerpts of one source recording. The shared filename stem raises a concrete source-independence question; it does not prove duplicated frames. Actual manifests, recording identities and cross-version overlap were not verified.

**Quality evidence.** Manual annotation is an author claim. Loader assertions check limited structural consistency, not box accuracy, exhaustive negatives or inter-annotator agreement. No empirical label audit was performed.

**What evaluation means.** The code averages sequence state accuracies combining present-frame IoU and absence handling. Its separate overlap/precision report adjusts first-frame boxes and mismatched lengths, making the exact evaluation protocol material to interpretation.

**Interpretation.** The accessible evidence establishes a thermal localization/existence schema and incomplete frame attributes, with stronger schema evidence than acquisition-quality evidence.

**New findings in this review:**

- Metadata establishes 200/90/120 annotation-list counts.
- A concrete train/test filename pair suggests adjacent source excerpts.
- The loader contains a placeholder download URL although README cloud links exist.

**Still unresolved:**

- Source-recording separation; complete frame attributes; full-paper annotation protocol; actual video/label consistency and residual errors.

**Sources and exact evidence:**

- [Dedicated Anti-UAV410 release](https://github.com/HwangBo94/Anti-UAV410) — README dataset description, attribute list, frame-attribute caveat and download links; annos/train, annos/val and annos/test directory listings. Reports 410 videos and manual boxes, explicitly warns of incomplete frame attributes; listing-only counts are 200/90/120 and show the cited adjacent filename ranges.
- [Official Anti-UAV410 loader](https://github.com/HwangBo94/Anti-UAV410/blob/main/datasets/antiuav410.py) — Lines 37–38 and 60–67; download routine. Finds IR_label.json, checks JPG/gt_rect counts and initial box length; the download routine has a placeholder URL.
- [Official Anti-UAV410 evaluator](https://github.com/HwangBo94/Anti-UAV410/blob/main/experiments/anti_uav.py) — Lines 86–102, 122–145, 260–266 and 290. Defines xywh overlap, absence handling, special report adjustments and sequence-averaged state accuracy.
- [Anti-UAV410 TPAMI publication record](https://doi.org/10.1109/TPAMI.2023.3335338) — Publication identifier only; full publisher text not retrieved. Identifies the publication; no full-paper annotation-quality claims are inferred from its inaccessible text.

<a id="d32"></a>

### D32 · AntiUAV600

**Evidence inspected.** Paper version 2 sections III-A–C and Appendix A, plus the official version table, were inspected. Actual video, box and attribute files were not audited.

**What a sample represents.** Six hundred thermal sequences contain over 723,000 densely annotated frames. The paper gives approximately 337,000/56,000/330,000 frames in train/validation/test.

**Collection and selection.** Thermal recordings are 640×512 at 25 FPS and include target appearance, disappearance and complex backgrounds. A target need not be visible in the first frame.

**Labels and negatives.** The paper describes dense bounding boxes when a UAV is present and 'Not Exist' labels when absent. It claims seven attributes for all frames; that completeness claim was not verified against released files. Absence is explicitly represented within sequences. This establishes present/absent evaluation states, but does not by itself establish a separately sampled, exhaustive target-free video population.

**Partitions and independence.** The stated sequence split is 300 train, 50 validation and 250 test. These counts are published assignments, without verified source-recording, site or target-identity exclusion. Cross-version reuse and source-video relationships were not audited. Anti-UAV300, 410 and 600 therefore cannot be added as disjoint captures or independent benchmark populations.

**Quality evidence.** Dense manual annotation and complete attributes are author statements. The reviewed sections do not provide an independently measured label-error rate or inter-annotator agreement, and no such audit was performed here.

**What evaluation means.** The Acc metric combines present-frame localization overlap and correct absence with an additional missed-presence penalty. Consequently it is not directly interchangeable with original Anti-UAV state accuracy despite related terminology.

**Interpretation.** This release evaluates UAV localization and existence through time, including initial absence. Its labels do not establish scenario narratives, intent or military identity.

**New findings in this review:**

- The deeper paper review establishes 300/50/250 sequences and approximate per-partition frame totals.
- First-frame presence is not guaranteed.
- All-frame attribute completeness is a paper claim, distinct from the 410 README's incompleteness caveat.

**Still unresolved:**

- Actual schema/attribute completeness; source-independent partitions; cross-version overlap; detailed negative-population sampling and label-quality measurements.

**Sources and exact evidence:**

- [AntiUAV600 primary paper, version 2](https://arxiv.org/html/2306.15767v2) — III-A–C; Appendix A, dataset and evaluation descriptions. Provides thermal resolution/rate, dense boxes and Not Exist states, seven frame attributes, 300/50/250 split and the modified accuracy definition.
- [Official Anti-UAV version table](https://github.com/ZhaoJ9014/Anti-UAV) — AntiUAV600 dataset entry and linked release. Distinguishes the infrared-only 600 release from earlier versions and links the publisher-hosted distribution.

<a id="d33"></a>

### D33 · DUT Anti-UAV

**Evidence inspected.** Primary paper sections III-A–C and evaluation descriptions and the official release README were inspected. Individual images, trajectories and ground-truth files were not audited.

**What a sample represents.** The detection subset has 10,000 images and 10,109 boxes. A separate tracking subset has twenty videos, averaging 1,240 frames. Table object totals must not be read as image counts.

**Collection and selection.** Visible-light imagery covers varied outdoor scenes, illumination and weather, with a wide range of image sizes. More than 35 visually represented drone types do not establish 35 annotated classes.

**Labels and negatives.** The authors claim precise manual detection boxes and per-frame tracking rectangles. The two subsets support distinct detection and initialized tracking evaluations; neither establishes a fine-grained platform ontology. Section III-C explicitly includes out-of-view among challenges, but the inspected descriptions do not establish an absent-target schema, negative-image sampling policy or absence-scoring rule.

**Partitions and independence.** Detection train/validation/test counts are 5,200/2,600/2,200 images and 5,243/2,621/2,245 boxes. The twenty tracking videos form a separate evaluation set. The image partition counts do not establish source-video or geographic disjointness. Authors' analysis reports concentration of targets near image centres, limiting claims of uniform spatial coverage.

**Quality evidence.** Manual precision is an author claim. A second-review protocol, agreement statistic and detailed image-source provenance were not verified; no annotation-error sampling was conducted.

**What evaluation means.** Detection mAP evaluates UAV boxes. Tracking overlap success, centre precision and normalized precision evaluate trajectories under their stated initialization and localization conventions. These metrics do not assess authorization, event semantics or intent.

**Interpretation.** The evidence supports generic visible-light UAV localization and trajectories, with documented central-position bias and limited tracking-video count.

**New findings in this review:**

- The paper names out-of-view difficulty without establishing a corresponding absence schema in the reviewed material.
- Visual drone-type diversity is not evidence of a multi-class label set.
- Detection and tracking sample counts and metrics must remain separate.

**Still unresolved:**

- Absent-target scoring; ignored/occluded-object policy; capture provenance and split independence; empirically measured manual-label consistency.

**Sources and exact evidence:**

- [DUT Anti-UAV primary paper](https://arxiv.org/html/2205.10851v1) — III-A–C; dataset statistics and evaluation descriptions. Separates images, boxes and videos, gives split totals and manual annotation claims, discusses central-position concentration and out-of-view challenges.
- [Official DUT Anti-UAV release](https://github.com/wangdongdut/DUT-Anti-UAV) — README detection and tracking download sections. Provides separately organized detection splits and tracking images/ground truth; actual files were not downloaded.

<a id="d34"></a>

### D34 · Military Vehicles in Low-FPS UAV Footage validation benchmark

**Evidence inspected.** Primary paper sections III-A–C, IV opening, evaluation tables and access statement, plus the linked request form, were inspected. No request was submitted or footage/annotations downloaded.

**What a sample represents.** The benchmark comprises 119 videos, 18,421 frames and 58,897 boxes. The request form states all recordings are 5 FPS; these units do not count unique vehicles across online sources.

**Collection and selection.** Authors select online UAV videos containing two or more vehicles and varied viewpoints. This is purposive selection from published footage, not a random population sample or verified independent acquisition campaign.

**Labels and negatives.** Experts assign boxes, three coarse vehicle classes, persistent within-video track IDs and temporal links. The paper's separate discussion of single-frame training labels must not be substituted for the validation benchmark's temporal annotations. No exhaustive target-free-clip sampling, occlusion/ignore-region rule or annotation-completeness policy was established in the reviewed sections.

**Partitions and independence.** The release is described as a validation benchmark. No public canonical train/test partition or source-deduplicated manifest was verified. Online reposts, related clips and source chains were not independently deduplicated. A persistent ID establishes within-video continuity, not identity across recordings.

**Quality evidence.** The authors state that annotations receive multiple reviews for object and temporal consistency. This is a documented procedure, without an independently measured residual error rate or reviewer-agreement result.

**What evaluation means.** Reported tracking experiments use detections from a common binary detector. HOTA, MOTA, IDF1, association accuracy and identity switches therefore characterize tracking conditional on that detection stream; they do not validate the three-class ontology or full scene understanding.

**Interpretation.** The annotations establish coarse military-vehicle categories, location and within-clip identity. They do not establish exact platforms, allegiance, intent or event narratives.

**New findings in this review:**

- The common binary detection stream materially conditions the reported tracking scores.
- Multi-vehicle clip selection shapes the evaluation population.
- The request form restricts use to the declared purpose and requires authorization for redistribution or repurposing.

**Still unresolved:**

- Source-chain duplication and rights; detailed ignore/occlusion policy; canonical partitions; archive-level label and track consistency.

**Sources and exact evidence:**

- [Military Vehicles in Low-FPS UAV Footage paper](https://arxiv.org/html/2507.05229v1) — III-A–C; IV opening; V table headings; conclusion/access statement. Provides clip/frame/box totals, multi-vehicle selection, expert temporal annotation and multiple reviews; states that tracking experiments share a binary detector.
- [Author dataset request form](https://docs.google.com/forms/d/e/1FAIpQLSdKceLoF_L3242FDJLLFdIiVDepQ0imt54SwbxnFgt1sSpjug/viewform?usp=sharing) — Dataset description and applicant-use agreement; read only. States 5 FPS and purpose/redistribution restrictions. The form was inspected but not submitted; no access grant or download was tested.
- [Published benchmark paper](https://doi.org/10.1109/ICMCIS64378.2025.11047873) — Publication identifier. Identifies the published 2025 work; the author full text supplies the inspected annotation and evaluation detail.

<a id="d35"></a>

### D35 · VTUAV / DUT-VTUAV

**Evidence inspected.** Paper sections 3.1–3.3 and official release notices were inspected. Video pairs, sparse boxes, masks and attribute files were not audited.

**What a sample represents.** Five hundred sequences contain 1,664,549 RGB-T pairs. Manual boxes every ten frames total 326,961 across modalities; 24,464 masks occur at 1 FPS in 100 clips.

**Collection and selection.** A UAV captures ordinary targets over a year in two cities: 325 daytime and 175 nighttime clips. Native 640×480 thermal imagery is enlarged to 1920×1080 output.

**Labels and negatives.** One initial-frame alignment transform is applied to each whole video. Boxes are separately annotated by modality. The paper discusses tracker-guided densification, which does not establish dense manual ground truth. Among 430,960 attributes on 301,678 frames, FM/SV/LR/TVS are automatically defined; other attributes are expert-labelled. Long-term sequences have target out-of-view periods exceeding twenty consecutive frames. This is a tracking-condition definition, not evidence of a separately sampled target-free-video population.

**Partitions and independence.** The 250/250 train/test split contains 207/43 and 176/74 short-/long-term clips respectively. The mask subset has fifty train and fifty test sequences. Frame pairs, sparse boxes and masks are distinct counts. Source-video, location and target-identity exclusions between partitions were not verified; initial-frame alignment cannot establish perfect later-frame registration.

**Quality evidence.** Published cadence and separate modality annotations clarify provenance. The release corrected three archive parts in April 2022. No independent mask, box or residual-registration audit was performed.

**What evaluation means.** Maximum success rate uses the greater overlap against modality-specific ground truth to accommodate displacement. Maximum precision is likewise benchmark-specific with a twenty-pixel centre criterion. Mask evaluation uses region Jaccard and contour F-score.

**Interpretation.** VTUAV observes ordinary objects from a UAV, unlike datasets observing UAV targets. It supplies localization, masks and challenge labels, not military scenario or intent annotations.

**New findings in this review:**

- Whole-video registration uses a transform estimated at the initial frame.
- Some challenge attributes are automatic rather than human judgements.
- Published localization scores explicitly accommodate modality displacement.

**Still unresolved:**

- Complete dense-label provenance, if released; residual per-frame alignment; source-independent partitions; quality of corrected archive contents.

**Sources and exact evidence:**

- [VTUAV author paper](https://arxiv.org/html/2204.04120v1) — 3.1 Data Collection; 3.2 Annotation; 3.3 Evaluation Metrics. Documents initial-frame alignment, native/output resolution, sparse modality-specific boxes, masks, automatic/expert attributes, partitions and maximum-modality evaluation.
- [Official VTUAV project](https://zhang-pengyu.github.io/DUT-VTUAV/) — Dataset summary and April 2022 release notices. Provides release organization and notices correcting three archive parts; corrected files were not inspected.
- [Official VTUAV repository](https://github.com/zhang-pengyu/DUT-VTUAV) — README dataset and download sections. Distinguishes RGB-T, RGB-only and mask products and links their releases.

<a id="d36"></a>

### D36 · IRSTD-1k

**Evidence inspected.** The CVPR paper's dataset and evaluation sections and current ISNet README were inspected. No image, mask or partition-list contents were audited.

**What a sample represents.** The paper describes 1,000 real 512×512 infrared images, while the current official README says 1,001. The discrepancy remains unresolved without a versioned file manifest.

**Collection and selection.** Real infrared scenes include sea, river, field, mountain, city and cloud backgrounds with varied target shapes and sizes. Object names in the collection narrative do not establish class-labelled segmentation categories.

**Labels and negatives.** Targets receive manually drawn pixel-level masks. The verified semantic product is generic target/background shape, rather than military identity, activity or physical object type. The reviewed paper sections do not specify a dedicated target-free-image arm. Background pixels supply segmentation negatives, which are not equivalent to independently sampled empty scenes.

**Partitions and independence.** The paper assigns 50% train, 30% validation and 20% test. This is an image-level allocation; source-sequence or geographic grouping was not established. The counts and image split do not prove separate source videos, acquisition sessions or backgrounds. A single image may contain multiple annotated target regions.

**Quality evidence.** Manual pixel labelling is a published claim. No comprehensive boundary-adjudication procedure or inter-annotator agreement was verified, and no independent mask-error sample was examined.

**What evaluation means.** IoU compares target-mask area; nIoU averages image-level IoUs. Detection probability counts correctly predicted targets, whereas false-alarm rate counts false predicted pixels divided by all image pixels. Their numerators have different units.

**Interpretation.** The dataset evaluates generic infrared target extent and localization. Reported overlap or detection scores cannot establish platform identity or scene semantics.

**New findings in this review:**

- The deeper review clarifies that target-level detection probability and pixel-level false alarms are not interchangeable rates.
- The 1,000/1,001 paper-versus-README discrepancy persists.
- Collection object names are not a verified multi-class mask ontology.

**Still unresolved:**

- Version-count reconciliation; explicit empty-image policy; mask-boundary consistency; source grouping and exact split manifests.

**Sources and exact evidence:**

- [ISNet CVPR 2022 paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Zhang_ISNet_Shape_Matters_for_Infrared_Small_Target_Detection_CVPR_2022_paper.pdf) — 3.5 IRSTD-1k dataset; 4.1 Experimental Settings and Evaluation Metrics. States 1,000 real manually pixel-labelled images and 50:30:20 split; distinguishes IoU/nIoU, target-count detection probability and pixel-count false alarms.
- [Official ISNet/IRSTD-1k repository](https://github.com/RuiZhang97/ISNet) — README dataset table and download description. Currently reports 1,001 images, leaving a documented discrepancy with the paper; files were not inspected.

<a id="d37"></a>

### D37 · NUDT-SIRST

**Evidence inspected.** The author paper's synthesis, evaluation and experimental-setting sections and official repository description were inspected. Synthetic images, masks and split lists were not audited.

**What a sample represents.** The release describes 1,327 synthetic 256×256 images. Approximately 37% contain multiple targets; image count is not target count or a count of independent real acquisitions.

**Collection and selection.** Gaussian point models and collected target templates are combined with real infrared backgrounds. Background classification and predefined plausibility rules constrain combinations; intensity and blur are adjusted during construction.

**Labels and negatives.** Target masks derive from the construction process. They are known synthetic labels, not empirical human tracing of newly observed real targets. Point, spot and extended forms describe appearance rather than verified platform classes. No dedicated target-free image arm was specified in the inspected description. Synthetic background pixels provide negatives, without demonstrating the distribution of wholly empty real scenes.

**Partitions and independence.** The experiment uses a 50%/50% image split. Independence of background images, target templates and source material across the two halves was not established. Shared backgrounds or target templates may connect nominally separate images; this was not audited. Multiple synthetic examples do not necessarily add independent natural target observations.

**Quality evidence.** Authors report manually removing visually poor synthesized images. Such visual selection can improve presentation, but construction-known masks and curation do not independently establish physical realism or real-domain representativeness.

**What evaluation means.** IoU measures mask overlap. Published detection probability matches targets using centroid deviation below three pixels. False-alarm rate counts false/unmatched pixels divided by total image pixels, not the proportion of images containing a false alarm.

**Interpretation.** The release is a synthetic generic-target segmentation benchmark with construction-derived masks. Known labels do not establish military identity or observed event ground truth.

**New findings in this review:**

- Background classification, plausibility rules and manual rejection are explicit parts of construction.
- Approximately 37% of images are multi-target.
- The centroid-based detection metric and pixel-based false-alarm metric use different units.

**Still unresolved:**

- Background/template separation across partitions; exact split manifests; dedicated negatives; empirical realism and independent label/scene audits.

**Sources and exact evidence:**

- [DNANet/NUDT-SIRST author paper](https://arxiv.org/html/2106.00487) — IV-B dataset synthesis; IV-C evaluation; V-A experimental settings. Describes real backgrounds plus synthetic/template targets, plausibility checks and manual filtering, multi-target proportion, 50:50 experiment and metric definitions.
- [Official NUDT-SIRST repository](https://github.com/YeRen123455/Infrared-Small-Target-Detection) — README NUDT-SIRST dataset and split description. Reports 1,327 synthetic 256×256 images and pixel-level masks; published split options do not prove source/template independence.

<a id="d38"></a>

### D38 · SIRST (often called NUAA-SIRST in later papers)

**Evidence inspected.** The original WACV paper sections 3.1–3.4 and official README were inspected. Images, masks, boxes and source/partition manifests were not audited.

**What a sample represents.** The original release contains 427 representative images and 480 target instances. One selected image per source sequence is the stated design; SIRST v2 is a separate release.

**Collection and selection.** Images are selected from infrared sequences spanning several spectral bands and backgrounds. Each target is confirmed by motion in its source video to distinguish real targets from pulse noise, while evaluation retains a single frame.

**Labels and negatives.** The paper describes five annotation forms: category, instance segmentation, bounding box, semantic mask and instance spotting. The current README explicitly confirms boxes and semantic masks and says the rest will come; paper scope and confirmed release documentation differ. About 90% of images contain one target and the published target-number plot starts at one. No dedicated target-free population is documented; background pixels provide negatives within selected images.

**Partitions and independence.** The original paper uses approximately 50% train, 20% validation and 30% test. Later papers vary, so their splits cannot be silently equated with the original protocol. Selecting one representative image per sequence is intended to avoid sequence overlap. It does not independently prove different acquisition sites, underlying targets or source-video lineage without source metadata.

**Quality evidence.** Motion confirmation supplies a documented target-selection check. No mask-boundary adjudication or inter-annotator agreement was verified, and the one-image-per-source rule was not independently checked against a manifest.

**What evaluation means.** nIoU averages image-level overlaps. Fixed-threshold mask scores and a receiver-operating-characteristic curve across thresholds answer different evaluation questions; neither establishes fine-grained object identity or event semantics.

**Interpretation.** This is a generic infrared small-target resource with temporally informed selection and single-frame evaluation. Binary masks do not identify military objects.

**New findings in this review:**

- Motion in the source video confirms target reality before single-frame selection.
- Five annotation forms in the paper exceed the two explicitly confirmed in current release documentation.
- Authors request the name SIRST rather than NUAA-SIRST.

**Still unresolved:**

- Availability of the other paper-described annotation forms; complete source manifest; dedicated negative population; boundary consistency and exact original split files.

**Sources and exact evidence:**

- [Original SIRST WACV paper](https://openaccess.thecvf.com/content/WACV2021/papers/Dai_Asymmetric_Contextual_Modulation_for_Infrared_Small_Target_Detection_WACV_2021_paper.pdf) — 3.1–3.4, dataset construction, annotations, analysis and evaluation protocol. Describes motion-confirmed targets, representative-frame selection, 427 images/480 instances, five annotation forms, target-number distribution and original split/evaluation.
- [Official SIRST repository](https://github.com/YimianDai/sirst) — README naming notice and annotation availability. Requests SIRST naming; explicitly confirms bounding boxes and semantic masks while describing other annotation forms as forthcoming.

<a id="d39"></a>

### D39 · 15-class RGB military-vehicle collection described by TNO studies

**Evidence inspected.** Full-text inspection of the 2026 TNO-associated study, especially its real-dataset subsection; no released image archive or annotation manifest inspected.

**What a sample represents.** 959 RGB images representing 15 vehicle classes. This is the reused real-image collection, not a count of the synthetic images in the later experiment.

**Collection and selection.** The authors explicitly say the images were collected by web scraping and are identical to the collection in their earlier study. Collection locations, original websites and per-image dates are not documented in the inspected subsection.

**Labels and negatives.** The study uses class-labelled bounding boxes for detection evaluation. The inspected real-data section does not establish who drew every original box, the treatment of ambiguous identities, or agreement among annotators. A separately sampled background-only or out-of-vocabulary image population is not established. A class-selected collection cannot be assumed to represent the frequency of empty scenes.

**Partitions and independence.** The paper reports 360 training images (24 per class), 150 validation images (10 per class), and 449 test images (21–50 per class). These sum to 959; class balance differs between training and test. Reuse across the earlier and later studies means those are not two independent real-data collections. Source-site, source-video and physical-object separation across partitions remains unverified.

**Quality evidence.** The paper documents repeated experiments, but repetitions of a model experiment are not an independent label-quality audit. No measured annotation error or deduplication rate was found.

**What evaluation means.** Published box/category scores describe performance on this specific web-image test set. They do not establish accuracy across unrelated sources, continuous video, or unobserved conditions.

**Interpretation.** This is a small, explicitly class-selected research collection whose methodology is partially visible. Its evidence is substantially narrower than a general dataset of scene understanding.

**New findings in this review:**

- Resolved the exact 360/150/449 real-image split and explicit reuse of the earlier collection.
- The 15-class collection remains paper-described; a complete public release and dataset rights were not verified.

**Still unresolved:**

- Original annotation handbook and rights chain.
- Public archive and stable release identifier.
- Source grouping and duplicate-image audit.

**Sources and exact evidence:**

- [Primary TNO-associated study](https://arxiv.org/html/2604.18076) — §3.1, Table 1; §3.3.3. Reports 959 web images, reuse of earlier collection and exact partitions.

<a id="d40"></a>

### D40 · milair-dataset

**Evidence inspected.** Creator README plus a direct GitHub filename-tree check on 10 November 2026. This is a file inventory, not an image or XML-content audit.

**What a sample represents.** 374 image paths and 374 XML paths with matching basename sets in the untruncated public tree. The README class-occurrence sum is 660, a different counting unit.

**Collection and selection.** Images are 1280×720 stills extracted from several YouTube videos. Video-derived stills retain camera, background and object similarities that do not disappear when stored as separate files.

**Labels and negatives.** The repository advertises Pascal VOC aircraft-type boxes for six classes. Matching image/XML basenames establishes file pairing, not valid coordinates, exhaustive boxes or correct types. The README does not define a background-only sample policy, treatment of other aircraft classes, or missing/uncertain objects. Negative-example coverage is therefore unknown.

**Partitions and independence.** No official source-video-independent train/validation/test protocol was established from the README or filename inventory. Multiple frames can depict the same physical aircraft and near-identical scene. Repository MIT licensing does not by itself verify rights to all underlying video frames.

**Quality evidence.** The checked tree was not truncated, and image and annotation stems matched without exceptions. XML values, box counts, visual duplicates and inter-annotator consistency were not inspected.

**What evaluation means.** These files document still-image detection annotations. Frame origin does not establish track IDs, time alignment or a temporal tracking benchmark.

**Interpretation.** The repository is inspectable enough to establish a modest paired-file collection. The most consequential missing evidence concerns source independence and annotation contents.

**New findings in this review:**

- Directly counted 374 image paths and 374 corresponding XML paths.
- Clarified that 660 refers to summed README class occurrences, not the checked unique image-path count.

**Still unresolved:**

- XML object counts, class inventory and coordinate validity.
- Source-video identities and adjacent-frame overlap.
- Underlying video-frame rights and release history.

**Sources and exact evidence:**

- [Creator repository](https://github.com/tlkh/milair-dataset) — README: dataset and class table. Describes YouTube frames, six classes and VOC labels.
- [Checked GitHub tree](https://api.github.com/repos/tlkh/milair-dataset/git/trees/master?recursive=1) — Tree SHA 93d91400fa5b606df32fe030c2b167a45cb9fcff. Untruncated filename inventory: 374 image paths and 374 XML paths with equal basename sets.

<a id="d41"></a>

### D41 · Military Aircraft Detection Dataset (Kaggle v105)

**Evidence inspected.** Owner Kaggle card and version metadata, current version 105 on the review date. No full archive, annotation CSV or image inventory was downloaded.

**What a sample represents.** Images, annotated object boxes and derived crops are distinct units. A verified current unique-image total could not be established from the inspected owner description.

**Collection and selection.** A community collection of visible aircraft photographs with mixed viewpoints. The card names aircraft types but does not establish a complete per-image source or geographic sampling frame.

**Labels and negatives.** The stated CSV schema includes filename, dimensions, class and xmin/ymin/xmax/ymax box coordinates. Separate crop folders expose an object-centred representation of the same source imagery. The card does not establish systematic background-only images, open-category exclusions or whether all visible objects are annotated. Crops by construction also omit much of the surrounding scene.

**Partitions and independence.** A source-independent official split and a correspondence manifest linking all crops back to full images were not verified. Changing ontology, derivative crops and older mirrors can create version overlap. Rights remain unresolved: current owner metadata says Unknown, despite permissive tags on some mirrors.

**Quality evidence.** The owner acknowledges visually similar variants and class consolidation. This is useful ontology documentation, but not a quantified annotation audit or evidence that every difficult example was adjudicated.

**What evaluation means.** Full-image boxes and object crops support different published task formulations. Their scores and sample counts cannot be compared as if they were independent scenes with identical context.

**Interpretation.** This is a version-sensitive community resource. Its explicit box schema is better documented than its source provenance, split independence and current complete inventory.

**New findings in this review:**

- Version 105 describes 114 classes: 103 military-labelled types and 11 commercial types; older 43-class cards are different snapshots.
- Owner metadata records an update on 29 October 2026 and an Unknown licence.

**Still unresolved:**

- Exact image/box counts and per-class distribution for v105.
- Per-image rights and relation to older mirrors.
- Annotation review, duplicate handling and source split policy.

**Sources and exact evidence:**

- [Owner metadata](https://www.kaggle.com/api/v1/datasets/view/a2015003713/militaryaircraftdetectiondataset) — Version 105 metadata and description. Current ontology, update date, box schema and licence field.
- [Owner page](https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset) — Dataset description. Full photographs and crop representations are described.

<a id="d42"></a>

### D42 · Military and Civilian Vehicles Classification (Mendeley v1)

**Evidence inspected.** Versioned Mendeley v1 deposit documentation. No individual image or annotation file was audited.

**What a sample represents.** 6,772 images: 6,642 positive and 130 negative, with 11,528 annotated objects according to the depositor. Object count is not image count.

**Collection and selection.** The deposit provides mixed visible photographs and six broad vehicle/aircraft categories divided into civilian-labelled and military-labelled groups. A reproducible image-acquisition and source-attribution manifest is not exposed in the inspected description.

**Labels and negatives.** TXT, CSV, XML and TFRecord annotations are advertised. Multiple object instances and object-oriented formats make this more than the single image label suggested by its Classification title; exact cross-format equivalence was not checked. An explicit negative subset is a useful distinction. The description does not adequately define whether negative means no vehicle, no in-scope class, or an unannotated image, nor explain how negatives were selected.

**Partitions and independence.** The inspected deposit does not establish how source photographs, related frames or duplicate images were separated across training and evaluation. Potential overlap with community repackagings cannot be quantified without source identifiers. CC BY 4.0 is declared by the deposit; underlying image rights were not individually traced.

**Quality evidence.** Named contributors, a DOI and fixed version support traceability. They do not provide a label-error estimate, a class-confusion audit or proof that all four annotation representations agree.

**What evaluation means.** Category/box labels describe the depositor’s visual categories. They do not establish ownership, affiliation, legal status or observed actions.

**Interpretation.** This deposit has useful versioning and explicit sample units, but scientific interpretation still depends on missing annotation rules and source provenance.

**New findings in this review:**

- The title’s classification wording hides a documented multi-object annotation collection.
- The positive/negative distinction exists but its operational annotation definition remains unspecified.

**Still unresolved:**

- Definition and provenance of 130 negative images.
- Cross-format consistency and complete category counts.
- Source-independent splits and original-image rights.

**Sources and exact evidence:**

- [Mendeley Data v1](https://data.mendeley.com/datasets/njdjkbxdpn/1) — Description; DOI 10.17632/njdjkbxdpn.1. Reports positive/negative images, instance totals, annotation formats and CC BY 4.0.

<a id="d43"></a>

### D43 · Military Assets Dataset (Kaggle v5)

**Evidence inspected.** Owner Kaggle v5 documentation and metadata only; file-level annotations and image contents remain uninspected.

**What a sample represents.** 26,315 author-reported labelled images: 21,978 train, 2,941 validation and 1,396 test. These are split image totals, not independently verified distinct scenes.

**Collection and selection.** The community card describes 12 broad categories spanning vehicles, aircraft, ships, people, equipment and structures. Original collection sources, locations and temporal coverage are insufficiently documented.

**Labels and negatives.** YOLO object annotations are advertised. The card supplies a class list but does not document annotation ambiguity rules, exhaustive labelling requirements, occlusion policy or adjudication of person-role categories. Counts of explicitly empty images and rules for unrelated or ambiguous objects were not established. A missing label file cannot safely be interpreted as a certified negative without inspecting the release policy.

**Partitions and independence.** Named train/validation/test partitions and their sizes are present. The unit used to create these partitions—image, source scene, video, contributor or original archive—is not established. Repackaging or augmentation could alter nominal counts without adding independent source scenes; whether this happened is unverified, not asserted. The upstream rights chain is also unresolved.

**Quality evidence.** A public author, fixed version and declared CC BY 4.0 licence improve traceability. No measured label quality, deduplication report or augmentation accounting was verified.

**What evaluation means.** Any result concerns the supplied broad category and box conventions. Person-role labels are especially limited: a visual category does not establish status, intent or behaviour.

**Interpretation.** The documentation supports an inventory entry but not a strong conclusion about data quality. Its broad vocabulary should not be mistaken for validated scenario annotations.

**New findings in this review:**

- Verified that reported split totals add to 26,315.
- The published split sizes are substantially better specified than the method used to keep their source content independent.

**Still unresolved:**

- Original sources and augmentation history.
- Empty-image and uncertain-label policy.
- Class balance, duplicate audit and split creation method.

**Sources and exact evidence:**

- [Owner metadata](https://www.kaggle.com/api/v1/datasets/view/rawsi18/military-assets-dataset-12-classes-yolo8-format) — Version 5 description and metadata. Twelve classes, split counts and declared licence.
- [Owner card](https://www.kaggle.com/datasets/rawsi18/military-assets-dataset-12-classes-yolo8-format) — Dataset description. Advertised annotation task and collection claims.

<a id="d44"></a>

### D44 · Military-Aircraft-Detection (Illia56 mirror)

**Evidence inspected.** Hugging Face card plus first-page repository tree metadata. The returned 1,000 entries were not a complete paginated inventory.

**What a sample represents.** The card describes 43 aircraft types; a verified unique-image or instance total is unavailable. Crop folders, annotated samples and full-image files are separate representations, not necessarily distinct observations.

**Collection and selection.** A community-hosted aircraft collection whose full connection to a particular upstream release is not established. The file tree visibly includes crop, dataset, memo and annotated_samples directories.

**Labels and negatives.** The card describes Pascal VOC-coordinate boxes. Broad platform tags such as segmentation or depth estimation do not establish the existence of corresponding masks or depth labels. Neither an explicit negative-image policy nor handling of unlisted aircraft types is documented in the inspected card.

**Partitions and independence.** No official independent source-level split was established. An incomplete tree response cannot determine partition counts or provide a complete duplicate analysis. A mirror or derivative may share originals with other aircraft resources. Its Apache-2.0 card tag cannot resolve conflicting or missing upstream image rights.

**Quality evidence.** The card requests reports of duplicates and incorrect labels. This acknowledges possible issues, but it is not a completed correction log or quantified quality-control study.

**What evaluation means.** Only the documented aircraft categories and boxes have an evidentiary basis. The presence of a platform task tag does not create benchmark ground truth for that task.

**Interpretation.** Treat this as a distinct packaging/ontology snapshot until its provenance is traced, rather than as a demonstrated independent collection.

**New findings in this review:**

- Direct tree metadata confirmed separate crop and annotated-example folders.
- The 1,000-entry API response is explicitly incomplete; no full size is inferred from it.

**Still unresolved:**

- Exact upstream source and version mapping.
- Complete pagination, image inventory and full-image/crop associations.
- Licence chain and annotation correction history.

**Sources and exact evidence:**

- [Raw dataset card](https://huggingface.co/datasets/Illia56/Military-Aircraft-Detection/raw/main/README.md) — Card text and metadata. 43-type description, box coordinates, task tags and licence.
- [Checked first tree page](https://huggingface.co/api/datasets/Illia56/Military-Aircraft-Detection/tree/main?recursive=true&limit=1000) — First 1,000 entries returned on review date. Directory structure only; not complete counts.

<a id="d45"></a>

### D45 · RGB military-target collection described by Jeong et al. (2025)

**Evidence inspected.** Full 2025 manuscript, including dataset construction and Table 2. The paper still promises public release upon acceptance; a usable released archive was not verified.

**What a sample represents.** Table 2 gives 14,944 synthetic training instances, 1,267 real training instances and 514 real validation instances. These are explicitly object-instance totals, not image totals.

**Collection and selection.** Synthetic RGB imagery comes from rendered scenes; real image/label pairs are compiled from six existing Roboflow collections. This is a derivative real-image compilation, not an entirely new independently captured photographic collection.

**Labels and negatives.** Six matched broad classes and bounding boxes are described. The manuscript does not provide a sufficient independent adjudication or inter-annotator study for the merged real labels. A systematic background-only population is not established. Synthetic postprocessing excludes extremely small, repeated/stagnant, unrecognizable and out-of-class samples, so the published collection is filtered by recognizability.

**Partitions and independence.** Real training/validation size is worded as 600/174 in §III-B, but its surrounding per-class phrasing is ambiguous. A reliable unique-image manifest is needed before turning that wording into a total. The real subset inherits upstream annotation conventions and potentially repeated originals across community sources. Synthetic scene reuse also limits independent environmental diversity.

**Quality evidence.** Explicit filtering criteria are valuable documentation but do not quantify residual error. Manual removal of repeated frames is not evidence of a complete duplicate or source-overlap audit.

**What evaluation means.** The experiment concerns correspondence between a filtered synthetic collection and a small compiled real-image set. It does not establish broad distributional coverage or scene-level event truth.

**Interpretation.** This remains a paper-described derivative collection with unresolved image accounting and access. Its methodological claims should be separated from verified release contents.

**New findings in this review:**

- Replaced vague size claims with the paper’s exact instance totals.
- The real data are sourced from existing Roboflow image/label collections; release remains promised at a placeholder LINK.

**Still unresolved:**

- Unique-image totals and interpretation of 600/174 wording.
- Actual archive, release licence and constituent rights.
- Merged-label consistency and source overlaps.

**Sources and exact evidence:**

- [Jeong et al. manuscript](https://arxiv.org/pdf/2512.23208) — Abstract; Table 2; §III-A/B, PDF pp.5–6; conclusion release footnote. Instance totals, filtering policy, Roboflow origins and promised release.

<a id="d46"></a>

### D46 · CAMO

**Evidence inspected.** Full original CAMO paper (CVIU 2019, later arXiv posting) and creator documentation. Images and segmentation masks were not independently audited.

**What a sample represents.** The paper distinguishes CAMO: 1,250 camouflage-positive images, from CAMO-COCO: those 1,250 plus 1,250 COCO negatives, totalling 2,500. The earlier catalogue used the combined count under CAMO.

**Collection and selection.** About 3,000 web-search candidates were reduced to 1,250 by manually removing duplicates and low-resolution images. Content includes natural animal camouflage and artificial human camouflage.

**Labels and negatives.** Three people independently marked each positive image using an interactive segmentation tool. Masks represent camouflaged foreground; they are not fine-grained object identities. The paper reports 2–5 minutes per annotator/image. The COCO comparison half has all-zero camouflage masks even when ordinary objects are visible. Negative therefore means no camouflaged foreground, not no object.

**Partitions and independence.** Each positive/negative half is randomly split 1,000 train / 250 test. Source-site or source-photo grouping across these splits is not established. COCO reuse creates a known dependency on an existing collection. Natural and artificial camouflage categories do not establish a general military identity taxonomy. CAMO++ is a separate extension.

**Quality evidence.** Multiple independent annotators and documented filtering provide process evidence. Their agreement, reconciliation procedure and residual pixel error are not quantified in the inspected sections.

**What evaluation means.** CAMO-only segmentation assumes camouflage is present; CAMO-COCO also examines responses when it is absent. These evaluation populations should not be conflated.

**Interpretation.** The key scientific distinction is camouflage foreground versus ordinary visible objects. Its negative policy makes that distinction explicit.

**New findings in this review:**

- Corrected the naming distinction between 1,250-image CAMO and 2,500-image CAMO-COCO.
- Verified zero masks for non-camouflaged COCO images and three independent annotators.

**Still unresolved:**

- Annotator agreement and mask reconciliation.
- Source-level independence after random splitting.
- Per-image source rights beyond declared noncommercial terms.

**Sources and exact evidence:**

- [Original CAMO paper](https://arxiv.org/html/2105.09451) — §3.2–3.3; §5.1 and Table 2. Candidate filtering, three annotators, separate CAMO/CAMO-COCO definitions, zero masks and random split.
- [Creator page](https://sites.google.com/view/ltnghia/research/camo) — Dataset and licence. Creator release links and CC BY-NC-SA 4.0 declaration.

<a id="d47"></a>

### D47 · COD10K

**Evidence inspected.** Full CVPR 2020 paper plus creator repository. No mask archive or image-level visual audit performed.

**What a sample represents.** 10,000 total images with a 6,000/4,000 train/test split. The main camouflage segmentation evaluation uses 2,026 camouflage-positive test images, not all 4,000 test images.

**Collection and selection.** Web-collected natural scenes are organized into 78 categories: 69 camouflage and nine noncamouflage. The full collection includes camouflage positives, ordinary noncamouflaged objects and background examples.

**Labels and negatives.** Category labels, boxes, object-level masks, instance labels and challenge attributes are described. The paper reports 5,069 object-level masks and 5,930 instance ground truths; these units need not equal image count. Section 3.1 initially reports 5,066 camouflage, 3,000 background and 1,934 noncamouflage images. Later prose swaps the descriptions attached to the two noncamouflage counts; this internal inconsistency remains unresolved here.

**Partitions and independence.** Random splitting is performed within subclasses. This preserves category representation but does not demonstrate separation of original websites, related photographs or physical scenes. Web imagery can overlap other camouflage collections; no exhaustive cross-dataset image comparison was done. Its natural categories do not constitute a military identity or scenario ontology.

**Quality evidence.** The paper describes three reviewers and a re-verification process using the phrase 10-fold cross-validation. This wording documents a review procedure, not a measured annotation error rate or ten independent dataset releases.

**What evaluation means.** Reported segmentation measures assess foreground masks on the selected benchmark subset. Full-release size and benchmark-test size therefore answer different questions.

**Interpretation.** The collection has unusually rich annotation types, but counting conventions and benchmark subset selection are essential to interpreting it correctly.

**New findings in this review:**

- Distinguished the 2,026 positive evaluation images from the full 4,000-image test partition.
- Preserved the paper’s conflicting background/noncamouflage count descriptions rather than silently choosing one.

**Still unresolved:**

- Reconciliation of the two negative-subset descriptions.
- Mask agreement and current archive-version accounting.
- Cross-dataset source overlap.

**Sources and exact evidence:**

- [CVPR 2020 paper](https://openaccess.thecvf.com/content_CVPR_2020/papers/Fan_Camouflaged_Object_Detection_CVPR_2020_paper.pdf) — §3.1 and benchmark dataset subsection. Annotation hierarchy, full/positive split sizes and inconsistent negative-subset descriptions.
- [Creator repository](https://github.com/DengPingFan/SINet) — Dataset downloads and terms. Release packaging and noncommercial restrictions.

<a id="d48"></a>

### D48 · FSAR-Cap

**Evidence inspected.** Full preprint plus current creator release announcement and public file-list metadata. The linked Science Data Bank V1 archive was not downloaded.

**What a sample represents.** 14,480 source images and 72,400 caption associations: five descriptions per image. Images derive from FAIR-CSAR and are not a new independent sensor acquisition.

**Collection and selection.** The paper describes 22 underlying object categories across 32 source locations. Ten scene categories are added through a scene classifier, alongside information extracted from detection annotations.

**Labels and negatives.** Initial text uses 25 templates for counts, image-relative position and box-derived size/shape. Humans correct and supplement these descriptions; a language model then standardizes them into five captions per image. The paper does not establish a separate verified object-free or unknown-scene benchmark. Absence from a detection annotation cannot establish absence from the underlying image.

**Partitions and independence.** The experimental split is 10,000 training, 2,240 validation and 2,240 test images. Separation of the 32 source locations across those partitions is not demonstrated by an inspected manifest. It shares imagery with FAIR-CSAR. Five captions increase linguistic supervision but not independent visual scenes. Scene labels generated by a classifier introduce another potential error source before human review.

**Quality evidence.** Manual verification is explicitly described, but annotator count, agreement and residual factual error are not quantified. Caption length, token volume and a word cloud do not measure correctness.

**What evaluation means.** Caption similarity measures agreement with reference language. Fluent references generated from existing labels can preserve inherited omissions; language similarity alone is not a factual scene audit.

**Interpretation.** This is an expanded textual annotation layer over existing imagery. Its value as a documented language resource should be distinguished from evidence of independent scene understanding.

**New findings in this review:**

- Verified the 10,000/2,240/2,240 experimental split and multi-stage label construction.
- Updated access evidence: the creator now links a Science Data Bank V1 release; archive completeness and licence remain unchecked.

**Still unresolved:**

- Source-location grouping and actual caption manifest.
- Post-language-model factual audit.
- V1 archive completeness and dataset licence.

**Sources and exact evidence:**

- [FSAR-Cap paper](https://arxiv.org/html/2510.16394v1) — §II-A–D; §III-A. Annotation stages, underlying imagery, captions and split.
- [Creator release](https://github.com/hitjiao/FSAR-Cap) — README release announcement. Public V1 link is now present.
- [Science Data Bank V1](https://www.scidb.cn/en/detail?dataSetId=e4c17cc137e74878b46c03d8650ffa78&version=V1&code=o00118) — Creator-linked landing page. Release pointer verified; archive contents not checked.

<a id="d49"></a>

### D49 · Functional Map of the World (fMoW)

**Evidence inspected.** Full primary fMoW paper, creator data guide and licence. No full imagery or geospatial split manifest inspected.

**What a sample represents.** The headline exceeds one million images, but temporal sites and paired pansharpened/multispectral products are distinct units. Reported unique boxes are 83,412 train, 14,241 validation, 16,948 test and 18,115 seq.

**Collection and selection.** Candidate functional locations originate in map/volunteered geographic information, followed by crowd validation and image selection. About 30% of candidate imagery was removed for cloud cover.

**Labels and negatives.** Annotators mark selected regions with functional categories and acquisition metadata. The paper describes 642 GeoHIVE users, about 2,800 annotation hours and a second crowd grading boxes. Scenes are not exhaustively annotated for every surrounding object. The provided regions focus evaluation on selected categories; the false-detection category does not turn all unmarked pixels into reliable negatives.

**Partitions and independence.** Temporal sequences are assigned to partitions while balancing binned metadata. This is a documented sequence-level design, though the underlying complete location manifest was not independently checked. Repeated observations of a site and paired spectral products are correlated. 21.2% of sequences have one view; 95% have ten or fewer, with a maximum of 41. A sequence is not continuous video.

**Quality evidence.** Multiple review stages are described and residual geographical bias is acknowledged. Neither annotation hours nor crowd size constitutes a verified residual error rate.

**What evaluation means.** Its core task classifies the function of supplied regions. The presence of boxes should not be mistaken for exhaustive full-scene object-detection ground truth.

**Interpretation.** This is a contextual, temporal function-classification resource. Its annotation policy is fundamentally different from an exhaustively labelled object scene.

**New findings in this review:**

- Clarified selected-region annotation and its effect on interpreting unlabelled surrounding objects.
- Separated temporal acquisitions from paired image products and documented the sequence-size distribution.

**Still unresolved:**

- Independent verification of location grouping and complete release counts.
- Class- and geography-specific annotation reliability.
- Version-specific correspondence between full and RGB products.

**Sources and exact evidence:**

- [Primary fMoW paper](https://arxiv.org/html/1711.07846v3) — §3–4; Appendix II. Collection pipeline, QC, partial scene annotations, sequence properties and partitions.
- [Creator guide](https://github.com/fMoW/dataset) — README. Product definitions and access.
- [Data licence](https://raw.githubusercontent.com/fMoW/dataset/master/LICENSE) — Functional Map of the World Challenge Public License. Custom data terms; trained algorithms excluded from Adapted Material definition.

<a id="d50"></a>

### D50 · LEVIR-CC

**Evidence inspected.** Read the recovered 20-page original paper, especially section III, and creator repository documentation. Caption JSON, imagery and archive contents were not independently audited.

**What a sample represents.** 10,077 before/after image pairs and 50,385 caption records, five per pair. Published counts separate 5,038 changed and 5,039 no-change pairs; multiple captions are not independent visual observations.

**Collection and selection.** The paper says imagery mainly derives from LEVIR-CD: 20 Texas regions, 0.5 m/pixel and 5–15-year intervals. Original 1024×1024 pairs are cropped to 256×256. Pixel registration is an author claim, not an independently measured error bound.

**Labels and negatives.** Five different annotators provide descriptions per pair. Instructions emphasize significant object changes and appearing/disappearing objects while excluding irrelevant appearance differences. No-change pairs use five prescribed sentences; these are standardized references, not unrestricted independent descriptions. LEVIR-MCI masks are a separate release product. No-change means only irrelevant changes under the annotation policy. Examples ignore lighting, shadows and small tree-related changes; it does not mean pixel identity or absence of all real-world activity.

**Partitions and independence.** Table I gives 6,815 training, 1,333 validation and 1,929 test pairs. Changed/no-change counts are 3,407/3,408, 667/666 and 964/965 respectively. These nearly balanced assignments do not establish source-image or regional separation. Derived subtiles can share parent imagery, and the collection primarily reuses LEVIR-CD. Five fixed no-change references and multiple descriptions per pair do not add independent scenes.

**Quality evidence.** Authors checked spelling and grammar. Their human-agreement experiment scores one reference against four others using BLEU, METEOR and ROUGE-L. This measures linguistic agreement, not independent factual correctness or annotator consensus about every visible change.

**What evaluation means.** Reference-caption scores concern visible differences. The paper omits CIDEr-D for its no-change-only evaluation because repetitive vocabulary drives that metric near zero, illustrating how reference construction changes metric interpretation.

**Interpretation.** The primary paper substantially strengthens the methodological record, while its label definition remains narrower than unrestricted change or event understanding.

**New findings in this review:**

- Recovered exact partitions, near-equal changed/no-change sampling and prescribed no-change language.
- Separated the paper's reference-agreement measurement from factual annotation validation.

**Still unresolved:**

- Manifest-level source-image and regional split independence.
- Independent visual/factual caption audit and residual registration error.
- Underlying image rights relative to the HF Apache-2.0 tag.

**Sources and exact evidence:**

- [Original LEVIR-CC paper: Remote Sensing Image Change Captioning with Dual-branch Transformers](https://levir.buaa.edu.cn/publications/ChangeCaptioning.pdf) — Section III-A–C, PDF pp.4–7; Tables I and IV; section V-C and Table VII. Recovered 20-page primary PDF; documents mainly LEVIR-CD imagery, five annotators, prescribed no-change references, exact splits, grammar correction, reference-agreement experiment and no-change-only CIDEr-D limitation. Extracted text retained as evidence/deep_levircc2022.txt.
- [Creator dataset repository](https://github.com/Chen-Yang-Liu/LEVIR-CC-Dataset) — LEVIR-CC and LEVIR-MCI sections. Confirms pair/sentence counts, folder layout and separate mask-bearing LEVIR-MCI resource.
- [Author-linked file list](https://huggingface.co/api/datasets/lcybuaa/LEVIR-CC/tree/main?recursive=true&limit=1000) — Returned public tree on review date. Archive and README are visible; caption JSON was not separately inspected and archive contents were not audited.

<a id="d51"></a>

### D51 · LEVIR-CD (original release)

**Evidence inspected.** Creator dataset page and original STANet repository documentation. Publisher full text returned HTTP 403; no image/mask archive was audited.

**What a sample represents.** 637 original 1024×1024 image pairs at 0.5 m/pixel, with 31,333 changed-building instances according to the creator. Later 256×256 tiles are derivatives of these original pairs.

**Collection and selection.** Google Earth imagery covers 20 regions in Texas, with acquisition years 2002–2018 and paired intervals of 5–14 years. Seasonal and illumination differences are intentionally present.

**Labels and negatives.** Experts mark binary building-related change: new construction or decline. Every sample is labelled by one interpreter and checked by another according to the creator. Zero denotes no annotated building change. It does not mean no other change, no building, or no activity. Seasonal appearance differences are meant to remain negative for this particular label definition.

**Partitions and independence.** Official train/validation/test folder structure is documented. STANet describes non-overlapping 256×256 crops. Geographic independence of all partitions was not established by an inspected spatial audit. Spatially adjacent chips and all subtiles of an original image share context. The original LEVIR-CD and the later LEVIR-CD+ extension are different releases.

**Quality evidence.** Two-person review gives process evidence but no measured residual error or boundary agreement. The creator added per-sample geographic information in 2023, making source-location relationships more inspectable.

**What evaluation means.** Masks measure visible building change between two dates. They neither date an intervening event precisely nor explain the cause of disappearance or construction.

**Interpretation.** This is a well-bounded building-change task with a documented review process, but restricted geography and broad time gaps limit interpretation beyond that label definition.

**New findings in this review:**

- Confirmed the exact meaning of zero labels and the original-to-subtile relationship.
- Creator documentation records a 2023 geographic-metadata supplement, not a new independent image collection.

**Still unresolved:**

- Spatial split audit using the geographic supplement.
- Residual annotation error and boundary conventions.
- Release-specific original-pair versus subtile inventories.

**Sources and exact evidence:**

- [Creator LEVIR-CD page](https://justchenhao.github.io/LEVIR/) — Overview, geographical distribution, News and Usage. Original sample units, two-person annotations and academic-only terms.
- [STANet README](https://raw.githubusercontent.com/justchenhao/STANet/master/README.md) — Change log; Prepare Datasets. 2023 geospatial supplement, folder splits and non-overlapping patch derivatives.

<a id="d52"></a>

### D52 · RSICD

**Evidence inspected.** Creator documentation plus direct parsing of the public annotation JSON; exact filename/string comparisons only. No image pixels or caption correctness were audited.

**What a sample represents.** Verified 10,921 image records with 10,921 distinct filenames and 54,605 sentence records, exactly five per image. Five records do not imply five distinct texts.

**Collection and selection.** Creator documentation lists Google Earth, Baidu Map, MapABC and Tianditu imagery, standardized to 224×224 with varying original resolution. A complete original-source/location manifest is not established.

**Labels and negatives.** The JSON associates raw sentences and tokens with image identifiers and split fields. The inspected metadata establishes associations, not whether sentences are complete or visually correct. This is not a foreground/background detector benchmark. Captions can omit visible objects; omission from a sentence is not evidence of absence.

**Partitions and independence.** Directly counted 8,734 train, 1,094 validation and 1,093 test image records. Unique filenames do not prove source-scene or pixel independence across those partitions. Image records can originate from shared maps or nearby locations, and repeated generic sentences can occur across unrelated scenes. The check did not measure visual duplication or semantic equivalence.

**Quality evidence.** There are 18,190 globally distinct raw exact caption strings. Within-image comparisons trim outer whitespace: 10,197 images have repeated strings among their five captions; only 724 have five distinct captions.

**What evaluation means.** Text-reference metrics reflect this repeated reference structure. Repetition reduces reference diversity but does not alone establish incorrect captions or invalid benchmark results.

**Interpretation.** The most substantial new evidence is a reproducible distinction between sentence-record count and reference-language diversity. It warrants precise wording about what five captions means.

**New findings in this review:**

- Verified split/image/caption counts directly from creator JSON.
- Per-image distinct-caption counts: 4,853 have one; 1,667 two; 2,182 three; 1,495 four; 724 five.

**Still unresolved:**

- Reason for repeated caption records and any corrected release.
- Independent visual/factual caption audit.
- Original image rights, spatial overlap and source-level partitions.

**Sources and exact evidence:**

- [Creator repository](https://github.com/201528014227051/RSICD_optimal) — README. Image sources and caption structure.
- [Inspected annotation JSON](https://raw.githubusercontent.com/201528014227051/RSICD_optimal/master/dataset_rsicd.json) — SHA256 5e342037d469d074711676bdb9c02b6942a624530b1959d24d2734e68af9cede. Parsed record counts and exact-string checks saved in deep_metadata_checks.json.

<a id="d53"></a>

### D53 · RSVQA-HR

**Evidence inspected.** Full primary RSVQA paper v2 and creator repository; no complete image or QA archive independently audited.

**What a sample represents.** 10,659 image patches and 1,066,316 question–answer pairs from 161 source tiles. Many questions reuse each patch.

**Collection and selection.** USGS aerial RGB orthophotos, 512×512 patches. The dataset subsection states 15 cm and a matching patch area; the conclusion instead says 30 cm, an internal discrepancy.

**Labels and negatives.** OSM features and question templates generate presence, counting, comparison and area questions. Counts are exact answer categories; areas are quantized. Rural/urban questions belong to LR, not HR. A no/zero answer means no matching mapped entity under the query definition. Missing OSM entries, misregistration or acquisition-date mismatch can produce an incorrect apparent negative.

**Partitions and independence.** The paper separates source tiles and includes a second test set in Philadelphia with a sensor absent from training; the first test set covers similar regions to training. Manifest-level verification remains open. Questions from one patch are correlated, and template vocabulary is narrower than unrestricted conversation. Neither answer accuracy nor mapped relations establishes open-ended scenario comprehension.

**Quality evidence.** The paper openly discusses incomplete map annotations and date mismatch. Automatic generation is reproducible but is not an independent human verification of every image/answer pair.

**What evaluation means.** The original model still achieved 73.78% overall accuracy on test 1 and 72.51% on test 2 when images were randomly reassigned to questions. These author-reported controls show strong answer/language priors.

**Interpretation.** This is a constrained map-derived visual-question benchmark. Its clearest contribution is explicit question construction and split methodology, accompanied by unusually candid bias analysis.

**New findings in this review:**

- HR separates in-region and unseen-region/sensor tests; those test scores have different meanings.
- The paper includes a random-image control, a stronger caution about language bias than headline QA accuracy alone.

**Still unresolved:**

- QA factual correctness after time alignment.
- Complete source manifest and current download availability.
- Resolution wording discrepancy and map/image rights chain.

**Sources and exact evidence:**

- [Primary RSVQA paper](https://arxiv.org/html/2003.07333v2) — §II-A–C; §IV Language biases and Generalization to unseen areas. Collection, map-derived labels, tile splits, question differences and random-image control.
- [Creator repository](https://github.com/syvlo/RSVQA) — README and code licence. Code availability; code licence does not establish unified data rights.

<a id="d54"></a>

### D54 · RSVQA-LR

**Evidence inspected.** Full primary RSVQA paper v2 and creator repository; no complete image or QA archive independently audited.

**What a sample represents.** 772 image patches and 77,232 question–answer pairs from nine source tiles. The QA total does not represent 77,232 independent visual scenes.

**Collection and selection.** Low-cloud Sentinel-2 RGB tiles over the Netherlands, at 10 m resolution, divided into 256×256 patches. Only nine source tiles underlie the patch collection.

**Labels and negatives.** OSM and templates generate presence, comparison, counting and rural/urban questions. Count answers are binned; rural/urban is a building-density rule, not independent land-use adjudication. A no/zero answer means no matching mapped entity under the query definition. Missing OSM entries, misregistration or acquisition-date mismatch can produce an incorrect apparent negative.

**Partitions and independence.** Source tiles, rather than individual questions, are split 7 training / 1 validation / 1 test. This limits spatial leakage, though the small number of source tiles constrains geographic breadth. Questions from one patch are correlated, and template vocabulary is narrower than unrestricted conversation. Neither answer accuracy nor mapped relations establishes open-ended scenario comprehension.

**Quality evidence.** The paper openly discusses incomplete map annotations and date mismatch. Automatic generation is reproducible but is not an independent human verification of every image/answer pair.

**What evaluation means.** The original model retained 73.78% overall accuracy with randomly reassigned images, versus about 79.08% normally. This author-reported control shows that many correct answers need little image evidence.

**Interpretation.** This is a constrained map-derived visual-question benchmark. Its clearest contribution is explicit question construction and split methodology, accompanied by unusually candid bias analysis.

**New findings in this review:**

- LR rural/urban labels are rule-generated and its numerical answers are categories, not precise counts.
- The paper includes a random-image control, a stronger caution about language bias than headline QA accuracy alone.

**Still unresolved:**

- QA factual correctness after time alignment.
- Complete source manifest and current download availability.
- Objects below visible resolution and map/image rights chain.

**Sources and exact evidence:**

- [Primary RSVQA paper](https://arxiv.org/html/2003.07333v2) — §II-A–C; §IV Language biases and Generalization to unseen areas. Collection, map-derived labels, tile splits, question differences and random-image control.
- [Creator repository](https://github.com/syvlo/RSVQA) — README and code licence. Code availability; code licence does not establish unified data rights.

<a id="d55"></a>

### D55 · SARChat-2M / SARChat-Bench

**Evidence inspected.** Full paper v5 and creator repository. The README dataset URL remained a YourOrg/SARChat placeholder at review; no released dialogue archive was verified.

**What a sample represents.** 2,063,548 dialogue samples: 1,836,912 training and 226,636 test. They reuse SARDet-100K imagery and labels rather than introducing two million independently acquired images.

**Collection and selection.** SARDet-100K already combines multiple source datasets. SARChat adds six language task families over those inherited object annotations.

**Labels and negatives.** Templates derive category, counts, box coordinates, image-relative positions and size/shape descriptions. Here cross-modal identification receives coordinates and describes attributes; it is not evidence of paired optical/SAR acquisitions. Missing source boxes can propagate into incorrect counts or absent descriptions. The authors even show an example containing an additional object absent from original annotations; exhaustive scene truth is therefore not established.

**Partitions and independence.** Train/test dialogue totals are reported. Complete source-image and constituent-dataset partition independence were not verified from a downloaded dialogue manifest. Many tasks repeat each image. Roughly 77.5% of dialogue entries are cross-modal identification, so the overall two-million count is strongly influenced by one task’s generation scheme.

**Quality evidence.** The fine-grained description subset filters small images, very small or unusually shaped boxes and invalid coordinates. These checks concern geometry and selection, not independent verification of category identity or caption truth.

**What evaluation means.** The benchmark evaluates structured tasks, including box overlap and attribute agreement. A geometry-derived description score is narrower evidence than an independently verified explanation of a scene.

**Interpretation.** This is a large structured-text derivative whose core evidence comes from existing annotation geometry. Its scale and language form should not obscure inherited source limitations.

**New findings in this review:**

- Clarified the paper’s cross-modal identification term and strong task-count imbalance.
- The public release remains unverified because the official dataset link is a placeholder; paper and code access are different.

**Still unresolved:**

- Actual public dialogue archive and image-ID split audit.
- Correction of missing source annotations.
- Constituent licence reconciliation with repository CC BY-NC 4.0.

**Sources and exact evidence:**

- [Primary SARChat v5](https://arxiv.org/html/2502.08168v5) — §3.1.2–3.1.3; §5.4; Appendix A.3. Task definitions, generated labels, omission example and task counts.
- [Creator repository](https://github.com/JimmyMa99/SARChat) — Dataset link and README. Placeholder release URL at review.
- [Repository licence](https://raw.githubusercontent.com/JimmyMa99/SARChat/main/LICENSE) — CC BY-NC 4.0. Repository terms; does not independently resolve constituent data rights.

<a id="d56"></a>

### D56 · xBD

**Evidence inspected.** Full primary xBD paper, including annotation instructions and limitations; no image or polygon archive independently audited.

**What a sample represents.** 22,068 pre/post images across 19 disasters; 850,736 polygon annotations. The damage-class counts sum to 425,368, consistent with pre/post representation, so 850,736 must not be called unique buildings.

**Collection and selection.** Disaster areas are selected to include damage and surrounding negative buffer. This deliberate selection is not an unbiased sample of all buildings or disaster damage prevalence.

**Labels and negatives.** Pre-event building polygons are transferred to post-event imagery, then assigned ordinal damage levels. Post-event buildings without transferred pre-event polygons are deliberately ignored. Environmental factors use polygons in the detailed method, although the abstract calls them boxes. No damage is a labelled category, but unannotated post-event structures are not certified negatives. Selection and transferred footprints determine which buildings enter assessment.

**Partitions and independence.** Exact reported image counts are 18,336 train, 1,866 test and 1,866 holdout. The paper also says 80/10/10, which does not match those exact image counts; the discrepancy is retained. Pre/post images share footprints and buildings; crops can share event context. Strong class imbalance favours no damage, and environmental visibility varies across disasters.

**Quality evidence.** Multiple annotation rounds and expert review are described. Experts found and corrected 2–3% errors in a random sample, but no sample size or guarantee of the remaining error rate is provided.

**What evaluation means.** Damage classes are approximate interpretations from satellite imagery, explicitly distinguished by the authors from authoritative on-site structural inspection. They do not identify the cause of arbitrary damage.

**Interpretation.** This dataset supports a specific humanitarian observation: visible building damage after known disasters. Its annotation instructions are as consequential as its large headline scale.

**New findings in this review:**

- Clarified the pre/post polygon counting unit and deliberately ignored unmatched post-event buildings.
- Documented the qualified 2–3% correction statement, geometry wording conflict and split-percentage mismatch.

**Still unresolved:**

- Complete release counts and explanation of split percentages.
- Expert audit sample size and residual uncertainty.
- Release-specific licence and event/geographic partition audit.

**Sources and exact evidence:**

- [Primary xBD paper](https://arxiv.org/html/1911.09296) — §3–6, annotation and statistics sections. Polygon transfer, ignored buildings, exact counts, QC and limitations.
- [Official landing page](https://xview2.org/dataset) — Dataset access. Release workflow not verified in this review.

## What this review establishes

The catalogue now has a deeper, source-linked explanation for every one of its 56 entries. It identifies what is labelled, how labels were generated, where source dependence is known, and which apparent contradictions remain open. It does not establish a single overall quality order, raw-image cleanliness across all releases, or a measured improvement of any application.

Claims about scenario understanding need to be read at the level of the annotations: visible category, location, temporal continuity, defined change, mapped relation or reference description. None of the reviewed evidence by itself establishes a general capacity to infer hidden intent or causal explanations. Model and hardware research remains a separate later stage.
