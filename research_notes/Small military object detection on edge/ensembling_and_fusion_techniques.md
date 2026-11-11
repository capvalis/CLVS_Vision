# Ensembling and Fusion Techniques for Tiny/Small Object Detection on Low-End Edge Compute

Scope: box-level fusion, slicing/tiling, coarse-to-fine cascades, TTA, RGB-T fusion, temporal fusion, distillation, learned fusion, competition write-ups, and measured edge numbers (Jetson Orin Nano / RPi5 / Rockchip NPU class). Benchmarks named wherever available. Research date: 2026-11-10. Note: most published accuracy numbers below were measured on workstation GPUs; edge-measured numbers are called out explicitly in the final section.

---

## Q1. Box-level fusion (WBF, Soft-NMS, DIoU-NMS, NMW, Confluence, newer methods): gains for heterogeneous vs homogeneous ensembles; open-source libraries

### Takeaway
WBF is the de-facto standard for merging 2+ detectors and typically yields +1 to +3 mAP for 2-model ensembles and up to ~+8 mAP for 5+ diverse models; gains grow with architectural diversity (CNN + transformer) but every added model multiplies inference cost. For a *single* detector in dense aerial scenes, swapping hard NMS for Soft-NMS/DIoU-NMS (or cluster-DIoU-NMS) gives +2 to +6 mAP@0.5 at near-zero cost, whereas WBF applied to a single model's output is worse than NMS.

### Cited Findings
- WBF reference benchmark (ZFTurbo repo, Open Images): five single models at 0.491–0.516 mAP@0.5; combined via NMS 0.5642, Soft-NMS 0.5616, NMW 0.5667, WBF 0.5982 — i.e. WBF ≈ +8 mAP over the best single model and +3.4 over NMS-ensembling. The same README warns WBF on a single model is worse than NMS (single-model NMS 0.4902 vs WBF 0.4532). — [ZFTurbo/Weighted-Boxes-Fusion](https://github.com/ZFTurbo/Weighted-Boxes-Fusion); [WBF paper, arXiv 1910.13302](https://arxiv.org/abs/1910.13302)
- WBF paper: "even for the ensemble of only two models, the WBF method outperformed significantly other methods"; large COCO ensemble reached 56.1 mAP val / 56.4 test. — [arXiv 1910.13302](https://arxiv.org/abs/1910.13302)
- VisDrone-DET2021 (aerial, tiny objects): ViT-YOLO team ensembled YOLOv5, YOLOv4 and ViT-YOLO with TTA + WBF, reaching 39.41 mAP on test-challenge (2nd place, 0.02 behind winner). — [ViT-YOLO, ICCVW 2021](https://openaccess.thecvf.com/content/ICCV2021W/VisDrone/papers/Zhang_ViT-YOLOTransformer-Based_YOLO_for_Object_Detection_ICCVW_2021_paper.pdf)
- VisDrone-DET2021 organisers: "ensemble learning of a few powerful detectors can largely boost the detection performance"; winner DBNet 39.43 mAP / 65.34 AP50 (Cascade R-CNN + BiFPN, multi-scale test + fused outputs); top-10 all >38.0 mAP. — [VisDrone-DET2021 results, ICCVW 2021](https://openaccess.thecvf.com/content/ICCV2021W/VisDrone/papers/Cao_VisDrone-DET2021_The_Vision_Meets_Drone_Object_Detection_Challenge_Results_ICCVW_2021_paper.pdf)
- TPH-YOLOv5 (VisDrone 2021, 5th): multi-scale testing + 5-model ensemble gave 39.18 mAP vs 2020's best 37.37. — [TPH-YOLOv5, arXiv 2108.11539](https://arxiv.org/abs/2108.11539)
- Heterogeneous-YOLO ensemble + WBF (disaster-scene dataset, 2025/26): 2 models + NMS ≈ 0.70 mAP → 2 models + WBF ≈ 0.707 → 4 models + WBF 0.746 → 8 models + WBF 0.756, "at a steep cost in FPS"; authors state WBF's advantage over suppression methods "is further amplified when paired with heterogeneous model ensembles". — [Technologies 14(9):530](https://doi.org/10.3390/technologies14090530)
- Cross-architecture CNN + transformer WBF (RT-DETR-X + Faster R-CNN, floating-waste dataset): ensemble mAP50 89.08%, beating each individual model (YOLOv8s, RT-DETR-X). — [Neural Computing & Applications](https://link.springer.com/article/10.1007/s00521-026-12051-w)
- Confidence-aware WBF (weights = each model's validation mAP) marginally beat equal-weight WBF (0.833 mAP) on a weapon dataset; authors argue the fusion weighting matters as much as diversity. — [arXiv 2509.23697](https://arxiv.org/abs/2509.23697)
- Head-to-head *under sliced inference* on VisDrone-val (TPH-YOLOv5 + ASAHI; mAP / mAP50 / mAP50_small / img/s): NMS 33.9 / 55.8 / 47.4 / 3.06; Soft-NMS 32.3 / 52.6 / 44.3 / 2.72; WBF 33.4 / 55.1 / 46.7 / 2.88; Cluster-DIoU-NMS (CDN) 36.0 / 56.8 / 48.5 / 5.26. CDN = +2.1 mAP vs NMS and 72% faster. Note: here WBF and Soft-NMS were *worse* than NMS for merging tile outputs of a single detector. — [ASAHI, arXiv 2604.19233](https://arxiv.org/abs/2604.19233)
- Single-detector NMS variants on aerial data (YOLOv5s-DSD; four numbers = mAP@0.5 etc.): Soft-NMS-IoU 52.4, -GIoU 53.0, -DIoU 53.6, -CIoU 53.7; replacing hard NMS with Soft-NMS-CIoU gave +4.4 mAP@0.5 on dense aerial objects. — [YOLOv5s-DSD, Sensors 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10422290/)
- HSP-YOLOv8 (UAV imagery): introducing Soft-NMS raised mAP@0.5 by 6.1%, "alleviates missed detections caused by clustering of small objects". — [HSP-YOLOv8](https://pdfs.semanticscholar.org/fc3a/457027fc0c98756b362ef5248826e514b4f7.pdf)
- DIoU-NMS replacing NMS in YOLOv5 "significantly enhances the detection accuracy of dense small objects" on VisDrone2019 (no isolated delta given in snippet). — [Radioengineering 2024](https://www.radioeng.cz/fulltexts/2024/24_01_0012_0023.pdf)
- Confluence (non-IoU NMS alternative): on COCO/VOC it beat Greedy-NMS and Soft-NMS by 0.6–1.7 AP@0.5 and is less threshold-sensitive (0.2% vs 0.4% AP variation); no aerial benchmark reported. — [Confluence, arXiv 2012.00257](https://arxiv.org/abs/2012.00257)
- Ultralytics built-in ensembling (YOLOv5 `--weights a.pt b.pt`): yolov5x + yolov5l6 ensemble 0.515 AP vs 0.504 baseline (COCO); mAR 0.681→0.689. Newer `ultralytics` package (v8/11) has no equivalent multi-model CLI flag. — [Ultralytics model-ensembling docs](https://docs.ultralytics.com/yolov5/tutorials/model-ensembling)
- Libraries: `ensemble-boxes` (pip) from ZFTurbo implements NMS, Soft-NMS, NMW, WBF (plus 3D variants); the FAIR1M 3rd-place team extended WBF for oriented boxes. — [ZFTurbo/Weighted-Boxes-Fusion](https://github.com/ZFTurbo/Weighted-Boxes-Fusion); [G-Naughty/Fine-grained-OBB-Detection](https://github.com/G-Naughty/Fine-grained-OBB-Detection)

### Inferences
- The ASAHI table is the most directly relevant data point for edge tiling: when merging *one* model's tile predictions, a cluster-DIoU-NMS is both more accurate and faster than WBF/Soft-NMS; reserve WBF for merging *different* models or TTA views.
- Reported heterogeneous gains (YOLO + DETR/R-CNN) are consistently positive but the only aerial-tiny-object evidence is the 2021 VisDrone workshop (YOLOv4/v5/ViT-YOLO); no 2023-2026 paper isolating "YOLO + RT-DETR via WBF on VisDrone/AI-TOD" was found.
- On an edge budget, a 2-model heterogeneous ensemble halves FPS for roughly +1–3 mAP; a NMS-variant swap is nearly free and gives comparable gains in dense scenes, so it should be the first thing tried.

### Gaps
- No paper found that isolates WBF-vs-NMS deltas on VisDrone/AI-TOD/DOTA with modern (2023+) YOLO + DETR pairs; VisDrone challenge reports bundle ensembling with TTA and multi-scale.
- Confluence has no published aerial/tiny-object evaluation.
- A "hybrid ensemble of 4 YOLO variants + RF-DETR on DroneVision" was mentioned in search summaries without a retrievable URL, so it is not cited.

---

## Q2. Slicing / tiling inference (SAHI and successors): AP_small gains on VisDrone/xView, latency multiplier, edge-optimised strategies

### Takeaway
SAHI inference alone adds +5–7 AP50 on VisDrone (+4–5 AP50_small) and is the single largest cheap gain for tiny objects, rising to +13–15 AP50 when the model is also fine-tuned on slices; the cost is ≈ (tiles + 1) forward passes per frame (typically 4–12×). ASAHI (fixed tile count), full-image + slice fusion, and ROI/motion-gated tiling are the main cost reducers; batching tiles through a TensorRT/NPU engine is what makes it viable on Orin-Nano-class hardware.

### Cited Findings
- SAHI (VisDrone2019-DET test-dev, AP50 / AP50_small): TOOD full-image 29.4 / 18.1 → +SAHI 31.9 / 22.6 → +SAHI+FI+PO 34.7 / 23.8 → +slice-fine-tuned +SAHI+FI+PO 43.5 / 31.7. FCOS 25.8/14.2 → 31.0/19.8 (inference only) → 38.5/25.9 (with SF). VFNet 28.8/16.8 → 33.9/22.4 → 42.2/29.6. Inference-only gains: +6.8 / +5.1 / +5.3 AP50 (FCOS/VFNet/TOOD); cumulative with slice-fine-tuning +12.7 / +13.4 / +14.5. — [SAHI, arXiv 2202.06934 (ar5iv tables)](https://ar5iv.labs.arxiv.org/html/2202.06934); [obss/sahi](https://github.com/obss/sahi)
- SAHI on xView (AP50 / AP50_small): full-image inference is essentially useless (TOOD 2.1 / 0.1) vs TOOD+SF+SAHI+PO 20.6 / 14.9 — objects are <1% of image width. Settings: 640×640 slices (VisDrone), 400×400 (xView), 25% overlap, NMS IoU 0.5. — [SAHI, ar5iv](https://ar5iv.labs.arxiv.org/html/2202.06934)
- SAHI side-effects: 25% overlap raises small/medium AP but "slightly decreases large object AP"; adding full-image inference (FI) recovers large objects (xView up to +3.3 AP50_large) at a tiny cost to small AP. — [SAHI, ar5iv](https://ar5iv.labs.arxiv.org/html/2202.06934)
- ASAHI (2026; TPH-YOLOv5 backbone, RTX 3080): fixed slice *count* (6 if max(W,H) ≤ 1818 px, else 12) instead of fixed 512-px slice size. VisDrone2019-DET-test: SAHI(512) 28.7 mAP / 42.2 mAP50 / 29.8 mAP50_s at 3.69 img/s vs ASAHI-adaptive 30.4 / 45.6 / 33.8 at 4.88 img/s. xView-test: SAHI 16.07 / 20.4 / 14.9 at 2.56 img/s vs ASAHI 17.5 / 22.7 / 17.3 at 3.58 img/s. Redundant-computation reduction vs SAHI: 38.7% at 960×540, ~25% at 1920×1080, 7% at 2913×2428. — [ASAHI, arXiv 2604.19233](https://arxiv.org/abs/2604.19233)
- ASAHI ablation (VisDrone-val, mAP / mAP50 / mAP50_small / mAP50_large): full-image only 15.7 / 34.2 / 21.4 / 74.4 → +ASAHI 34.1 / 54.4 / 46.6 / 58.9 → +FI 34.1 / 55.5 / 46.7 / 76.5 → +overlap 34.3 / 55.5 / 46.8 / 77.6 → +slice-fine-tune +CDN 36.0 / 56.8 / 48.5 / 72.9. Tile-count sweep on VisDrone-test: 4 slices 5.19 img/s / 23.9 mAP; 6 slices 4.98 / 28.5; 12 slices 2.98 / 29.3; 15 slices 2.39 / 27.2 (more tiles eventually hurts). — [ASAHI, arXiv 2604.19233](https://arxiv.org/abs/2604.19233)
- ASAHI vs coarse-to-fine SOTA on VisDrone-val (mAP / mAP50 / img/s): Focus&Detect 42.0 / 66.1 / 0.73; ClusDet 32.4 / 56.2 / 1.29; DMNet 28.2 / 30.5 / 1.87; GLSAN 30.7 / 55.4 / 2.30; QueryDet 33.9 / 56.1 / 2.75; TPH+SAHI 34.9 / 55.1 / 4.67; TPH+ASAHI 36.0 / 56.8 / 5.26 (≈7.2× faster than Focus&Detect). — [ASAHI, arXiv 2604.19233](https://arxiv.org/abs/2604.19233)
- Earlier ASAHI (Remote Sensing 2023) introduced the fixed-slice-count idea and reported 20–25% inference-time reduction vs SAHI. — [ASAHI 2023](https://www.researchgate.net/publication/368856750_Adaptive_Slicing-Aided_Hyper_Inference_for_Small_Object_Detection_in_High-Resolution_Remote_Sensing_Images)
- ROI-Gated SAHI (2026): YOLOv8n at 416 px proposes ROIs, boxes expanded 1.3×, SAHI (640 tiles, YOLOv8s) run only inside ROIs if coverage R < 0.40, else full SAHI; proposer + refiner merged by NMS 0.45. On COCO128: static gating is *slower* on average (0.88×) and loses ~0.10 mAP@0.5 (sparse scenes 0.646→0.363 because missed proposals cannot be recovered); adaptive routing gives only 1.02× speedup at 0.7305 vs 0.7569 mAP@0.5. Per-image speedups 0.96× (dense), 2.38× (moderate), 6.90× (sparse, 2.7% ROI coverage). No aerial dataset, no edge hardware. — [ROI-Gated SAHI, arXiv 2608.23923](https://arxiv.org/abs/2608.23923)
- Tiling + full-frame fusion wins Drone-vs-Bird 2025: YOLO11m on 4 overlapping tiles (each 55% of W and H, e.g. 1920×1080 → four 1056×594 tiles) + full frame, merged with NMS (IoU 0.1). Validation mAP@0.5 averaged 0.739 vs 0.552 full-frame only (+18.7 points); one of seven videos regressed (0.741→0.499) because rocks/vegetation produced false positives at higher recall. YOLO11m-P2 and 1280-px input were tried and dropped (modest gains, prohibitive training time). No FPS reported; authors note 5 detector calls per frame is the bottleneck. — [Laroca et al., arXiv 2504.19347](https://arxiv.org/abs/2504.19347)
- Cost model for 1080p + 640 tiles + 20% overlap + 1 full-frame pass at 8 ms/slice: 7 × 8 ≈ 56 ms (~18 FPS ceiling) vs ~12 ms (~80 FPS) whole-frame; "often a 4–5× latency increase". — [Technolynx SAHI+YOLO](https://www.technolynx.com/post/sahi-yolo-slicing-aided-inference-for-small-faces-and-distant-objects/)
- The stock `sahi` package runs slices sequentially (batch=1 only), confirmed by maintainers; community forks add slice batching. — [obss/sahi discussion #972](https://github.com/obss/sahi/discussions/972); [ultralytics discussion #4769](https://github.com/orgs/ultralytics/discussions/4769); [ultralytics SAHI guide](https://docs.ultralytics.com/guides/sahi-tiled-inference)
- Practical batching recipe: an RF-DETR+SAHI user exported with batch_size=5 (4 slices + 1 resized full image) so one forward pass covers all tiles, then built a TensorRT engine with a matching profile. — [roboflow/rf-detr issue #780](https://github.com/roboflow/rf-detr/issues/780)
- Slice-assisted *training only* (SliceTrain, YOLOv8-SMOT, MVA 2025 SMOT4SB birds): train on 1280×1280 tiles (20% overlap) from 4K frames, infer on the full frame with no stitching; YOLOv8-S reaches 53.8 SO-HOTA at 17.6 FPS on RTX 3090 at 2160×3840 vs YOLOv8-L 55.2 at 5.7 FPS. — [YOLOv8-SMOT, arXiv 2507.12087](https://arxiv.org/abs/2507.12087)

### Inferences
- Latency multiplier is ≈ N_tiles (+1 if full-frame pass is fused). ASAHI's own sweep shows 6 tiles is the knee for 1080p-class imagery; 12+ tiles buys <1 mAP for ~2× cost.
- Slice-aided *fine-tuning* roughly doubles the benefit of slice inference (SAHI table: +5 → +14 AP50) and costs nothing at run time — it should always be done before deploying tiled inference on edge.
- ROI-gated tiling is only a win in sparse scenes (which is typical of military/anti-UAV sky or open-terrain imagery) and must be paired with a recall-oriented proposer or a motion cue; dense urban VisDrone-style scenes gain nothing.
- Choosing a mid-size model at higher input resolution (e.g. 960) can rival tiling at lower complexity; evidence is dataset-specific (see Q9 CSCWD RPi5 numbers).

### Gaps
- No published AP_small numbers for SAHI/ASAHI measured *on* Jetson/RPi/RK3588 — all accuracy tables are desktop GPU.
- "PowerSAHI" and "learned slicing" (2024–2025) did not surface in searches; S³AHI (test-time adaptation with teacher-student) was only mentioned in ROI-Gated SAHI's related work.
- Motion-guided tiling for video exists in practice (GL-YOMO's ROI switching, Q3) but no paper quantified tile-count reduction from motion cues.

---

## Q3. Cascades / coarse-to-fine (ClusDet, DMNet, CRENet, UFPMP-Det, CZDet, YOLC, Focus&Detect, AD-Det, GL-YOMO): accuracy and compute profile on VisDrone/UAVDT

### Takeaway
Cluster/density-guided zoom-in methods remain the accuracy leaders on VisDrone (Focus&Detect 42.0 mAP) but run at 0.7–2 img/s on desktop GPUs with heavy backbones; the practical edge variant is a *global-then-local ROI* scheme (GL-YOMO) that runs at 21.6 FPS on Jetson Xavier NX and raises recall from 0.56 to 0.83 on 1-px-to-146-px fixed-wing targets. The paradigm's known failure mode is that tiny objects missed in the coarse pass are never recovered.

### Cited Findings
- VisDrone-val speed/accuracy of coarse-to-fine methods (mAP / mAP50 / img/s, from ASAHI's SOTA table): Focus&Detect 42.0 / 66.1 / 0.73; CRENet 33.7 / 54.3 / 1.10; ClusDet 32.4 / 56.2 / 1.29; DMNet 28.2 / 30.5 / 1.87; GLSAN 30.7 / 55.4 / 2.30; QueryDet 33.9 / 56.1 / 2.75. — [ASAHI, arXiv 2604.19233](https://arxiv.org/abs/2604.19233)
- Focus&Detect: two-stage region-search framework with ResNeXt-101 in both focus and detection stages; 42.06 AP on VisDrone-val. — [Focus&Detect, arXiv 2203.12976](https://arxiv.org/abs/2203.12976)
- ClusDet (ICCV 2019 baseline): cluster proposal sub-net + scale estimation + detector; iterative cluster merging limits chip count to cut compute. — [ClusDet, arXiv 1904.08008](https://arxiv.org/abs/1904.08008)
- YOLC (2024): Local Scale Module finds cluster regions, crops, rescales 1.5×, pads to 1024×640, re-detects with the *same* detector and replaces coarse results in that region without NMS; reported best accuracy with fewer processed crops and higher s/img than ClusDet/DMNet-style methods; reference implementation uses HRNet-W48 (not edge-friendly). — [YOLC, arXiv 2404.06180](https://arxiv.org/abs/2404.06180)
- RemDet (AAAI 2025) argues for single-pass efficient design instead of cropping: VisDrone 40% mAP, "8.2% over YOLC and 6.8% over CZDet"; UAVDT 20.6%. Also notes UFPMP-Det clusters then packs crops into a mosaic for one inference. — [RemDet, arXiv 2412.10040](https://arxiv.org/abs/2412.10040)
- AD-Det (Remote Sensing 2025): coherent coarse-to-fine with final output = NMS(Coarse(G), Fine(S_i)); evaluated on VisDrone and UAVDT, reported to beat CZDet, "the best prior cluster-based method". — [AD-Det, arXiv 2504.05601](https://arxiv.org/abs/2504.05601)
- AdaZoom authors: coarse-to-fine performance "is limited by the initial detection ... small objects are easily missed in coarse-level detection". — [AdaZoom, arXiv 2106.10409](https://arxiv.org/abs/2106.10409)
- GL-YOMO (Nov 2024, small UAV detection): global YOLO on full 1920×1080 (resized 640) → after 30 consecutive hits switch to a 300×300 local ROI (separate local YOLO), revert after 60 misses; ROI grows with missed frames. Fixed-Wings test set (targets 1×1 to 146×95 px, mean 0.01% of image): global-only P/R/F1/AP 0.968 / 0.560 / 0.709 / 0.553 → global+local 0.989 / 0.829 / 0.902 / 0.828 → +motion fallback 0.981 / 0.861 / 0.917 / 0.822. Runs at 21.6 FPS on Jetson Xavier NX (TensorRT, 640×640). — [GL-YOMO, arXiv 2411.02582](https://arxiv.org/abs/2411.02582)
- Edge-oriented single-stage alternatives: LEAF-YOLO (ISWA 2025) >30 FPS on Jetson AGX Xavier (TensorRT FP16) on VisDrone-val; a 2026 local-context method reports 50.55 mAP50 / 31.81 mAP50-95 at 1024 px, 12.6M params, 36.65 ms / 27.3 FPS on Jetson Orin NX. — [LEAF-YOLO](https://github.com/highquanglity/LEAF-YOLO); [SIVP 2026](https://link.springer.com/article/10.1007/s11760-026-05799-0)

### Inferences
- Classic cluster-based cascades (ClusDet/DMNet/CRENet/Focus&Detect) are not viable on Orin-Nano-class hardware: they use ResNeXt-101/HRNet backbones and run ~1 img/s on desktop GPUs.
- A two-model cascade of a nano global detector plus a small ROI detector (GL-YOMO pattern) is the compute-feasible version: it converts the tiling multiplier into 1–2 passes per frame once a target is locked.
- For stationary-camera anti-UAV, replacing the learned coarse stage with a motion-based proposer (Q6) is cheaper still.

### Gaps
- Could not retrieve AD-Det's result tables (arXiv HTML 404, PDF fetch returned binary) — its AP/FPS numbers vs CZDet/YOLC are not recorded.
- No 2024–2026 cluster/zoom-in paper was found with Jetson Orin Nano / RPi5 measurements.
- CZDet's own numbers and compute profile were not fetched (only referenced via RemDet/AD-Det).

---

## Q4. Test-time augmentation (multi-scale + flip): gains vs cost for small objects

### Takeaway
TTA gives roughly +1 to +2 mAP (Ultralytics: 0.504→0.516 on COCO) and more for tiny objects when the extra scale is an *upscale*, but cost grows linearly with views (3 scales × flip ≈ 6×); it is a competition tool, not an edge tool, except for a single cheap horizontal flip.

### Cited Findings
- Ultralytics YOLOv5 TTA (`--augment`, reflection + scale): COCO mAP 0.504→0.516, mAR 0.681→0.696; YOLOv5x6 at 1536 px 55.0→55.8 with TTA. TTA can be stacked on ensembles with the same flag. — [Ultralytics TTA docs](https://docs.ultralytics.com/yolov5/tutorials/test-time-augmentation)
- Small-bird challenge 2023 (YOLOv7): multi-scale inference at 3200/3360/3520 px + flips, merged with WBF, won the development track (public AP@0.5 0.732). — [arXiv 2401.01018](https://arxiv.org/abs/2401.01018)
- Shift-TTA on COCO: CenterNet +1.0 AP / +2.2 AP50 from 4 shifts, "4× inference time". — [arXiv 2008.05787](https://arxiv.org/abs/2008.05787)
- Scale-aware AutoAug: FCOS 49.6 AP → 51.4 AP with multi-scale testing at [480, 800, 1400]; AP_small 37.4 with MS-test; training-time augmentation gains (+1.6 AP_s) "introduce no additional cost to inference". — [arXiv 2103.17220](https://arxiv.org/abs/2103.17220)
- FudanDML (Anti-UAV 2023, IR tiny drones): spatial-scale TTA at ratios [0.5,1,2] or [0.5,0.75,1,1.5,2] + flips raised validation score 0.679→0.697; adding *temporal* scales (multi-frame differencing) gave far more: 0.769–0.803. — [3rd Anti-UAV report, arXiv 2305.07290](https://arxiv.org/abs/2305.07290)
- Albumentations TTA guide: horizontal flip is the cheapest and most common; pushing to 9 extra views costs ~9× for +0.42%. — [Albumentations TTA](https://albumentations.ai/docs/4-advanced-guides/test-time-augmentation/)
- One challenge report found flips/rotations did not help when the model was not trained with matching augmentations. — [arXiv 2504.09507](https://arxiv.org/pdf/2504.09507)
- ASA-TTA (2025) benchmarks TTA fusion for oriented detectors on DOTA-v1.0, FAIR1M-2.0, DIOR-R, HRSC2016 across YOLO11 n–x and Oriented R-CNN (76 settings). — [ASA-TTA](https://github.com/Yongt-D/ASA-TTA)

### Inferences
- Within a fixed compute budget, one extra *upscaled* pass (or tiling) beats flip/shift TTA for tiny objects because it directly increases object pixel count; flip adds ~0.5–1 AP at 2× cost.
- Temporal "TTA" (multi-frame difference inputs) gave 5–10× the gain of spatial TTA in the IR anti-UAV setting, suggesting edge budgets should be spent on temporal cues before spatial TTA.

### Gaps
- No paper found reporting TTA AP_small deltas specifically on VisDrone/AI-TOD with a stated latency multiplier.

---

## Q5. Multi-modal RGB + thermal/IR fusion for small targets: early/mid/late, lightweight nets, is WBF late fusion competitive?

### Takeaway
On DroneVehicle, simple late fusion (averaging separate RGB and IR detectors) beats early channel concatenation (44.2 vs 43.7 mAP vs 42.3 RGB-only) and is close to a purpose-built mid-level fusion net (45.8); gains concentrate at night / low visibility. Late fusion of two small detectors is therefore competitive and modular, but costs two forward passes; mid-fusion lightweight nets (GLFDet, ATM-Net) are the research direction for edge.

### Cited Findings
- DroneVehicle: 28,439 RGB-IR pairs, 5 vehicle classes; baseline UA-CMDet (two modality branches + fused branch, independent heads) 64.01 mAP50 (OBB). — [UA-CMDet, arXiv 2003.02437](https://arxiv.org/abs/2003.02437)
- AMSRDet (Sensors 2026) fusion-level comparison on DroneVehicle (same backbone): RGB-only 42.3 mAP (day 44.8 / night 35.2); early fusion (concat) 43.7; late fusion (average predictions of separate RGB and IR detectors) 44.2 "with more balanced day/night"; AMSRDet mid-level CMGF fusion 45.8 (day 47.5 / night 44.2). — [AMSRDet](https://www.mdpi.com/1424-8220/26/3/817)
- ERDF-Anchor (Electronics Letters 2026): lightweight decision-level fusion where a 4-channel early-fusion detector supplies anchors and RGB-only / IR-only detectors act as experts for confidence reweighting and weighted box refinement; on DroneVehicle 50.6% of objects are more reliable in RGB and 46.8% in IR. Cites UA-CMDet 0.640, TSFADet 0.7306, SAMS-YOLO-OBB 0.8075 mAP50. — [ERDF-Anchor](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ell2.70683)
- ISQED efficient RGB-IR aerial fusion: "fusion methods provide marginal improvements in well-lit daytime conditions, the gains are concentrated in low-visibility settings". — [ISQED proceedings](https://www.isqed.org/English/Proceedings/pdf/6C-3-170.pdf)
- GLFDet (Chinese J. Aeronautics 2025): global–local feature optimisation, best results on DroneVehicle, VEDAI, LLVIP and "more lightweight than other comparable models ... appealing to edge devices such as drones". — [GLFDet](https://www.sciopen.com/article/10.1016/j.cja.2025.103781)
- ATM-Net (Drones 2026): lightweight multimodal fusion for real-time UAV detection; characterises early fusion (FGMF, UA-CMDet) as causing "destructive inter-modal coupling" and late fusion (CIAN, AR-CNN) as missing feature-level complementarity. — [ATM-Net](https://doi.org/10.3390/drones10010067)
- SpectraSentinel (RGB-IR drone detection): mid-fusion 0.81, mid-to-late fusion 0.78, mid-fusion + transformer 0.84 mAP@0.5:0.95. — [arXiv 2507.22650](https://arxiv.org/abs/2507.22650)
- Other 2025 options: WaveMamba (ICCV 2025, M3FD + DroneVehicle), YOLOv11-RGBT single-stage multispectral framework (arXiv 2506.14696). — [WaveMamba supp.](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Zhu_WaveMamba_Wavelet-Driven_Mamba_ICCV_2025_supplemental.pdf)
- Anti-UAV 2023 was IR-only (640×512), and most misses occur on drones under 10×10 px (SIA-DT). — [3rd Anti-UAV report](https://arxiv.org/abs/2305.07290)

### Inferences
- The AMSRDet ladder (RGB 42.3 → early 43.7 → late 44.2 → mid 45.8) implies late fusion via WBF/averaging captures ~60% of the best fusion gain with zero architecture work, which is attractive when two separately-trained tiny detectors already exist.
- Because gains are night/low-visibility dominated, an edge system could run IR-only at night and RGB-only by day (adaptive sensor selection) rather than always paying for two passes.

### Gaps
- No paper found that specifically fuses two *nano*-size RGB and IR detectors via WBF and reports DroneVehicle/LLVIP numbers plus edge FPS.
- GLFDet/ATM-Net parameter counts and FPS were not retrieved.

---

## Q6. Temporal fusion for video: tracking-by-detection, temporal aggregation, motion proposals; what Anti-UAV winners do

### Takeaway
Every top Anti-UAV 2023 entry was detection-centric with a motion branch: frame differencing / background alignment / motion-intensity maps added +1 to +8 points, and global re-detection was the single biggest tracker gain (+8.4). Tracking (ByteTrack/OC-SORT) mainly suppresses false positives and fills gaps; for tiny boxes, expanding boxes and using centre-distance costs instead of raw IoU is critical (SO-HOTA 44.2→55.2).

### Cited Findings
- 3rd Anti-UAV (CVPR 2023, IR, 640×512): Track 1 — Colalab 0.700, USTC 0.688, SIA-DT 0.680; Track 2 — Z-Y 0.611, FudanDML 0.591, Colalab 0.570. — [3rd Anti-UAV report, arXiv 2305.07290](https://arxiv.org/abs/2305.07290)
- Colalab (Track 1 winner): "Strong Detector" (several detectors combined) + rule-based tracker + frame-difference/background motion model + video-clip classifier re-scoring + SOT post-processing. Ablation: 0.532 → +threshold 0.557 → +simple track 0.599 → +motion model 0.607 → +SOT 0.609. — [same](https://arxiv.org/abs/2305.07290)
- USTC UTTracker: background alignment +3.8, global re-detection +8.4, multi-region local tracking +2.4, dynamic small-target detection (statistical clustering) +0.5 (53.7→68.8). — [same](https://arxiv.org/abs/2305.07290)
- SIA-DT: pure detector ensemble (Cascade R-CNN, Guided Anchor, Faster R-CNN with Swin-T, anchor scale 8→2, + YOLOX-X), 12-weight box fusion: YOLOX 0.623, Cascade 0.661, 4-model fusion 0.667, 12-weight fusion 0.680. — [same](https://arxiv.org/abs/2305.07290)
- Z-Y (Track 2 winner): YOLOv5 + retinal-motion-extraction map used to enhance candidate features + spatial/coordinate attention: YOLOv5s 53.6 → +motion 61.3 → +attention 61.9 → YOLOv5l 62.3. — [same](https://arxiv.org/abs/2305.07290)
- FudanDML: multi-frame differences fed as input channels + spatio-temporal multi-scale TTA: 0.679 (no temporal) → 0.769–0.803 with 1–3 temporal scales. — [same](https://arxiv.org/abs/2305.07290)
- CVPR 2024 UG2+ anti-UAV winner: YOLOv9 + EfficientNet-B7 classifier, multi-modal (stereo/LiDAR/radar/audio) 3D tracking. — [arXiv 2405.16464](https://arxiv.org/abs/2405.16464); [Anti-UAV survey, arXiv 2504.11967](https://arxiv.org/abs/2504.11967)
- GL-YOMO motion fallback (Jetson Xavier NX, 21.6 FPS): three-frame LK-aligned differencing + template matching + Kalman verification triggered only when YOLO confidence is below threshold; recall +5.7 pts (global) / +3.2 pts (global-local) with slight precision drop. — [GL-YOMO, arXiv 2411.02582](https://arxiv.org/abs/2411.02582)
- RT-DETR + ByteTrack + training-free motion-consistent fusion: suppresses false positives but recall drops 90%→76% — "a deliberate trade-off". — [Motion-consistent temporal fusion](https://ait.knu.ua/en/article/view/9132)
- Drone-vs-Bird 2025 winner temporal post-processing: match detections within ±6 frames (same class, IoU ≥ 0.1), linearly interpolate missing boxes with confidence = half the mean of matched boxes; improves consistency "albeit with a minor increase in the number of false positives" (no numeric ablation). — [arXiv 2504.19347](https://arxiv.org/abs/2504.19347)
- YOLOv8-SMOT (tiny birds, OC-SORT base with ByteTrack tiers): tracker ablation 44.2 → +EMA velocity 47.9 → +2× box expansion 51.4 → +DIoU-like centre-distance 55.2 SO-HOTA; GT inter-frame IoU 10th percentile 0.048 raw vs 0.621 with the fixes. — [arXiv 2507.12087](https://arxiv.org/abs/2507.12087)
- Spatio-temporal anti-UAV (Sensors 2026): motion branch via inter-frame differencing activated when the appearance detector is uncertain, to recover misses on "extremely small" UAVs. — [Sensors 26(5):1492](https://www.mdpi.com/1424-8220/26/5/1492)
- TRX-TCRNet: statistical temporal anomaly detector (temporal Reed-Xiaoli, stationary background) in parallel with a lightweight CNN, described as "remarkably lightweight ... well-suited for edge applications". — [Sensors 26(1):170](https://doi.org/10.3390/s26010170)
- Drone-vs-Bird 2023 (ICASSP): winner OBSS AI (SAHI authors) trained on four drone datasets + synthetic copy-paste backgrounds; another entry used YOLOv7 + CSRT tracker with confidence thresholding to cut false positives (0.885 mAP val). — [ICASSP 2023 review](https://ieeexplore.ieee.org/document/10475518); [YOLOv7+CSRT](https://www.academia.edu/102124877/Drone_vs_Bird_Drone_Detection_Using_YOLOv7_with_CSRT_Tracker)

### Inferences
- For a fixed or slowly-panning camera, frame differencing / background modelling is the cheapest "second detector" available — it costs CPU-only milliseconds and gave gains comparable to adding a whole second CNN in the Anti-UAV ablations.
- Tracker choice matters less than tiny-box association metrics: expanded-box IoU plus centre-distance cost should be the default for sub-20-px targets.
- Temporal interpolation/tracking consistently trades a few false positives for recall; conversely motion-consistency filters trade recall for precision — the direction should be chosen per mission.

### Gaps
- Could not retrieve the 4th Anti-UAV (2024/2025) challenge winners' component ablations.
- TRX-TCRNet's quantitative numbers and edge latency were not retrievable (MDPI returned 403).
- No edge-measured numbers found for ByteTrack/OC-SORT overhead on Orin Nano/RPi5 beyond the tensorrtx SAHI+ByteTrack ~15 FPS figure (Q9).

---

## Q7. Knowledge distillation / model merging as an alternative to runtime ensembles; open-vocabulary auto-labeling

### Takeaway
Feature distillation from a high-resolution (P2) teacher into a nano student adds +3 to +5 mAP@0.5 on tiny drones at zero inference cost (CSCWD: YOLO11n 47.3→50.2 at 640, 48.0→52.9 at 960, 12 FPS on RPi5 NCNN), and a progressive YOLOv7-X→L→Tiny chain adds ~+2.7 AP50 on VisDrone. Grounding-DINO auto-labeling works as a pipeline but the teacher itself is weak on small objects, so it needs tiled labeling and review.

### Cited Findings
- CSCWD (2025): teacher YOLO11m-P2 (20.8M, 134.5 GFLOPs) → student YOLO11n (2.58M, 6.4 GFLOPs); teacher P2 features distilled to student P3. Drone-vs-Bird: baseline YOLO11n 47.25 mAP@0.5 / 16.92 mAP@0.5:0.95 / 56.18 recall → 50.17 / 17.30 / 59.73; beats YOLO11s (46.17, 21.6 GFLOPs) by +4.0. Zero-shot DUT-Anti-UAV 48.29→50.06. Ablation: plain YOLO11m teacher CWD *hurt* (44.08); same-scale P2 teacher 48.08; cross-scale 50.17. Code not released. — [CSCWD, arXiv 2609.30395](https://arxiv.org/abs/2609.30395)
- CSCWD on Raspberry Pi 5 (8 GB, NCNN FP16, batch 1): 640 px — 50.32 mAP@0.5 at 82.3 ms mean / 110 ms P95 / 12.15 FPS / 560 MB (baseline 47.81 at identical latency); 960 px — 52.85 vs 47.99 at 183.5 ms / 5.45 FPS; 1280 px — 48.53 vs 39.17 (accuracy non-monotonic in resolution); teacher 0.94 FPS. 10-min sustained 11.85 FPS at 72.5 °C with no throttling. — [CSCWD](https://arxiv.org/abs/2609.30395)
- Domain-invariant progressive KD (2024, VisDrone AP50): YOLOv7-Tiny baseline 21.95 → 24.68 with YOLOv7-L teacher; progressive X→L→Tiny chain +1.15 over using YOLOv7-X alone. — [arXiv 2408.11407](https://arxiv.org/abs/2408.11407)
- HMKD (JCST 2024): hierarchical matching distillation evaluated on COCO and VisDrone; authors report the student outperforms the teacher on VisDrone. — [HMKD](https://jcst.ict.ac.cn/fileup/1000-9000/PDF/JCST-2024-4-5-4158-798.pdf)
- YOLOv8l→YOLOv8s KD for blurry UAV images, validated on VisDrone. — [Complex & Intelligent Systems 2024](https://link.springer.com/article/10.1007/s40747-024-01676-w)
- Autodistill: Grounding DINO labels images from text prompts, YOLOv8 trains on them in one CLI command. Comparison notes Grounding DINO "struggles with small objects and fine distinctions" (1–2 s/image); GroundedSAM "misses small objects". — [autodistill](https://github.com/autodistill/autodistill); [Autodistill overview](https://labelyourdata.com/articles/data-annotation/autodistill)
- Grounding DINO teacher → YOLO student (MDPI Applied Sciences 2024, multi-sensor): auto-labels alone "does not lead to a degradation in performance"; mixing auto + manual labels improves; limitation: only works where Grounding DINO can detect the object. — [MDPI Appl. Sci. 14(6):2232](https://www.mdpi.com/2076-3417/14/6/2232)
- DART pipeline: Grounding DINO *base* (Swin-B) gives better boxes than tiny for a YOLOv8n student; offline labeling cost is negligible. — [DART, arXiv 2407.09174](https://arxiv.org/abs/2407.09174)
- Per-object co-teaching for noisy VLM pseudo-labels (NMS + 0.3 threshold, YOLOv5 student, version-agnostic). — [arXiv 2511.09955](https://arxiv.org/abs/2511.09955)
- DisDop (2026): distillation with domain priors for open-vocabulary *aerial* detection. — [arXiv 2605.24639](https://arxiv.org/abs/2605.24639)

### Inferences
- Distilling a high-resolution teacher into a nano student is the only technique in this survey that improves small-object accuracy with *zero* runtime cost; its gains (+3–5 mAP@0.5) are of the same order as a 2-model runtime ensemble.
- The CSCWD negative result (bigger plain teacher hurt) means ensemble-distillation should pair teacher features at the resolution where tiny objects live (P2/stride-4), not just use a bigger model.
- Open-vocabulary auto-labeling should be run on tiles/zoomed crops for aerial tiny objects, given Grounding DINO's small-object weakness.

### Gaps
- No paper found distilling an *ensemble* or DINOv2/DINOv3/Co-DETR teacher into a nano student with AP_small reported on VisDrone/AI-TOD.
- No benchmark of Grounding DINO / YOLO-World auto-labels on VisDrone, DOTA or AI-TOD was found.

---

## Q8. Stacking / learned fusion and confidence calibration across heterogeneous models

### Takeaway
Learned meta-model fusion of box coordinates exists (StackBox, 2022, medical domain) and reliability-weighted WBF variants exist (2025), but there is no 2023–2026 evidence on aerial tiny-object benchmarks; the practical recipe is per-model validation-mAP weights (or calibrated scores) fed into WBF.

### Cited Findings
- StackBox: level-0 detectors' predicted coordinates + ground truth train a level-1 meta-learner (sklearn / XGBoost); "independently of the meta learner used, the mAP increased significantly"; claimed first stacking of predicted coordinates across detectors (polyp detection). — [StackBox, Sci. Reports 2022](https://www.nature.com/articles/s41598-022-21574-w)
- Confidence-aware WBF: per-model mAP as fusion weights marginally beat equal weights (0.833). — [arXiv 2509.23697](https://arxiv.org/abs/2509.23697)
- ERDF-Anchor: reliability-guided decision fusion where auxiliary single-modality detectors reweight confidences and filter unsupported anchors (DroneVehicle). — [Electronics Letters 2026](https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/ell2.70683)
- MMLF (Oct 2024): multi-modal multi-class late fusion with uncertainty estimation; fusion "reduced uncertainty ... enhancing confidence and reliability". — [arXiv 2410.08739](https://arxiv.org/abs/2410.08739)
- Calibration metric reference for detectors: "Beyond Classification: Definition and Density-based Estimation of Calibration in Object Detection" (WACV 2024). — [arXiv 2312.06645](https://arxiv.org/abs/2312.06645)
- Negative result on learned stackers (AI-image detection, not boxes): a stacker fitted on a foreign corpus failed; max-rule fusion was 22.9 points below learned fusion — the meta-model's training distribution must match deployment. — [arXiv 2609.31749](https://arxiv.org/abs/2609.31749)
- Model-level mixture-of-experts for domain-specialised detection (2026) is the nearest "learned routing" alternative. — [arXiv 2604.18256](https://arxiv.org/pdf/2604.18256)

### Inferences
- Heterogeneous detectors (YOLO objectness × class vs DETR sigmoid logits) have different score distributions; SIA-DT's Anti-UAV recipe (YOLOX objectness threshold 0.5 but 0.05 for R-CNNs before fusion) is the pragmatic calibration most teams actually use.
- A stacked meta-model is cheap at runtime (tabular features) but needs held-out data from the deployment domain; it is unproven for sub-20-px objects.

### Gaps
- No 2023–2026 paper found that trains a learned box-fusion meta-model and reports gains on VisDrone/AI-TOD/DOTA.
- No study found that applies temperature scaling / isotonic calibration to heterogeneous detectors before WBF and quantifies the mAP effect.

---

## Q9. Competition write-ups and practical edge budget: what winners ensembled, and measured FPS on Orin Nano / RPi5 / RK3588

### Takeaway
Challenge winners (VisDrone-DET, xView3, FAIR1M/DOTA, Anti-UAV, Drone-vs-Bird) all stack multi-scale/tiled inference + multi-model (or multi-fold) ensembles + WBF/NMS + flip TTA, each worth +1 to +3 points and together ~5× or more compute. On edge, the only measured multi-pass numbers found are: SAHI + YOLOv8s INT8 TensorRT on Jetson Orin Nano 8 GB ≈ 44 ms/image (~22 FPS) and ~15 FPS for 1080p video with ByteTrack; 12-tile YOLOv8n on RPi5 + Hailo-8L ≈ 8 FPS; and a distilled YOLO11n on bare RPi5 at 12 FPS (640) / 5.5 FPS (960).

### Cited Findings — competition write-ups
- VisDrone-DET2021 winner DBNet 39.43 mAP (Cascade R-CNN + BiFPN, ShiftScaleRotate/multi-scale/CenterCrop aug, multi-scale testing with fused outputs); 2nd ViT-YOLO 39.41 (YOLOv4+v5+ViT-YOLO, TTA + WBF); TPH-YOLOv5 39.18 (5-model ensemble, multi-scale test); VistrongerDet used TTA at 3200×2100 without cropping. — [VisDrone-DET2021 results](https://openaccess.thecvf.com/content/ICCV2021W/VisDrone/papers/Cao_VisDrone-DET2021_The_Vision_Meets_Drone_Object_Detection_Challenge_Results_ICCVW_2021_paper.pdf); [ViT-YOLO](https://openaccess.thecvf.com/content/ICCV2021W/VisDrone/papers/Zhang_ViT-YOLOTransformer-Based_YOLO_for_Object_Detection_ICCVW_2021_paper.pdf); [TPH-YOLOv5](https://arxiv.org/abs/2108.11539); [VistrongerDet](https://openaccess.thecvf.com/content/ICCV2021W/VisDrone/papers/Wan_VistrongerDet_Stronger_Visual_Information_for_Object_Detection_in_VisDrone_Images_ICCVW_2021_paper.pdf)
- VisDrone 2023 (ICCV) and 2024 (CCDM) editions ran detection + zero-shot tracks on the same VisDrone2019-DET data (6,471 / 548 / 3,190 images); no published results paper found, and the leaderboard page states results are provisional. — [VisDrone 2023](http://aiskyeye.com/challenge-2023/); [VisDrone 2024](https://aiskyeye.com/challenge-2024/); [leaderboard](https://aiskyeye.com/leaderboard/)
- xView3 (SAR dark vessels) 1st place: 12-model deep ensemble (EfficientNet-B4/B5/V2S × 4 folds, custom CircleNet), flip-LR TTA only, "up to 12 minutes per scene"; score 0.617 holdout, 3× the government baseline. — [BloodAxe/xView3-The-First-Place-Solution](https://github.com/BloodAxe/xView3-The-First-Place-Solution); [GFW press release](https://globalfishingwatch.org/press-release/xview3-winners-announced/)
- FAIR1M (2021 Gaofen fine-grained OBB) 3rd/220: Swin backbone, ReDet + Oriented R-CNN + ROI-Transformer ensembled with WBF modified for OBB, multi-scale train/test at 1.0 and 1.5, 1024 crops stride 800, score threshold 0.005. — [G-Naughty/Fine-grained-OBB-Detection](https://github.com/G-Naughty/Fine-grained-OBB-Detection)
- DOTA-v1.5 DOAI-2019: "most of these results were achieved using an ensemble of detection models", one single-model entry at 74.9 OBB / 77.9 HBB; multi-scale + rotation used in train and test; standard MS protocol rescales to 0.5/1.0/1.5 and crops 1024 with 500-px overlap. — [DOTA benchmark, arXiv 2102.12219](https://arxiv.org/abs/2102.12219); [Strip R-CNN](https://arxiv.org/pdf/2501.03775)
- Anti-UAV 2023 component contributions (see Q6): SIA-DT ensemble +1.9 over best single detector; Z-Y motion branch +7.7; USTC global re-detection +8.4; FudanDML temporal scales +9 to +12 vs spatial TTA +1.8. — [arXiv 2305.07290](https://arxiv.org/abs/2305.07290)
- Drone-vs-Bird 2025 winner: YOLO11m, 4 tiles + full frame + NMS (+18.7 mAP@0.5 over full-frame), copy-paste augmentation, ±6-frame temporal interpolation; 16 algorithms competed. — [arXiv 2504.19347](https://arxiv.org/abs/2504.19347); [IJCNN 2025 challenge overview](https://publica.fraunhofer.de/entities/publication/267aa1ec-a62d-4afa-99ad-cc369f57642b)
- Drone-vs-Bird 2023 winner OBSS AI: multi-dataset training + synthetic copy-paste; organisers noted other entries "struggle" on smaller drones. — [ICASSP 2023 review](https://ieeexplore.ieee.org/document/10475518)

### Cited Findings — measured edge numbers
- Jetson Orin Nano 8 GB, YOLOv8s INT8 TensorRT, batch 8 slices of 640×640, SAHI C++: 43–46 ms per image after warm-up (~22 FPS implied); 1080p video with SAHI + ByteTrack ramps to 14–15 FPS. No accuracy comparison provided; slice count per frame not stated. — [HouYanSong/tensorrtx-yolov8-sahi](https://github.com/HouYanSong/tensorrtx-yolov8-sahi)
- Orin Nano full-frame baselines (640, batch 1): YOLOv8n TensorRT FP16 225 FPS / INT8 286 FPS (MAXN_SUPER), 204 FPS INT8 at 15 W; another author at 15 W: FP32 28, FP16 47, INT8 185 FPS; PyTorch FP32 ~20–26 FPS. YOLOv8s FP16 ~38–40 FPS (arXiv). — [tildalice](https://tildalice.io/yolov8-int8-quantization-jetson/); [hokwangchoi](https://hokwangchoi.com/blog/vision-benchmarks/); [arXiv 2502.15737](https://arxiv.org/pdf/2502.15737)
- Orin NX: batching 1→4 raised YOLOv8n throughput 23.67→32.04 FPS (+35%) — argument for batching tiles. — [Computers 15(2):74](https://www.mdpi.com/2073-431X/15/2/74)
- Raspberry Pi 5 + Hailo-8L, 4608×2592 IMX708, YOLOv8n: raw NPU 106 FPS (batch 1) / 174 FPS (batch 8); TAPPAS simple tiling with 12 tiles reached only 8 FPS (≈106/12 ≈ 13 FPS theoretical); multiscale tiling would be slower; the Pi 5 CPU pre/post-processing, not the NPU, is the bottleneck. Hailo ships `hailo-tiling` and `hailo-tiling --multi-scale` examples. — [Hailo community tiling thread](https://community.hailo.ai/t/how-to-implement-tiling-without-downsampling/17407); [DataRoot Labs Hailo guide](https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines)
- Raspberry Pi 5 bare CPU (NCNN FP16): YOLO11n 12.15 FPS at 640, 5.45 FPS at 960; distilled student +2.5 mAP@0.5 (640) and +4.9 (960) at identical latency. — [CSCWD, arXiv 2609.30395](https://arxiv.org/abs/2609.30395)
- RK3588 NPU baselines: YOLOv8n 53.1 FPS, v8s 28.5, v8m 12.1 (Qengineering); YOLOv8n@480 330 FPS / YOLO11n@480 279 FPS with 3-core pipelining; NPU is DDR-bandwidth sensitive (CPU memory-heavy side work dropped FPS 84→62) — relevant because tile slicing/merging on CPU competes for bandwidth. — [Qengineering/YoloV8-NPU](https://github.com/Qengineering/YoloV8-NPU); [rknn_model_zoo issue #454](https://github.com/airockchip/rknn_model_zoo/issues/454)
- Jetson Xavier NX: GL-YOMO global/local YOLOv5-based cascade + motion fallback at 21.6 FPS (TensorRT, 640). — [arXiv 2411.02582](https://arxiv.org/abs/2411.02582)
- Jetson Orin NX: 12.6M-param single-stage UAV detector at 1024 px, 36.65 ms / 27.3 FPS TensorRT, 50.55 mAP50 VisDrone. — [SIVP 2026](https://link.springer.com/article/10.1007/s11760-026-05799-0)
- Alternative to tiling: YOLOv8s-P2 at 1024 px ran ~50 FPS FP32 / ~98 FPS FP16 on AGX Orin 64 GB (NVIDIA forum). — [NVIDIA forum](https://forums.developer.nvidia.com/t/yolov5s-model-performance-testing-benchmark/329949)

### Inferences (accuracy-per-watt ranking for an Orin Nano / RPi5 / RK3588 budget)
1. Free: slice-aided fine-tuning + P2/high-res-teacher distillation into the nano student (+3–14 AP50 depending on baseline) and Soft/DIoU/cluster-NMS instead of hard NMS (+2–6 mAP@0.5 in dense scenes).
2. ~1.5–2×: one nano full-frame pass + CPU motion/frame-difference branch with tracker (ByteTrack/OC-SORT with expanded-box + centre-distance costs) — Anti-UAV ablations show this is worth more than a second CNN.
3. ~2×: global→local ROI cascade (GL-YOMO) — recall 0.56→0.83 on sub-150-px targets at 21.6 FPS on Xavier NX; expected similar or better on Orin Nano.
4. ~4–7×: 4–6-tile ASAHI-style slicing + full-frame pass, tiles batched through TensorRT/NPU — ~15–22 FPS on Orin Nano with YOLOv8s INT8, ~8 FPS on RPi5+Hailo-8L with 12 tiles; +5–7 AP50 / +4–5 AP50_small.
5. ≥2× on top: heterogeneous 2-model WBF ensemble (+1–3 mAP) or flip TTA (+0.5–1) — lowest return per watt; use only when the budget is already met.

### Gaps
- No source measured AP_small *and* FPS together for SAHI/ensembles on Orin Nano or RPi5; the tensorrtx repo gives latency only, CSCWD gives accuracy + FPS but for a single model.
- No published VisDrone-DET 2023/2024 results paper; winner compositions unknown.
- No 2-model (e.g. YOLO + RT-DETR) ensemble measured on any of the three edge platforms.
- No RK3588-specific SAHI/tiling FPS measurements were found (only single-model NPU baselines).
