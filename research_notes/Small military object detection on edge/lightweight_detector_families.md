# Lightweight Open-Source Object Detector Families for Small-Object Detection on Low-End Edge Hardware (2024-2026)

Notes compiled 2026-11-10. Facts are appended incrementally with source URLs. "Vendor-claimed" = numbers from the model authors' own README/docs; "independent" = third-party measurement.

## KQ1: Current best lightweight detectors — per-family spec table (params / FLOPs / COCO mAP / AP_small / license / repo / release)

### Takeaway
(filled at end)

### Cited Findings

## KQ2: Best AP_small relative to compute cost

### Takeaway

### Cited Findings

## KQ3: Measured FPS/latency on edge devices (Jetson Orin Nano / Nano, RPi 5 (CPU, Hailo-8L AI HAT+), Coral TPU, RK3588, Hailo-8) with precision

### Takeaway

### Cited Findings

## KQ4: INT8 quantization accuracy loss per family

### Takeaway

### Cited Findings

## KQ5: P2 (stride-4) head / 1280+ input support

### Takeaway

### Cited Findings

## KQ6: Licensing constraints

### Takeaway

### Cited Findings

## KQ7: Open-vocabulary (YOLO-World / YOLOE) edge feasibility

### Takeaway

### Cited Findings

## Inferences (cross-cutting)

## Gaps

<!-- BATCH 1: Ultralytics YOLO26/YOLO11, D-FINE, DEIMv2, RF-DETR (all vendor-claimed from official docs/READMEs) -->

#### Ultralytics YOLO26 (AGPL-3.0 / Enterprise)
- Docs page created 2025-09-25 (YOLO Vision 2025 announcement); Ultralytics platform card says "released January 2026"; paper cited as arXiv 2606.03748 (ID as shown on docs page; verify). — [Ultralytics YOLO26 docs](https://docs.ultralytics.com/models/yolo26/)
- Dual-head design: default one-to-many head outputs (N, nc+4, 8400) and STILL requires NMS; optional one-to-one end-to-end head (`nms=False`) outputs (N,300,6), max 300 dets, no NMS. e2e head costs 0.6-0.8 mAP. DFL removed to simplify export. — [Ultralytics YOLO26 docs](https://docs.ultralytics.com/models/yolo26/)
- COCO 640 (fused, NMS-free head timing): YOLO26n 40.9 mAP (40.1 e2e), 2.4M params, 5.5 GFLOPs, CPU ONNX 38.9 ms, T4 TRT10 1.7 ms; YOLO26s 48.6 (47.8 e2e), 9.5M, 20.9 GFLOPs, CPU 87.2 ms, T4 2.5 ms; YOLO26m 53.1, 20.4M, 68.4 GFLOPs, CPU 220 ms, T4 4.7 ms. — [Ultralytics YOLO26 docs](https://docs.ultralytics.com/models/yolo26/)
- CPU speedup claim: "up to 43% faster CPU ONNX inference for YOLO26n vs YOLO11n" — measured on Intel Xeon @2.0GHz (server CPU, NOT an edge ARM measurement). — [Ultralytics YOLO26 docs](https://docs.ultralytics.com/models/yolo26/)
- Export: TensorRT, ONNX, CoreML, LiteRT (TFLite), OpenVINO; `nms=True` can embed NMS in export. License: AGPL-3.0 + Enterprise. — [Ultralytics YOLO26 docs](https://docs.ultralytics.com/models/yolo26/)

#### Ultralytics YOLO11 (AGPL-3.0 / Enterprise), released 2024-09-27
- COCO 640: YOLO11n 39.5 mAP, 2.6M, 6.5 GFLOPs, CPU ONNX 56.1 ms, T4 TRT10 1.5 ms; YOLO11s 47.0, 9.4M, 21.6 GFLOPs, CPU 90.0 ms, T4 2.5 ms; YOLO11m 51.5, 20.1M, 68.1 GFLOPs, 183.2 ms CPU, 4.7 ms T4. No formal paper. — [Ultralytics YOLO11 docs](https://docs.ultralytics.com/models/yolo11/)

#### D-FINE (Apache-2.0), arXiv 2410.13842, ICLR 2025 Spotlight, released 2024-10-18 (N added 2024-11-07)
- COCO val: D-FINE-N 42.8 AP, 4M params, 7 GFLOPs, 2.12 ms T4 (FP16 TRT10.4 bs1, ~472 FPS); D-FINE-S 48.5 AP, 10M, 25 GFLOPs, 3.49 ms; D-FINE-M 52.3, 19M, 57 GFLOPs, 5.62 ms; L 54.0, 31M, 91 GFLOPs, 8.07 ms; X 55.8, 62M, 202 GFLOPs, 12.89 ms. — [D-FINE GitHub](https://github.com/Peterande/D-FINE)
- Objects365->COCO fine-tuned: S 50.7, M 55.1, L 57.3, X 59.3 (same cost). Obj365 checkpoints flagged as possibly subject to Objects365 dataset terms (commercial caution). — [D-FINE GitHub](https://github.com/Peterande/D-FINE)
- AP_small NOT listed in README. Export: ONNX (export_onnx.py) -> TensorRT via trtexec --fp16; onnxruntime/TRT/PyTorch inference scripts. Built on RT-DETR codebase. — [D-FINE GitHub](https://github.com/Peterande/D-FINE)

#### DEIMv2 (CUSTOM "DEIMv2 License" — NOT Apache; commercial use requires contacting authors), arXiv 2509.20787, released 2025-09-26
- COCO: Atto 23.8 AP, 0.5M, 0.8 GFLOPs, 1.10 ms; Femto 31.0, 1.0M, 1.7 GFLOPs, 1.45 ms; Pico 38.5, 1.5M, 5.2 GFLOPs, 2.13 ms; N 43.0, 3.6M, 6.8 GFLOPs, 2.32 ms (all HGNetv2 backbone); S 50.9, 9.7M, 49.5 GFLOPs, 5.78 ms (ViT-Tiny distilled from DINOv3-S); M 53.0, 18.1M, 84.1 GFLOPs, 8.80 ms; L 56.0, 32.2M, 144.5 GFLOPs (DINOv3-S); X 57.8, 50.3M, 200 GFLOPs. Latency device/precision NOT stated in table (repo recommends TRT>=10.6 FP16). — [DEIMv2 GitHub](https://github.com/Intellindust-AI-Lab/DEIMv2)
- GFLOPs revised 2026-10-22 (earlier tool omitted attention FLOPs — older numbers in papers/blogs are understated for S/M/L/X). AP_small not listed. — [DEIMv2 GitHub](https://github.com/Intellindust-AI-Lab/DEIMv2)
- Export: ONNX -> TensorRT (trtexec --fp16; TRT 10.4 FP16 has known wrong-output bug); OpenVINO IR with INT8 via Intel Geti integration (S/M/L). — [DEIMv2 GitHub](https://github.com/Intellindust-AI-Lab/DEIMv2)
- LICENSE CAUTION: unlike D-FINE/DEIM (Apache-2.0), DEIMv2 ships a custom license requiring contact for commercial use. — [DEIMv2 GitHub](https://github.com/Intellindust-AI-Lab/DEIMv2)

#### RF-DETR (Apache-2.0), arXiv 2511.09554, ICLR 2026, Roboflow
- Nano: 48.4 AP50:95 COCO, 30.5M params (fused), 384x384, 2.3 ms T4 TRT FP16 bs1; Small: 53.0 AP, 32.1M, 512x512, 3.5 ms; Medium 54.7, 33.7M, 576, 4.4 ms; Large 56.5, 33.9M, 704, 6.8 ms. Backbone DINOv2 ViT. GFLOPs not reported. — [RF-DETR GitHub](https://github.com/roboflow/rf-detr)
- NOTE: even "Nano" is ~30M params (DINOv2 backbone) — far heavier in weights than YOLO26n (2.4M); latency competitive on GPU because of low input res (384), but memory footprint on edge is large. Smaller Atto/Femto/Pico variants use PE-Core-T backbone under a different "PML 1.0" license (rfdetr[plus]) — not Apache. No Jetson/edge numbers in README. — [RF-DETR GitHub](https://github.com/roboflow/rf-detr)

<!-- BATCH 2: Ultralytics device guides (Jetson, RPi5, Coral) + DEIM v1 -->

#### Ultralytics Jetson guide benchmarks (vendor-claimed, Ultralytics 8.4.33, imgsz 640, YOLO26n, excludes pre/post-processing; power mode not stated)
- Jetson Orin Nano Super (JP6.1): YOLO26n PyTorch 15.60 ms / 0.479 mAP; ONNX 15.76 ms; TensorRT FP32 7.53 ms (0.477); TensorRT FP16 4.57 ms (0.480, ~219 FPS); TensorRT INT8 3.80 ms (0.449 -> ~3 pts mAP drop from INT8 PTQ); NCNN 47.5 ms; TF Lite 286 ms. — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- Jetson Orin NX 16GB (Seeed J4012): YOLO26n TRT FP16 4.13 ms (0.479); TRT INT8 3.49 ms (0.449); NCNN 34.31 ms. — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- NO Jetson Nano (original, Maxwell) benchmark table on the page; Jetson Nano 4GB only listed as JP4.6.1-compatible device. — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- INT8 caveat: TensorRT 10.3.0 (JetPack 6) has a known issue preventing INT8 engines with NMS-free or embedded-NMS outputs; TRT >= 10.7 recommended. — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- mAP in these tables is on COCO128-style small eval (0.479 for YOLO26n vs 40.9 on full COCO val) — NOT comparable to published COCO mAP; use only for relative format-to-format drops. — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)

#### Ultralytics Raspberry Pi 5 benchmarks (vendor-claimed, CPU only, FP32, imgsz 640, excludes pre/post)
- YOLO26 ONNX on Pi 5 (Ultralytics 8.4.14): YOLO26n 128.42 ms (7.79 FPS, 40.1 mAP e2e); YOLO26s 352.84 ms (2.8 FPS, 47.8); YOLO26m 993.78 ms. YOLO11n ONNX = 6.79 FPS (~147 ms). — [Ultralytics RPi guide](https://docs.ultralytics.com/guides/raspberry-pi/)
- YOLO26n on Pi 5 by format (8.4.108): NCNN 67.03 ms (~14.9 FPS, best); MNN 91.87 ms; OpenVINO 104.55 ms; LiteRT 123.3 ms; ONNX 125.99 ms; PyTorch 299 ms. YOLO26s NCNN ~173 ms (staff comment). — [Ultralytics RPi guide](https://docs.ultralytics.com/guides/raspberry-pi/)
- No Raspberry Pi 4 table in current guide; no AI HAT+/Hailo section (maintainer suggests YOLO26n @ imgsz 320 on CPU first). — [Ultralytics RPi guide](https://docs.ultralytics.com/guides/raspberry-pi/)

#### Ultralytics Coral Edge TPU guide (vendor-claimed, USB Coral on Raspberry Pi, YOLOv8, INT8 full-integer)
- Pi 4B + USB Coral: YOLOv8n @320 32.2 ms std / 26.7 ms high-freq (~31-37 FPS); YOLOv8s @320 47.1/39.8 ms; YOLOv8n @512 73.5/60.7 ms; YOLOv8s @512 149.6/125.3 ms. Pi 5 ~22-30% faster. No mAP reported. — [Ultralytics Coral guide](https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/)
- Limitations: at 640 most ops fall back to CPU (author: need imgsz <=512); models > "s" exceed 8 MB on-chip cache; SiLU unsupported (ReLU swap helps); TRANSPOSE/SOFTMAX/head ops fall to CPU; YOLO11 has ~275 CPU-fallback ops vs 22 for YOLOv8; YOLOv10+ had edgetpu_compiler CONV_2D v6 opcode failures (May 2025) though YOLO11n@320 exported with TF 2.18 (June 2025). Maintainer: "significant accuracy loss is sadly expected with the coral TPU." — [Ultralytics Coral guide](https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/)
- Anecdotal user: YOLO11n ~2.5 FPS Pi CPU -> ~10 FPS on Coral, with clear accuracy drop. — [Ultralytics Coral guide comments](https://docs.ultralytics.com/guides/coral-edge-tpu-on-raspberry-pi/)

#### DEIM v1 (Apache-2.0), arXiv 2412.04234, CVPR 2025, released 2024-12-03 (N added 2025-03-05)
- DEIM-D-FINE: N 43.0 AP (4M, 7 GFLOPs, 2.12 ms); S 49.0 (10M, 25 GFLOPs, 3.49 ms); M 52.7 (19M, 57); L 54.7 (31M, 91); X 56.5 (62M, 202). DEIM-RT-DETRv2-S (r18vd) 49.0 AP, 20M, 60 GFLOPs, 4.59 ms. Latency device not stated (same T4 FP16 numbers as D-FINE README). Export ONNX -> TRT. — [DEIM GitHub](https://github.com/ShihuaHuang95/DEIM)

<!-- BATCH 3: RKNN/RK3588, YOLOv10, YOLOv13, RT-DETR/v2, Hailo-8L model zoo -->

#### Ultralytics RKNN integration — RK3588 (Radxa Rock 5B, ultralytics 8.4.60, imgsz 640 implied, COCO128 eval; vendor-claimed)
- YOLO26n rknn FP16 58.5 ms (0.477 mAP, 7.2 MB); INT8 41.2 ms (0.463, 4.1 MB) ~1.4 pt drop; YOLO26s FP16 93.8 ms (0.569) / INT8 61.9 ms (0.554); YOLO26m FP16 226 ms / INT8 122 ms. — [Ultralytics RKNN docs](https://docs.ultralytics.com/integrations/rockchip-rknn/)
- Caveats: INT8 accuracy "validated with rknn-toolkit2 simulator but not yet on Rockchip hardware"; INT8 uses RKNN `auto_hybrid` (high-error layers kept FP16) on FP16-capable chips; box decode runs on host CPU in float via tail.onnx. A commenter reports ~11 ms/img for native RKNN using all 3 NPU cores of RK3588; maintainer calls published figures "conservative end-to-end". Export x86 Linux only. Supported: rk3588/3576/3566/3568/3562/rk2118/rv1126b (FP16+INT8); rv1103/1106 INT8-only. — [Ultralytics RKNN docs](https://docs.ultralytics.com/integrations/rockchip-rknn/)

#### YOLOv10 (AGPL-3.0), arXiv 2405.14458, NeurIPS 2024, released ~2024-05-25, THU-MIG
- COCO 640: N 38.5 AP, 2.3M, 6.7 GFLOPs, 1.84 ms; S 46.3, 7.2M, 21.6 GFLOPs, 2.49 ms; M 51.1, 15.4M, 59.1 GFLOPs, 4.74 ms; B 52.5, 19.1M, 92 GFLOPs. Latency: T4 TensorRT FP16 (paper); NMS-free via consistent dual assignments. Export ONNX (opset13) + TensorRT. Claims 1.8x faster than RT-DETR-R18 at similar AP, 2.8x fewer params/FLOPs. — [YOLOv10 GitHub](https://github.com/THU-MIG/yolov10)

#### YOLOv13 (AGPL-3.0, built on Ultralytics), arXiv 2506.17733, released 2025-06-21/22, iMoonLab
- COCO: N 41.6 AP, 2.5M, 6.4 GFLOPs, 1.97 ms; S 48.0, 9.0M, 20.8 GFLOPs, 2.98 ms; L 53.4, 27.6M, 88.4 GFLOPs, 8.63 ms; X 54.8, 64M, 199 GFLOPs, 14.67 ms. Device not stated in README (paper: T4 TRT FP16). Uses hypergraph HyperACE + FullPAD; supports Flash Attention — attention ops are LESS edge-NPU-friendly than pure-conv. Latency is higher than YOLO11 at every scale (N 1.97 vs 1.53 ms). Third-party RKNN and ncnn Android ports exist. — [YOLOv13 GitHub](https://github.com/iMoonLab/yolov13)
- Comparison in same table: YOLO11-N 38.6 (1.53 ms), YOLOv12-N 40.1 (1.83 ms), YOLOv13-N 41.6 (1.97 ms); S: 45.8 / 47.1 / 48.0. — [YOLOv13 GitHub](https://github.com/iMoonLab/yolov13)

#### RT-DETR / RT-DETRv2 (Apache-2.0), arXiv 2304.08069 (CVPR 2024) / 2407.17140 (v2 released 2024-07-24), lyuwenyu
- RT-DETR-R18: 46.5 AP, 20M, 60 GFLOPs, 217 FPS T4 TRT FP16; R34 48.9, 31M, 92 GFLOPs, 161 FPS; R50 53.1, 42M, 136 GFLOPs, 108 FPS. RT-DETRv2-S (r18) 48.1 AP (same cost, 217 FPS); v2-M* 49.9; v2-L 53.4. Obj365->COCO R18 49.2. — [RT-DETR GitHub](https://github.com/lyuwenyu/RT-DETR)
- Smallest RT-DETR is 20M params / 60 GFLOPs — ~8x the params of YOLO26n; no sub-10M variant. RT-DETRv4 announced 2025-11-18 (separate repo). Deployment: ONNX Runtime, TensorRT, OpenVINO. — [RT-DETR GitHub](https://github.com/lyuwenyu/RT-DETR)

#### Hailo-8L model zoo (vendor-claimed; DFC 2.20, Intel i5-9400 host PCIe Gen3 x4 — NOT a Raspberry Pi host; "Hardware mAP" = compiled/quantized HEF, Hailo quantizes to INT8/INT4 per layer, bit-width not stated on page)
- yolov8n 640: float 37.0 -> HW 36.4 mAP (-0.6); 201 FPS b1 / 437 b8. yolov8s: 44.6 -> 43.9; 110/208 FPS. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- yolov11n 640: 39.0 -> 37.5 (-1.5); 157/370 FPS. yolov11s: 46.3 -> 45.1 (-1.2); 91.9/190 FPS. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- yolov10n 640: 38.5 -> 36.6 (-1.9); 150/359 FPS. yolov10s 45.9 -> 44.9; 87.2/187. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- yolo26n 640: 40.0 -> 38.4 (-1.6); 111/255 FPS (slower than yolov8n on Hailo-8L despite fewer FLOPs). yolo26s 47.5 -> 45.3 (-2.2); 66.5/147 FPS. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- yolov12n 640: 40.5 -> 39.3; only 38.4/86.3 FPS (attention ops ~4x slower than yolov11n on Hailo-8L). — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- nanodet_repvgg 416: 29.3 -> 28.6; 620 FPS. yolox_tiny 416: 32.6 -> 31.4; 214/509 FPS. yolox_s_leaky 640: 38.1 -> 37.3; 109/199. efficientdet_lite0 320: 27.3 -> 26.5; 92/238 FPS. efficientdet_lite2 448: 35.9 -> 34.7; 39.8/88.4. yolov6n 34.3 -> 32.4; 356 FPS. damoyolo_tinynasL20_T 42.8 -> 42.2; 124/268. ssd_mobilenet_v2 300: 24.2 -> 23.0; 130/293. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- No RT-DETR / D-FINE / DEIM / RF-DETR entries found in the Hailo-8L detection table (transformer decoders not in public zoo). — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)

<!-- BATCH 4: AP_small from D-FINE and DEIMv2 papers; YOLOv12; NanoDet-Plus; YOLOE -->

#### AP_small (COCO val2017) — from D-FINE paper Table 1/7 (T4 TRT FP16 end-to-end latency)
- S-scale: YOLOv8-S 25.7 AP_S (44.9 AP, 11M, 29 GFLOPs); YOLOv10-S 26.8 (46.3 AP, 7M, 22 GFLOPs, 2.65 ms); YOLO11-S 28.7 (46.6 AP, 9M, 22 GFLOPs; 29.0 with tuned NMS); RT-DETR-R18 28.4 (46.5 AP, 20M, 61 GFLOPs, 4.63 ms); D-FINE-S 29.1 (48.5 AP, 10.2M, 25.2 GFLOPs, 3.49 ms); D-FINE-S Obj365-pretrained 32.7 AP_S (50.7 AP); RT-DETR-R18 Obj365 33.2 AP_S (49.2 AP); LW-DETR-S Obj365 26.8 AP_S (48.0 AP, 15M, 17 GFLOPs, 3.02 ms). — [D-FINE paper arXiv 2410.13842](https://arxiv.org/html/2410.13842)
- M-scale: YOLOv8-M 32.0; YOLOv10-M 33.8 (51.1 AP, 15M, 59 GFLOPs, 4.97 ms); YOLO11-M 33.0; D-FINE-M 33.2 (52.3 AP, 19.2M, 56.6 GFLOPs); D-FINE-M Obj365 37.9 AP_S (55.1 AP); RT-DETR-R34 30.6. — [D-FINE paper arXiv 2410.13842](https://arxiv.org/html/2410.13842)
- L-scale: D-FINE-L 36.5 (54.0 AP, 31M, 91 GFLOPs, 8.07 ms); D-FINE-L Obj365 40.0; YOLO11-L 35.6; YOLOv10-L 35.8; YOLOv9-C 36.2; YOLOv9-E 40.2 (57M, 189 GFLOPs, 20.5 ms — highest non-pretrained AP_S); RT-DETRv2-L 36.1; LW-DETR-L Obj365 37.2. — [D-FINE paper arXiv 2410.13842](https://arxiv.org/html/2410.13842)
- CAUTION: RT-DETRv2-S/M AP_S values printed as 36.1/35.8 in both papers appear to be copy errors (identical to v2-L/X sub-metrics); YOLOv9-S/M rows duplicate YOLOv8-S/M. Do not cite RT-DETRv2-S AP_S=36.1. — [D-FINE paper](https://arxiv.org/html/2410.13842); [DEIMv2 paper](https://arxiv.org/html/2509.20787)

#### AP_small — from DEIMv2 paper Table 3 (latency device NOT specified; authors say latency "not optimized")
- DEIM-S 30.4 AP_S (49.0 AP, 10M, 25 GFLOPs, 3.66 ms); DEIMv2-S 31.4 AP_S (50.9 AP, 9.7M, 50 GFLOPs, 5.78 ms); DEIM-M 35.3 AP_S (52.7 AP, 19M, 57 GFLOPs); DEIMv2-M 34.2 (53.0 AP, 18.1M, 84 GFLOPs, 8.80 ms); DEIM-L 36.9; DEIMv2-L 37.5 (56.0 AP, 145 GFLOPs); DEIM-X 38.8; DEIMv2-X 39.2 (57.8 AP). Authors note DEIMv2 gains over DEIM come from medium/large objects; small-object AP "remains largely unchanged". — [DEIMv2 paper arXiv 2509.20787](https://arxiv.org/html/2509.20787)
- Ultra-light table (no AP_S): NanoDet-M 416 1.0M/0.7G 23.5 AP; DEIMv2-Atto 320 0.5M/0.8G 23.8; YOLOX-Nano 416 0.9M/1.1G 25.8; PicoDet-S 416 1.0M/1.2G 30.7; PicoDet-ShuffleNetV2-1x 416 1.2M/1.5G 30.0; DEIMv2-Femto 416 1.0M/1.7G 31.0; YOLOv10-N 640 2.3M/6.7G 38.5; YOLOv8-N 3.2M/8.7G 37.4; DEIMv2-Pico 640 1.5M/5.2G 38.5; YOLOv12-N 2.6M/6.5G 40.6; DEIM-Nano 3.6M/6.9G 43.0; D-FINE-Nano 3.8M/7.2G 42.8; DEIMv2-Nano 3.6M/6.9G 43.0. — [DEIMv2 paper arXiv 2509.20787](https://arxiv.org/html/2509.20787)
- Nano-scale AP_S for YOLO26n/YOLO11n/YOLOv10n/D-FINE-N/DEIM-N is NOT reported in either paper (see Gaps). — [DEIMv2 paper](https://arxiv.org/html/2509.20787)

#### YOLOv12 (AGPL-3.0), arXiv 2502.12524, NeurIPS 2025, released 2025-02-19 (turbo 2025-03-09), sunsmarterjie
- Turbo (default) 640, T4 TRT10: YOLO12n 40.4 mAP, 1.60 ms, 2.5M, 6.0 GFLOPs; YOLO12s 47.6, 2.42 ms, 9.1M, 19.4 GFLOPs; YOLO12m 52.5, 4.27 ms, 19.6M, 59.8 GFLOPs. v1.0: n 40.6/2.6M/6.5G; s 48.0/9.3M/21.4G. Attention-centric (area attention); requires flash-attn for efficient training; authors say the Ultralytics port "is inefficient, requires more memory, and has unstable training". — [YOLOv12 GitHub](https://github.com/sunsmarterjie/yolov12)
- Edge note: Hailo-8L runs yolov12n at only 38.4 FPS vs 157 for yolov11n (see Hailo section) — attention is poorly suited to fixed-function NPUs. — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)

#### NanoDet-Plus (Apache-2.0), RangiLyu — largely dormant since ~2023-01 (PyTorch <2.0 requirement)
- NanoDet-Plus-m 320: 1.17M, 0.9 GFLOPs, 27.0 mAP, 11.97 ms on Kirin 980 ARM CPU (ncnn), 1.2 MB INT8; 416: 1.52 GFLOPs, 30.4 mAP, 19.77 ms; Plus-m-1.5x 416: 2.44M, 2.97 GFLOPs, 34.1 mAP, 25.49 ms ARM. Deploy: ONNX, ncnn (Android), MNN, OpenVINO; no TensorRT. — [NanoDet GitHub](https://github.com/RangiLyu/nanodet)

#### YOLOE (AGPL-3.0), arXiv 2503.07465, ICCV 2025, THU-MIG — open-vocabulary
- YOLOE-v8-S: 12M (text prompt), 305.8 FPS T4 TRT, 64.3 FPS iPhone 12 CoreML (~15.6 ms), LVIS AP 27.9; YOLOE-11-S: 10M, 301 FPS T4, 73.3 FPS iPhone 12 (~13.6 ms), AP 27.5. Prompt-free mode (built-in vocab) costs ~5-8 AP: v8-S 21.0 AP at 95.8 FPS (PyTorch T4). No N variant. Claims 1.4x faster and +3.5 AP vs YOLO-Worldv2-S at 3x less training. After re-parameterization to a fixed class set it matches YOLOv8/YOLO11 with "zero inference overhead". — [YOLOE GitHub](https://github.com/THU-MIG/yoloe)

<!-- BATCH 5: P2 head config, independent Jetson Orin Nano transformer benchmarks, INT8 quantization of DETRs, Pi5+Hailo-8L independent FPS, YOLO-NAS/YOLOX/PicoDet licensing -->

#### P2 (stride-4) head support
- Ultralytics ships `yolov8-p2.yaml` ("P2/4 - P5/32 outputs"): head adds layer 18 "P2/4-xsmall" (C2f 128ch, concat backbone layer 2), Detect inputs [18, 21, 24, 27] = (P2,P3,P4,P5); scales n/s/m/l/x defined; no params/GFLOPs listed in file. Train with `YOLO("yolov8n-p2.yaml")`. — [yolov8-p2.yaml](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/models/v8/yolov8-p2.yaml)
- `ultralytics/cfg/models/11/yolo11-p2.yaml` returned 404 on raw GitHub (no official YOLO11-P2 yaml at that path at time of check; users typically copy the v8-p2 head pattern into a yolo11/yolo26 yaml). — [raw.githubusercontent 404](https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/models/11/yolo11-p2.yaml)
- A 2026 drone-imagery paper (LAF-YOLOv10) adds an "Auxiliary P2 Head" to YOLOv10 for small objects — evidence the P2 pattern transfers to YOLOv10 within Ultralytics-style yaml. — [arXiv 2602.13378](https://arxiv.org/pdf/2602.13378)
- RT-DETR/D-FINE/DEIM: use HybridEncoder on S3-S5 (stride 8/16/32) features; adding stride-4 requires editing encoder `in_channels`/`feat_strides` and backbone return_idx in config yaml — no official P2 config found in READMEs (see Gaps). — [D-FINE GitHub](https://github.com/Peterande/D-FINE)

#### Independent Jetson Orin Nano (Super) measurements
- visionanalysis.org (independent, mini500 subset, Orin Nano Super 8GB): D-FINE-L TensorRT FP16 18.6 FPS / 53.6 ms; TRT FP32 12.5 FPS / 80.2 ms; ONNX Runtime FP32 5.0 FPS; PyTorch 4.7 FPS. D-FINE-X TRT FP16 14.2 FPS / 70.5 ms. — [visionanalysis D-FINE-L](https://www.visionanalysis.org/model/dfine-l); [visionanalysis D-FINE-X](https://www.visionanalysis.org/model/dfine-x)
- Independent 2026 paper, Orin Nano, trtexec FP16 bs1, 1000 iters after warm-up: RT-DETR-R18 80.99 FPS; RT-DETR-R50 39.92 FPS (~25 ms e2e); YOLOv8-S 189.37 FPS; YOLOv10-S 172.99 FPS; YOLOv12-S 111.92 FPS. — [arXiv 2606.14005](https://arxiv.org/pdf/2606.14005)
- AgriJetsonBench (independent, external power meter): RT-DETR-R18 on Orin Nano ~72.7 FPS (p95 13.79 ms) vs AGX Orin ~105.1 FPS; on AGX Orin RT-DETR-R18 INT8 @640 reached 164.61 FPS at 0.1735 J/inference. — [arXiv 2608.00927](https://arxiv.org/html/2608.00927v1)
- RF-DETR paper caveat: D-FINE's hyperparameters were swept on COCO val; on RF100-VL test, D-FINE underperforms RT-DETR — COCO-tuned numbers may overstate transfer. — [RF-DETR paper arXiv 2511.09554](https://arxiv.org/pdf/2511.09554)

#### INT8 quantization of transformer detectors (RT-DETR / D-FINE / RF-DETR)
- NVIDIA TAO forum (RT-DETR R50): TensorRT native PTQ via cal.bin -> "many drops in detections"; ModelOpt explicit PTQ (`tao model rtdetr quantize`) better. NVIDIA: "encoder/decoder/head layers can be especially sensitive to INT8 quantization"; recommends layer exclusion for sensitive parts and larger calibration sets. — [NVIDIA TAO forum](https://forums.developer.nvidia.com/t/rt-detr-tao-6-x-int8-accuracy-drops-than-fp16-fp32/375782)
- RF-DETR on RTX 5090 (independent blog): calibrated INT8 build placed ZERO layers in INT8 (TensorRT timing chose FP16 everywhere); forcing INT8 via Q/DQ put 166 layers in INT8, ran 17% SLOWER than FP16 and cut mAP50:95 by >75%. TensorRT 10.2 release notes list INT8 slower than FP16 for some transformer models incl. DETR. — [dev.to RF-DETR INT8](https://dev.to/khadimhussain/tensorrt-int8-vs-fp16-on-rf-detr-measured-on-an-rtx-5090-3med)
- DETR user: after TensorRT 8.6.1 INT8 PTQ, COCO AP = 0.005 (near zero); unchanged with TRT 10.5. — [NVIDIA TensorRT forum](https://forums.developer.nvidia.com/t/after-tensorrt-quantize-detr-model-map-nealy-zero/309566)
- Research: QRT-DETR (PTQ pipeline with EMA-MSE quantizer + reconstruction) and Q-DETR / AQ-DETR (QAT, down to 4-bit) exist to address severe low-bit degradation in DETRs; "Enabling Fully Integer-Only Inference for Lightweight Detection Transformers" (2026) targets this problem. — [arXiv 2607.24981](https://arxiv.org/pdf/2607.24981)
- Contrast — CNN YOLOs INT8 PTQ losses measured: YOLO26n TRT INT8 on Orin Nano Super -3 pts (0.480->0.449 COCO128); RK3588 RKNN INT8 -1.4 pts (0.477->0.463); Hailo-8L yolov8n -0.6, yolov11n -1.5, yolov10n -1.9, yolo26n -1.6, yolo26s -2.2. — [Ultralytics Jetson](https://docs.ultralytics.com/guides/nvidia-jetson/); [Ultralytics RKNN](https://docs.ultralytics.com/integrations/rockchip-rknn/); [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- NVIDIA TAO blog (general): QAT keeps accuracy within 1% of FP32 whereas PTQ on the same model "made accuracy drop significantly". — [NVIDIA blog](https://developer.nvidia.com/blog/improving-int8-accuracy-using-quantization-aware-training-and-tao-toolkit/)

#### Raspberry Pi 5 + AI HAT+ (Hailo-8L, 13 TOPS) — independent / community
- End-to-end camera pipeline (1080p capture -> 640 resize -> YOLOv8n -> NMS -> draw, 10k frames): ~30 FPS on Pi 5 + Hailo-8L. Another build guide: YOLOv8n 640 = 32.0 FPS @13.5 W vs Pi 5 CPU XNNPACK 4.5 FPS @11 W. — [sixfab Pi camera build](https://sixfab.com/blog/raspberry-pi-ai-camera-build/); [electricalflux build](https://electricalflux.com/mcu-projects/raspberry-pi-5-hailo-8l-machine-learning-build)
- NPU-only: Seeed tutorial reports YOLOv8n 136.7 FPS on Pi 5 + Hailo-8L (likely batched hailortcli); Hailo community user: YOLOv8s 640 127.85 FPS at batch 8 PCIe Gen3. ~30 FPS ceiling is often CPU-side NMS (set NMS engine on Hailo HW) or camera-bound. Hailo-8 (26 TOPS): expect 55-70 FPS YOLOv8n 640 b1 with on-chip NMS. — [industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/fixing-empty-yolov8n-detections-on-raspberry-pi-5-hailo-ai-hat); [sixfab DEEPX vs Hailo benchmark](https://sixfab.com/blog/raspberry-pi-5-ai-hat-benchmark-deepx-vs-hailo/)
- Sixfab (Oct-Nov 2026) HAT comparison: AI HAT+ (Hailo-8L) lowest power 6.08 W avg, 1.69 FPS/W end-to-end; Hailo-8 1.74 FPS/W. — [sixfab DEEPX vs Hailo](https://sixfab.com/blog/raspberry-pi-5-ai-hat-benchmark-deepx-vs-hailo/)

#### Licensing — YOLO-NAS, YOLOX, PP-PicoDet
- YOLO-NAS: super-gradients code Apache-2.0 but LICENSE.YOLONAS.md: "The weights and architecture of the YOLO-NAS model are licensed under the Deci License – for research and non-commercial use only"; NVIDIA forum moderator: Deci dissolved after NVIDIA acquisition (May 2024), product no longer maintained, "commercial use is not permitted, and we are no longer issuing licenses". Pretrained weight URLs reported 404ing. AVOID for commercial. — [NVIDIA forum](https://forums.developer.nvidia.com/t/licensing-and-usage-terms-for-yolo-nas-model/326342); [YOLONAS.md](https://github.com/Deci-AI/super-gradients/blob/master/YOLONAS.md)
- YOLOX (Megvii, 2021): Apache-2.0 code AND weights, no carve-outs. PP-PicoDet / PP-YOLOE (Baidu PaddleDetection): Apache-2.0 code and weights. DAMO-YOLO Apache-2.0. — [libreyolo license guide](https://www.libreyolo.com/articles/yolo-licenses-explained); [libreyolo PicoDet](https://www.libreyolo.com/docs/models/picodet)
- All Ultralytics models (v5/v8/11/12-port/26) + YOLOv10 + YOLOv12 + YOLOv13 + YOLOE/YOLO-World(Ultralytics port) = AGPL-3.0 (or paid Enterprise). Apache-2.0: RT-DETR/v2, D-FINE, DEIM v1, RF-DETR (Nano/S/M/L; NOT Atto/Femto/Pico "PML 1.0"), YOLOX, NanoDet, PP-PicoDet/PP-YOLOE, LW-DETR. Custom/restricted: DEIMv2 (contact for commercial), YOLO-NAS weights (non-commercial, defunct). — see per-family sections above.

---

## TAKEAWAYS, INFERENCES, GAPS (final)

### KQ1 Takeaway — per-family spec summary (COCO 640 unless noted; all vendor-claimed)
| Family (license) | Smallest useful variant | Params / GFLOPs | COCO mAP | T4 TRT FP16 ms | Release |
|---|---|---|---|---|---|
| YOLO26n/s (AGPL) | n / s | 2.4M/5.5G ; 9.5M/20.9G | 40.9 ; 48.6 (e2e 40.1 ; 47.8) | 1.7 ; 2.5 | Sep 2025 announce / Jan 2026 weights |
| YOLO11n/s (AGPL) | n / s | 2.6M/6.5G ; 9.4M/21.6G | 39.5 ; 47.0 | 1.5 ; 2.5 | 2024-09-27 |
| YOLOv10n/s (AGPL) | n / s | 2.3M/6.7G ; 7.2M/21.6G | 38.5 ; 46.3 | 1.84 ; 2.49 | May 2024 |
| YOLOv12n/s turbo (AGPL) | n / s | 2.5M/6.0G ; 9.1M/19.4G | 40.4 ; 47.6 | 1.60 ; 2.42 | Feb/Mar 2025 |
| YOLOv13n/s (AGPL) | n / s | 2.5M/6.4G ; 9.0M/20.8G | 41.6 ; 48.0 | 1.97 ; 2.98 | Jun 2025 |
| D-FINE-N/S (Apache) | N / S | 4M/7G ; 10M/25G | 42.8 ; 48.5 (Obj365: 50.7) | 2.12 ; 3.49 | Oct-Nov 2024 |
| DEIM-N/S (Apache) | N / S | 4M/7G ; 10M/25G | 43.0 ; 49.0 | 2.12 ; 3.49 | Dec 2024 / Mar 2025 |
| DEIMv2 Atto..N/S (custom lic.) | Pico / N / S | 1.5M/5.2G ; 3.6M/6.8G ; 9.7M/49.5G | 38.5 ; 43.0 ; 50.9 | 2.13 ; 2.32 ; 5.78 (device unstated) | Sep 2025 |
| RT-DETRv2-S (Apache) | S (r18) | 20M/60G | 48.1 | 4.6 (217 FPS) | Jul 2024 |
| RF-DETR Nano/Small (Apache) | Nano@384 / Small@512 | 30.5M / 32.1M (GFLOPs n/a) | 48.4 ; 53.0 | 2.3 ; 3.5 | 2025 (paper Nov 2025) |
| LW-DETR-S (Apache) | S | 15M/17G | 43.6 (Obj365: 48.0) | 3.02 | 2024 |
| NanoDet-Plus-m (Apache) | m@320/416 | 1.17M/0.9-1.5G | 27.0 ; 30.4 | ARM Kirin980 12-20 ms | 2021-23, dormant |
| YOLOX-Nano/Tiny (Apache) | Nano@416 / Tiny@416 | 0.9M/1.1G ; 5.05M/6.4G | 25.8 ; 32.6 | — | 2021 (baseline) |
| PP-PicoDet-S (Apache) | S@416 | 1.0M/1.2G | 30.7 | — | 2021 (baseline) |
| EfficientDet-Lite0/2 (Apache) | lite0@320 / lite2@448 | 3.56M/1.94G ; 5.93M/6.84G | 27.3 ; 35.9 | — | 2020-21 (baseline) |
| YOLOE-11-S (AGPL, open-vocab) | S | 10M | LVIS 27.5 | 3.3 (301 FPS); iPhone12 13.6 ms | Mar 2025 |

### KQ2 Takeaway — AP_small vs compute
- At S scale (~10M / 20-25 GFLOPs): DEIM-S 30.4 AP_S > D-FINE-S 29.1 > YOLO11-S 28.7 > YOLOv10-S 26.8 > YOLOv8-S 25.7; DEIMv2-S 31.4 but at 2x FLOPs (50G). With Objects365 pretraining D-FINE-S jumps to 32.7 AP_S and RT-DETR-R18 to 33.2 — pretraining data matters more than architecture for small objects. Sources: D-FINE/DEIMv2 papers above.
- At M scale: DEIM-M 35.3 AP_S (19M/57G) is best per-FLOP; YOLOv10-M 33.8 (15M/59G) best among AGPL YOLOs; D-FINE-M Obj365 37.9.
- Nano-scale AP_S is unreported in all primary sources found (gap). Expect ~20-24 AP_S for 40-mAP nano models by extrapolation (inference, not sourced).

### KQ3 Takeaway — edge FPS (precision stated)
- Jetson Orin Nano Super: YOLO26n TRT FP16 4.57 ms (~219 FPS), INT8 3.80 ms (vendor); RT-DETR-R18 FP16 ~73-81 FPS (independent, 2 sources); D-FINE-L FP16 18.6 FPS (independent). No D-FINE-N/S or DEIM Orin Nano numbers found.
- Raspberry Pi 5 CPU: YOLO26n NCNN FP32 67 ms (~15 FPS); ONNX 126-128 ms; YOLO26s NCNN ~173 ms (vendor). YOLOv8n CPU ~4.5 FPS end-to-end (independent, XNNPACK).
- Pi 5 + Hailo-8L: YOLOv8n ~30 FPS end-to-end camera pipeline (independent); 130-217 FPS NPU-only/batched; Hailo zoo (i5 host) yolov8n 201 FPS b1, yolo11n 157, yolo26n 111, yolov12n 38.
- RK3588: YOLO26n RKNN FP16 58.5 ms / INT8 41.2 ms (vendor, conservative single-core pipeline); community ~11 ms with 3 NPU cores.
- Coral USB on Pi 4B: YOLOv8n INT8 @320 32 ms (~31 FPS); must use imgsz<=512 and <=s size; YOLO11/YOLOv10+ compile poorly.
- Original Jetson Nano: no 2024-26 benchmark found for any listed family (gap).

### KQ4 Takeaway — INT8 loss
- CNN YOLOs: 0.6-3 pt PTQ loss (Hailo 0.6-2.2; RKNN hybrid 1.4; TRT entropy PTQ on YOLO26n 3 pt). DETR family: TensorRT native PTQ can be catastrophic (near-zero AP for DETR; RF-DETR -75% when forced; TRT often silently keeps FP16 and INT8 is slower). NVIDIA confirms RT-DETR encoder/decoder/head are INT8-sensitive; ModelOpt explicit PTQ with layer exclusion or QAT (Q-DETR/AQ-DETR/QRT-DETR) needed. No measured INT8 numbers for D-FINE/DEIM specifically were found (gap); DEIMv2 offers OpenVINO INT8 via Intel Geti (no accuracy reported).

### KQ5 Takeaway — P2 / high-res
- Ultralytics: official yolov8-p2.yaml (Detect on P2-P5) and arbitrary imgsz (1280 via `imgsz=1280`) — cheapest path; P2 head adds a stride-4 C2f branch and roughly doubles head compute at the same imgsz (exact cost not sourced). YOLOv10 P2 variants demonstrated in literature. DETR-family (RT-DETR/D-FINE/DEIM): no official P2 configs; 300 queries and HybridEncoder on S3-S5 make stride-4 expensive (AIFI attention on S5 is cheap, but CCFM fusion on S2 at 1280 would be large) — config-level edit required, unverified.

### KQ6 Takeaway — licensing
- AGPL-3.0 (copyleft; requires source release of network-served/distributed derivatives or Enterprise license): all Ultralytics (v8/11/26), YOLOv10, YOLOv12, YOLOv13, YOLOE/YOLO-World ports. Apache-2.0: RT-DETR/v2, D-FINE, DEIM v1, RF-DETR Nano-Large, LW-DETR, YOLOX, NanoDet, PP-PicoDet/PP-YOLOE, DAMO-YOLO, EfficientDet. Restricted: DEIMv2 (custom, contact for commercial), RF-DETR Atto/Femto/Pico (PML 1.0), YOLO-NAS weights (non-commercial, licensing channel closed), D-FINE/DEIM Objects365-pretrained checkpoints (Objects365 dataset terms caveat).

### KQ7 Takeaway — open-vocabulary on edge
- YOLOE-11-S (10M) runs 73 FPS on iPhone 12 CoreML and 301 FPS on T4 — edge-feasible on phone-class ARM/NPUs; after re-parameterizing to a fixed vocabulary it has the cost of plain YOLO11-S. No N-size variant; LVIS AP 27.5 (zero-shot) is far below closed-set COCO-trained small detectors; prompt-free mode loses 5-8 AP. AGPL-3.0. No Jetson/RPi/Hailo numbers found for YOLOE/YOLO-World (gap).

## Inferences (cross-cutting)
- For sub-10 W edge NPUs (Hailo-8L, RK3588, Coral) pure-CNN YOLO (v8n/11n/26n) remains the pragmatic choice: fully supported in vendor zoos, 0.6-2 pt INT8 loss, 100+ FPS. Attention-based YOLOv12/13 and DETRs are poorly matched (yolov12n 4x slower than yolov11n on Hailo-8L; no DETR in Hailo zoo).
- For Jetson Orin Nano (FP16 TensorRT, GPU), D-FINE-S/DEIM-S (Apache-2.0, ~10M, 49 AP, AP_S ~30) are the best accuracy-per-FLOP small-object choices with permissive licensing; expect roughly 100+ FPS FP16 by scaling from RT-DETR-R18 (73-81 FPS at 60 GFLOPs) — not directly measured.
- Objects365 pretraining gives +3-5 AP_S at zero inference cost (D-FINE-S 29.1->32.7); for small military targets, pretraining data/resolution likely dominates architecture choice.
- YOLO26's CPU-speed claim (43% vs YOLO11n) is from Xeon; on Pi 5 ONNX the measured gain is ~15% (7.79 vs 6.79 FPS); NCNN gives bigger wins than model choice.
- RF-DETR "Nano" is not nano in memory terms (30M params); low latency comes from 384 input, which is hostile to small objects.

## Gaps
- AP_small for nano-scale models (YOLO26n, YOLO11n, YOLOv10n, D-FINE-N, DEIM-N/v2-N, YOLOv12n) not reported in any primary source fetched; YOLO26 paper tables not checked.
- No measured Jetson Orin Nano FPS for D-FINE-N/S, DEIM, DEIMv2, RF-DETR Nano, or YOLOE; no original Jetson Nano (Maxwell) benchmark for any 2024-26 model.
- No measured INT8 accuracy numbers for D-FINE/DEIM/DEIMv2 (only RT-DETR/RF-DETR/DETR anecdotes); DEIMv2 latency device/precision unstated by authors.
- DEIMv2 custom license text not read directly; RF-DETR exact release date not found; YOLO26 paper arXiv ID shown as 2606.03748 (unverified).
- P2-head cost (params/GFLOPs) for YOLO26/YOLO11 not sourced; no official P2 config for DETR families confirmed.
- Hailo-8L zoo figures use an x86 host, not Pi 5; Pi-hosted numbers are community/blog measurements of variable rigor.
- RK3588 INT8 accuracy validated only in simulator per Ultralytics; rknn_model_zoo (Rockchip official) tables not fetched.
- YOLO-World, PP-YOLOE+, MobileNetV4, FastestDet, YOLOv9t, Qualcomm AI Hub and Seeed wiki not fetched within budget; MobileNetV4/FastestDet have no entries here.
