# Tiny/Small Object Detection in Aerial, UAV and Satellite Imagery (2024–2026), with Emphasis on Edge-Deployable Methods

Scope note: Benchmarks referenced throughout use these size conventions. AI-TOD / AI-TOD-v2: AP_vt = very tiny (2–8 px), AP_t = tiny (8–16 px), AP_s = small (16–32 px), AP_m = medium (32–64 px); AI-TOD-v2 has 28,036 images / 700,621 instances with 86% of objects < 16 px and mean object size 12.8 px — [Dome-DETR](https://arxiv.org/html/2505.05741v2). SODA-D uses AP_eS (0–12 px), AP_rS (12–20 px), AP_gS (20–32 px), AP_N (32–45 px); SODA-D has 24,828 images / 278,433 instances with mean size 20.31 px; SODA-A has 2,513 very large aerial images / 872,069 oriented boxes (~347 instances/image) — [SODA project page](https://shaunyuan22.github.io/SODA/). VisDrone: ~75% of objects occupy fewer than 2,000 pixels and 97% occupy < 1% of image area — [YOLO26 vs YOLOv8 benchmark](https://arxiv.org/pdf/2605.24831). Unless noted, VisDrone numbers are on VisDrone2019-DET-val, which is the convention in nearly every paper below; some older works (Drone-YOLO) also report test-dev. Numbers across papers are NOT directly comparable unless they come from the same table (different input sizes, splits, GPUs, FP16/FP32).

---

## Key Question 1: Strongest architectural techniques for tiny objects (P2 heads, FPN variants, attention, context, SPD-Conv, dynamic heads, density/“no-downsampling” designs)

### Takeaway
The single most reliable gain on VisDrone-class data is restoring high-resolution features (a stride-4 P2 head, or reviving the discarded C1/P1 level in DETRs), and the newest SOTA on AI-TOD-v2 all comes from density-guided, dynamic-compute DETRs (Dome-DETR family) that spend compute only where tiny objects cluster. Frequency-domain feature enhancement (HS-FPN, SET, UFO-DETR, DyFrDet) is the fastest-growing 2025 trend; attention modules and IoU-loss swaps give small (+0.5–1 AP) gains relative to P2/feature-resolution changes.

### Cited Findings

**High-resolution (P2 / stride-4) heads and feature revival**
- Adding a P2 head to a YOLOv8-style model "increases parameter count by only 3.50% but increases GFLOPs by 55.74%", i.e., high-resolution detection is parameter-light but compute-heavy — [SSCW-YOLO](https://www.researchgate.net/publication/399548381_SSCW-YOLO_A_Lightweight_and_High-Precision_Model_for_Small_Object_Detection_in_UAV_Scenarios)
- In LAF-YOLOv10's VisDrone ablation, the P2-add / P5-remove head reallocation gave the largest single improvement (+1.3 mAP@0.5), vs. PC-C2f (+1.0), AG-FPN (+0.6) and WIoU (+0.5) — [LAF-YOLOv10, arXiv 2602.13378](https://arxiv.org/pdf/2602.13378)
- DroneScan-YOLO (arXiv Apr 2026) adds a stride-4 P2 head ("MSFD") costing only 114,592 params (+1.1%), uses 1280×1280 input, dynamic filter pruning, and a hybrid NWD + size-adaptive CIoU loss; reports VisDrone2019-DET mAP50 55.3% (+16.6 over YOLOv8s), mAP50-95 35.6% (+12.3), recall 0.374→0.518, 96.7 FPS (hardware not stated on abstract page), no code URL — [DroneScan-YOLO](https://arxiv.org/abs/2604.13278)
- An "Enhanced YOLOv12" replaces the 20×20 large-object head with a 160×160 head and reports +10.4% mAP@0.5 over YOLOv12 on VisDrone-DET2021/UAVDT — [Springer 2026](https://link.springer.com/article/10.1007/s42452-026-08496-2)
- MASF-YOLO (YOLOv11-based) adds a fourth detection layer at 1/4 input scale (160×160 for 640 input) to preserve detail for objects as small as 4×4 px; MASF-YOLO-n: 37.3 mAP50 / 23.0 mAP50-95, 3.31M params; -s: 42.8 / 26.8, 12.05M; -m: 45.4 / 28.6, 27.56M (VisDrone val) — [MASF-YOLO, arXiv 2504.18136](https://arxiv.org/pdf/2504.18136)
- Input resolution alone matters enormously: a plain YOLO11s on VisDrone yields AP_small 0.111 at 640 vs 0.223 at 1280; SAHI-style tiling (640 + tiles with edge merging) reaches mAP50 0.425 / AP_small 0.176 vs 0.355 / 0.115 for plain 640 inference, at 510–560 ms/image vs 73 ms — [tanirim/aerial-object-detection](https://github.com/tanirim/aerial-object-detection)
- ReDHF (arXiv 2611.07994, Nov 2026 preprint) revives the discarded highest-resolution backbone feature C1 in DETR-like detectors via Cross-Scale Deformable Fusion, an ellipse-shaped training-only shallow supervision head, and full-scale query interaction; Dome-DETR-L + ReDHF reaches 35.7 AP / 20.8 AP_vt on AI-TOD-v2 (39.0M params, 415.3 avg GFLOPs); Dome-DETR-S + ReDHF: 33.5 AP / 18.9 AP_vt (15.9M, 188.2 GFLOPs); average gains +1.4 AP (AI-TOD-v2), +1.7 AP_s (VisDrone), +1.8 AP_eS (SODA-D); on SODA-D Dome-DETR-L goes 37.6→38.7 AP and AP_eS 19.7→21.4; no code URL and no FPS in the readable portion — [ReDHF](https://arxiv.org/html/2611.07994)
- Ellipse-shaped positive assignment in ReDHF's shallow head beat rectangle (33.2/17.6 AP/AP_vt) and circle (33.3/18.1) with 33.5/18.9 — [ReDHF](https://arxiv.org/html/2611.07994)

**Density-guided / dynamic-compute DETR designs (the current AI-TOD-v2 SOTA line)**
- Dome-DETR (ACM MM 2025; built on D-FINE, HGNetv2 backbone, 800×800) uses a Density-Focal Extractor (0.8M params, 17.6 GFLOPs) to produce compact foreground masks, Masked Window Attention Sparsification, and Progressive Adaptive Query Initialization; AI-TOD-v2: S 33.3 AP / 17.8 AP_vt (13.2M, 154.2 avg GFLOPs), M 34.0 / 18.4 (23.9M, 252.6), L 34.6 / 19.0 (36.0M, 358.7) vs D-FINE-S/M/L 30.1/30.8/31.3 AP; VisDrone val: S 33.5 AP / 56.6 AP50, M 36.1 / 59.8, L 39.0 / 61.1 (L at 1200×800: 40.5 / 64.5); T4 latency < 15 ms (M) and < 20 ms (L); compute is dynamic: Dome-DETR-S spans 123.3 GFLOPs (sparse scene) to 193.8 (dense); code: https://github.com/RicePasteM/Dome-DETR — [Dome-DETR](https://arxiv.org/html/2505.05741v2)
- Dome-DETR ablation (S, AI-TOD-v2): base D-FINE-S 30.1 AP / 14.0 AP_vt → DeFE+MWAS 31.2 / 17.4 → DeFE+PAQI 32.1 / 16.9 → all three 33.3 / 17.8; AP_vt gains come mostly from the density-focal masking — [Dome-DETR](https://arxiv.org/html/2505.05741v2)
- ScaleBridge-Det (Dec 2025) with a Density-Guided Dynamic Query module reports 35.7% mAP on AI-TODv2, 29.8% on DTOD, 30.7% on VisDrone; the 3.0B-parameter variant is what hits 35.7 — not an edge model — [ScaleBridge-Det](https://arxiv.org/html/2512.01665v1)
- DRMNet (Dec 2025) uses density maps as explicit spatial priors to guide adaptive feature learning for dense tiny clusters, with a module (DFFM) targeting degradation of tiny features in deep layers — [DRMNet, arXiv 2512.22949](https://arxiv.org/abs/2512.22949)
- D³R-DETR (Jan 2026, submitted to IEEE) fuses spatial and frequency domain information to refine low-level maps and predict a more accurate density map; claims +2.6% AP, +3.1% AP50, +2.0% AP_vt, +2.7% AP_t over its Dome-DETR baseline on AI-TOD-v2; no absolute numbers or code on the abstract page — [D³R-DETR](https://arxiv.org/abs/2601.02747); baseline identified as Dome-DETR in [search summary of the HTML](https://arxiv.org/html/2601.02747v1)

**Frequency-domain / high-frequency enhancement**
- HS-FPN (AAAI 2025) adds a High-Frequency Perception module (high-pass filter responses used as spatial+channel mask weights) and a Spatial Dependency Perception module at each FPN lateral; Faster R-CNN + HS-FPN: 20.3 AP on AI-TOD vs 18.3 baseline; DetectoRS + RFLA + HS-FPN: 25.1 AP on AI-TOD — [HS-FPN, arXiv 2412.10116](https://arxiv.org/html/2412.10116v3)
- SET: Spectral Enhancement for Tiny Object Detection (CVPR 2025) improves FCOS by +2.0/+0.9/+1.2 AP/AP_vt/AP_t, Cascade R-CNN by +1.1/+1.3 AP_vt/AP_t, and RFLA to 28.5 AP on AI-TOD (+0.7 AP_vt, +0.5 AP_t) — [SET CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Sun_SET_Spectral_Enhancement_for_Tiny_Object_Detection_CVPR_2025_paper.pdf)
- UFO-DETR (CSCWD 2026; arXiv Feb 2026) uses an LSKNet backbone, DAttention + AIFI, and a DynFreq-C3 "cross-space frequency feature enhancement" module; claims better accuracy and efficiency than RT-DETR-L for UAV edge computing, but the abstract page gives no numbers and no code — [UFO-DETR](https://arxiv.org/abs/2602.22712)
- DyFrDet (dynamic frequency suppression + label disambiguation) reports SODA-A SOTA of 37.8 AP / 73.4 AP50 / 34.3 AP75 (AP_rS 31.9, AP_gS 49.5, AP_N 41.0), surpassing GauCho by 4.6 AP — [DyFrDet, arXiv 2608.02495](https://arxiv.org/pdf/2608.02495)
- YOLO12-MambaScan combines high-frequency enhancement with state-space modeling, stating high-frequency cues are critical for small objects — [arXiv 2609.13647](https://arxiv.org/pdf/2609.13647)

**SPD-Conv (space-to-depth) and reduced downsampling**
- HSP-YOLOv8 reports that replacing backbone Conv with SPD-Conv raised mAP0.5 by 2.3% on UAV data — [HSP-YOLOv8](https://pdfs.semanticscholar.org/fc3a/457027fc0c98756b362ef5248826e514b4f7.pdf)
- SEMA-YOLO terminates backbone convolutions at P4 and removes unnecessary downsampling to preserve low-level features — [SEMA-YOLO preprint](https://www.preprints.org/manuscript/202504.1115/v1)
- FBRT-YOLO's Multi-Kernel Perception unit replaces the final backbone downsampling stage (and removes the corresponding deep head), and its Feature Complementary Mapping module explicitly carries shallow spatial information into deep layers; ablation on YOLOv8-S (VisDrone): 23.6 AP (11.2M, 28.6G) → +RR 23.4 (9.1M, 25.5G) → +FCM 24.3 (7.2M, 23.2G) → +MKP 25.9 (2.9M, 22.9G) — [FBRT-YOLO](https://arxiv.org/html/2504.20670v1)
- The Sensors 2025 real-time aerial survey lists SPDConv + ECA, extra shallow detection heads, and BiFPN with skip connections as the recommended small-object fixes while warning each raises compute — [Habash et al., Sensors 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)

**Attention and Mamba/state-space modules**
- The Sensors 2025 survey recommends lightweight attention (ECA, Shuffle Attention, Triplet, NAM, parameter-free SimAM, Coordinate Attention) over SE/CBAM/GCNet and flags transformer self-attention as costly for UAV onboard use — [Habash et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)
- SMA-YOLO (Remote Sensing 2025, YOLOv8n base, parameter-free attention + multi-scale fusion): 42.3 mAP@0.5, 25.3 mAP@0.5:0.95, 2.6M params, 20.9 GFLOPs on VisDrone2019 (+7.4 mAP50 over baseline with 13.3% fewer params) — [SMA-YOLO](https://doi.org/10.3390/rs17142421)
- HIC-YOLOv5 (ICRA 2024) uses an involution block between backbone and neck and CBAM at backbone end; +6.42 mAP@[.5:.95] and +9.38 mAP@0.5 on VisDrone-2019-DET; LEAF-YOLO's table lists it at 9.3M params, 30.9 GFLOPs, 24.9 AP / 43.0 AP50 / 15.8 APs, 29.7 ms (RTX 3090, b=1) — [HIC-YOLOv5](https://arxiv.org/pdf/2309.16393); [LEAF-YOLO README](https://github.com/highquanglity/LEAF-YOLO)
- HDMamba-YOLO (arXiv 2609.23061) is a heterogeneous state-space + convolutional detector for UAV small objects; notably its ablation found adding NWD gave no additional localization benefit over CIoU under its VisDrone protocol — [HDMamba-YOLO](https://arxiv.org/html/2609.23061v1)
- MambaRefine-YOLO's hierarchical fusion neck (HFAN) gave +6.0% over an FPN baseline on VisDrone, with the hierarchical multi-scale structure the most important component (−3.6% when removed) — [MambaRefine-YOLO](https://arxiv.org/html/2511.19134)
- Cross-DINO (IEEE TMM, May 2025) adds a deep MLP for short/long-range context, a Cross Coding Twice Module, and a Category-Size soft label with a "Boost Loss"; 36.4% AP_S on COCO with 45M params (+4.4 over DINO) and evaluated on VisDrone, AI-TOD, SODA-D; code (forthcoming) https://github.com/Med-Process/Cross-DINO — [Cross-DINO](https://arxiv.org/abs/2505.21868)

**Context aggregation / FPN denoising**
- DNTR (arXiv 2406.05755v4, Apr 2025): DeNoising FPN uses InfoNCE contrastive losses to keep geometric info from laterals and semantic info from upper levels (training-only, zero inference cost), plus a Trans R-CNN head; AI-TOD R50 800×800: 26.2 AP / 56.7 AP50 / 12.8 AP_vt / 26.4 AP_t; 1000×1000 (DNTR-L): 29.0 AP / 17.3 AP_vt; VisDrone val 33.1 AP / 53.8 AP50 without cropping; 167.5 GFLOPs, 11.9 FPS on RTX 3090; plugging DN-FPN into YOLOv8s lifted it 11.6→18.7 AP on AI-TOD at unchanged 169.5 FPS; code https://github.com/hoiliu-0801/DNTR — [DNTR](https://arxiv.org/html/2406.05755)
- Scale-Aware Relay Layer + Scale-Adaptive Loss (Nov 2025): plug-ins for YOLOv5/YOLOX with a claimed +5.5% AP and 29.0% AP on noisy AI-TOD-v2; no code listed — [SARL/SAL](https://arxiv.org/abs/2511.09891)

**Sparse / region-selective compute for high-resolution inputs (the practical "edge" answer to no-downsampling)**
- ESOD (IEEE TIP 2024, Alibaba/ZJU) reuses the detector backbone for feature-level object seeking and patch slicing plus a sparse-convolution detection head so 1080P+ inputs are affordable; claims ~8% AP gains over SOTA on VisDrone, UAVDT, TinyPerson; SparseHead saves >50 GFLOPs; reduces ViT GPU memory from 161 GB to 19 GB at 1920×1920; code https://github.com/alibaba/esod — [ESOD abs](https://arxiv.org/abs/2407.16424); [ESOD html](https://arxiv.org/html/2407.16424v1)
- DenseScout (ACM MM 2026): a 1.01M-param "dense-response selector" that drops box regression and ranks patch centers so a heavier detector only processes selected regions; evaluated on VisDrone and DOTA; profiled on Jetson Orin NX and RK3588; frames edge tiny-object perception as a selection-and-deployment co-design problem; code repo promised in v2 but URL not on abstract page — [DenseScout](https://arxiv.org/abs/2604.25300)
- Dome-DETR's comparison with cluster-crop pipelines: Focus&Detect 42.0 AP at 1362 ms (2080Ti), YOLC 39.6 AP at 441 ms, UFPMP-Det-ResNeXt101 40.1 AP at > 200 ms vs Dome-DETR-L 39.0–40.5 AP at < 20 ms (T4) — [Dome-DETR Table 8](https://arxiv.org/html/2505.05741v2)
- ROI-Gated SAHI proposes content-adaptive slicing to make slicing-based inference cheaper — [arXiv 2608.23923](https://arxiv.org/pdf/2608.23923)

### Inferences
- For a fixed edge budget, the best ROI ordering suggested by the ablations is: (1) raise effective input resolution (native, tiled, or sparse/selective), (2) add a stride-4 head and remove/shrink P5, (3) frequency-aware or density-aware feature enhancement, (4) lightweight attention, (5) loss swaps. Each step past (2) typically yields < +1.5 AP on VisDrone.
- "No-downsampling" dense detectors in the literal sense do not appear in the 2024–2026 literature I found; what has emerged instead is density-guided sparse compute (Dome-DETR, DenseScout, ESOD) that approximates full-resolution processing only where tiny objects cluster — this is the edge-compatible version of the idea.
- Training-only modules (DN-FPN, ReDHF's EGSS head, SR-as-auxiliary) are especially attractive for edge: they raise AP with zero inference cost.

### Gaps
- No paper found that benchmarks P2-head, SPD-Conv, HS-FPN/BiFPN/AFPN/Gold-YOLO GD and attention variants head-to-head under one protocol on VisDrone or AI-TOD; comparisons above come from heterogeneous ablations.
- Gold-YOLO gather-and-distribute, AFPN and ASF were only mentioned as design trends in the Sensors survey; I found no 2024–2026 tiny-object paper with specific numbers for them.
- UFO-DETR, D³R-DETR, DRMNet and DenseScout absolute numbers/code were unavailable (PDF-only or not yet released).

---

## Key Question 2: Loss-function and label-assignment advances for tiny objects (NWD, RFLA, DotD, Wise-IoU, Inner-IoU, Shape-IoU, Focaler-IoU, MPDIoU)

### Takeaway
NWD and RFLA remain the foundational assignment-side fixes (RFLA 24.8 AP vs NWD 20.8 on AI-TOD with DetectoRS), while 2025 UAV detectors mostly combine IoU variants (Inner/Focaler/MPDIoU/Wise) with NWD blends; measured gains from loss swaps alone are modest (+0.4–0.8 AP on VisDrone), and two 2025 papers found NWD alone can hurt unless blended with IoU.

### Cited Findings
- Why IoU fails on tiny boxes: for a normal-sized face a tiny pixel offset drops IoU 0.81→0.66, but for a very small target the same offset drops IoU 0.39→0.14 — [SME-YOLO, arXiv 2601.11402](https://arxiv.org/pdf/2601.11402); large objects tolerate localization deviation so the regression loss under-weights tiny objects — [SARL/SAL](https://arxiv.org/html/2511.09891v1)
- NWD (Gaussian Wasserstein) original ablation on Faster R-CNN (AI-TOD): as assignment metric NWD gave 16.1 AP (+9.6 APt vs IoU); as loss 12.1 AP — [NWD, arXiv 2110.13389](https://arxiv.org/pdf/2110.13389)
- RFLA (ECCV 2022) replaces IoU/center sampling with a Receptive Field Distance between the Gaussian receptive field and GT — [RFLA](https://www.ecva.net/papers/eccv_2022/papers_ECCV/papers/136690518.pdf); on AI-TOD with DetectoRS: NWD 20.8 AP / 6.4 AP_vt, RFLA 24.8 AP / 9.3 AP_vt, NWD-RKA 23.4 AP — [Dome-DETR Table 1](https://arxiv.org/html/2505.05741v2); [CEM-FBGTinyDet, arXiv 2506.09897](https://arxiv.org/pdf/2506.09897) (its own E-FPN-BS reaches 26.1 AP, +1.3 over RFLA)
- NWD-alone caveat: a YOLOv10 UAV study found NWD alone yields lower accuracy than IoU, while combined IoU + NWD was best (mAP@0.5 0.497, mAP@0.5:0.95 0.270) — [Sci. Reports 2025](https://www.nature.com/articles/s41598-025-14880-6); HDMamba-YOLO likewise found no extra benefit from NWD and kept pure CIoU — [HDMamba-YOLO](https://arxiv.org/html/2609.23061v1); DroneScan-YOLO instead uses a hybrid "SAL-NWD" (NWD + size-adaptive CIoU weighting) inside YOLOv8's TaskAligned assigner — [DroneScan-YOLO](https://arxiv.org/abs/2604.13278)
- Shape-IoU focuses on the shape and scale of the box itself and proposes shape-dot-distance and shape-NWD variants for tiny targets — [Shape-IoU](https://arxiv.org/pdf/2312.17663)
- Wise-IoU v3 uses an outlier-degree metric to attenuate gradients from low-quality annotations; TinyDef-DETR argues its default form "deemphasizes geometric shape and aspect consistency crucial for sub-pixel localization" and proposes Focaler–Wise–SIoU — [TinyDef-DETR](https://arxiv.org/pdf/2509.06035)
- Inner-IoU: UAV-DETR used Inner-SIoU with ratio 1.25 (GIoU 29.0 → Inner-SIoU 29.8 AP in its ablation; an earlier ablation step showed 27.1 AP after adding Inner-SIoU) — [UAV-DETR](https://arxiv.org/pdf/2501.01855)
- Combined variants on VisDrone: CDF-DETR's Focaler-MPDIoU (RT-DETR-R18 baseline) with ablations over GIoU / MPDIoU / Focaler-IoU / Focaler-MPDIoU — [CDF-DETR, Remote Sensing 2025](https://www.mdpi.com/2072-4292/18/16/2793); AUHF-DETR's Inner-MPDIoU with small-object penalty reported best among mainstream IoU losses — [AUHF-DETR](https://www.researchgate.net/publication/392358547_AUHF-DETR_A_Lightweight_Transformer_with_Spatial_Attention_and_Wavelet_Convolution_for_Embedded_UAV_Small_Object_Detection); WIPIoU (Wise + MPD + Inner) — [Remote Sensing 17(13) 2025 via search](https://www.mdpi.com/2072-4292/18/16/2793); PTCDet's inner-Focaler IoU — [PTCDet](https://www.nature.com/articles/s41598-024-78749-w)
- Focaler-IoU alone: MD-DRIFPN on VisDrone reaches AP0.50:0.95 0.248 (claimed +40.9% over baseline) with 23.9% fewer params at 104 FPS (RTX 3090) — [MD-DRIFPN](https://link.springer.com/article/10.1007/s11227-025-08104-x)
- Magnitude calibration: WIoU contributed +0.5 mAP@0.5 in LAF-YOLOv10's VisDrone ablation vs +1.3 for the P2 head — [LAF-YOLOv10](https://arxiv.org/pdf/2602.13378)
- Scale-Adaptive Loss (SAL) dynamically down-weights larger objects in IoU-type losses; combined with SARL gives +5.5 AP on YOLOv5/YOLOX baselines (datasets AI-TOD, DOTA-v2.0, VisDrone2019) — [SARL/SAL](https://arxiv.org/abs/2511.09891)
- Label assignment on the DETR side: DEIM refines Hungarian matching / dense sample assignment and is the training recipe under D-FINE-based UAV detectors (PFE-Det, HMF-DEIM) — [PFE-Det](https://doi.org/10.3390/s26155003); one paper found plain D-FINE-S (22.7 AP / 12.8 APs) slightly above DEIM-D-FINE-S (21.5 / 12.2) on VisDrone 640, suggesting COCO-tuned assignment tweaks do not always transfer — [SCA-DEIM](https://pmc.ncbi.nlm.nih.gov/articles/PMC12788032)
- Other 2024 assignment work cited: Gaussian label assignment for tiny objects (IEEE TGRS 2024) and similarity-distance-based label assignment (IROS 2024) — [SET CVPR 2025 references](https://openaccess.thecvf.com/content/CVPR2025/papers/Sun_SET_Spectral_Enhancement_for_Tiny_Object_Detection_CVPR_2025_paper.pdf)

### Inferences
- For a YOLO-style edge detector, the evidence favors: keep CIoU/SIoU as the base, blend in NWD (not replace), and optionally use Inner/Focaler modulation; expect < 1 AP from the loss change and prioritize architectural resolution changes.
- RFLA-style receptive-field assignment is the most effective assignment fix for anchor-based two-stage detectors on AI-TOD but is rarely ported to YOLO heads; its ideas appear indirectly in ellipse/Gaussian assignment of auxiliary heads (ReDHF).

### Gaps
- No single 2025 paper compares NWD, RFLA, DotD, Wise/Inner/Shape/Focaler/MPDIoU under identical conditions; DotD did not appear in any 2024–2026 VisDrone ablation I found.
- Exact per-loss AP numbers from CDF-DETR's and AUHF-DETR's tables were not retrievable (only qualitative conclusions).

---

## Key Question 3: Leading lightweight YOLO variants for drone/aerial small objects, and best VisDrone mAP per GFLOP

### Takeaway
On VisDrone-val at 640, the strongest open-source, edge-verified points in the ~5–25 GFLOP band are LEAF-YOLO (28.2 AP / 48.3 AP50 at 20.9 GFLOPs, 32 FPS FP16 on Jetson AGX Xavier) and FBRT-YOLO-S (25.9 AP / 42.4 AP50 at 22.9 GFLOPs, 2.9M params); in the sub-8-GFLOP tier, FBRT-YOLO-N (20.2 AP / 34.4 AP50, 6.7 GFLOPs, 0.9M) and LEAF-YOLO-N (21.9 AP / 39.7 AP50, 5.6 GFLOPs, 1.2M, 56 FPS on AGX Xavier) lead. Higher-accuracy claims (DroneScan-YOLO 35.6 AP, SRTSOD-YOLO-l 33.8) rely on 1280 input or ≥ 95 GFLOPs.

### Cited Findings

**Same-table comparison (VisDrone2019-DET-val, 640, RTX 3090 FP16 b=1) from the LEAF-YOLO README**
- HIC-YOLOv5: 9.3M, 30.9G, 24.9 AP, 43.0 AP50, 15.8 APs, 29.7 ms; PDWT-YOLO: 6.44M, 24.5G, 24.3 AP, 42.6 AP50, 15.9 APs, 22.2 ms; EdgeYOLO-T: 5.5M, 27.24G, 21.8 AP, 38.5 AP50, 12.4 APs, 29.93 ms; EdgeYOLO-S: 9.3M, 45.32G, 23.5 AP, 40.8 AP50, 13.8 APs, 38.18 ms; Drone-YOLO-N/T/S: 3.05/5.35/10.0M, 22.7/25.6/27.0 AP, 38.1/42.8/44.3 AP50 (no FLOPs); LEAF-YOLO-N: 1.2M, 5.6G, 21.9 AP, 39.7 AP50, 14.0 APs, 16.2 ms; LEAF-YOLO: 4.28M, 20.9G, 28.2 AP, 48.3 AP50, 20.0 APs, 21.7 ms — [LEAF-YOLO README](https://github.com/highquanglity/LEAF-YOLO)
- Jetson AGX Xavier, TensorRT 8.5.2 FP16, end-to-end with EfficientNMS: EdgeYOLO-T 27 FPS (b=1) / 65 (b=16); EdgeYOLO-S 21 / 54; LEAF-YOLO-N 56 / 147; LEAF-YOLO 32 / 87 — [LEAF-YOLO README](https://github.com/highquanglity/LEAF-YOLO)
- LEAF-YOLO (Intelligent Systems with Applications vol. 25, 2025, DOI 10.1016/j.iswa.2025.200484; YOLOv7-style codebase, GPL-3.0) also claims 23% AP50 on TinyPerson, beating models ≥ 20M params — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2667305325000109); [GitHub](https://github.com/highquanglity/LEAF-YOLO)

**FBRT-YOLO (AAAI 2025) — full VisDrone table (RTX 3080 FPS)**
- FBRT-YOLO-N 20.2 AP / 34.4 AP50, 6.7G, 0.9M, 192 FPS; -S 25.9 / 42.4, 22.9G, 2.9M, 143 FPS; -M 28.4 / 45.9, 58.7G, 7.2M, 94 FPS; -L 29.7 / 47.7, 119.2G, 14.6M, 70 FPS; -X 30.1 / 48.4, 185.8G, 22.8M, 52 FPS; baselines in same table: YOLOv8-N 19.6 / 33.3 (8.7G, 3.2M), YOLOv8-S 23.6 / 39.6 (28.6G, 11.2M), YOLOv10-S 23.8 / 39.3 (21.6G, 7.2M), RT-DETR-R50 28.8 / 48.3 (136G, 42M); UAVDT: 18.4 AP / 31.1 AP50 (vs CEASC 17.1); AI-TOD: FBRT-YOLO-S 20.2 AP / 45.8 AP50 (2.9M, 22.9G, 142 FPS) vs YOLOv8-S 19.1 / 43.6; 300 epochs; code https://github.com/galaxy-oss/FCM ("will be available") — [FBRT-YOLO arXiv](https://arxiv.org/html/2504.20670v1); [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/view/32937/35092)
- Re-runs by others differ slightly: an MDPI paper lists FBRT-YOLO-M at 28.7 AP / 46.1 AP50 and a 2026 DERNet paper lists FBRT-YOLO-N/S/M at mAP50 0.265/0.323/0.344 with APs 12.2/16.2/17.5 — [search summary citing DERNet and MDPI](https://arxiv.org/pdf/2504.20670)

**Other named variants**
- Drone-YOLO (Drones 2023, YOLOv8-based with sandwich fusion + RepVGG): VisDrone-val nano 38.1 mAP50 / 22.7 mAP50-95 (3.05M), tiny 42.8 / 25.6 (5.35M), small 44.3 / 27.0 (10.9M), large 51.3 / 31.9 (76.2M); test-dev large 40.7 / 23.8; GFLOPs not reported — [Drone-YOLO](https://www.mdpi.com/2504-446x/7/8/526)
- SOD-YOLO (Remote Sensing 2024, YOLOv8-based): -n 33.0 mAP50 / 19.3 mAP50-95, 0.6M, 7.8G, 145 FPS; -s 42.0 / 25.1, 1.75M, 20.1G, 126 FPS; -m 48.5 / 29.5, 6.3M, 65.8G, 103 FPS; -l 51.5 / 32.0, 17.6M, 167G, 88 FPS (RTX 3090) — [SOD-YOLO RS 2024](https://www.mdpi.com/2072-4292/16/16/3057). Two other unrelated "SOD-YOLO"s exist: YOLOv8-m based (mAP50:95 0.351, mAP50 0.526, 22.6M, 94.9G) — [arXiv 2507.12727](https://arxiv.org/pdf/2507.12727); YOLOv7-based (AP50 50.7, 30.3M, 83.5G, 72.5 FPS RTX 4060) — [Sci. Reports 2024](https://www.nature.com/articles/s41598-024-77513-4)
- EdgeYOLO (2023 foundational edge baseline): 26.4 AP / 44.8 AP50 on VisDrone2019-DET, ≥ 30 FPS on Jetson AGX Xavier (FP16 TensorRT 7.1.3); a survey lists it at 44.8 mAP50 / 34 FPS on Xavier — [EdgeYOLO](https://arxiv.org/html/2302.07483v1); [Habash et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)
- LUD-YOLO (Information Sciences 2024, YOLOv8-based): 2.8M params, 9.3 GFLOPs, VisDrone APs 13.7% (as reported in MFA-YOLO's comparison); authors note overall mAP "is not dominant" but balanced — [LUD-YOLO](https://www.sciencedirect.com/science/article/pii/S0020025524012805); [MFA-YOLO](https://www.nature.com/articles/s41598-025-32247-9)
- YOLO-UAV (YOLOv5s-based): VisDrone mAP0.5 35.1→46.7, mAP0.5:0.95 19.1→27.4 — [YOLO-UAV](https://www.researchgate.net/publication/375245748_YOLO-UAV_Object_Detection_Method_of_Unmanned_Aerial_Vehicle_Imagery_Based_on_Efficient_Multi-scale_Feature_Fusion)
- SL-YOLO: 46.9 mAP50 / 28.9 mAP50-95, 9.6M, 36.7G, 132 FPS (VisDrone val) — [SL-YOLO](https://arxiv.org/pdf/2411.11477)
- SRTSOD-YOLO-l (YOLO11-based): 53.8 mAP50 / 33.8 mAP50-95, 27.6M, 94.7G, 99 FPS — [SRTSOD-YOLO preprint](https://www.preprints.org/manuscript/202507.2594)
- I-YOLOv11n (Sensors 2025): +7.1 mAP@0.5 / +4.9 mAP@0.5:0.95 over YOLOv11 on VisDrone, AI-TOD, SODA-A; 14.7 GFLOPs (vs 28.5 for YOLOv8s) — [I-YOLOv11n](https://doi.org/10.3390/s25154857)
- CF-YOLO (YOLOv11-based; VisDrone, HIT-UAV, TinyPerson): Lightweight Spatial-Depth Enhanced Cross-Detection head; surpasses RT-DETR small-object accuracy by an average 15.3% — [CF-YOLO](https://www.nature.com/articles/s41598-025-99634-0)
- YOLO11s-UAV (J. Imaging 2026): CARAFE upsampling + "PAFPN-tiny" — [YOLO11s-UAV](https://doi.org/10.3390/jimaging12020069)
- SSCW-YOLO (YOLOv8-based): 37.6% mAP with 3M params on VisDrone — [SSCW-YOLO](https://www.researchgate.net/publication/399548381_SSCW-YOLO_A_Lightweight_and_High-Precision_Model_for_Small_Object_Detection_in_UAV_Scenarios)
- EDNet (UIC 2024; YOLOv10-based, NMS-free, XSmall head + Cross Concat + C2f-FCA + WIoU, 7 sizes): up to +5.6 mAP@50 with fewer params; 16–55 FPS on an iPhone 12; code https://github.com/zsniko/EDNet — [EDNet](https://arxiv.org/abs/2501.05885)
- LD-YOLOv10: 25 FPS on Jetson Orin Nano, compared against LWUAVDet and EfficientDet — [LD-YOLOv10](https://www.researchgate.net/publication/383222713_LD-YOLOv10_A_Lightweight_Target_Detection_Algorithm_for_Drone_Scenarios_Based_on_YOLOv10)
- LWUAVDet: validated on Jetson Xavier NX and Jetson Nano across VisDrone, UAVDT, VOC2012 — [LWUAVDet](https://www.researchgate.net/publication/379802333_LWUAVDet_A_Lightweight_UAV_Object_Detection_Network_on_Edge_Devices)
- GAME-YOLO (Entropy 2025) claims to surpass LEAF-YOLO (48.3), PDWT-YOLO (42.6) and YOLOv8-p2-S (42.9) on VisDrone AP50, deployed on Jetson Xavier NX at 15 W — [GAME-YOLO](https://www.mdpi.com/1099-4300/27/12/1263)
- From the Sensors 2025 survey's VisDrone table (desktop GPUs): MFRENet (YOLOv8m) 53.4 mAP50, 27.1M, 50.5 FPS; AMMFN (YOLOv5s) 48.1, 7.7M; MFFSODNet 45.5, 4.5M; GCL-YOLO-n 31.7 mAP50 at 0.4M params; MSFE-YOLO-n 33.8 mAP50, 149 FPS; EL-Net (YOLOv7-tiny) 38.7 mAP50, 2.0M; Jetson-family RGB deployments generally land at 14–47 FPS — [Habash et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)
- YOLO26-based: MD-YOLO (Algorithms 2026) improves over YOLO26 on VisDrone/UAVDT/NWPU — [MD-YOLO](https://doi.org/10.3390/a19090737); Aero-YOLO26 (Sensors 2026) — [Aero-YOLO26](https://www.mdpi.com/1424-8220/26/19/6346); a YOLO26-vs-YOLOv8 benchmark finds YOLO26's gains are smaller on VisDrone than on Pascal VOC and "dense aerial small-object detection remains difficult for both" — [arXiv 2605.24831](https://arxiv.org/pdf/2605.24831)
- YOLOv12-based: LCS-YOLO (YOLOv12n, re-parameterizable conv) on VisDrone2019/HIT-UAV/CODrone — [LCS-YOLO](https://link.springer.com/article/10.1007/s12145-026-02132-8); Dome-DETR's re-implementation shows stock YOLOv12-S/M/L/X only reach 11.5/14.0/14.6/16.1 AP on AI-TOD-v2 (AP_vt 2.7–5.4), far below DETR-based tiny detectors — [Dome-DETR](https://arxiv.org/html/2505.05741v2)
- Edge Pareto benchmark (IEEE Access 2025, Shakya et al.): eight lightweight YOLOs (YOLOX-Nano, YOLOv6–v12 nano) on VisDrone2019, DOTA-v1.5, xView; A100 and Jetson Orin Nano (PyTorch and TensorRT FP16); TensorRT gives 3–5× speedup; power 7.6–10.4 W; "no single model dominates"; YOLOv8-Nano and YOLOv11-Nano are the common Pareto-optimal picks (YOLOv8n reference for DOTA-v1.5, YOLOv11n for xView) — [DSU repository](https://scholar.dsu.edu/ccspapers/124/)
- TPH-YOLOv5 (transformer prediction heads, VisDrone 2021 challenge) and SAHI slicing are repeatedly cited as foundational baselines in 2024–2025 work — [From Blurry to Brilliant](https://arxiv.org/pdf/2401.14661); [tanirim SAHI benchmark](https://github.com/tanirim/aerial-object-detection)

### Inferences
- Computing AP50 per GFLOP from same-protocol numbers: LEAF-YOLO-N ≈ 7.1 AP50/GFLOP (39.7/5.6), FBRT-YOLO-N ≈ 5.1 (34.4/6.7), SOD-YOLO-n ≈ 4.2 (33.0/7.8), LEAF-YOLO ≈ 2.3 (48.3/20.9), FBRT-YOLO-S ≈ 1.9 (42.4/22.9), SMA-YOLO ≈ 2.0 (42.3/20.9). LEAF-YOLO is the best-documented accuracy/efficiency point with verified Jetson FPS; FBRT-YOLO is the strongest peer-reviewed (AAAI) family scaling from 0.9M to 22.8M params.
- Reported "SOTA" mAP50 above ~50 on VisDrone-val almost always comes with either ≥ 65 GFLOPs, 1280-px input, or both; for sub-10 W edge targets, 40–48 AP50 at 640 is the realistic 2025 ceiling.

### Gaps
- FFCA-YOLO (original numbers), YOLO-TLA, DRD-YOLO and the original UAV-YOLO could not be located with VisDrone numbers; "UAV-YOLO" (2020) is a YOLOv3 human detector on a custom dataset.
- The Pareto benchmark's per-model mAP/FPS tables on Orin Nano were behind a 403 (DSU PDF and ResearchGate); only its qualitative conclusions are captured.
- HIC-YOLOv5's own absolute numbers come from LEAF-YOLO's re-benchmark, not its paper.

---

## Key Question 4: Transformer/DETR-style small-object methods (DNTR, DQ-DETR, Dome-DETR, D-FINE/DEIM UAV adaptations, RT-DETR UAV variants) and edge feasibility

### Takeaway
The density-guided DETR lineage DQ-DETR (30.2 AP) → Dome-DETR (34.6) → Dome-DETR + ReDHF (35.7) now owns AI-TOD-v2, and Dome-DETR-S (13.2M, ~150–190 GFLOPs, < 15 ms on T4 for M) is the most edge-plausible of them; for sub-25-GFLOP budgets, DEIM-D-FINE-S/N adaptations (HF-D-FINE, HMF-DEIM, PFE-Det, SCA-DEIM) are the real-time DETR option at ~21–24 AP on VisDrone 640.

### Cited Findings
- DQ-DETR (ECCV 2024): categorical counting module + counting-guided feature enhancement + dynamic query selection; 30.2 AP on AI-TOD-v2 (15.3 AP_vt, 58.7M params, but ~1805 avg GFLOPs per Dome-DETR's measurement); VisDrone val 35.2 AP / 54.9 AP50; code https://github.com/hoiliu-0801/DQ-DETR — [DQ-DETR abs](https://arxiv.org/abs/2404.03507); [Dome-DETR tables](https://arxiv.org/html/2505.05741v2)
- Dome-DETR: see KQ1; key point for edge: 13.2M-param S variant achieves 33.3 AP on AI-TOD-v2 (beating 58.7M DQ-DETR by +3.1 AP at ~10× fewer GFLOPs) and compute adapts to scene density — [Dome-DETR](https://arxiv.org/html/2505.05741v2)
- D-FINE as tiny-object baseline (4 feature levels, 800×800): D-FINE-S 30.1 AP / 14.0 AP_vt (11.6M, 112.4G), -M 30.8 / 14.3 (22.3M, 211.4G), -L 31.3 / 15.3 (34M, 327.5G) on AI-TOD-v2; VisDrone 31.2 / 33.6 / 36.5 AP — [Dome-DETR](https://arxiv.org/html/2505.05741v2)
- DEIM-D-FINE at 640 on VisDrone: N 3.73M / 7.12 GFLOPs / 9.58 ms; S 10.18M / 24.86 GFLOPs / 10.56 ms; M 19.19M / 56.37 GFLOPs / 14.83 ms; PFE-Det (DEIM-D-FINE-S base) reaches AP 0.225, APs 0.134 (+13.5% relative APs) — [PFE-Det, Sensors 2026](https://doi.org/10.3390/s26155003)
- HMF-DEIM: +2.1 mAP50 / +1.6 mAP50-95 over DEIM-D-FINE-S with +1.69M params; bootstrap CIs: baseline mAP50 [0.378, 0.390], HMF-DEIM AP_s [0.141, 0.155] vs baseline AP_s [0.115, 0.129]; beats DEIM-D-FINE-M with 61.9% of its params — [HMF-DEIM](https://www.mdpi.com/1424-8220/26/7/2187)
- HF-D-FINE (Image and Vision Computing): high-resolution features + auxiliary boxes to expand regression range; +3.2 AP / +4.3 AP50 over D-FINE-S on VisDrone with "a tiny increase in FLOPs"; also on AI-TOD, UAVDT — [HF-D-FINE](https://www.sciencedirect.com/science/article/abs/pii/S0262885625004226)
- SCA-DEIM-S: 23.4 AP / 38.6 AP50 / 13.9 APs vs D-FINE-S 22.7 / 39.4 / 12.8 and DEIM-D-FINE-S 21.5 / 38.4 / 12.2 (VisDrone 640; small objects are 62.4% of instances) — [SCA-DEIM](https://pmc.ncbi.nlm.nih.gov/articles/PMC12788032)
- D-FINE-N: 3.7M params, 7.1 GFLOPs, 0.334 mAP50 on VisDrone (as a cross-domain baseline) — [TinyDef-DETR](https://arxiv.org/pdf/2509.06035)
- UAV-DETR (arXiv Jan 2025, v3 Jul 2025): multi-scale fusion with frequency enhancement, frequency-focused downsampling, semantic alignment; +3.1 AP / +4.2 AP50 over its RT-DETR baseline on VisDrone; Dome-DETR lists it at 32.4 AP / 51.9 AP50 with 45.5M params, 247.1 GFLOPs (800 input); code https://github.com/ValiantDiligent/UAV-DETR — [UAV-DETR](https://arxiv.org/abs/2501.01855); [Dome-DETR Table 2](https://arxiv.org/html/2505.05741v2)
- AUHF-DETR (lightweight transformer with spatial attention + wavelet conv for embedded UAV) is singled out by the Applied Sciences 2025 survey as the edge-constrained DETR example ("high FPS with low parameter/FLOP budgets, latency suitable for on-board UAV", 640×1280 input) — [Applied Sciences survey via search](https://www.mdpi.com/2076-3417/15/22/11882); [AUHF-DETR](https://www.researchgate.net/publication/392358547_AUHF-DETR_A_Lightweight_Transformer_with_Spatial_Attention_and_Wavelet_Convolution_for_Embedded_UAV_Small_Object_Detection)
- CDF-DETR (RT-DETR-R18 base, Remote Sensing 2025) and LGI-DETR (local-global interaction, arXiv 2503.18785) are further RT-DETR UAV adaptations — [CDF-DETR](https://www.mdpi.com/2072-4292/18/16/2793); [LGI-DETR](https://arxiv.org/pdf/2503.18785)
- DNTR (hybrid CNN + transformer R-CNN) remains the strongest non-DETR on AI-TOD (26.2 AP, 12.8 AP_vt) but at 128.4M params / 298 GFLOPs and 11.9 FPS on an RTX 3090 — not edge-feasible — [DNTR](https://arxiv.org/html/2406.05755); [Dome-DETR Table 1](https://arxiv.org/html/2505.05741v2)
- Tiny-object DETRs show lower false-negative rates: oLRP (lower better) DINO-DETR 78.9, DQ-DETR 73.4, D-FINE-L 72.5, Dome-DETR-L 70.1 on AI-TOD-v2 — [Dome-DETR Table 5](https://arxiv.org/html/2505.05741v2)

### Inferences
- Edge feasibility tiers: (a) DEIM-D-FINE-N/S derivatives (7–25 GFLOPs at 640, ~10 ms on desktop GPU) are deployable on Orin-class devices today; (b) Dome-DETR-S (~150–190 GFLOPs at 800) is borderline for Orin AGX, not for Orin Nano; (c) DQ-DETR, DNTR, ScaleBridge-Det are server-only.
- The DETR advantage over YOLO is largest on AI-TOD-v2 (very tiny objects): D-FINE-S at 11.6M params scores 30.1 AP vs YOLOv12-X at 59.3M scoring 16.1 — suggesting that for sub-16-px targets the query-based paradigm with 4-level features is worth its cost.

### Gaps
- No FPS for Dome-DETR or ReDHF on any Jetson; only T4 latency bounds (< 15 / < 20 ms) exist.
- UFO-DETR, D³R-DETR absolute numbers unavailable (PDF-only).
- DQ-DETR code status ("will be available") was not verified.

---

## Key Question 5: Super-resolution / feature-level SR for tiny objects and practicality at the edge

### Takeaway
Image-level SR helps modestly (≈ +5 AP points for small objects with 2× SRGAN in one 2025 drone study) but 4× SR hurt, and the 2025–2026 trend is toward latent/feature-level restoration (CoLR-Det) or train-only SR branches, because explicit SR front-ends multiply input pixels and are hard to justify under edge budgets.

### Cited Findings
- A 2025 drone construction-site study with PP-YOLOE-SOD found 2× SRGAN super-resolution improved small-object detection by ~5 percentage points, while 4× SR decreased detection performance — [Sensors and Materials 37(6) 2025](https://sensors.myu-group.co.jp/sm_pdf/SM4080.pdf)
- "From Blurry to Brilliant" (arXiv Jan 2024) combines YOLO with SR for aerial detection, building on SuperYOLO (TGRS, SR-assisted multimodal RS detection) — [arXiv 2401.14661](https://arxiv.org/pdf/2401.14661)
- Sentinel-2 4× SR to 2.5 m GSD plus a YOLOv8 detector fused with a ViT density estimator reduced false positives and improved precision/F1 for tiny objects — [ISPRS Archives 2025](https://isprs-archives.copernicus.org/articles/XLVIII-M-6-2025/61/2025/isprs-archives-XLVIII-M-6-2025-61-2025.pdf)
- CoLR-Det (Jan 2026) performs collaborative latent (feature-space) restoration for small objects in low-resolution RS images rather than explicit image SR — [CoLR-Det, arXiv 2601.12507](https://arxiv.org/pdf/2601.12507)
- The Sensors 2025 real-time aerial survey lists "train-only super-resolution modules" among recommended small-object techniques precisely because they add no inference cost — [Habash et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)
- The Acta Aeronautica 2025 review categorizes UAV small-object methods into discriminative feature learning, super-resolution technology, real-time lightweight detection, and other ideas — [Wu & Tong 2025](https://www.sciopen.com/article/10.7527/S1000-6893.2024.30848)
- Resolution-vs-cost reality check: plain YOLO11s at 1280 doubles AP_small vs 640 (0.223 vs 0.111) — the same effect SR aims for, but at ~4× compute; sliced inference costs 7× latency — [tanirim benchmark](https://github.com/tanirim/aerial-object-detection)

### Inferences
- At the edge, native higher-resolution input with sparse/selective compute (ESOD, DenseScout) or a P2 head is a better use of FLOPs than an SR front-end; SR is most defensible as a training-only auxiliary branch or for fixed-GSD satellite pipelines run offline.

### Gaps
- No 2024–2026 paper found that reports SR-assisted detection latency on Jetson-class hardware.
- No AP_vt / AI-TOD numbers for any SR method surfaced.

---

## Key Question 6: Conclusions of 2024–2026 surveys on cost/accuracy trade-offs

### Takeaway
Surveys converge on: real-time (≥ 30 FPS) is routine on desktop GPUs but "severely degrades" onboard (Jetson RGB detectors: 14–47 FPS); every small-object fix raises compute; the recommended recipe is anchor-free one-stage YOLO-style detectors with a shallow extra head, lightweight attention, BiFPN/GD-style necks, plus TensorRT FP16/INT8, pruning and distillation; and benchmarks must report efficiency metrics, not only mAP.

### Cited Findings
- Habash, Abu Alqumsan & Zhou, "Recent Real-Time Aerial Object Detection Approaches… for Onboard Performance: A Survey", Sensors 25(24):7563, Dec 2025: real-time defined as ≥ 30 FPS; moving models to edge causes "severe speed degradation"; Jetson RGB deployments report 14–47 FPS; embedded platforms typically < 15 W with TX2 and Xavier NX most used; cloud offload example: YOLOv8s FP16 on Orin Nano RTT 35.09 ms vs cloud RTT 348.21 ms (network latency dominates); anchor-free one-stage favored (OBB needs ~6× the anchors of HBB); recommended backbones MobileNet/ShuffleNet/GhostNet/FasterNet (FasterNet-T0 2.8×/3.3×/2.4× faster than MobileViT-XXS on GPU/CPU/ARM); compression via PTQ/QAT, structured pruning, KD, re-parameterization, TensorRT, hardware-aware NAS, NMS-free heads; FPGA results LCAM-YOLOX 195 FPS on ZCU102 — [Sensors 2025 survey](https://pmc.ncbi.nlm.nih.gov/articles/PMC12736610)
- "Advancements in Small-Object Detection (2023–2025)…Practical Guidance", Applied Sciences 15(22):11882: 2023–2025 characterized by consolidation of attention and transformer architectures, renewed multiscale fusion, and emphasis on edge efficiency; accuracy-only metrics are "not a complete measure" for edge; INT8 quantization and knowledge distillation highlighted; AUHF-DETR named as the UAV-embedded exemplar; future work: lightweight SOD architectures via NAS — [Applied Sciences 2025](https://www.mdpi.com/2076-3417/15/22/11882)
- "Small Object Detection: A Comprehensive Survey on Challenges, Techniques and Real-World Applications" (arXiv 2503.20516, 2025): downsampling in CNNs "leads to a significant reduction in small-object information"; defines Dense Small Objects (DSO) for crowded UAV scenes; concludes lightweight networks, KD and self-supervised learning are the promising directions for UAV/edge — [arXiv 2503.20516](https://arxiv.org/pdf/2503.20516)
- "A survey of small object detection based on deep learning in aerial images", Artificial Intelligence Review (Mar 2025) — consolidates remote-sensing and drone small-object challenges — [AI Review 2025](https://link.springer.com/article/10.1007/s10462-025-11150-9)
- Wu & Tong, Acta Aeronautica et Astronautica Sinica 46(3) 2025: five-year review, analyzes algorithm performance via the VisDrone Challenge — [Acta Aeronautica 2025](https://www.sciopen.com/article/10.7527/S1000-6893.2024.30848)
- Edge Pareto benchmark (IEEE Access 2025): "no single model dominates"; YOLOv8n and YOLOv11n are Pareto-optimal on VisDrone/DOTA-v1.5/xView; lightweight YOLOs < 15 GFLOPs are suitable for real time; TensorRT FP16 3–5× speedup; 7.6–10.4 W on Orin Nano (8 GB LPDDR5) — [Shakya et al.](https://scholar.dsu.edu/ccspapers/124/)
- SODA benchmark (TPAMI, "Towards Large-Scale Small Object Detection: Survey and Benchmarks") baseline finding: all detectors collapse on extremely small objects; on SODA-D Cascade R-CNN AP_eS 14.1, RetinaNet 11.9 — [SODA page](https://shaunyuan22.github.io/SODA/); [alphaXiv listing](https://www.alphaxiv.org/abs/2207.14096)
- Current SODA bests: SODA-A 37.8 AP (DyFrDet) and 37.4 AP50:95 with 23.0M params (SPEANet + Oriented R-CNN, 18.1M fewer params than baseline) — [DyFrDet](https://arxiv.org/pdf/2608.02495); [SPEANet](https://arxiv.org/pdf/2609.26064); SODA-D 38.7 AP / 21.4 AP_eS (Dome-DETR-L + ReDHF) — [ReDHF](https://arxiv.org/html/2611.07994)

### Inferences
- The surveys' quantitative anchors (Jetson 14–47 FPS; < 15 W; TensorRT 3–5×) imply a practical envelope for a 640-px UAV small-object detector of roughly ≤ 25 GFLOPs for Orin Nano real time and ≤ 60 GFLOPs for AGX Orin.
- Survey authors treat AP_eS / AP_vt (< 12–16 px) as the open problem: even 2026 SOTA sits at ~21 AP_eS (SODA-D) and ~21 AP_vt (AI-TOD-v2).

### Gaps
- Sections 5–7 of the Sensors survey (quantization/pruning specifics and the edge-device benchmark table) were truncated; its Table 5 lists edge platforms without mAP/FPS.
- The Applied Sciences survey full text was blocked (403); conclusions rely on search-extracted passages.

---

## Key Question 7: Foundation-model approaches (SAM 2/3, DINOv2/v3 distillation, YOLO-World / YOLOE) for tiny objects, and distillation into edge models

### Takeaway
Zero-shot open-vocabulary YOLOs fail almost completely on aerial imagery (YOLO-World / YOLOE F1 < 4% on LAE-80C), so foundation models help tiny-object detection only through adaptation or distillation — e.g., DisDop (RemoteCLIP + DINOv3 priors distilled into a lightweight detector) and DINOv2→YOLOv8 feature distillation — while SAM-family work targets prompt-based small-object segmentation (SOPSeg) rather than edge detection.

### Cited Findings
- Comparative zero-shot evaluation (Grounding DINO, OWLv2, YOLO-World, YOLOE, LLMDet) on LAE-80C: the YOLO family "exhibits near-catastrophic failure in zero-shot aerial transfer, with F1-scores below 4%"; YOLOE precision 0.367 but recall 0.020 — [arXiv 2601.22164](https://arxiv.org/abs/2601.22164)
- DisDop (May 2026): distills multi-level domain priors from remote-sensing foundation models (RemoteCLIP, DINOv3) into a lightweight detector backbone via teacher fusion with self-similarity calibration, plus textual/contextual prior distillation "to enhance small object recognition"; evaluated on DIOR, DOTAv2.0, LAE-80C — [DisDop](https://arxiv.org/abs/2605.24639)
- DINOv2 → YOLOv8 distillation (ICIP 2025): adds a distillation branch in each detection head matching resized frozen DINOv2 patch tokens for fast few-shot detection — [Fourret et al., ICIP 2025](https://www.lirmm.fr/~chaumont/publications/ICIP-2025-FOURRET-CHAUMONT-FIORIO-SUBSOL-BRAU-DinoDistillationIntoYoloV8_ForFSD.pdf)
- CastDet (ECCV 2024): CLIP-activated student-teacher open-vocabulary aerial detector, 46.5% mAP on VisDroneZSD novel categories (+21.0 over prior OV detectors) — [CastDet listing](https://awesomepapers.io/generative-models/papers/2311.11646)
- SOPSeg (Sept 2025) adapts SAM for small-object instance segmentation in RS imagery with region-adaptive magnification, an oriented prompt (box + 3 keypoints) and an edge-aware decoder, noting the scarcity of pixel labels for tiny objects — [SOPSeg](https://arxiv.org/abs/2509.03002)
- SAM 3 zero-/one-shot promptable concept segmentation has been evaluated on remote sensing — [arXiv 2607.09583](https://arxiv.org/pdf/2607.09583); SAM 2 (Aug 2024) is used for promptable segmentation of drone imagery via samgeo workflows — [samgeo workshop](https://samgeo.gishub.org/workshops/AIforGood_2025/); a SciPy Proceedings workflow uses SAM zero-shot on drone orthomosaics for detection/localization — [SciPy Proceedings](https://proceedings.scipy.org/articles/uhje9464)
- YOLOE-v8-S beats YOLO-Worldv2-S by +3.5 AP on LVIS with 3× less training cost and 1.4× faster inference, and supports text/visual/prompt-free modes — [Ultralytics YOLOE docs](https://docs.ultralytics.com/models/yoloe); YOLOE-26 integrates YOLO26 with YOLOE — [arXiv 2602.00168](https://arxiv.org/pdf/2602.00168)
- Small-object KD for UAV: feature-alignment distillation losses "preserve fine-grained spatial features critical for small-object localization"; SDD-YOLO introduces DroneSOD-30K of spot-level targets < 20 px — [SDD-YOLO](https://arxiv.org/pdf/2603.25218); LT-DETR (lightweight UAV detection + dual KD) cited as related — [search summary](https://arxiv.org/pdf/2603.25218)
- Cross-DINO (DINO-style DETR with deep-MLP context + Boost Loss) is the main 2025 "DINO" line for small objects (36.4 AP_S COCO, 45M params) — [Cross-DINO](https://arxiv.org/abs/2505.21868)
- Other OV aerial work: SOAR (semi-supervised OV aerial detection, AAAI 2026) and an OV framework for dense small-object RS detection (Remote Sensing 2026) are catalogued — [Awesome RS OV learning](https://github.com/zhangda1018/Awesome-Remote-Sensing-Open-Vocabulary-Learning)

### Inferences
- Foundation models are currently useful for tiny aerial objects as teachers (DINOv2/v3, RemoteCLIP) or as annotation tools (SAM 2/3 for mask/box pseudo-labels), not as deployable detectors; distillation into YOLO/D-FINE-N-class students is the viable edge path, but no paper yet reports AI-TOD/VisDrone AP_vt gains from such distillation.

### Gaps
- No quantitative evidence found of SAM 2 or DINOv2/v3 distillation improving AP_vt/AP_s on VisDrone, AI-TOD or SODA; DisDop's numbers are on DIOR/DOTAv2/LAE-80C (not tiny-object metrics).
- No YOLOE/YOLO-World fine-tuning results on AI-TOD-v2 surfaced beyond a user question in the Ultralytics docs.

---

## Dataset coverage notes (DOTA, xView, DroneVehicle, UAVDT, TinyPerson)

### Takeaway
Lightweight 2024–2026 work concentrates on VisDrone and AI-TOD; UAVDT and DroneVehicle have a few strong lightweight results, DOTA/xView lightweight numbers are sparse, and TinyPerson has essentially no 2025 leaderboard activity.

### Cited Findings
- UAVDT: FBRT-YOLO 18.4 AP / 31.1 AP50 vs CEASC 17.1 / 30.9, GFL 16.9, GLSAN 17.0, ClusDet 13.7 — [FBRT-YOLO](https://arxiv.org/html/2504.20670v1); HF-D-FINE and LUD-YOLO also evaluate on UAVDT — [HF-D-FINE](https://www.sciencedirect.com/science/article/abs/pii/S0262885625004226); [LUD-YOLO](https://www.sciencedirect.com/science/article/pii/S0020025524012805)
- DroneVehicle (RGB-T): CTU-YOLO 73.9% mAP with 4.2 MB params, 13.8 GFLOPs, 129.9 FPS — [CTU-YOLO](https://doi.org/10.3390/electronics15020298); M2I2HA-n (YOLOv8n) 84.2 mAP@.5 / 62.1 mAP with 6.1M params, -s 85.4 / 63.4 at 24.2M / 68.8G; YOLOv13s RGB 71.1 / IR 79.6; DLANet 0.858 mAP0.5 at 39.04M / 72.69G — [M2I2HA](https://arxiv.org/pdf/2601.14776)
- DOTA/xView: Pareto benchmark finds YOLOv8n (DOTA-v1.5) and YOLOv11n (xView) Pareto-optimal with YOLOv7-tiny fastest but least accurate on xView — [Shakya et al.](https://scholar.dsu.edu/ccspapers/124/); SARL/SAL evaluates on DOTA-v2.0 — [SARL/SAL](https://arxiv.org/abs/2511.09891); HS-FPN on DOTA_mini10 — [HS-FPN](https://arxiv.org/html/2412.10116v3); a pruned + INT8 YOLOv7-tiny on xView reports 0.62 small-object mAP and 12 MB → 4.3 MB size — [GitHub](https://github.com/Durganadh2424/uav-aerial-small-object-detection-or-yolov7-tiny-aerial-detection-.)
- TinyPerson: mean person size 18 px, 794/816 train/test images; historical AP50_tiny ~47 (Scale Match baseline) → ~60.7 (EFFM 2022) — [Scale Match](https://arxiv.org/pdf/1912.10664); LEAF-YOLO 23% AP50 (metric likely standard AP50, not AP50_tiny) — [LEAF-YOLO](https://www.sciencedirect.com/science/article/pii/S2667305325000109); ESOD and CF-YOLO also use TinyPerson — [ESOD](https://arxiv.org/abs/2407.16424); [CF-YOLO](https://www.nature.com/articles/s41598-025-99634-0); recent tiny-person work shifted to RGB-T ("Visible-thermal tiny object detection", TPAMI 2025; "Drone-based RGBT tiny person detection", ISPRS) — [SET CVPR 2025 references](https://openaccess.thecvf.com/content/CVPR2025/papers/Sun_SET_Spectral_Enhancement_for_Tiny_Object_Detection_CVPR_2025_paper.pdf)
- AI-TOD-v2 historical anchor: NWD-RKA reported 24.7 AP / 57.2 AP0.5 at release; SOTA is now 35.7 — [search summary of AI-TOD-v2 page](https://chasel-tsui.github.io/AI-TOD-v2/); [ReDHF](https://arxiv.org/html/2611.07994)

### Inferences
- For military-style small targets at the edge, VisDrone/AI-TOD-v2/UAVDT numbers are the usable proxies; DroneVehicle results indicate RGB-T fusion is reachable in ~14 GFLOPs.

### Gaps
- No 2024–2026 paper found reporting a lightweight model on all of DOTA, xView and DroneVehicle; no TinyPerson 2025 leaderboard with AP50_tiny for modern lightweight detectors.
- Papers With Code leaderboards could not be consulted (not reachable in this session).
