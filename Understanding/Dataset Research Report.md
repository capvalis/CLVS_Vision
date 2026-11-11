# Public military and related computer-vision datasets

Literature and dataset-documentation review | 10 November 2026

This catalogue contains **56 dataset or release entries across 8 families**, with **136 distinct source URLs**. Versions, derivatives and public-paper-only collections are counted as separate entries where that distinction matters. This is not a count of independent image collections, a claim to have found every dataset, or an audit of downloaded image archives.

The review addresses what datasets contain, how objects or scenes are labelled, which sensor and media types they use, how the labels were obtained, and what the documented evidence says about provenance, access, licensing and quality. Military-labelled datasets are explicitly distinguished from general remote-sensing, civilian, natural-camouflage and humanitarian datasets often mentioned in the same literature. No dataset is ranked for military use, and this report does not prescribe combinations, training recipes or an operational recognition system.

The request also distinguishes detecting objects from understanding a scenario. This report therefore records the **meaning actually supplied by the annotations**, rather than inferring capability from a dataset's title. The objective of comparing achievable performance remains open. Model comparisons, deployment measurements and the separate DEIMv2 licence issue belong to the later phase requested by the user.

## How to read the evidence

The source material was checked through creator repositories, project pages, primary papers, publisher/deposit metadata, original licence texts and public dataset cards. An accessible webpage is recorded separately from a verified data download. No access requests were submitted. No full image/video dataset archives were downloaded. Public repository file listings were checked in a few cases, notably SAMPLE, and are identified as such.

**Documented strengths** below means a property supported by the publication or creator's documentation. It does not mean an independent verification of label correctness. **Limitations** distinguish reported defects or contradictions from questions that still require a file-level audit. Missing evidence is described as missing, not treated as proof of poor data. There is no invented numerical quality score.

General search engines were unreliable in this session, so discovery relied mainly on primary-project links, arXiv searches, repository/dataset indices and citation-following. The register covers the major identified public families and selected recent papers through the review date. Restricted, private, undisclosed and newly published resources can be absent. Sparse community mirrors are represented as such, rather than counted as independent primary datasets.

## Dataset families

| Family | Entries | What distinguishes the family |
|---|---:|---|
| SAR imagery | 8 | Radar imagery, often cropped recognition chips or satellite detection patches. Radar scattering is a different measurement from visible appearance. |
| Overhead optical imagery | 16 | Satellite/aerial photographs with image labels or horizontal/oriented boxes, sometimes ship/aircraft attributes. |
| Visible and thermal imagery | 5 | Visible, near-infrared or thermal bands, including paired/registered field trials and object annotations. |
| Video tracking | 6 | Sequences with boxes and object identities across time. Label frequency and absent-object flags matter. |
| Infrared small spots | 3 | Small bright or low-contrast foreground regions, usually binary masks. Spot localization does not supply object identity. |
| Web and synthetic imagery | 7 | Photographs, video stills or rendered imagery. Original media rights, duplication and release availability vary. |
| Camouflage segmentation | 2 | Masks for objects blending into a background, frequently natural subjects. Camouflage labels are not military-role labels. |
| Scene, change and language | 9 | Region function, pre/post change, captions or question-answer pairs. Text may be human-written or derived from existing annotations. |

## What the labels mean

| Annotation | Information it supplies | Information it does not establish by itself |
|---|---|---|
| Image or crop category | A label for an image or a preselected object chip | Location of every object in a full scene; independence of the original observations |
| Horizontal bounding box | Rectangular image extent and assigned category | Exact silhouette, heading, actions or intent |
| Oriented box / quadrilateral | Rotated extent of an elongated object | A true pixel mask or verified physical movement direction |
| Semantic foreground mask | Which pixels belong to foreground or a category | Separate object identity when instances touch; detailed type |
| Instance mask | Separate outlines for each annotated object | Temporal continuity or hidden state |
| Track ID | The same annotated object across frames | Its real-world identity, affiliation, purpose or an explanation of the event |
| Attributes | Explicit properties such as shape, broad role or visibility | Properties omitted from the ontology or ambiguous from the imagery |
| Pre/post change label | Visible difference between two acquisition times | Cause, intent or everything that occurred between the images |
| Caption / question-answer pair | A description or answer in a specified annotation scheme | Grounded truth about all possible questions or unobserved events |
| Clip-level action brief | A documented description of a scripted or observed sequence | Dense event boundaries, per-frame action labels or real-world event attribution unless separately supplied |

Sensor labels also require care. RGB is visible colour. NIR is near-infrared and is not the same as heat imagery. MWIR/LWIR measure different thermal infrared bands. SAR measures radar backscatter; amplitude chips, complex-valued products and different polarizations are not interchangeable representations. A paired RGB/thermal collection is not necessarily geometrically registered, and a registered pair is not evidence that all objects have labels in both sensors.

## Findings that change how this literature should be read

1. **There is no single meaning of military dataset.** The catalogue includes controlled vehicle collections, web photographs with assigned military categories, aircraft/ship taxonomies, general satellite benchmarks, and adjacent datasets that have no military identity labels. Dataset sponsorship, an application mentioned in a paper, and actual annotation content are three different things.

2. **Counts use incompatible units.** Images, source scenes, cropped chips, object instances, frames, image pairs and text pairs cannot be summed. FGSC-23 contains 22 ship categories plus one negative class. VTUAV's image-pair total is far larger than its sparse annotation count. SARChat's roughly two million examples are dialogue samples derived from a much smaller image base. Exact units and discrepancies are retained in each card.

3. **Naming does not resolve an ontology.** The word tank may describe storage infrastructure, and xView's Tank Car is a railway category. Broad aircraft/ship labels do not imply military subtype, affiliation or intent. A dataset card's list of supported tasks does not prove that all those annotation types exist.

4. **Derivative collections reuse evidence.** DOTA releases reuse earlier imagery; DIOR-R reannotates DIOR; MTARSI 2 changes the original classification; ShipRSImageNet draws from xView, HRSC2016, FGSD and others; SARDet-100K combines ten sources; SARChat builds on SARDet; FSAR-Cap builds on FAIR-CSAR. This establishes overlap in origin, not a measured duplicate percentage.

5. **Documentation can conflict with current files.** SAMPLE's paper declares 1,366 measured plus 1,366 synthetic samples, while the inspected repository tree contains 1,345 files in each branch. IRSTD-1k's paper says 1,000 images and its current README says 1,001. ShipRSImageNet's listed source contributions do not reconcile with its headline image total. These are unresolved version/count issues, not numbers to silently average.

6. **A large video count does not imply dense labels.** Some tracking datasets label every frame, while VTUAV's boxes are sparse at a ten-frame interval. Still-image collections extracted from video may have no track IDs at all. Temporal correlation and annotation frequency are therefore recorded separately from frame totals.

7. **Scenario description exists in several limited forms.** TRICLOBS has clip-level scripted action briefs; tracking datasets provide continuity; fMoW supplies region-function labels; LEVIR datasets supply changes; caption/VQA datasets describe image content or map-derived relations. None of these forms alone establishes full open-ended understanding of intent, affiliation or causality. Absence of an annotation is different from evidence that a model could never infer anything about it.

8. **Language labels are not necessarily independent observations.** RSVQA uses OpenStreetMap and templates, with acknowledged temporal and registration mismatch. SARChat largely derives language from categories and geometry. FSAR-Cap combines templates, manual correction and model-standardized language. Fluent or long descriptions are not a measured guarantee of factual grounding.

9. **Access and reuse rights differ.** DSIAC's public-release statement accompanies a request/distribution process. The 2025 military tracking set requires an author-reviewed request with restrictions. Some recent papers describe datasets without a verified public archive. SARChat's creator README contains a placeholder dataset URL. A public paper, a public download and permission for a proposed use are separate facts.

10. **Licensing cannot be copied from a mirror or code repository.** The current Kaggle aircraft owner says Unknown, while a smaller HF mirror says Apache-2.0. ShipRSImageNet contains both academic-only image terms and an Apache statement. DOTA, MAR20, DIOR, COD10K and other datasets state research/noncommercial restrictions. The report records declared terms without giving a blanket rights-clearance conclusion.

## A descriptive view of dataset quality

| Dimension | Evidence recorded | What remains unmeasured without archive inspection |
|---|---|---|
| Provenance | Creator, original sensor/media source, parent datasets, publication/deposit version | Per-image rights chain, whether filenames preserve original identities, actual duplicate rates |
| Annotation quality | Stated annotators, second review, expert adjudication, formats and ontology | Missing objects, wrong labels, box/mask accuracy and inter-annotator agreement |
| Representativeness | Documented locations, sensors, seasons, viewpoints, real/synthetic origin | Coverage of any future footage; bias in unreported conditions |
| Class balance | Published class counts and negative/background categories | Actual per-class distributions in a particular release and consistency across splits |
| Independence | Stated geographic, source-video or time-based partitions; known derivative relationships | Near duplicates, overlapping crops or the same physical objects crossing partitions |
| Access/reproducibility | Working documentation, version identifiers, public/request route | Download success, file completeness, checksums and current availability of all labels |
| Rights | Dataset licence text or owner declaration, plus identified conflicts | Legal clearance of all upstream images and applicability to a future use |
| Semantic coverage | Object, region, temporal, attribute, language or scenario label definitions | Truth of claims beyond the labelled properties |

The register supports a documentary comparison and identifies evidence gaps. It does not support a claim that all listed archives have been validated, that any dataset is universally highest quality, or that combining their advertised sizes creates a larger independent benchmark. The sources are given on every dataset card so each claim and caveat can be followed to its origin.

## Dataset index

| ID | Dataset / release | Family | Reported primary count | Unit |
|---|---|---|---:|---|
| D01 | FUSAR-Ship / FUSAR-Ship1.0 | SAR imagery | 16,144 | Chips in journal-hosted FUSAR-Ship1.0 |
| D02 | HRSID | SAR imagery | 5,604 | Images in original release |
| D03 | MSTAR | SAR imagery | Not established | Archive/collection; no unified chip count verified |
| D04 | OpenSARShip (original release) | SAR imagery | 11,346 | Ship chips in original paper |
| D05 | SAMPLE | SAR imagery | 1,345 | Measured/synthetic chip pairs in current public Git tree |
| D06 | SAR-AIRcraft-1.0 | SAR imagery | 4,368 | Images in original source release |
| D07 | SARDet-100K | SAR imagery | 116,598 | Images/patches in derivative aggregate benchmark |
| D08 | SSDD / Official SSDD | SAR imagery | 1,160 | Images in source dataset |
| D09 | DIOR | Overhead optical imagery | 23,463 | images |
| D10 | DIOR-R | Overhead optical imagery | 23,463 | images |
| D11 | DOTA v1.0 | Overhead optical imagery | 2,806 | images |
| D12 | DOTA v1.5 | Overhead optical imagery | 2,806 | images |
| D13 | DOTA v2.0 | Overhead optical imagery | 11,268 | images |
| D14 | FAIR1M (original paper release) | Overhead optical imagery | 15,266 | images |
| D15 | FGSC-23 | Overhead optical imagery | 4,052 | instance image chips |
| D16 | FGSD | Overhead optical imagery | 2,612 | selected labelled images |
| D17 | HRSC2016 | Overhead optical imagery | Not established | images |
| D18 | MAR20 | Overhead optical imagery | 3,842 | images |
| D19 | MTARSI (original 2019 deposit) | Overhead optical imagery | 9,385 | single-aircraft image chips |
| D20 | MTARSI 2 (separate 2021 derivative) | Overhead optical imagery | Not established | image chips |
| D21 | MVRSD | Overhead optical imagery | 3,000 | images |
| D22 | RarePlanes | Overhead optical imagery | 14,707 | real aircraft instances |
| D23 | ShipRSImageNet (paper counts; repository currently V1.1) | Overhead optical imagery | 3,435 | images |
| D24 | xView (2018 detection dataset) | Overhead optical imagery | 1,000,000 | object instances (approximately) |
| D25 | DroneVehicle | Visible and thermal imagery | 28,439 | image pairs |
| D26 | DSIAC ATR Algorithm Development Image Database / historical SENSIAC lead | Visible and thermal imagery | 206 | archive size (GB) |
| D27 | M3FD | Visible and thermal imagery | 4,200 | image pairs |
| D28 | TNO Image Fusion Dataset | Visible and thermal imagery | Not established | complete image/sequence total unspecified |
| D29 | TRICLOBS Dynamic Multiband Image Dataset | Visible and thermal imagery | 16 | motion sequences |
| D30 | Anti-UAV original / later Anti-UAV300 label | Video tracking | 318 | RGB-T video pairs |
| D31 | Anti-UAV410 | Video tracking | 410 | videos |
| D32 | AntiUAV600 | Video tracking | 600 | video sequences |
| D33 | DUT Anti-UAV | Video tracking | 10,000 | detection images |
| D34 | Military Vehicles in Low-FPS UAV Footage validation benchmark | Video tracking | 119 | videos |
| D35 | VTUAV / DUT-VTUAV | Video tracking | 1,664,549 | RGB-T frame pairs |
| D36 | IRSTD-1k | Infrared small spots | 1,000 | images |
| D37 | NUDT-SIRST | Infrared small spots | 1,327 | images |
| D38 | SIRST (often called NUAA-SIRST in later papers) | Infrared small spots | 427 | images |
| D39 | 15-class RGB military-vehicle collection described by TNO studies | Web and synthetic imagery | 959 | real images |
| D40 | milair-dataset | Web and synthetic imagery | 660 | class occurrences |
| D41 | Military Aircraft Detection Dataset (Kaggle v105) | Web and synthetic imagery | Not established | images |
| D42 | Military and Civilian Vehicles Classification (Mendeley v1) | Web and synthetic imagery | 6,772 | images |
| D43 | Military Assets Dataset (Kaggle v5) | Web and synthetic imagery | 26,315 | images |
| D44 | Military-Aircraft-Detection (Illia56 mirror) | Web and synthetic imagery | Not established | images |
| D45 | RGB military-target collection described by Jeong et al. (2025) | Web and synthetic imagery | Not established | images |
| D46 | CAMO | Camouflage segmentation | 2,500 | images |
| D47 | COD10K | Camouflage segmentation | 10,000 | images |
| D48 | FSAR-Cap | Scene, change and language | 14,480 | images |
| D49 | Functional Map of the World (fMoW) | Scene, change and language | Not established | images |
| D50 | LEVIR-CC | Scene, change and language | 10,077 | image pairs |
| D51 | LEVIR-CD (original release) | Scene, change and language | 637 | image pairs |
| D52 | RSICD | Scene, change and language | 10,921 | images |
| D53 | RSVQA-HR | Scene, change and language | 10,659 | image patches |
| D54 | RSVQA-LR | Scene, change and language | 772 | image patches |
| D55 | SARChat-2M / SARChat-Bench | Scene, change and language | 2,063,548 | dialogue samples |
| D56 | xBD | Scene, change and language | 850,736 | building annotations |


## SAR imagery


### D01. FUSAR-Ship / FUSAR-Ship1.0

**Scope:** Adjacent/general maritime ship and non-ship SAR chips  
**Year:** 2020  
**Sensor / representation:** Gaofen-3 SAR with AIS-matched ship subset

**Size and units:** Portal: 16,144 total = 6,252 AIS-matched ship + 2,045 strong ship-like false-alarm + 1,461 bridge/coastline + 1,010 coastal land/island + 1,967 complex wave clutter + 1,785 ordinary sea + 1,624 land chips. Paper says more than 5,000 ship chips, not total dataset size. Portal labelled 2022 issue 1; paper published 10 March 2020.

**Categories:** Extensible hierarchy: 15 primary ship categories and 98 subcategories plus non-ship categories. Taxonomy-node count does not establish 98 populated/balanced classes.

**Annotations and identification:** Fixed 512 x 512 chips with hierarchical class and AIS-associated ship information. Portal describes ship-centred crop construction. Exhaustive full-scene boxes/masks not verified.

**Distinctive features:** 126 original Gaofen-3 scenes; UFS mode, DH/DV; portal reports 1.124 m x 1.728 m resolution. Sea, land, coast, river, island and explicit clutter/false-alarm categories.

**Origin and provenance:** Fudan University electromagnetic-waves laboratory and Shanghai Gaofen Data/Application Center. Hou, Ao, Song, Lai, Wang and Xu; Science China Information Sciences 63,140303; published 10 March 2020; DOI 10.1007/s11432-019-2772-5.

**Documented strengths:** Exact category totals, sensor/crop metadata, scene count, AIS-associated positives and explicit non-ships are documented. Separate guide states ownership, access and permitted use.

**Limitations and open questions:** Only 6,252 of 16,144 chips are AIS-matched ships. Exact class occupancy, AIS match errors, unique-vessel count, acquisition dates and split independence unverified. Taxonomy size is not class-balance evidence.

**Split evidence:** No universal train/validation/test split verified in portal/use guide.

**Access checked:** Guide: initial registration/email verification; Chinese workflow uses WeChat, English-site workflow may use email verification. Current portal exposes verification/download UI. No registration/archive download performed.

**Declared rights:** Primary guide: Fudan laboratory ownership; free teaching/research use with citation or acknowledgement; unauthorized commercial use prohibited, commercial requests to journal editorial office. Custom use policy, not a verified CC licence.

**Meaning supported by labels:** Marine-object/ship taxonomy and AIS-matched type, with non-ship clutter classes; no hostility or military-affiliation labels.

**Sources:** [Journal of Radars primary release portal](https://radars.ac.cn/web/data/getData?dataType=FUSAR); [Publisher abstract and publication history](https://link.springer.com/article/10.1007/s11432-019-2772-5); [Paper DOI](https://doi.org/10.1007/s11432-019-2772-5); [Primary dataset use guide](https://radars.ac.cn/fileLDXB/cms/news/info/2022/04/1dfced94b3d14d989a9fda322ab143f6/FUSAR-Ship%E6%95%B0%E6%8D%AE%E9%9B%86%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E.pdf)


### D02. HRSID

**Scope:** Adjacent/general maritime SAR detection and segmentation  
**Year:** 2020  
**Sensor / representation:** High-resolution measured spaceborne SAR chips

**Size and units:** Official README: 5,604 images / 16,951 ship instances. SARDet reports 16,969 instances in its HRSID contribution, an unresolved 18-instance difference. Later supplemental negatives are separate.

**Categories:** One object category: ship

**Annotations and identification:** Ship detection, instance segmentation and semantic segmentation; COCO-based construction and public annotations directory. Updated package adds inshore/offshore annotation.

**Distinctive features:** Official README: 0.5 m,1 m,3 m resolutions; varied polarization, sea conditions, sea areas and ports. SARDet Table 2 names Sentinel-1B, TerraSAR-X and TanDEM-X. Exact original per-sensor/source-scene counts unverified.

**Origin and provenance:** Wei, Zeng, Qu, Wang, Su and Shi, HRSID: A High-Resolution SAR Images Dataset for Ship Detection and Instance Segmentation, IEEE Access 8 (2020),120234-120254; DOI 10.1109/ACCESS.2020.3005861. Publication year verified; exact day not established here.

**Documented strengths:** Dense instance/semantic annotation, multiple resolutions and explicit high-fidelity PNG versus JPG options. Official project separately supplies 400 pure-background images and an ALOS-2 test image.

**Limitations and open questions:** Updated official scene proportions: 18.4% inshore / 81.6% offshore. JPG/PNG and supplemental packages require version distinction. Source/aggregate instance counts differ; temporal coverage, source-scene separation and annotation error rates not audited.

**Split evidence:** No universal split verified from reviewed source README. SARDet contribution uses 3,642/981/981 images train/val/test; common source train/test ratios not asserted from memory.

**Access checked:** Official repository lists Google Drive/Baidu packages, revised context annotations and supplemental background/test imagery. Archives not downloaded.

**Declared rights:** Official repository LICENSE is GNU GPL v3. IEEE article separately CC BY 4.0 in publisher-deposited metadata. Scope over satellite imagery/downloaded packages not independently adjudicated.

**Meaning supported by labels:** Ship geometry and limited scene context; no affiliation/threat labels.

**Sources:** [Official HRSID repository/README](https://github.com/chaozhong2010/HRSID); [Original paper DOI](https://doi.org/10.1109/ACCESS.2020.3005861); [Publisher-deposited Crossref date/article-rights metadata](https://api.crossref.org/works/10.1109/ACCESS.2020.3005861); [Official GPL v3 licence](https://raw.githubusercontent.com/chaozhong2010/HRSID/master/LICENSE); [SARDet Tables 1-2, derivative counts/sensors](https://arxiv.org/html/2403.06534v3)


### D03. MSTAR

**Scope:** Military-origin public SAR benchmark archive  
**Year:** Not established from inspected documentation  
**Sensor / representation:** Measured airborne X-band SAR; target chips and separate clutter scenes

**Size and units:** Official overview: September 1995 collection has 13 target types / 20 actual targets; November 1996 has 15 types / 27 actual targets. These are collection counts, not one standardized classification split. Official clutter page separately reports 100 full-scene images. A later comparison reports a 5,950-image, 10-class benchmark, not the complete archive.

**Categories:** Collection-dependent. Official September public-target page lists T-72, BMP2, BTR-70 and SLICY; other subcollections and common ten-class subsets differ.

**Annotations and identification:** Target class/identity and acquisition metadata; replicate identities. Full-archive bounding-box or mask truth was not verified.

**Distinctive features:** Official target page documents one-foot-resolution spotlight SAR, full-aspect coverage for listed targets, and strip-map collection for clutter.

**Origin and provenance:** Sandia National Laboratory platform at Redstone Arsenal, Huntsville, Alabama; DARPA/AFRL MSTAR program. Official overview dates collections to September 1995 and November 1996. No single publication/release date verified; year intentionally null.

**Documented strengths:** Official collector, acquisition context, replicate identities and separate target/clutter/variant/mixed-target subcollections are documented.

**Limitations and open questions:** Archive and common ten-class benchmark are not interchangeable. SAMPLE Section 1 warns that MSTAR evaluations may share backgrounds, radar parameters, weather and articulation and overfit that operating-condition space. Full inventory and a universal split were not verified.

**Split evidence:** Multiple research protocols; no universal archive split asserted. Official target acquisition-angle groups are not themselves one complete train/test protocol.

**Access checked:** Official overview says immediately downloadable. Linked Public Data Downloads requires a public-download or VDL account. No account created; no archive downloaded.

**Declared rights:** Reviewed official pages establish public access but no standardized dataset licence. Public availability does not establish unrestricted reuse.

**Meaning supported by labels:** Historical vehicle/engineering-target types and acquisition metadata; no affiliation, combatant status, intent or current-location labels.

**Sources:** [AFRL SDMS MSTAR overview (primary)](https://www.sdms.afrl.af.mil/index.php?collection=mstar); [AFRL public targets (primary)](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=targets); [AFRL clutter (primary)](https://www.sdms.afrl.af.mil/index.php?collection=mstar&page=clutter); [AFRL download access](https://www.sdms.afrl.af.mil/index.php?collection=registration); [SAMPLE author manuscript Section 1, MSTAR limitations](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/sample_public.pdf); [SAR-AIRcraft Table 1 (secondary MSTAR subset count)](https://radars.ac.cn/article/doi/10.12000/JR23043)


### D04. OpenSARShip (original release)

**Scope:** Adjacent/general maritime SAR interpretation  
**Year:** 2018  
**Sensor / representation:** Sentinel-1 SAR ship chips integrated with AIS messages

**Size and units:** Original abstract: 11,346 SAR ship chips integrated with AIS. Original paper January 2018; DOI registered 2017. OpenSARShip 2.0 is a separate 2017 conference release; its count is not merged.

**Categories:** 17 categories reported by SAR-AIRcraft Table 1 (secondary comparison); exact original taxonomy/occupancy not independently recovered.

**Annotations and identification:** Chip-level ship/AIS-associated information. Original abstract verifies AIS integration; exact schema and box/mask availability were not checked.

**Distinctive features:** Sentinel-1 specificity; official portal lists original and uint8 packages. Exact GRD/SLC composition, polarization, chip dimensions and source-scene count remain unverified.

**Origin and provenance:** Huang and coauthors, OpenSARShip: A Dataset Dedicated to Sentinel-1 Ship Interpretation, IEEE JSTARS 11(1),195-208, January 2018; DOI 10.1109/JSTARS.2017.2755672. SJTU institutional OpenSAR hosts data. Original author abstract retrieved via OpenAlex index because IEEE returned an empty body.

**Documented strengths:** Author abstract verifies SAR/AIS integration and public-benchmark construction. Institutional portal provides dataset links and original/2.0 citations; no independent label-accuracy claim.

**Limitations and open questions:** Original/2.0 and original/uint8 packages are distinct. AIS match error, taxonomy occupancy, temporal/geographic distribution and source-scene independence remain audit questions. Chips are not unique vessels or independent scenes.

**Split evidence:** No universal split verified from accessible original documentation.

**Access checked:** SJTU Data & Codes lists OpenSARShip_1, OpenSARShip_2, OpenSARShip_original_zip, OpenSARShip_uint8; no account gate visible on page. Archives not attempted; suffixes not assumed to identify publication versions.

**Declared rights:** Institutional portal requests citation; no explicit dataset reuse licence located. IEEE article rights are not dataset-use terms.

**Meaning supported by labels:** AIS-associated reported ship type and matched observations; no ownership, military affiliation or intent ground truth.

**Sources:** [SJTU OpenSAR portal (primary)](https://opensar.sjtu.edu.cn/); [SJTU Data & Codes (primary)](https://opensar.sjtu.edu.cn/DataAndCodes.html); [Original paper DOI](https://doi.org/10.1109/JSTARS.2017.2755672); [Publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1109/JSTARS.2017.2755672); [Original author abstract indexed by OpenAlex (secondary retrieval)](https://api.openalex.org/works/https://doi.org/10.1109/JSTARS.2017.2755672); [Separate OpenSARShip 2.0 paper](https://doi.org/10.1109/BIGSARDATA.2017.8124929); [SAR-AIRcraft Table 1 (secondary taxonomy comparison)](https://radars.ac.cn/article/doi/10.12000/JR23043)


### D05. SAMPLE

**Scope:** Military-origin paired measured/synthetic SAR chips  
**Year:** 2019  
**Sensor / representation:** MSTAR-derived measured SAR paired with simulated SAR; complex MAT and magnitude PNG products

**Size and units:** Untruncated official Git tree on 2026-11-10 lists 1,345 real MAT + 1,345 synth MAT files = 2,690 complex images (tree SHA 1bae4156afcba7ad9c9f2eb743ed20675ed14fb1). Paper Table 5 instead declares 1,366 + 1,366 = 2,732 images. Cause unresolved. Commonly repeated 1,367 was not verified. PNG normalizations are alternative representations, not new acquisitions.

**Categories:** 10: 2S1, BMP2, BTR70, M1, M2, M35, M548, M60, T72, ZSU23-4. This is not the usual MSTAR ten-class list.

**Annotations and identification:** Chip class, measured/synthetic pairing and acquisition/image metadata. Paper Table 4: azimuth, elevation, polarization, range/cross-range resolution, target_name; official verify.py documents source_mstar_file and alignment/image fields.

**Distinctive features:** 128 x 128 complex arrays; decibel and quarter-power magnitude PNG variants. Synthetic imagery matched to historical measured geometry and checked CAD configurations.

**Origin and provenance:** AFRL Sensors Directorate and Wright State University. MSTAR measurements paired with electromagnetic simulations based on CAD models checked against historical photographs/notes. SPIE paper published 14 May 2019; DOI 10.1117/12.2523460.

**Documented strengths:** Explicit pairing, complex products, source metadata, documented CAD truthing and public composition-check script support traceability.

**Limitations and open questions:** Selection restricted to vehicles with satisfactory CAD models and narrow geometry/flight coverage. Public subset: 10-80 degrees azimuth and 14-17 degrees elevation (Section 4.1). Synthetic background speckle not fully matched to measured clutter (Section 2.2). Manifest/paper count conflict; filename inventory only, no image-content audit.

**Split evidence:** Several paper protocols, not one universal split. Current per-class real MAT counts in listed class order: 174,107,92,129,128,129,128,176,108,174; synth count equals real for each at filename level.

**Access checked:** Official GitHub publicly lists MAT/PNG files, README and paper. Original paper says contact authors; current repository provides direct public access. Dataset files were not downloaded.

**Declared rights:** README: Distribution A, Approved for public release, Distribution unlimited. Paper PA approval 88ABW-2019-1483; dataset 88ABW-2019-1300. No standalone standardized licence at repository root; distribution statement is not converted into a CC licence.

**Meaning supported by labels:** Historical vehicle-type labels and measured/synthetic correspondence; no threat, affiliation or activity labels.

**Sources:** [Official SAMPLE repository/README](https://github.com/benjaminlewis-afrl/SAMPLE_dataset_public); [SAMPLE paper DOI/publication date](https://doi.org/10.1117/12.2523460); [Author manuscript, Tables 1,4,5 and Sections 2,4.1](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/sample_public.pdf); [Immutable official tree used for filename inventory](https://api.github.com/repos/benjaminlewis-afrl/SAMPLE_dataset_public/git/trees/1bae4156afcba7ad9c9f2eb743ed20675ed14fb1?recursive=1); [Official composition script, read only](https://raw.githubusercontent.com/benjaminlewis-afrl/SAMPLE_dataset_public/master/verify.py)


### D06. SAR-AIRcraft-1.0

**Scope:** Adjacent/general SAR aircraft detection and civil-type recognition  
**Year:** 2023  
**Sensor / representation:** Gaofen-3 spaceborne SAR aircraft imagery

**Size and units:** Primary abstract: 4,368 images / 16,463 aircraft instances. Table 1 image-size range 800-1500 pixels. SARDet derivative: 18,888 patches / 38,475 annotations, not the source count.

**Categories:** 7: A220, A320/321, A330, ARJ21, Boeing737, Boeing787, other. Table 3 totals respectively 3,730;1,771;309;1,187;2,557;2,645;4,264.

**Annotations and identification:** Instance-localization boxes and category labels for detection/recognition. Detailed annotation-file schema not retrieved. Method's scattering keypoints are not assumed to be manually annotated dataset truth.

**Distinctive features:** Gaofen-3 and seven classes verified by primary abstract. SARDet source table reports 1 m, C-band, uni-polar; those sensor details are secondary evidence here.

**Origin and provenance:** Wang Zhirui, Kang Yuzhuo, Zeng Xuan, Wang Yuelei, Zhang Ting and Sun Xian; AIR/CAS and UCAS. Journal of Radars 12(4),906-922; online 17 July 2023, issue publication 28 August 2023; DOI 10.12000/JR23043.

**Documented strengths:** Primary bilingual paper publishes source counts, class counts, train/test instance counts, labelled examples and explicit detection/recognition tasks.

**Limitations and open questions:** Class imbalance: A330 309 vs other 4,264. Other is heterogeneous. Paper documents discrete scattering and strong background interference. Unique-airframe count, source-scene independence, acquisition dates and direct dataset-use terms remain audit questions.

**Split evidence:** Table 3: 13,513 train / 2,950 test instances. These are object counts, not image counts. Separate validation split unverified.

**Access checked:** Paper states publicly released dataset; journal SAR catalogue returned CAPTCHA in one read. Specific paper page was readable. Archive access not completed.

**Declared rights:** SARDet Table 2 reports dataset CC BY-NC 4.0; direct dataset-specific licence not retrieved. Primary article dc.rights metadata says CC BY 3.0 for the article, a separate matter.

**Meaning supported by labels:** Named civil aircraft types plus other and image-local geometry; not military affiliation, operator or threat labels.

**Sources:** [Primary bilingual paper, Tables 1/3 and publication dates](https://radars.ac.cn/article/doi/10.12000/JR23043); [Paper DOI](https://doi.org/10.12000/JR23043); [Journal SAR catalogue, CAPTCHA observed](https://radars.ac.cn/web/data/getData?dataType=SARDataset); [SARDet Tables 1-2/Appendix A.2, secondary metadata and derivative counts](https://arxiv.org/html/2403.06534v3)


### D07. SARDet-100K

**Scope:** Adjacent/general aggregate SAR detection benchmark; mixed source provenance  
**Year:** 2024  
**Sensor / representation:** Standardized SAR intensity imagery from satellite and airborne/synthetic source datasets

**Size and units:** Official current README and paper v3: 116,598 images/patches / 245,653 object annotations from 10 source datasets. Not newly collected scenes. Do not sum aggregate and constituent counts as independent data.

**Categories:** 6 labels: Aircraft, Ship, Car, Bridge, Tank, Harbor. Tank is not automatically armored vehicle: primary MSAR explicitly labels oil tanks. Meaning of other Tank contributor OGSOD not independently verified.

**Annotations and identification:** Source annotations unified into COCO object-detection format. README describes separate RSAR as an approximate rotation-labelled version; SARDet-100K is not silently equated with RSAR.

**Distinctive features:** Sources: AIR_SARShip 1/2, HRSID, MSAR, SADD, SAR-AIRcraft, ShipDataset, SSDD, OGSOD, SIVED. Mixed resolution/bands/polarization. Appendix documents overlapping crops of larger-image sources, explaining count/dependence changes.

**Origin and provenance:** Yuxuan Li and coauthors; initial arXiv 11 March 2024, NeurIPS 2024 spotlight; current v3 9 August 2025. Authors collect/standardize existing datasets; not one new acquisition campaign.

**Documented strengths:** Public source tables, per-source image/instance counts, annotation-format standardization, split-conversion rules, repository licence and download links.

**Limitations and open questions:** Derivative overlap with source benchmarks and overlapping crops require careful interpretation; no independent duplicate/source-scene audit. HRSID contribution 16,969 vs source 16,951; SSDD 2,587 vs original commonly quoted 2,456. README labels links Train/Val/Test but also says only Train/Val released. Mixed upstream licences and unspecified entries remain unresolved.

**Split evidence:** Images train/val/test 94,493/10,492/11,613; annotations 198,747/22,703/24,023. Appendix: retain existing source splits, otherwise 8:1:1. Recorded as benchmark documentation, not training guidance.

**Access checked:** Official GitHub lists Baidu and Kaggle datasets. Current test-release status contradictory in README; archive download and permissions not checked.

**Declared rights:** Repository LICENSE: CC BY-NC 4.0. Paper/arXiv: CC BY-NC-SA 4.0. Source table includes GPL, Apache 2.0, CC BY-NC 4.0 and unspecified entries; no assumption all upstream rights are harmonized.

**Meaning supported by labels:** Broad object labels, not military affiliation/threat/intent. Upstream oil-storage tanks must not be reinterpreted as armored combat vehicles solely from the English label Tank.

**Sources:** [Official repository/statistics/access](https://github.com/zcablii/SARDet_100K); [Paper version and submission history](https://arxiv.org/abs/2403.06534); [Current paper v3, Tables 1-2/Appendix A.2](https://arxiv.org/html/2403.06534v3); [Official CC BY-NC 4.0 repository licence](https://raw.githubusercontent.com/zcablii/SARDet_100K/main/LICENSE); [Primary MSAR portal: oil-tank semantics](https://radars.ac.cn/web/data/getData?dataType=MSAR)


### D08. SSDD / Official SSDD

**Scope:** Adjacent/general maritime SAR detection and segmentation  
**Year:** 2021  
**Sensor / representation:** Measured spaceborne SAR from multiple sensors

**Size and units:** 1,160 images. Original commonly cited version: 2,456 ship instances (also SAR-AIRcraft Table 1). SARDet standardized contribution: 2,587 instances. Different release/annotation contexts; not reconciled. Original SSDD appeared in 2017; official corrected/expanded paper published 15 September 2021.

**Categories:** One object category: ship

**Annotations and identification:** 2021 official versions: horizontal boxes (BBox-SSDD), rotated boxes (RBox-SSDD), pixel-level polygon segmentation (PSeg-SSDD). Paper describes VOC/COCO format variants and inshore/offshore analysis.

**Distinctive features:** Paper reports RadarSat-2, TerraSAR-X, Sentinel-1; approximately 1-15 m resolution; HH,VV,VH,HV; varied sea conditions and coastal/offshore scenes.

**Origin and provenance:** Tianwen Zhang and coauthors revisit initial SSDD, correct annotations and standardize usage. Remote Sensing 13(18),3690, 15 September 2021, DOI 10.3390/rs13183690.

**Documented strengths:** Official release explicitly repairs missing/false labels and loose boxes and adds rotated/polygon annotations. Published size, orientation and inshore/offshore analyses.

**Limitations and open questions:** Paper documents small scale, original label errors and inconsistent historical splits. Source-vs-aggregate instance counts differ. Source-scene independence/geographic leakage and actual error rates were not independently audited.

**Split evidence:** 2021 paper standardizes a partition and notes varying historical ratios. SARDet derivative uses 928/116/116 images train/val/test, which is a different benchmark context.

**Access checked:** Official GitHub lists Google Drive/Baidu downloads. Links observed; archive content and permissions not tested.

**Declared rights:** Official-SSDD repository LICENSE is Apache 2.0. Article separately CC BY 4.0. Scope over third-party source satellite imagery not independently legally verified.

**Meaning supported by labels:** Ship-instance geometry; no nationality, military status, identity, intent or payload labels.

**Sources:** [Official SSDD repository/download links](https://github.com/TianwenZhang0825/Official-SSDD); [Official 2021 paper DOI](https://doi.org/10.3390/rs13183690); [Publisher-hosted paper, read in memory](https://mdpi-res.com/d_attachment/remotesensing/remotesensing-13-03690/article_deploy/remotesensing-13-03690.pdf); [Official Apache 2.0 licence](https://raw.githubusercontent.com/TianwenZhang0825/Official-SSDD/main/LICENSE); [SAR-AIRcraft Table 1 (secondary original SSDD count)](https://radars.ac.cn/article/doi/10.12000/JR23043); [SARDet Table 1, derivative SSDD count](https://arxiv.org/html/2403.06534v3)


## Overhead optical imagery


### D09. DIOR

**Scope:** General object detection in optical remote sensing images  
**Year:** 2020  
**Sensor / representation:** Optical remote sensing images

**Size and units:** Current creator page: 23,463 images / 192,518 object instances. Older comparison tables sometimes state 192,472; do not silently mix those annotation totals.

**Categories:** 20 broad object categories; aircraft/ship classes do not establish military subtype labels.

**Annotations and identification:** Horizontal bounding boxes.

**Distinctive features:** Multi-category full-image detection benchmark.

**Origin and provenance:** Ke Li, Gang Wan, Gong Cheng, Liqiu Meng and Junwei Han, ISPRS Journal of Photogrammetry and Remote Sensing 159, 296–307 (2020); creator Gong Cheng's dataset page.

**Documented strengths:** Creator-hosted current counts, annotation format, licence and download links.

**Limitations and open questions:** A broad detection taxonomy does not provide fine military model labels. Source-location and temporal independence, current manifest count and class-level errors were not audited.

**Split evidence:** Not verified from the current creator page inspected.

**Access checked:** Google Drive/Baidu links on creator page; archives untested.

**Declared rights:** Creator page: CC BY-NC 4.0.

**Meaning supported by labels:** Visible category and horizontal position/extent; no scene captions or status labels.

**Sources:** [Creator DIOR/DIOR-R data and licence page](https://gcheng-nwpu.github.io/); [Example of different historical instance count, FAIR1M table](https://arxiv.org/html/2103.05569)


### D10. DIOR-R

**Scope:** General object detection; oriented reannotation of DIOR  
**Year:** 2022  
**Sensor / representation:** Same optical images as DIOR

**Size and units:** Shares DIOR's 23,463 images. The creator page does not separately state a DIOR-R instance total; do not assume identity of annotation counts.

**Categories:** Same broad DIOR taxonomy (20 categories).

**Annotations and identification:** Oriented bounding boxes, replacing/augmenting DIOR's horizontal representation.

**Distinctive features:** Orientation-aware ground-truth geometry on an existing image set.

**Origin and provenance:** Gong Cheng et al., Anchor-free Oriented Proposal Generator for Object Detection, IEEE TGRS (2022); DIOR creator page.

**Documented strengths:** Creator explicitly states that the same imagery is used, clarifying provenance.

**Limitations and open questions:** Not an independent dataset from DIOR; comparing or combining imagery across these names does not add independent observations. Full per-instance manifest not audited.

**Split evidence:** Image correspondence with DIOR documented; file-level split mapping unverified.

**Access checked:** Download links through creator page; archive untested.

**Declared rights:** Creator page: CC BY-NC 4.0.

**Meaning supported by labels:** Broad object category and orientation geometry; no new fine-grained military taxonomy.

**Sources:** [Creator DIOR and DIOR-R description](https://gcheng-nwpu.github.io/)


### D11. DOTA v1.0

**Scope:** General remote-sensing objects; aircraft and ship are broad categories  
**Year:** 2018  
**Sensor / representation:** Mixed optical RGB and grayscale remote-sensing/aerial images

**Size and units:** 2,806 images; 188,282 object instances; 15 categories.

**Categories:** 15 broad classes including plane, ship, helicopter, vehicles, harbour, sports facilities and other infrastructure.

**Annotations and identification:** Oriented quadrilateral (8-coordinate) boxes; category; difficult flag.

**Distinctive features:** Large images and wide object scale/orientation variation; aerial and satellite sources.

**Origin and provenance:** Gui-Song Xia et al., CVPR 2018; creator DOTA project. Images from Google Earth, GF-2, JL-1 and CycloMedia aerial imagery.

**Documented strengths:** Expert aerial-image interpretation; published annotation geometry and category definitions; formal benchmark splits.

**Limitations and open questions:** Mixed sensor provenance; generic plane/ship labels do not encode military subtype or affiliation. Versions reuse images, so totals across releases cannot be added as unique scenes. Upstream Google Earth terms apply.

**Split evidence:** Creator page: approximately 1/2 train, 1/6 validation, 1/3 test.

**Access checked:** Official page provides Google Drive and Baidu links; archive not downloaded.

**Declared rights:** Official page: academic purposes only, commercial use prohibited; Google Earth terms also apply.

**Meaning supported by labels:** Object location and broad visible category; no military status or scene narratives.

**Sources:** [Creator version counts](https://captain-whu.github.io/DOTA/); [Source, licence and annotation specification](https://captain-whu.github.io/DOTA/dataset.html)


### D12. DOTA v1.5

**Scope:** General remote-sensing objects, revised annotation coverage  
**Year:** 2019  
**Sensor / representation:** Same optical/aerial images as DOTA v1.0

**Size and units:** Same 2,806 images as v1.0; 403,318 instances and 16 categories, including added extremely small instances (<10 pixels) and container crane.

**Categories:** 16 broad categories.

**Annotations and identification:** Oriented quadrilateral boxes; category; difficult flag.

**Distinctive features:** Denser annotations and an extra category, rather than a new image collection.

**Origin and provenance:** DOTA creator project; CVPR 2019 DOAI challenge release.

**Documented strengths:** Creator explicitly documents changes from v1.0 and keeps image split counts constant.

**Limitations and open questions:** Not independent of v1.0. Instance-count growth mainly reflects changed annotation policy. Results across v1.0/v1.5 require identifying the version.

**Split evidence:** Same images and splits as v1.0.

**Access checked:** Official Google Drive/Baidu links published; archive untested.

**Declared rights:** Academic only; no commercial use; upstream Google Earth terms.

**Meaning supported by labels:** Broad visible object categories and location; no military subtype labels.

**Sources:** [Creator version counts and differences](https://captain-whu.github.io/DOTA/); [Annotation and use terms](https://captain-whu.github.io/DOTA/dataset.html)


### D13. DOTA v2.0

**Scope:** General aerial object detection benchmark  
**Year:** 2021  
**Sensor / representation:** Mixed optical satellite and aerial RGB/grayscale imagery

**Size and units:** 11,268 images; 1,793,658 instances; 18 categories. Includes relabelled earlier images and additional imagery.

**Categories:** 18 categories; airport and helipad added beyond v1.5.

**Annotations and identification:** Oriented quadrilateral boxes; category; difficult flag.

**Distinctive features:** Larger image set; objects over diverse sizes/orientations; separate test-dev and test-challenge.

**Origin and provenance:** Jian Ding et al., Object Detection in Aerial Images: A Large-Scale Benchmark and Challenges (2021); DOTA creator project.

**Documented strengths:** Official image and instance totals given for each split; annotation version changes explicitly documented.

**Limitations and open questions:** Not all 11,268 images/labels are freely downloadable training data. Test-dev labels withheld; test-challenge images and labels described as challenge-only. Earlier DOTA imagery is reused and relabelled.

**Split evidence:** Train 1,830 images / 268,627 instances; validation 593 / 81,048; test-dev 2,792 / 353,346; test-challenge 6,053 / 1,090,637.

**Access checked:** Official page publishes extra-image and annotation links; requires earlier v1.0 imagery. Test access restrictions described above; archive untested.

**Declared rights:** Academic only; no commercial use; Google Earth source terms apply.

**Meaning supported by labels:** Generic object classes and spatial boxes, not military identity or scene-level reasoning labels.

**Sources:** [Creator counts and split disclosure](https://captain-whu.github.io/DOTA/); [Data source, download and licence terms](https://captain-whu.github.io/DOTA/dataset.html)


### D14. FAIR1M (original paper release)

**Scope:** General fine-grained transport/infrastructure imagery, including one warship category  
**Year:** 2022  
**Sensor / representation:** Gaofen and Google Earth high-resolution optical imagery; 0.3–0.8 m stated spatial resolution

**Size and units:** 2021 arXiv v2 table: 15,266 images and approximately 1.02 million instances; 37 subcategories under 5 broad categories. Journal article appeared in 2022. Later FAIR1M 2.0/challenge totals are separate and were not verified here.

**Categories:** Airplanes, ships, vehicles, courts, roads; 37 subcategories. Airplane classes are largely named civil airliners; ship classes include a single warship category and functional civil types.

**Annotations and identification:** Oriented rectangular boxes with ordered vertices and direction; additional flags for occlusion/uncertain direction; source geographic/resolution metadata described.

**Distinctive features:** Multi-source and multi-temporal imagery; fine transport classes and geographic metadata.

**Origin and provenance:** Xian Sun et al.; ISPRS Journal of Photogrammetry and Remote Sensing, DOI 10.1016/j.isprsjprs.2021.12.004; original arXiv v2 March 2021; Gaofen challenge/ISPRS benchmark site.

**Documented strengths:** Paper documents image cleaning, geometric/radiometric preparation, paired annotation checks, supervisor review and expert review.

**Limitations and open questions:** Sampling from civil airports/harbours/cities and class imbalance are relevant representativeness limits. Image cleaning removes some adverse-quality scenes. The annotation threshold passage specifies 16 pixels but has confusing example wording. Exact manifest and later-release counts not audited.

**Split evidence:** No file-level release split verified; original paper and later challenge releases must be identified separately.

**Access checked:** Paper points to gaofen-challenge.com; current benchmark route rendered a JavaScript shell in HTTP inspection. Account/terms/download process not verified.

**Declared rights:** Explicit dataset reuse licence was not verified in the inspected paper or accessible benchmark shell; do not infer a data licence from article access.

**Meaning supported by labels:** Named civil aircraft types, functional vehicle/ship types and broad warship class; not a military equipment identity catalogue.

**Sources:** [Primary full text, original paper version](https://arxiv.org/html/2103.05569); [Journal paper DOI](https://doi.org/10.1016/j.isprsjprs.2021.12.004); [Official benchmark route](https://www.gaofen-challenge.com/benchmark)


### D15. FGSC-23

**Scope:** Fine-grained ship classification; inspect full taxonomy before assigning a military-only scope  
**Year:** 2021  
**Sensor / representation:** High-resolution optical image chips cut from Google Earth and GF-2 scenes

**Size and units:** 4,052 chips in 23 total categories: 22 ship categories plus one negative/background category. The 23 is not the number of ship types.

**Categories:** 22 ship categories + 1 negative category.

**Annotations and identification:** Human-interpreted chip class; ship aspect ratio; angle between the ship central axis and horizontal image axis.

**Distinctive features:** Object-centred crops; shape/direction attributes; image-scene and category diversity.

**Origin and provenance:** Libo Yao, Xiaohan Zhang, Yafei Lyu, Weiwei Sun, Mengyang Li; Journal of Image and Graphics, 26(10), 2337–2345 (2021), DOI 10.11834/jig.200261.

**Documented strengths:** Original bilingual publisher abstract documents exact chip count, negative class, annotation attributes and class imbalance.

**Limitations and open questions:** Classification chips do not provide equivalent evidence to detecting objects in full scenes. Class imbalance is acknowledged. A random within-category split is not evidence of separation by source scene, ship identity, time, or location. Full per-class taxonomy and reuse licence were not established.

**Split evidence:** Paper: approximately 1:4 testing-to-training ratio, random within categories.

**Access checked:** Primary paper is publicly readable; a creator-controlled downloadable archive and current archive accessibility were not verified.

**Declared rights:** Dataset-specific reuse licence not found in inspected primary material; article access is not data reuse permission.

**Meaning supported by labels:** Ship identity class plus aspect ratio and direction, with a negative chip class; no scene captions.

**Sources:** [Original publisher article and bilingual abstract](https://www.cjig.cn/zh/article/doi/10.11834/jig.200261/); [Paper DOI](https://doi.org/10.11834/jig.200261)


### D16. FGSD

**Scope:** Mixed military/civilian fine-grained ship dataset with a separate dock class  
**Year:** 2020  
**Sensor / representation:** Google Earth optical overhead imagery, including historical imagery; 0.12–1.93 m reported resolution

**Size and units:** 2,612 selected/labelled images from 4,736 collected pictures; 5,634 ship instances and separately 1,366 docks. Images 930×930.

**Categories:** 43 ship classes + Dock; ship hierarchy includes warship, carrier, submarine and civil ship.

**Annotations and identification:** Horizontal and rotated boxes, ship orientation, multi-level class labels; source port ID, resolution and Google Earth resolution level.

**Distinctive features:** 17 ports in four countries; historical imagery; fine-grained ship taxonomy plus dock context.

**Origin and provenance:** Kaiyan Chen, Ming Wu, Jiaming Liu, Chuang Zhang, Beijing University of Posts and Telecommunications; original arXiv paper 2003.06832 (2020). Also named as a source of ShipRSImageNet.

**Documented strengths:** Original full paper provides collection-vs-labelled counts, split counts, annotation definitions and source metadata.

**Limitations and open questions:** Paper says map shifts/spins were used during sample collection, so unique physical observations and split independence need audit. Only selected ports are represented. 43 counts ships, excluding dock; 5,634 also excludes 1,366 docks.

**Split evidence:** Training 1,917 images / 3,964 ships; validation 268 / 590; test 427 / 1,080. These sum to 2,612 images / 5,634 ships.

**Access checked:** Original paper says forthcoming and invites dataset requests by email. Public uptake evidenced by creator ShipRSImageNet reuse; no currently working direct FGSD archive was verified and no email was sent.

**Declared rights:** Dataset-specific licence not established. arXiv paper licence does not license source imagery.

**Meaning supported by labels:** Ship identity/type and position/orientation, plus dock geometry; not textual situational understanding.

**Sources:** [Original full paper](https://arxiv.org/html/2003.06832); [Original bibliographic record](https://arxiv.org/abs/2003.06832); [ShipRSImageNet provenance corroboration](https://github.com/zzndream/ShipRSImageNet)


### D17. HRSC2016

**Scope:** Ship benchmark with hierarchical ship/category/type labels including military-associated classes  
**Year:** 2017  
**Sensor / representation:** High-resolution optical satellite/Google Earth overhead imagery

**Size and units:** Common later-literature count: 1,070 images / 2,976 ship instances. However FAIR1M's own comparison text says 1,061 images while its table says 1,070. Original accessible abstract gives no total; the discrepancy was not resolved against a release manifest.

**Categories:** Three annotation levels: ship, ship category, ship type. Later literature describes 22 ship classes; many detection papers collapse these to one ship class.

**Annotations and identification:** Horizontal and rotated boxes; head points for V-shaped bows; sea/land segmentation masks for test images.

**Distinctive features:** Multiple annotation tasks in one collection; rotated geometry and hierarchical identity labels.

**Origin and provenance:** Zikun Liu, Liu Yuan, Lubin Weng, Yiping Yang; ICPRAM 2017, pp. 324–331, DOI 10.5220/0006120603240331. Original creator URL: escience.cn/people/liuzikun/DataSet.html.

**Documented strengths:** Original paper abstract precisely documents annotation types and accompanying annotation/development tools.

**Limitations and open questions:** Canonical count/version, licence and current original-host access need verification. Later literature reports images from a small set of ports and 0.4–2 m spatial resolution. Single-class detector results do not establish fine-grained type classification quality.

**Split evidence:** Canonical train/validation/test file lists were not checked; do not conflate HRSC2016 with the later HRSC2016-MS derivative.

**Access checked:** Original author URL timed out; historical Google Sites URL redirected to sign-in. Third-party mirrors exist but their fidelity was not audited.

**Declared rights:** Dataset licence not established. SciTePress's CC BY-NC-ND 4.0 notice applies to the article and must not be assumed to license image archives.

**Meaning supported by labels:** Object/type identities, orientation and sea-land masks; no human-authored scene or operational-situation narrative.

**Sources:** [Original publisher record](https://www.scitepress.org/Link.aspx?doi=10.5220/0006120603240331); [Original creator address](http://www.escience.cn/people/liuzikun/DataSet.html); [Count discrepancy in later FAIR1M paper](https://arxiv.org/html/2103.05569); [Separate HRSC2016-MS creator repository](https://github.com/wmchen/HRSC2016-MS)


### D18. MAR20

**Scope:** Explicit military-aircraft-labelled research benchmark  
**Year:** 2023  
**Sensor / representation:** Optical remote sensing images; overhead aircraft appearances

**Size and units:** 3,842 images; 22,341 aircraft instances; 20 military aircraft types. Creator page cites 2022; the published journal record is 2023, volume 27(12), pp. 2688–2696.

**Categories:** 20 military aircraft types.

**Annotations and identification:** Both horizontal bounding boxes and oriented bounding boxes for every instance.

**Distinctive features:** Fine-grained aircraft type labels with location and orientation geometry.

**Origin and provenance:** Wenqi Yu, Gong Cheng, Meijun Wang, Yanqing Yao, Xingxing Xie, Xiwen Yao, Junwei Han; Northwestern Polytechnical University; Journal of Remote Sensing, DOI 10.11834/jrs.20222139.

**Documented strengths:** Creator page explicitly provides image/instance/type counts, dual annotation formats, and licence; paper describes within-class appearance variation and similarity across types.

**Limitations and open questions:** Full sensor/source inventory, acquisition dates, geographic split independence and annotation-error rates were not established from accessible primary material. Journal full text is gated. Do not turn 22,341 instances into 22,341 images.

**Split evidence:** Split counts not verified from accessible primary pages.

**Access checked:** Creator page publishes OneDrive and BaiduNetDisk links; archive retrieval was not tested.

**Declared rights:** Creator page: research purposes only; CC BY-NC 4.0.

**Meaning supported by labels:** Military aircraft model/type category plus image geometry; no labels for missions, intent, readiness, or scene narratives.

**Sources:** [Creator dataset page](https://gcheng-nwpu.github.io/); [Published journal record](https://www.ygxb.ac.cn/zh/article/doi/10.11834/jrs.20222139/); [Paper DOI](https://doi.org/10.11834/jrs.20222139)


### D19. MTARSI (original 2019 deposit)

**Scope:** Aircraft classification with explicit military aircraft types and a broad Boeing category  
**Year:** 2019  
**Sensor / representation:** Google Earth optical overhead image chips

**Size and units:** 9,385 images, manually expanded; 20 types across 36 airports. Each image contains one complete aircraft. This is not a count of independent source scenes.

**Categories:** 20 aircraft types; granularity is uneven (specific model designations coexist with Boeing).

**Annotations and identification:** Image-level aircraft class; seven interpretation specialists labelled the chips. Bounding boxes are not documented in the repository metadata.

**Distinctive features:** Single-object crops; military and civil-associated aircraft labels; manually expanded imagery.

**Origin and provenance:** Zhize Wu, Hefei University; dataset DOI deposit in 2019. Associated paper: A benchmark data set for aircraft type recognition from remote sensing images, Applied Soft Computing (2020), DOI 10.1016/j.asoc.2020.106132.

**Documented strengths:** Creator-deposited DOI metadata states the count, provenance, class inventory, one-aircraft-per-image rule, and seven-specialist labelling.

**Limitations and open questions:** Manual expansion means image totals are not independent observations. A 2022 follow-up reports limited complexity/heterogeneity and labelling errors with poor generalization despite very high internal validation scores. No file-level duplicate or split audit performed here.

**Split evidence:** Original split policy was not established from the metadata inspected; distinguish derivatives and augmented siblings.

**Access checked:** Public Zenodo deposit is documented. Zenodo landing/API requests returned 403 in this session; publisher-deposited DataCite DOI metadata was accessible. No archive downloaded.

**Declared rights:** Deposit metadata: CC BY 4.0. Google Earth imagery is upstream material; the deposit does not itself establish a separate clearance chain for every source image.

**Meaning supported by labels:** Aircraft type labels on cropped overhead appearances; no textual situation descriptions, activity labels, or current operational status.

**Sources:** [Original version DOI](https://doi.org/10.5281/zenodo.3464319); [Creator-deposited DataCite metadata](https://api.datacite.org/dois/10.5281/zenodo.3464319); [Dataset paper](https://doi.org/10.1016/j.asoc.2020.106132); [Independent quality study, Gao et al. (2022)](https://doi.org/10.1109/ACCESS.2022.3231327)


### D20. MTARSI 2 (separate 2021 derivative)

**Scope:** Reclassified and augmented derivative of MTARSI  
**Year:** 2021  
**Sensor / representation:** Optical overhead aircraft image chips

**Size and units:** The inspected deposit states 42 classifications but does not state a total image count; do not transfer the original 9,385 count.

**Categories:** 42 reclassified aircraft categories.

**Annotations and identification:** Image-level class labels; no additional annotation geometry established.

**Distinctive features:** Additional augmentation and reclassification; unequal class frequencies and varying light/view angles explicitly noted.

**Origin and provenance:** Richard Rudd-Orthner and Lyudmila Mihaylova, University of Sheffield; 2021 deposit explicitly derived from MTARSI DOI 10.5281/zenodo.3464319.

**Documented strengths:** Explicit parent-dataset provenance and an independently identified deposit.

**Limitations and open questions:** Not a new independent source collection. Different class definitions and augmentation make its numbers incompatible with the original release without a manifest audit.

**Split evidence:** Not established from inspected deposit metadata.

**Access checked:** Zenodo deposit documented; DataCite metadata accessible, archive untested.

**Declared rights:** CC BY 4.0 in creator-deposited metadata; original imagery provenance remains relevant.

**Meaning supported by labels:** Alternative aircraft image classification taxonomy, not a larger set of independent scene detections.

**Sources:** [Derivative DOI](https://doi.org/10.5281/zenodo.5044950); [Creator-deposited metadata](https://api.datacite.org/dois/10.5281/zenodo.5044950)


### D21. MVRSD

**Scope:** Military-labelled collection  
**Year:** Not established from inspected documentation  
**Sensor / representation:** Google Earth overhead RGB; claimed 0.3 m spatial resolution

**Size and units:** 32,626 instances; 640 x 640 images; also 3 unlabelled large images. Counts are README claims, not archive counts.

**Categories:** Military vehicles; detailed class ontology not stated in the inspected README.

**Annotations and identification:** Object instances are described; exact annotation geometry and schema not verified.

**Distinctive features:** More than 40 collection scenarios across three continents are claimed.

**Origin and provenance:** Author repository baidongls/MVRSD; Google Earth source imagery.

**Documented strengths:** Creator gives image size, spatial resolution, instance count and collection breadth.

**Limitations and open questions:** No annotation review protocol, class distribution, scene-independent split, image-level source manifest or data licence verified. The phrase scenarios describes collection settings and does not establish scenario-level labels.

**Split evidence:** Not documented in inspected README.

**Access checked:** Public README, demo archive listing and Baidu link; actual downloads not tested.

**Declared rights:** No dataset licence found in inspected README; original imagery terms also require separate consideration.

**Meaning supported by labels:** Documented vehicle instances; scenario/action annotation ontology not established.

**Sources:** [Creator repository](https://github.com/baidongls/MVRSD)


### D22. RarePlanes

**Scope:** Aircraft imagery with civil and military role attributes; real and synthetic components  
**Year:** 2020  
**Sensor / representation:** Real Maxar WorldView-3 panchromatic, multispectral and pansharpened RGB; synthetic overhead RGB imagery

**Size and units:** Paper table: 14,707 real aircraft in 253 scenes across 112 locations, 22 countries and 2,142 km²; 629,551 synthetic annotations in 50,000 images. Site/abstract round to 14,700 and ~630,000. Synthetic images are 1,920×1,080; real products include 512×512 tiles.

**Categories:** 10 attributes / 33 attribute choices; seven role categories, including three civil size groups and four military role groups. Not a fixed aircraft-model taxonomy.

**Annotations and identification:** Diamond polygons (nose, wings, tail), bounding boxes, measured length/wingspan; full instance segmentation is synthetic-only.

**Distinctive features:** Wing/engine/tail/fuselage attributes; real RGB 0.31–0.39 m GSD; panchromatic and multispectral products; rich capture metadata.

**Origin and provenance:** Jacob Shermeyer et al., CosmiQ Works/In-Q-Tel and AI.Reverie; 2020 release, WACV 2021 paper; Maxar real imagery and AI.Reverie simulation.

**Documented strengths:** Professional real-data labelling with two quality-control rounds; explicit source and simulated/real distinction; documented feature definitions and geographic/seasonal variation.

**Limitations and open questions:** An airfield can occur in both real train and test splits at different dates; this is not a location-disjoint benchmark. Real tiles overlap by 20%. Diamond polygons are not full silhouette masks; synthetic masks are different ground truth. Real and synthetic totals must stay separate.

**Split evidence:** Paper explicitly allows same locations in real train/test at different dates. Synthetic study split: 45,000 images and 5,000 validation images; not 50,000 independent real observations.

**Access checked:** AWS Open Data registry provides public S3 access without an AWS account; no planned updates. Metadata verified; archive not downloaded.

**Declared rights:** Dataset CC BY-SA 4.0, explicitly stated by both creator and AWS registry.

**Meaning supported by labels:** Visual morphology and broad aircraft role labels; not model-specific identity, activity, intent or narrative descriptions.

**Sources:** [Creator dataset page](https://www.cosmiqworks.org/rareplanes/); [Primary paper full text (v2)](https://arxiv.org/html/2006.02963v2); [AWS Open Data access and licence](https://registry.opendata.aws/rareplanes/)


### D23. ShipRSImageNet (paper counts; repository currently V1.1)

**Scope:** Fine-grained mixed military and civilian ship labels  
**Year:** 2021  
**Sensor / representation:** High-resolution optical overhead images from several satellites and reused datasets

**Size and units:** Paper/README headline: 3,435 images and 17,573 ship instances, 50 types. Repository announces V1.1 with a dedicated test set but does not provide separate new headline totals. Source contributions listed in README sum to 3,473, not 3,435; unresolved.

**Categories:** Four-level hierarchy, 50 leaf labels; military ship classes/types, merchant/vessel functions, other categories and Dock.

**Annotations and identification:** Horizontal boxes, oriented boxes and polygons; formats include VOC and COCO.

**Distinctive features:** Approximately 930×930 images; mixed sensor and season provenance; fine-grained hierarchical labels.

**Origin and provenance:** Zhengning Zhang et al., IEEE JSTARS 14, 8458–8472 (2021), DOI 10.1109/JSTARS.2021.3104230; official zzndream repository.

**Documented strengths:** Experts relabelled source images, corrected mislabels and added missed small ships; repository explicitly documents source reuse and updated test release.

**Limitations and open questions:** README lists 532 xView crops (150-pixel overlap), 1,057 HRSC2016 images, 1,846 FGSD images, 21 Airbus challenge images, 17 GF-2/JL-1 images. Data independence from parent datasets cannot be assumed. Source totals and licences conflict internally. Polygon/mask representation should be inspected before calling it true silhouette segmentation.

**Split evidence:** V1.1 adds a dedicated test set; exact counts and source-disjointness not verified.

**Access checked:** Creator repository publishes Google Drive/Baidu V1.1 links; archive untested.

**Declared rights:** README expressly restricts images/annotations to academic use and prohibits commercial use, but its final section also claims Apache 2.0. Treat this as unresolved, not blanket Apache permission; source licences also differ.

**Meaning supported by labels:** Ship visible type/category, including civilian and military classes, plus dock; not allegiance, activity, readiness or textual scene explanation.

**Sources:** [Official repository and current V1.1 notice](https://github.com/zzndream/ShipRSImageNet); [Raw creator README with source/term statements](https://raw.githubusercontent.com/zzndream/ShipRSImageNet/main/README.md); [Dataset paper](https://doi.org/10.1109/JSTARS.2021.3104230)


### D24. xView (2018 detection dataset)

**Scope:** General overhead object detection; military sponsors do not make every class a military label  
**Year:** 2018  
**Sensor / representation:** Maxar/DigitalGlobe WorldView-3 optical imagery; RGB public release at about 0.3 m GSD

**Size and units:** Official page: approximately 1.0 million instances, 60 classes, 1,415 km². No canonical image-file count asserted here; image-chip counts in secondary sources vary.

**Categories:** 60 categories, with seven parent groups and additional standalone classes. Aircraft labels include small aircraft/cargo plane; maritime classes are functional vessel types.

**Annotations and identification:** Axis-aligned bounding boxes; parent/child class ontology. Paper describes RGB and 8-band imagery during annotation, but identifies the public RGB release separately.

**Distinctive features:** Wide geographic/scene diversity, small objects and pronounced class imbalance.

**Origin and provenance:** Darius Lam et al. (2018); Defense Innovation Unit Experimental, National Geospatial-Intelligence Agency and DigitalGlobe; arXiv:1802.07856.

**Documented strengths:** Three-stage quality-control process, expert gold-standard reannotation and remediation described in the primary paper.

**Limitations and open questions:** Building and small-car classes dominate. Axis-aligned boxes can include substantial background around rotated elongated objects; paper explicitly illustrates this. Image source/region independence and full current download access were not audited.

**Split evidence:** Training/validation/test manifest not inspected; historical challenge download flow is registration-linked.

**Access checked:** Official dataset and terms pages accessible; registration link published. Current complete archive retrieval was not tested.

**Declared rights:** Official terms section 5.1: CC BY-NC-SA 4.0 for the dataset. This differs from the paper's CC BY article licence.

**Meaning supported by labels:** General visible objects and some land-use groupings. Tank Car is a railway vehicle in the published ontology, not an armoured tank. No equipment-model military taxonomy or scene captions.

**Sources:** [Official dataset overview](https://xviewdataset.org/); [Primary full-text paper and class table](https://arxiv.org/html/1802.07856); [Official dataset licence, section 5.1](https://xviewdataset.org/terms.html)


## Visible and thermal imagery


### D25. DroneVehicle

**Scope:** Adjacent/general drone-view civilian vehicle detection.  
**Year:** 2022  
**Sensor / representation:** Paired RGB and infrared aerial still images.

**Size and units:** 28,439 pairs/56,878 images. Published class counts sum to 953,087 oriented boxes: 452,570 RGB + 500,517 IR. Not a unique physical-vehicle count.

**Categories:** Five: car, truck, bus, van, freight car.

**Annotations and identification:** Oriented boxes and vehicle classes separately annotated in each modality.

**Distinctive features:** Urban roads, residential areas, parking lots; day/night. 840x712 downloads include 100-pixel border around 640x512 image region.

**Origin and provenance:** Official VisDrone release; Sun, Cao, Zhu and Hu, IEEE TCSVT 2022, DOI 10.1109/TCSVT.2022.3168279.

**Documented strengths:** Detailed per-class/per-modality counts and border convention documented.

**Limitations and open questions:** Different annotation totals across modalities; pairing does not establish exact pixel registration. No military subclasses or event labels established.

**Split evidence:** Train/validation/test downloads provided; split sizes not stated in checked README.

**Access checked:** Baidu split links; README says Google Drive link will be released soon. Archives not tested.

**Declared rights:** No explicit dataset license found in README or GitHub license endpoint.

**Meaning supported by labels:** Vehicle class and oriented image location; no military activity, affiliation or intent.

**Sources:** [Official dataset README](https://github.com/VisDrone/DroneVehicle); [Author paper](https://arxiv.org/abs/2003.02437)


### D26. DSIAC ATR Algorithm Development Image Database / historical SENSIAC lead

**Scope:** Military-origin archive: military vehicles, civilian vehicles and people; request-based distribution.  
**Year:** Not established from inspected documentation  
**Sensor / representation:** Visible EO and mid-wave infrared (MWIR).

**Size and units:** Official page reports 206 GB multipart download, not an image/frame/sequence total. The 2,595-image/eight-class DSIAC description in a 2025 study is not a full-archive count.

**Categories:** People, foreign military vehicles and civilian vehicles; exact taxonomy not enumerated on current landing page.

**Annotations and identification:** Ground truth, meteorological data, target photographs, target/background temperature differentials, seven-section user guide and viewer. Exact ground-truth schema not stated in the landing-page summary.

**Distinctive features:** Commercial visible/MWIR cameras; multiple ranges and aspect angles; accompanying capture context.

**Origin and provenance:** US Army Night Vision and Electronic Sensors Directorate (NVESD), distributed by DSIAC. The old SENSIAC portal did not resolve in this audit.

**Documented strengths:** Publisher documents ground truth and capture/environment metadata; files not inspected.

**Limitations and open questions:** Complete counts, exact vehicle classes, box completeness, event labels and standard splits not established from current primary description.

**Split evidence:** No standard split stated. Paper-specific subsets must be identified separately.

**Access checked:** Current official page verified. Distribution Statement A, approved for public release, with DSIAC reserving final distribution. Request/contact process; no request submitted.

**Declared rights:** Public-release statement is not an explicit reusable-data license; distribution remains discretionary.

**Meaning supported by labels:** Military/civilian object imagery and capture metadata; no documented intent, allegiance, narrative or event-level annotation schema.

**Sources:** [Current official archive page](https://dsiac.dtic.mil/databases/atr-algorithm-development-image-database/); [Legacy URL, now redirected](https://dsiac.org/databases/atr-algorithm-development-image-database/); [2025 paper describing a DSIAC subset, IV-A](https://arxiv.org/html/2501.07396v1)


### D27. M3FD

**Scope:** Adjacent/general civilian road and public-scene multispectral detection.  
**Year:** 2022  
**Sensor / representation:** Registered visible and infrared still-image pairs.

**Size and units:** Main set: 4,200 pairs/8,400 images. Current README also lists 300 independent fusion pairs/600 images. Paper v1 reports 33,603 objects; current README 34,407 labels. Preserve discrepancy.

**Categories:** Six: People, Car, Bus, Motorcycle, Lamp, Truck.

**Annotations and identification:** Manual detection boxes/classes; YOLO text labels. Paper describes four environmental condition groups and ten sub-scenarios.

**Distinctive features:** Mostly 1024x768; synchronized optical/infrared sensor system; calibrated and homography-registered pairs.

**Origin and provenance:** TarDAL authors; Dalian University of Technology, Golden Stone Beach resort and Jinzhou District roads, Dalian, China.

**Documented strengths:** Alignment and capture sites documented. Authors explicitly acknowledge some labels may be missed or mismarked.

**Limitations and open questions:** Box count varies by source version. Separate 300-pair fusion set is not the 4,200-pair detection set. No independent label/image audit.

**Split evidence:** Repository describes train/val/pred metadata; canonical split totals not established here.

**Access checked:** Author Google Drive and Baidu links published; actual archives not tested.

**Declared rights:** TarDAL code is GPL-3.0; a separate clear off-site imagery license not verified.

**Meaning supported by labels:** Ordinary object boxes and environmental groups. Multi-scenario is not military event or intent annotation.

**Sources:** [Official dataset README](https://github.com/JinyuanLiu-CV/TarDAL); [Original paper v1, dataset section](https://arxiv.org/html/2203.16220v1); [Repository license](https://github.com/JinyuanLiu-CV/TarDAL/blob/main/LICENSE)


### D28. TNO Image Fusion Dataset

**Scope:** Military-relevant and civilian surveillance imagery; no formal detection taxonomy established.  
**Year:** 2014  
**Sensor / representation:** Intensified visual, NIR and LWIR nighttime imagery; different camera collections.

**Size and units:** Official v2 description does not give total items. Original v1 published 2014-04-26; current v2 published 2022-10-15. Third-party curated subset counts are not official totals.

**Categories:** No formal object class list in official description.

**Annotations and identification:** Camera/capture references in Athena, DHV, FEL and TRICLOBS folders; no box/mask/event schema documented on landing page.

**Distinctive features:** Multiband nighttime imagery with several sensor families and recording references.

**Origin and provenance:** TNO, Soesterberg, Netherlands; official versioned Figshare record.

**Documented strengths:** Versioned DOI, named sensor families and explicit reuse license.

**Limitations and open questions:** Complete counts and task labels not established in checked primary summary. Camera collections not necessarily homogeneous.

**Split evidence:** No standard train/validation/test split stated.

**Access checked:** Public Figshare release; files not downloaded.

**Declared rights:** Official v2 metadata CC BY 4.0; description allows research/publication with TNO credit and dataset citation.

**Meaning supported by labels:** Military-relevant scenes are described, but no formal military identity/event taxonomy. Separate from TRICLOBS dynamic release.

**Sources:** [Official v2 release](https://figshare.com/articles/dataset/TNO_Image_Fusion_Dataset/1008029); [Version 2 DOI](https://doi.org/10.6084/m9.figshare.1008029.v2); [Original version](https://doi.org/10.6084/m9.figshare.1008029.v1)


### D29. TRICLOBS Dynamic Multiband Image Dataset

**Scope:** Military/civilian surveillance field-trial scenarios with clip-level action descriptions; not real-combat footage.  
**Year:** 2016  
**Sensor / representation:** Registered visible (400-700 nm), NIR (700-1000 nm), LWIR (8-14 micrometers) motion sequences.

**Size and units:** 16 sequences at three locations. Table 1 per-sequence counts sum to 56,865 multiband time frames (derived, not a filesystem count).

**Categories:** No closed detection taxonomy. Described content includes military/civilian people, vehicles, carried objects, buildings and foliage.

**Annotations and identification:** Paper Table 1 supplies one natural-language Action brief plus frame count per clip. Reference color photographs and sensor documentation; no verified dense boxes, track IDs or timed event boundaries.

**Distinctive features:** Registered three-band 640x480 output; false-color RGB stores the three spectral bands; color reference photographs.

**Origin and provenance:** TNO field trials; Toet, Hogervorst and Pinkus, PLOS ONE 2016; official Figshare v1.

**Documented strengths:** Versioned licensed release, sensor characterization and explicit 16-row scenario-description table.

**Limitations and open questions:** Sixteen field-trial clips at three locations. Clip briefs are not dense action labels or intent ground truth. Dataset files not inspected.

**Split evidence:** No standard machine-learning split specified.

**Access checked:** Public Figshare record/files and open paper; files not downloaded.

**Declared rights:** Official dataset CC BY 4.0; paper and scenario table also CC BY.

**Meaning supported by labels:** Actual clip-level narrative scenario metadata for staged visible actions; no verified fine-grained event timeline or intent annotation.

**Sources:** [Official dataset](https://figshare.com/articles/dataset/The_TRICLOBS_Dynamic_Multiband_Image_Dataset/3206887); [Primary paper](https://doi.org/10.1371/journal.pone.0165016); [Scenario description table](https://doi.org/10.1371/journal.pone.0165016.t001)


## Video tracking


### D30. Anti-UAV original / later Anti-UAV300 label

**Scope:** Adjacent/general ground-to-air consumer-drone tracking; no military-platform taxonomy.  
**Year:** 2021  
**Sensor / representation:** Visible/thermal video pairs; original paper explicitly says unaligned.

**Size and units:** Original v3 paper: 318 pairs, ~585.9K boxes (abstract over 580K). Current umbrella calls RGB+IR release Anti-UAV300; version name is not exact paper count.

**Categories:** Tracked UAVs, mainly DJI and Parrot; no verified military subtype label set.

**Annotations and identification:** Boxes, per-frame existence/visibility flag, seven challenge attributes. Progressive coarse-to-fine annotation/correction described.

**Distinctive features:** 25 FPS MP4, day/night, diverse backgrounds and out-of-view targets.

**Origin and provenance:** UCAS/CASIA/Institute of North Electronic Equipment collaboration; original and umbrella author repositories.

**Documented strengths:** Annotation/split protocol, absence flags, challenge attributes and author start-frame corrections published.

**Limitations and open questions:** Modalities unaligned. Train/validation are different clips from same videos; test independent. Do not infer independent manual annotation for every release frame from total boxes.

**Split evidence:** 160 train, 67 validation, 91 test paired sequences in paper version.

**Access checked:** Author Drive/Baidu links; original README lists four start-frame corrections; archives not downloaded.

**Declared rights:** Umbrella project MIT; original paper says academic research. Separate off-site imagery terms not independently verified.

**Meaning supported by labels:** UAV location/existence and tracking conditions. No military identity, intent, threat, authorization or allegiance ground truth.

**Sources:** [Original paper v3](https://arxiv.org/html/2101.08466v3); [Original release/corrections](https://github.com/ucas-vg/Anti-UAV); [Current version/license table](https://github.com/ZhaoJ9014/Anti-UAV)


### D31. Anti-UAV410

**Scope:** Adjacent/general thermal drone tracking.  
**Year:** 2023  
**Sensor / representation:** Thermal infrared videos only.

**Size and units:** 410 videos with over 438K manually annotated boxes, per dedicated author README; not paired RGB-T.

**Categories:** UAV target; no military identity taxonomy verified.

**Annotations and identification:** Boxes, target absence, ten ordered video attributes including size bands. Frame attributes in IR_label.json explicitly incomplete.

**Distinctive features:** Thermal crossover, out-of-view, scale variation, fast motion, occlusion and background clutter.

**Origin and provenance:** Huang and coauthors, IEEE TPAMI 2023; official HwangBo94/Anti-UAV410 repository.

**Documented strengths:** Author toolkit, explicit attribute ordering and honest frame-attribute completeness caveat.

**Limitations and open questions:** Incomplete frame attributes are not exhaustive scenario labels. No RGB in this version; files not inspected.

**Split evidence:** Train/validation/test documented; exact split counts not established here.

**Access checked:** Dedicated official repository provides Drive/Baidu links although umbrella lists 410 Drive N/A.

**Declared rights:** Dedicated repo has no detected license; umbrella MIT does not independently verify off-site data terms.

**Meaning supported by labels:** Drone location/presence and image/tracking difficulty, not military identity or event narratives.

**Sources:** [Dedicated official release](https://github.com/HwangBo94/Anti-UAV410); [Umbrella version table](https://github.com/ZhaoJ9014/Anti-UAV)


### D32. AntiUAV600

**Scope:** Adjacent/general thermal drone detection/tracking; version disambiguation.  
**Year:** 2023  
**Sensor / representation:** Thermal infrared video only.

**Size and units:** 600 sequences and over 723K thermal frames densely annotated with boxes per paper v2. Overlap with prior versions not audited.

**Categories:** UAV target; no fine-grained military taxonomy established.

**Annotations and identification:** Dense frame boxes; umbrella task defines target absence/state handling. Files/schema not inspected.

**Distinctive features:** Complex backgrounds and drone appearance/reappearance.

**Origin and provenance:** Zhu and coauthors, arXiv:2306.15767v2; official Anti-UAV repository links ModelScope release.

**Documented strengths:** Primary count/dense annotation description and explicit publisher-linked release.

**Limitations and open questions:** Versions cannot be summed as disjoint datasets. No event/caption/identity-class audit.

**Split evidence:** Not established from checked abstract and umbrella README.

**Access checked:** Official repository points to ModelScope; actual archive access untested.

**Declared rights:** Umbrella MIT; ModelScope dataset-specific terms unverified.

**Meaning supported by labels:** Drone localization and existence; no military scenario/intent label schema.

**Sources:** [Primary paper v2](https://arxiv.org/abs/2306.15767v2); [Official version table](https://github.com/ZhaoJ9014/Anti-UAV); [Publisher-linked release](https://modelscope.cn/datasets/ly261666/3rd_Anti-UAV/files)


### D33. DUT Anti-UAV

**Scope:** Adjacent/general visible-light consumer-drone detection/tracking.  
**Year:** 2022  
**Sensor / representation:** Visible-light still images and video; no thermal channel.

**Size and units:** 10,000 images/10,109 object instances; separate 20 tracking videos (paper mean length 1,240 frames). Table Num values are objects, not images.

**Categories:** UAV target; over 35 drone types occur visually, but a 35-way annotated classification task not established.

**Annotations and identification:** Manual detection boxes and per-frame tracking boxes.

**Distinctive features:** Detection images 160x240 to 3744x5616; video 1280x720 or 1920x1080; varied outdoor scenes/light/weather.

**Origin and provenance:** Zhao, Zhang, Li and Wang, Dalian University of Technology, IEEE TITS 2022; author repository.

**Documented strengths:** Paper separates image and instance counts and documents manual labels, splits and image sizes.

**Limitations and open questions:** Source analysis shows central object-position bias. Only 20 tracking videos. No military classes/thermal channel; individual image rights/provenance not audited.

**Split evidence:** Train/test/validation images 5,200/2,200/2,600; boxes 5,243/2,245/2,621. Twenty tracking evaluation videos.

**Access checked:** Official Drive/Baidu detection splits and separate tracking images/ground truth; not downloaded.

**Declared rights:** Repository Apache-2.0; separate explicit off-site imagery terms unverified. Paper CC BY-NC-SA is not automatically data license.

**Meaning supported by labels:** UAV boxes and trajectories; no event, intent, threat or authorization labels.

**Sources:** [Official release](https://github.com/wangdongdut/DUT-Anti-UAV); [Primary paper III](https://arxiv.org/html/2205.10851v1); [Repository license](https://github.com/wangdongdut/DUT-Anti-UAV/blob/master/LICENSE)


### D34. Military Vehicles in Low-FPS UAV Footage validation benchmark

**Scope:** Explicit military vehicle MOT labels from online video; author-reviewed restricted-purpose access.  
**Year:** 2025  
**Sensor / representation:** UAV-view video; no thermal channel or registered multimodal release explicitly established.

**Size and units:** Paper III: 119 videos/18,421 frames/58,897 boxes. Live request form: all recordings 5 FPS. Sources 480p to 4K, analyzed clips 7-90 seconds.

**Categories:** Three coarse groups: Heavily Armored; Lightly Armored or Unarmored; Trucks. Not a fine-grained platform taxonomy.

**Annotations and identification:** Expert boxes, class labels, unique vehicle track IDs and temporal links; multiple-review quality control.

**Distinctive features:** Online UAV videos with varied views/occlusion; paper reports 14% winter/86% summer.

**Origin and provenance:** Kostiv and coauthors, UCU/CIDTD MoD Ukraine, ICMCIS 2025; raw sources Telegram, X and YouTube.

**Documented strengths:** Concrete clip/frame/box totals and human track-consistency review described.

**Limitations and open questions:** Original video redistribution rights not established. Grant/download untested. Coarse military classes and within-video IDs are not exact platform identities or scenario/intent labels.

**Split evidence:** Validation benchmark; no public canonical train/test split verified.

**Access checked:** Live author form verified, not submitted. Authors consider requests (form says 2-4 days); asks purpose/security and prior authorization for redistribution/repurposing.

**Declared rights:** No open data license verified. Purpose limitation/no redistribution or repurposing without authorization in request form. Paper license is separate.

**Meaning supported by labels:** Coarse military object class, location and within-video persistent identity; no documented event narratives, intent or allegiance annotation.

**Sources:** [Primary paper III/access statement](https://arxiv.org/html/2507.05229v1); [Verified author request form](https://docs.google.com/forms/d/e/1FAIpQLSdKceLoF_L3242FDJLLFdIiVDepQ0imt54SwbxnFgt1sSpjug/viewform?usp=sharing); [Published DOI](https://doi.org/10.1109/ICMCIS64378.2025.11047873)


### D35. VTUAV / DUT-VTUAV

**Scope:** Adjacent/general ordinary-object tracking filmed from a UAV; UAV is the camera platform.  
**Year:** 2022  
**Sensor / representation:** Registered visible/thermal video pairs.

**Size and units:** 500 sequences/1,664,549 pairs (~1.7M). Sparse boxes every 10 frames: 326,961 boxes across modalities. Mask subset: 24,464 masks at 1 FPS across 100 sequences.

**Categories:** Five superclasses: pedestrian, vehicle, animal, train, ship; 13 subclasses; 15 scene types in two cities.

**Annotations and identification:** Separate modality boxes every ten frames; masks; 13 sequence attributes; 301,678 frames with 430,960 frame-attribute labels (some automatically derived).

**Distinctive features:** 30 FPS; output stored 1920x1080; thermal native 640x480, rescaled during registration. Short-/long-term/mask subsets.

**Origin and provenance:** Dalian University of Technology authors; DJI Matrice 300 RTK/Zenmuse H20T; CVPR 2022.

**Documented strengths:** Precise annotation cadence/counts, mask subset and challenge hierarchy documented.

**Limitations and open questions:** 1.7M pairs are not 1.7M manually boxed pairs. Output thermal size is resampled. Three archive parts corrected April 2022. No military classes/events.

**Split evidence:** 250 train (207 short-term/43 long-term), 250 test (176/74). Masks: 50 train/50 test sequences.

**Access checked:** Official Drive/Baidu RGB-T, RGB-only and mask releases; archives not tested.

**Declared rights:** No explicit dataset license found in project/README; GitHub license endpoint no license.

**Meaning supported by labels:** Localization/masks and imaging/tracking challenges, plus generic scene categories. No military scenario or intent labels.

**Sources:** [Official project and release notices](https://zhang-pengyu.github.io/DUT-VTUAV/); [Official repository](https://github.com/zhang-pengyu/DUT-VTUAV); [Paper with annotation details](https://arxiv.org/html/2204.04120v1)


## Infrared small spots


### D36. IRSTD-1k

**Scope:** Adjacent/general real infrared small-target segmentation.  
**Year:** 2022  
**Sensor / representation:** Real infrared still images.

**Size and units:** CVPR paper: 1,000 images, 512x512. Current official README: 1,001. Discrepancy unresolved without archive inspection.

**Categories:** Paper describes drones, creatures, vessels and vehicles visually; multi-class identity labels not established.

**Annotations and identification:** Manual pixel-level target masks.

**Distinctive features:** Sea/river/field/mountain/city/cloud backgrounds; varied shapes and sizes.

**Origin and provenance:** Mingjin Zhang, Rui Zhang and coauthors, ISNet CVPR 2022; official RuiZhang97/ISNet.

**Documented strengths:** Real images, manually annotated masks and collection/resolution details documented.

**Limitations and open questions:** 1,000/1,001 discrepancy. Generic target masks do not identify military objects. Files not inspected.

**Split evidence:** Paper 50% train/30% validation/20% test.

**Access checked:** Official Drive and Chinese cloud mirror; archive not downloaded.

**Declared rights:** Dataset table explicitly says Agreement (MIT License); repository MIT. Underlying rights not separately audited.

**Meaning supported by labels:** Target presence/shape; varied scenery/content is not military identity or event annotation.

**Sources:** [Official release, 1,001 claim](https://github.com/RuiZhang97/ISNet); [CVPR paper, 1,000 claim](https://openaccess.thecvf.com/content/CVPR2022/papers/Zhang_ISNet_Shape_Matters_for_Infrared_Small_Target_Detection_CVPR_2022_paper.pdf); [Repository license](https://github.com/RuiZhang97/ISNet/blob/main/LICENSE)


### D37. NUDT-SIRST

**Scope:** Adjacent/general synthetic small-target segmentation; not military identity recognition.  
**Year:** 2023  
**Sensor / representation:** Synthetic infrared small targets with real infrared backgrounds.

**Size and units:** 1,327 synthesized 256x256 images; introduced in 2021 preprint, final IEEE TIP paper 2023.

**Categories:** Generic target, with point/spot/extended forms; not verified vehicle/platform identity classes.

**Annotations and identification:** Synthesis-derived pixel-level ground-truth target masks.

**Distinctive features:** Cloud/city/sea/field/highlight backgrounds; varied target morphology, size and count.

**Origin and provenance:** Li, Xiao, Wang and coauthors, DNANet; official YeRen123455/Infrared-Small-Target-Detection.

**Documented strengths:** Synthetic provenance, known masks, size and count explicitly stated.

**Limitations and open questions:** Synthetic realism not independently validated. Varied target forms are not military identity labels.

**Split evidence:** Repository shows a 50_50 split option; lists not inspected.

**Access checked:** Official Baidu download; archive not downloaded.

**Declared rights:** Repository MIT is software wording with inherited 2018 author credit; explicit dataset terms not independently verified.

**Meaning supported by labels:** Target/background and morphology; no military events or platform identity schema.

**Sources:** [Official dataset description](https://github.com/YeRen123455/Infrared-Small-Target-Detection); [Author paper](https://arxiv.org/abs/2106.00487); [Repository license](https://github.com/YeRen123455/Infrared-Small-Target-Detection/blob/master/LICENSE)


### D38. SIRST (often called NUAA-SIRST in later papers)

**Scope:** Adjacent/general single-frame infrared small-target localization.  
**Year:** 2021  
**Sensor / representation:** IR still images from sequences; paper includes short-/mid-wave and 950-nm images.

**Size and units:** Original paper: 427 images/480 target instances. Authors explicitly request SIRST rather than NUAA-SIRST. SIRST v2 is a separate release.

**Categories:** One generic target class; original paper explicitly declines finer classification for these small objects.

**Annotations and identification:** Bounding boxes and semantic segmentation masks.

**Distinctive features:** One representative image per source sequence; small/dim objects and diverse backgrounds.

**Origin and provenance:** Yimian Dai and coauthors, WACV 2021; official YimianDai/sirst repository.

**Documented strengths:** Primary counts, annotation formats and sequence-selection rationale documented.

**Limitations and open questions:** Small corpus and mixed IR wavelengths. Binary masks cannot establish military identities. Original image rights not individually audited.

**Split evidence:** Original paper approximately 50% train/20% validation/30% test; later papers use different splits.

**Access checked:** Public official GitHub release; no images/annotation files inspected.

**Declared rights:** No explicit license in checked README or GitHub license endpoint.

**Meaning supported by labels:** Target/background and target position only; no military subtype or scenario/event labels.

**Sources:** [Official repository/naming correction](https://github.com/YimianDai/sirst); [Original WACV paper](https://openaccess.thecvf.com/content/WACV2021/papers/Dai_Asymmetric_Contextual_Modulation_for_Infrared_Small_Target_Detection_WACV_2021_paper.pdf); [Separate successor](https://github.com/YimianDai/open-sirst-v2)


## Web and synthetic imagery


### D39. 15-class RGB military-vehicle collection described by TNO studies

**Scope:** Paper-described military vehicle image collection; public release unverified  
**Year:** 2026  
**Sensor / representation:** Real web-scraped RGB imagery; synthetic variants discussed separately

**Size and units:** 959 real images across 15 military-vehicle classes; 2026 paper reuses a collection from Heslinga et al. (SPIE, 2024). Do not count this as a newly independently acquired 2026 dataset.

**Categories:** 15 military-vehicle classes grouped under vehicle superclasses.

**Annotations and identification:** Object-detection labels; released annotation format and per-image object counts not verified.

**Distinctive features:** Web image provenance and explicit fixed real-image split sizes.

**Origin and provenance:** Ella P. Fokkinga et al., TNO, arXiv:2604.18076 (20 Apr 2026); cites Heslinga et al. (2024), Combining simulated data, foundation models, and few real samples for training object detectors.

**Documented strengths:** Primary full text reports exact real-image counts and explicitly acknowledges reuse of the earlier collection.

**Limitations and open questions:** Web image rights and independent scene/object identities are not documented in inspected text. Public downloadable dataset/manifest/licence not found; this is a literature entry, not a verified open-data asset. No operational performance conclusions included.

**Split evidence:** Paper reports 360 training, 150 validation and 449 test images; total 959.

**Access checked:** Public paper full text; a creator-controlled public data release was not verified.

**Declared rights:** No dataset-specific licence verified. The paper's arXiv licence does not grant rights in web images.

**Meaning supported by labels:** Fine-grained equipment identity classes in RGB images; no captions or current status/intent labels.

**Sources:** [Primary full-text paper](https://arxiv.org/html/2604.18076); [Primary arXiv record](https://arxiv.org/abs/2604.18076)


### D40. milair-dataset

**Scope:** Military-labelled aircraft  
**Year:** Not established from inspected documentation  
**Sensor / representation:** RGB frames from YouTube videos; 1280 x 720

**Size and units:** 660 is the sum of the six README class-occurrence counts, not a verified unique-image total.

**Categories:** 6 aircraft types.

**Annotations and identification:** Pascal VOC bounding boxes and type labels.

**Distinctive features:** Consistent image size; extracted video stills rather than a documented temporal tracking benchmark.

**Origin and provenance:** tlkh creator repository; frames from multiple YouTube videos.

**Documented strengths:** Annotations and images are listed in the repository; explicit source medium and per-class counts.

**Limitations and open questions:** Adjacent frames may be correlated. No verified split by source video, duplicate rate, annotation error rate or underlying video rights.

**Split evidence:** No official independent video-level split documented in README.

**Access checked:** Public repository; dataset images not downloaded.

**Declared rights:** Repository declares MIT; that alone does not establish rights to every source video frame.

**Meaning supported by labels:** Aircraft type and image location; no track continuity or event labels.

**Sources:** [Creator repository](https://github.com/tlkh/milair-dataset)


### D41. Military Aircraft Detection Dataset (Kaggle v105)

**Scope:** Military-labelled and civilian aircraft  
**Year:** 2026  
**Sensor / representation:** Visible photographs; mixed views

**Size and units:** Current metadata version 105, updated 29 October 2026. Inspected description does not provide a verified unique-image count; do not infer one from bytes or crop files.

**Categories:** 114 total classes in current description: 103 military-labelled aircraft types and 11 commercial airliner types.

**Annotations and identification:** CSV boxes in xmin/ymin/xmax/ymax coordinates, class and image dimensions; separate derived crop folders.

**Distinctive features:** Full-image object annotations and per-object classification crops are separate representations of overlapping content.

**Origin and provenance:** T Nakamura, Kaggle owner a2015003713. Current owner metadata inspected through public API.

**Documented strengths:** Active version history and an explicit annotation schema; merged visually similar variants are acknowledged.

**Limitations and open questions:** Older mirrors advertise different class totals and licences. No unique-image inventory, class balance, per-image provenance, inter-annotator accuracy or independent split audit completed.

**Split evidence:** Train/test source-independence not established by inspected description.

**Access checked:** Public owner card/API; download/login workflow not tested.

**Declared rights:** Current owner metadata says Unknown. A mirror Apache tag cannot resolve the owner licence.

**Meaning supported by labels:** Appearance category and box; no event or intent annotations. Crops do not add new independent scenes.

**Sources:** [Owner dataset page](https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset); [Owner metadata API](https://www.kaggle.com/api/v1/datasets/view/a2015003713/militaryaircraftdetectiondataset)


### D42. Military and Civilian Vehicles Classification (Mendeley v1)

**Scope:** Military-labelled and civilian objects  
**Year:** 2021  
**Sensor / representation:** Visible photographs; mixed viewpoints

**Size and units:** 6,642 positive images, 130 negative images; 11,528 annotated objects according to the depositor. These are different counting units.

**Categories:** 6 broad vehicle and aircraft categories, divided into military-labelled and civilian-labelled classes.

**Annotations and identification:** Object labels distributed as TXT, CSV, XML and TFRecord. Individual annotation files were not inspected.

**Distinctive features:** A negative-image subset is explicitly documented. Despite the title saying classification, the description discusses multiple labelled objects per image.

**Origin and provenance:** Versioned Mendeley deposit by Gupta, Pareek, Singal and Rao; DOI 10.17632/njdjkbxdpn.1. Original per-image provenance is not explained on the landing page.

**Documented strengths:** Stable DOI, named contributors, version number, explicit positive/negative counts and annotation formats.

**Limitations and open questions:** No verified label error rate, duplicate audit, source-video grouping or geographic coverage. Appearance labels are not evidence of ownership, affiliation or intent.

**Split evidence:** Independent scene/source split procedure not described on the inspected landing page.

**Access checked:** Public deposit and download controls visible; full archive not downloaded.

**Declared rights:** Deposit declares CC BY 4.0. Individual source-image rights were not independently traced.

**Meaning supported by labels:** Object categories and locations; no documented event, relationship or intent labels.

**Sources:** [Mendeley Data v1](https://data.mendeley.com/datasets/njdjkbxdpn/1)


### D43. Military Assets Dataset (Kaggle v5)

**Scope:** Military-labelled mixed objects  
**Year:** 2024  
**Sensor / representation:** Visible images; collection process incompletely documented

**Size and units:** 21,978 train + 2,941 validation + 1,396 test = 26,315 author-reported labelled images.

**Categories:** 12 broad categories spanning people, vehicles, aircraft, ships and other equipment or structures.

**Annotations and identification:** YOLO-format object labels advertised by title/card; annotation files were not audited.

**Distinctive features:** Published split counts and a mixed class vocabulary.

**Origin and provenance:** RAWx18 / Ryan Madhuwala community Kaggle deposit, current version 5.

**Documented strengths:** A public card identifies classes, split counts, author and declared licence.

**Limitations and open questions:** No per-image origins, deduplication report, label review study, augmentation accounting or scene-level split method shown. Publisher claims about suitability are not independent validation. Person-role labels cannot establish legal status or intent.

**Split evidence:** Published split sizes; independence and duplicate leakage unverified.

**Access checked:** Public card/API; archive download not performed.

**Declared rights:** Card declares CC BY 4.0; upstream rights and provenance remain unverified.

**Meaning supported by labels:** Object-category annotations; no documented temporal events or verified scenario explanations.

**Sources:** [Owner dataset card](https://www.kaggle.com/datasets/rawsi18/military-assets-dataset-12-classes-yolo8-format); [Owner metadata API](https://www.kaggle.com/api/v1/datasets/view/rawsi18/military-assets-dataset-12-classes-yolo8-format)


### D44. Military-Aircraft-Detection (Illia56 mirror)

**Scope:** Military-labelled aircraft; mirror status  
**Year:** Not established from inspected documentation  
**Sensor / representation:** Visible aircraft imagery

**Size and units:** Card text reports 43 types. Its raw size-category tag and platform index disagree; neither is a verified image inventory.

**Categories:** 43 aircraft types according to card; not interchangeable with the current 114-class Kaggle description.

**Annotations and identification:** Card describes Pascal VOC-coordinate boxes. Other task tags such as depth estimation or segmentation do not establish those annotations exist.

**Distinctive features:** Example of community repackaging with a different ontology snapshot.

**Origin and provenance:** Hugging Face Illia56 card; exact source/version chain not established by card.

**Documented strengths:** Public documentation makes its box representation visible and asks users to report duplicates and wrong labels.

**Limitations and open questions:** No verified image count, split protocol or data rights chain. Broad task tags are unsupported by a documented annotation inventory. Do not count as a known independent collection.

**Split evidence:** Not established.

**Access checked:** Card public; data files not downloaded.

**Declared rights:** Card declares Apache-2.0; source-image rights and relationship to differently licensed owner datasets unresolved.

**Meaning supported by labels:** Advertised aircraft labels and boxes only; no evidence for scene events or all tagged tasks.

**Sources:** [Dataset card](https://huggingface.co/datasets/Illia56/Military-Aircraft-Detection); [Raw card inspected](https://huggingface.co/datasets/Illia56/Military-Aircraft-Detection/raw/main/README.md)


### D45. RGB military-target collection described by Jeong et al. (2025)

**Scope:** Paper-described military object data; verified public dataset release not established  
**Year:** 2025  
**Sensor / representation:** Unreal Engine synthetic RGB imagery and web-collected real RGB images

**Size and units:** The accessible primary abstract does not report dataset sizes or a complete class inventory.

**Categories:** Military targets; exact label inventory not established from abstract.

**Annotations and identification:** Object detection context; precise released annotation schema not verified.

**Distinctive features:** Synthetic and real image components described in a research paper.

**Origin and provenance:** Jongoh Jeong, Youngjin Oh, Gyeongrae Nam, Jeongeun Lee, Kuk-Jin Yoon; Exploring Syn-to-Real Domain Adaptation for Military Target Detection, arXiv:2512.23208, 29 Dec 2025.

**Documented strengths:** Primary paper provenance is identifiable; real and synthetic origins are distinguished.

**Limitations and open questions:** A public paper and web-collected source images do not establish a publicly downloadable, rights-cleared dataset. Counts, annotations, source independence and data licence remain unverified.

**Split evidence:** Abstract describes a synthetic training/real validation pair; no exact file manifest verified.

**Access checked:** Public arXiv abstract/PDF link; no dataset release verified. HTML full text unavailable in this inspection.

**Declared rights:** No dataset-specific licence verified; arXiv article licence is separate.

**Meaning supported by labels:** Paper describes object detection labels, not scene-caption or situational-narrative annotations.

**Sources:** [Primary arXiv record](https://arxiv.org/abs/2512.23208)


## Camouflage segmentation


### D46. CAMO

**Scope:** Natural and artificial camouflage; adjacent comparison  
**Year:** 2019  
**Sensor / representation:** Visible images

**Size and units:** 1,250 camouflaged images plus 1,250 non-camouflaged COCO images. The often-quoted 1,250 refers to the camouflaged half.

**Categories:** Naturally and artificially camouflaged objects; paper context includes animals and humans.

**Annotations and identification:** Objectness/foreground masks; CAMO++ instance annotations belong to a separate extension.

**Distinctive features:** Includes both camouflaged examples and non-camouflaged comparison images.

**Origin and provenance:** Le et al., CVIU 2019; official author project page. Non-camouflaged images come from MS-COCO.

**Documented strengths:** Creator states subset counts, masks, split sizes and licence.

**Limitations and open questions:** Foreground mask is not fine-grained identity. COCO reuse means overlap with COCO-derived resources is possible. No independent data-quality audit performed.

**Split evidence:** Each half has 1,000 train / 250 test images, per creator page.

**Access checked:** Public creator links; archive not downloaded.

**Declared rights:** Creator page declares CC BY-NC-SA 4.0, with no commercial use.

**Meaning supported by labels:** Camouflaged foreground pixels; no action or scenario label system.

**Sources:** [Creator project page](https://sites.google.com/view/ltnghia/research/camo); [Creator evaluation repository](https://github.com/ltnghia/CAMO)


### D47. COD10K

**Scope:** General natural camouflage; not a military identity dataset  
**Year:** 2020  
**Sensor / representation:** Visible natural-scene images

**Size and units:** Original paper abstract reports 10,000 images across 78 categories; benchmark subsets must be distinguished from the full release.

**Categories:** Natural-scene object categories; name does not imply military classes.

**Annotations and identification:** Category, boxes, object/instance masks and detailed boundary/matting annotations described by paper.

**Distinctive features:** Objects visually similar to surrounding backgrounds; multiple annotation granularities.

**Origin and provenance:** Fan et al., CVPR 2020; creator SINet repository.

**Documented strengths:** Primary paper and creator repository document annotation diversity and a re-verification procedure.

**Limitations and open questions:** Natural camouflage is not evidence of military identity or intent. No label error audit conducted here. Historic project domain returned unrelated content during this review; cite the creator repository/paper instead.

**Split evidence:** Creator notes revised training/test bundles; release versions need explicit identification.

**Access checked:** Creator repository and cloud data links visible; archive not downloaded.

**Declared rights:** Creator explicitly restricts dataset and derived content to noncommercial purposes.

**Meaning supported by labels:** Visibility and shape of camouflaged objects; no operational event annotations.

**Sources:** [Primary CVPR paper](https://openaccess.thecvf.com/content_CVPR_2020/html/Fan_Camouflaged_Object_Detection_CVPR_2020_paper.html); [Creator repository](https://github.com/DengPingFan/SINet)


## Scene, change and language


### D48. FSAR-Cap

**Scope:** General fine-grained SAR descriptions  
**Year:** 2025  
**Sensor / representation:** SAR imagery and captions

**Size and units:** 72,400 image-text pairs, five captions per image. 2025 preprint; creator repository cites a 2026 IEEE GRSL publication and announces a V1 release.

**Categories:** Paper describes 22 underlying FAIR-CSAR object categories and 10 scene categories.

**Annotations and identification:** Image and object descriptions from templates, manual correction/supplementation and LLM language standardization.

**Distinctive features:** Descriptions combine scene labels, objects and spatial relations.

**Origin and provenance:** Derived from FAIR-CSAR; source collection described as 32 locations.

**Documented strengths:** Paper documents human review of generated descriptions and distinguishes image count from caption count.

**Limitations and open questions:** Annotation-quality superiority is the authors claim, not an independent audit. Caption length does not prove correctness; imagery overlaps FAIR-CSAR. Archive completeness and dataset licence not verified.

**Split evidence:** No independent source-split audit performed.

**Access checked:** Creator repository announces public availability and links a Science Data Bank V1 landing page. Archive download and file completeness not tested.

**Declared rights:** Dataset licence not verified. The arXiv article licence does not license source images.

**Meaning supported by labels:** Scene/object descriptions and geometry; no documented temporal military event truth.

**Sources:** [Primary paper](https://arxiv.org/html/2510.16394v1); [Creator repository and release announcement](https://github.com/hitjiao/FSAR-Cap); [Science Data Bank V1 landing page](https://www.scidb.cn/en/detail?dataSetId=e4c17cc137e74878b46c03d8650ffa78&version=V1&code=o00118)


### D49. Functional Map of the World (fMoW)

**Scope:** General land-use/function labels; government-sponsored  
**Year:** 2018  
**Sensor / representation:** Satellite RGB or 4-/8-band multispectral, temporal observations

**Size and units:** Primary CVPR abstract reports over one million images from over 200 countries. Different fMoW-full/RGB and derived releases must not be added together.

**Categories:** 63 categories in original abstract, including false detection; often described as 62 substantive classes.

**Annotations and identification:** Bounding regions with functional labels plus timestamps and acquisition metadata.

**Distinctive features:** Temporal images, image-acquisition metadata and region-function labels distinguish it from small-object box datasets.

**Origin and provenance:** Government-sponsored challenge with DigitalGlobe imagery; creator repository.

**Documented strengths:** Primary publication, public data guide, defined metadata and explicit custom licence.

**Limitations and open questions:** Function labels can depend on context beyond appearance; repeated observations of one site are correlated. No assurance of continuous events or operational activity labels.

**Split evidence:** Official challenge partitions exist; raw location grouping not independently audited.

**Access checked:** Public AWS data instructions; full approximately 3.5 TB or RGB approximately 200 GB reported by creator; not downloaded.

**Declared rights:** Custom Functional Map of the World Challenge Public License. Data sharing/adaptations restricted to noncommercial use; licence explicitly excludes trained algorithms from its Adapted Material definition. This is not a general Apache/MIT licence.

**Meaning supported by labels:** Functional land-use/region categories and temporal observations; not a complete scenario narrative.

**Sources:** [Primary CVPR paper](https://openaccess.thecvf.com/content_cvpr_2018/html/Christie_Functional_Map_of_CVPR_2018_paper.html); [Creator data guide](https://github.com/fMoW/dataset); [Data licence](https://raw.githubusercontent.com/fMoW/dataset/master/LICENSE)


### D50. LEVIR-CC

**Scope:** General remote-sensing change descriptions  
**Year:** 2022  
**Sensor / representation:** Paired optical remote-sensing images

**Size and units:** 50,385 difference-describing sentences; five per pair. Distinct from LEVIR-CD image-pair counts and LEVIR-MCI annotations.

**Categories:** Changes and unchanged content described in language.

**Annotations and identification:** Pre/post images and JSON captions; a separate LEVIR-MCI resource adds change masks.

**Distinctive features:** Temporal visual comparison with multiple textual descriptions.

**Origin and provenance:** Chen-Yang Liu creator repository and author-linked Hugging Face dataset card.

**Documented strengths:** Creator documents structure, pair/sentence units and train/validation/test folders.

**Limitations and open questions:** No verified source-scene independence, caption error rate or complete image-rights chain. Five captions for a pair do not provide five independent events.

**Split evidence:** Train/validation/test folders provided; source-scene independence not independently checked.

**Access checked:** Creator links Hugging Face and cloud downloads; download not tested.

**Declared rights:** Author-linked HF card declares Apache-2.0. Underlying imagery provenance/terms require clarification; do not automatically import or overwrite terms from similarly named LEVIR releases.

**Meaning supported by labels:** Textual differences between dates; causal explanations and intent are not established.

**Sources:** [Creator repository](https://github.com/Chen-Yang-Liu/LEVIR-CC-Dataset); [Author-linked card](https://huggingface.co/datasets/lcybuaa/LEVIR-CC/raw/main/README.md)


### D51. LEVIR-CD (original release)

**Scope:** Civilian building-change imagery  
**Year:** 2020  
**Sensor / representation:** Paired Google Earth RGB; 0.5 m/pixel; 1024 x 1024

**Size and units:** 31,333 individual changed-building instances; 5-14 year intervals. LEVIR-CD+ is a separate extension.

**Categories:** Binary changed/unchanged building regions.

**Annotations and identification:** Expert binary pixel masks for building growth or decline.

**Distinctive features:** Two dates per location; seasonal and illumination variation included.

**Origin and provenance:** 20 regions in Texas; imagery acquired 2002-2018.

**Documented strengths:** Creator describes annotation by one interpreter followed by checking by another; source regions and collection dates documented.

**Limitations and open questions:** Geography and subject matter are narrow. A change mask does not identify why a building changed. Smaller tiles/derivatives are not additional independent locations.

**Split evidence:** Original release and later CD+ extension must be distinguished; split manifest not audited.

**Access checked:** Creator page with public links; archive not downloaded.

**Declared rights:** Creator explicitly restricts images/annotations to academic purposes and prohibits commercial use; Google Earth terms also apply.

**Meaning supported by labels:** Where building-related change is visible between dates; no causal, military or event-intent labels.

**Sources:** [Creator dataset page](https://justchenhao.github.io/LEVIR/)


### D52. RSICD

**Scope:** General remote sensing; adjacent comparison  
**Year:** 2018  
**Sensor / representation:** RGB remote-sensing images, 224 x 224 with varying resolutions

**Size and units:** Five sentence descriptions per image according to creator README; sentence count is not independent image count.

**Categories:** Remote-sensing scene descriptions; not a military object taxonomy.

**Annotations and identification:** Image-caption associations in JSON.

**Distinctive features:** Multiple natural-language descriptions for the same scene.

**Origin and provenance:** Images collected from Google Earth, Baidu Map, MapABC and Tianditu; creator repository linked to Lu et al., TGRS 2018.

**Documented strengths:** Named paper, publicly described format, sources and image count.

**Limitations and open questions:** No pixel/box localization implied by captions. Image rights from source services and independence across derivatives need separate documentation; no annotation accuracy audit performed.

**Split evidence:** Published annotation JSON contains dataset organization; actual split records were not downloaded.

**Access checked:** Creator repository with data links; full download not tested.

**Declared rights:** No explicit dataset licence found in inspected README. Source-platform image terms remain separate.

**Meaning supported by labels:** Descriptions of visible scene content; captions do not establish hidden intent or full temporal events.

**Sources:** [Creator repository](https://github.com/201528014227051/RSICD_optimal)


### D53. RSVQA-HR

**Scope:** General remote sensing; adjacent comparison  
**Year:** 2020  
**Sensor / representation:** USGS aerial RGB orthophotos; dataset section states 15 cm; 512 x 512 patches

**Size and units:** 1,066,316 question-answer pairs from 10,659 images cut from 161 USGS tiles.

**Categories:** Static mapped entities and land-use concepts; answer spaces differ across LR and HR.

**Annotations and identification:** Image/question/answer triplets generated from OpenStreetMap records and templates.

**Distinctive features:** Presence/comparison and object-area questions; HR counting answers are not quantized. Multiple questions per image.

**Origin and provenance:** Lobry et al.; satellite or aerial imagery joined with volunteer OpenStreetMap annotations.

**Documented strengths:** Paper explicitly documents source-tile splitting and discusses source-label and time-alignment limitations.

**Limitations and open questions:** OSM can be incomplete, misregistered or temporally mismatched to imagery. Template questions have limited diversity. Labels may describe mapped information not visually resolvable in the image. Paper v2 has an internal resolution discrepancy: its conclusion mentions 30 cm while the dataset subsection states 15 cm; the stated patch area agrees with 15 cm.

**Split evidence:** Source-tile split with a second test region/sensor distinct from training; full manifest not audited.

**Access checked:** Paper and creator code public; historic dataset website failed DNS in this session; data download not verified.

**Declared rights:** Creator code GPL-3.0; this is not a verified unified licence for imagery, OSM-derived data and the full dataset.

**Meaning supported by labels:** Constrained questions about mapped scene content and relations, not open-ended events or intent.

**Sources:** [Primary paper v2](https://arxiv.org/html/2003.07333v2); [Creator repository](https://github.com/syvlo/RSVQA)


### D54. RSVQA-LR

**Scope:** General remote sensing; adjacent comparison  
**Year:** 2020  
**Sensor / representation:** Sentinel-2 RGB; 10 m bands; 256 x 256 image patches

**Size and units:** 77,232 question-answer pairs from 772 images cut from 9 source tiles.

**Categories:** Static mapped entities and land-use concepts; answer spaces differ across LR and HR.

**Annotations and identification:** Image/question/answer triplets generated from OpenStreetMap records and templates.

**Distinctive features:** Presence/comparison and rural/urban questions; LR counting answers are quantized. Multiple questions per image.

**Origin and provenance:** Lobry et al.; satellite or aerial imagery joined with volunteer OpenStreetMap annotations.

**Documented strengths:** Paper explicitly documents source-tile splitting and discusses source-label and time-alignment limitations.

**Limitations and open questions:** OSM can be incomplete, misregistered or temporally mismatched to imagery. Template questions have limited diversity. Labels may describe mapped information not visually resolvable in the image.

**Split evidence:** Source-tile split, 7 training / 1 validation / 1 test tile, documented to limit spatial correlation.

**Access checked:** Paper and creator code public; historic dataset website failed DNS in this session; data download not verified.

**Declared rights:** Creator code GPL-3.0; this is not a verified unified licence for imagery, OSM-derived data and the full dataset.

**Meaning supported by labels:** Constrained questions about mapped scene content and relations, not open-ended events or intent.

**Sources:** [Primary paper v2](https://arxiv.org/html/2003.07333v2); [Creator repository](https://github.com/syvlo/RSVQA)


### D55. SARChat-2M / SARChat-Bench

**Scope:** General SAR with inherited mixed labels  
**Year:** 2025  
**Sensor / representation:** SAR imagery with generated text

**Size and units:** Paper reports 1,836,912 train + 226,636 test = 2,063,548 dialogue samples. These reuse SARDet-100K imagery; they are not two million independent images.

**Categories:** Six inherited object groups; labels such as tank must be traced to source semantics rather than assumed to mean armored vehicles.

**Annotations and identification:** Template-generated classification, description, counting, grounding, referring and cross-modal dialogue examples.

**Distinctive features:** Language supervision is mostly derived from existing classes and geometric annotations.

**Origin and provenance:** Derived from SARDet-100K, itself a combination of ten SAR sources.

**Documented strengths:** Primary paper documents task construction and counts; repository exposes task totals and licence.

**Limitations and open questions:** Repeated source images limit independence; template bias and inherited annotation errors affect supervision quality. README dataset link literally points to YourOrg/SARChat; no actual HF dataset was returned by exact-name search in this session. No independently audited scenario truth.

**Split evidence:** Paper reports train/test dialogue counts; underlying-image split independence not independently audited.

**Access checked:** Paper and code public; official README dataset link is a placeholder. Public data release not verified.

**Declared rights:** Repository LICENSE is CC BY-NC 4.0. Constituent dataset rights remain separate.

**Meaning supported by labels:** Structured visible/mapped content and geometry-derived relations; no verified operational-event or intent ground truth.

**Sources:** [Primary paper v5](https://arxiv.org/html/2502.08168v5); [Creator repository](https://github.com/JimmyMa99/SARChat); [Repository licence](https://raw.githubusercontent.com/JimmyMa99/SARChat/main/LICENSE)


### D56. xBD

**Scope:** Humanitarian natural-disaster damage assessment  
**Year:** 2019  
**Sensor / representation:** Pre/post satellite imagery and satellite metadata

**Size and units:** Primary paper reports 850,736 building annotations across 45,362 square kilometres of imagery; this is not an image count.

**Categories:** Ordinal building-damage levels; environmental factors such as fire, water and smoke described.

**Annotations and identification:** Building polygons, damage labels and pre/post associations; environmental boxes also described by original paper.

**Distinctive features:** Event-linked imagery with a defined observable property: building damage after natural disasters.

**Origin and provenance:** Gupta et al.; collaboration with disaster-response agencies; xView2/xBD challenge.

**Documented strengths:** Primary paper states annotation units and an ordinal damage scale; event context is explicitly bounded to disaster assessment.

**Limitations and open questions:** Natural-disaster labels do not establish cause for arbitrary destruction or military events. Full release/version counts and label uncertainty were not audited.

**Split evidence:** Challenge partitions not independently inspected in this review.

**Access checked:** Paper accessible; xView2 dataset page required JavaScript and its data workflow was not verified.

**Declared rights:** Release-specific data licence not verified during this review.

**Meaning supported by labels:** Observable damage class and event pairing for natural disasters, not intent or attribution.

**Sources:** [Primary paper](https://arxiv.org/abs/1911.09296); [Official dataset landing page](https://xview2.org/dataset)


## Coverage limits and unresolved leads

This is a bounded public literature review. Community platforms contain many similarly named, mirrored or lightly documented collections. They cannot be enumerated as independent datasets from names, popularity or search counts. This review includes representative community cards where provenance and licence uncertainty are material, but does not treat every repository containing the word military as a computer-vision dataset.

Audio datasets, text-only news/event corpora, spending statistics, order-of-battle lists, communications datasets and model-only repositories were excluded from the vision catalogue. A paper about military scenario understanding that reuses DSIAC is not evidence of a newly released scenario-labelled collection. Dataset extensions outside the specific inspected versions remain separate leads, including FAIR1M challenge variants, HRSC2016 derivatives, CAMO++, additional SAR caption corpora and newer small-infrared releases.

Quantitative image-quality checks, label/error sampling, per-class distributions from files, duplicate detection, original-image rights tracing and split-independence audits have not been performed. Any future assertion about these properties needs the particular release and direct evidence. Model selection, training, hardware benchmarks and deployment remain outside this phase.
