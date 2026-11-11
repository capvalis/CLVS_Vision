# Edge Deployment of Small-Object Detectors: Hardware, Toolchains, Compression, Trade-offs (2024-2026)

Notes written incrementally (append-as-you-go). Every FPS number should carry device / precision / input size / software version where the source gives it. "Vendor" = vendor-published; "Indep." = independent measurement.

## Q1. Low-cost edge hardware landscape: measured detection throughput, price, power

### Takeaway
For nano/small YOLO at 640, every modern low-cost platform (Orin Nano Super, RPi5+Hailo-8/8L, RK3588, AX650N, QCS6490) exceeds 60 FPS engine-only; the real differentiators are (a) end-to-end pipeline overhead (host decode/pre/post on Pi 5 caps pipelines at ~7-30 FPS; Jetson Python pipelines are 2-4x slower than trtexec), (b) headroom for 1024-1280 inputs (only Jetson and Hailo-8/AX650N have published or demonstrated 1280 runs), and (c) DETR-family support (only Jetson TensorRT and Axera are safe). Orin Nano Super at $249 is the best-documented and most flexible; RPi5 + AI HAT+ (Hailo-8, $110) is the cheapest path to >100 FPS YOLOv8s but is PCIe-x1/host-bound; RK3588 boards are cheapest per unit but single-core NPU FPS is modest and INT8 is effectively mandatory.

### Cited Findings

**Ultralytics official Jetson guide (vendor-ish; Ultralytics-run, imgsz 640, COCO128 eval, pre/post-processing EXCLUDED; note page now benchmarks YOLO26n, not YOLO11/v8)** — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)
- Jetson Orin Nano Super Dev Kit (JetPack 6.1, Ultralytics 8.4.33), YOLO26n @640: PyTorch 15.60 ms; ONNX 15.76 ms; TensorRT FP32 7.53 ms (mAP50-95 0.477); TensorRT FP16 4.57 ms (0.480); TensorRT INT8 3.80 ms (0.449 -> ~3 pt drop vs FP16 on COCO128); NCNN (CPU) 47.5 ms. So ~219 FPS FP16 engine-only, ~263 FPS INT8 engine-only.
- Jetson Orin NX 16GB (JP 6.0): YOLO26n TRT FP16 4.13 ms, INT8 3.49 ms (mAP 0.449 vs 0.479 FP16).
- AGX Orin 64GB (JP 7.2): YOLO26n TRT FP16 2.62 ms, INT8 2.30 ms (0.464 vs 0.479).
- Jetson Nano 4GB (JP 4.6.1) is listed as tested but NO benchmark table (legacy; JetPack 4 only; TensorRT 8.x only).
- Orin Nano Super spec: 67 TOPS (sparse INT8), 1024-core Ampere GPU @1020 MHz, 6-core A78AE, 8 GB LPDDR5 102 GB/s. Orin NX 16GB: 100 TOPS, 2 DLA cores @614 MHz. DLA export requires FP16/INT8 ("dla:0"), aimed at throughput/efficiency not latency.
- TensorRT caveats: TRT 10.3.0 (JP6) has an INT8 bug with NMS-free/embedded-NMS exports -> use 10.7.0+; TRT 10.7 is last DLA-capable release; TRT 11 has no JetPack support.
- Memory: headless boot saves ~865 MB; total ~1 GB saving possible on 8 GB Orin Nano.

**Ultralytics Raspberry Pi guide (Pi 5 CPU only, Cortex-A76 2.4 GHz, Bookworm 64-bit, imgsz 640, FP32, Ultralytics 8.4.x, pre/post EXCLUDED)** — [Ultralytics RPi guide](https://docs.ultralytics.com/guides/raspberry-pi/)
- YOLO26n @640: PyTorch 299 ms; ONNX 126 ms; OpenVINO 104.6 ms; LiteRT 123 ms; MNN 91.9 ms; NCNN 67.0 ms (best, ~15 FPS); ExecuTorch 145 ms. YOLO26s NCNN 173 ms (Jocher comment). YOLO11n ONNX ~6.8 FPS (147 ms) per narrative ("6.79 -> 7.79 FPS" YOLO11n->YOLO26n). Models > s "run too slowly on Raspberry Pi to be practical". Pi 4 and YOLOv8/YOLO11 format tables no longer on page.
- Implication: Pi 5 CPU alone gives ~7-15 FPS for nano models at 640; at 1024+ CPU-only is impractical for real-time.

**Ultralytics RKNN guide (Radxa Rock 5B / RK3588, Ultralytics 8.4.60, default imgsz 640, COCO128, pre/post EXCLUDED)** — [Ultralytics RKNN integration](https://docs.ultralytics.com/integrations/rockchip-rknn/)
- YOLO26n RKNN FP16 58.5 ms (mAP 0.477) / INT8 41.2 ms (0.463); YOLO26s FP16 93.8 ms (0.569) / INT8 61.9 ms (0.554); YOLO26m INT8 122 ms. Doc explicitly says these are a conservative single-core baseline; a commenter reports ~11 ms/img for YOLO26n using all 3 RK3588 NPU cores with native RKNN runtime (unverified). INT8 accuracy validated only in rknn-toolkit2 simulator, not on hardware (doc caveat).
- Supported FP16+INT8 chips: RK3588, RK3576, RK3566, RK3568, RK3562, RK2118, RV1126B; INT8-only: RV1103/RV1106 family.

**Hailo Model Zoo, Hailo-8L (13 TOPS; the Raspberry Pi AI Kit / AI HAT+ 13T chip). Vendor numbers; host i5-9400, DFC v2.20.0, PCIe Gen3 x4; mAP float vs 'Hardware mAP' (compiled/quantized)** — [Hailo-8L object detection zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- yolov8n 640: 201 FPS b1 / 437 FPS b8; mAP 37.0 -> 36.4 (-0.6)
- yolov8s 640: 110 / 208 FPS; 44.6 -> 43.9 (-0.7)
- yolov8m 640: 50.7 / 87 FPS; 49.9 -> 49.2
- yolov11n 640: 157 / 370 FPS; 39.0 -> 37.5 (-1.5)
- yolov11s 640: 91.9 / 190 FPS; 46.3 -> 45.1 (-1.2)
- yolov11m 640: 35.3 / 57.8 FPS; 51.1 -> 49.9
- yolov10n 640: 150 / 359 FPS; 38.5 -> 36.6 (-1.9); yolov10s 87.2/187
- yolo26n 640: 111 / 255 FPS; 40.0 -> 38.4 (-1.6); yolo26s 66.5/147; 47.5 -> 45.3 (-2.2)
- yolov12n 640: only 38.4 / 86.3 FPS (attention blocks run poorly) 40.5 -> 39.3
- High-res entries: yolov5m6_6.1 @1280: 21.7 / 29.7 FPS (50.7 -> 49.4); yolov7e6 @1280: 6.44 / 7.97 FPS.
- DETR family: only detr_resnet_v1_18_bn @800: 23.4 / 50 FPS, 33.9 -> 31.5 (-2.4, largest drop in zoo). NO RT-DETR / D-FINE / DEIM entries in Hailo-8L zoo.
- On-chip NMS ("_nms_core") variants cost a lot of throughput: yolov6n 560 -> 199 FPS; yolov5xs 206 -> 67 FPS. Hailo's standard flow runs NMS/decoding on host CPU.
- Note: these FPS are chip-bound on an x86 host; on RPi5 the PCIe Gen3 x1 link and the Arm host doing pre/post-processing lower end-to-end FPS (see independent measurements below).


### Inferences

- Engine-only vendor FPS overstates deliverable throughput by 2-10x on Pi-hosted accelerators (Hailo zoo 491 FPS yolov8s on x86 Gen3 x4 vs 55 FPS on CM5 Gen3 x1 vs ~10 FPS end-to-end with Pi decode) and ~1.5-3x on Jetson (trtexec 225 FPS vs 37-60 FPS Ultralytics Python pipeline for nano models).
- Memory bandwidth, not TOPS, bounds high-resolution inference on Orin Nano (102 GB/s; NVIDIA confirms ~60% of FP16 peak achieved); expect roughly 3.5-4x latency from 640 to 1280 (extrapolation, not measured).
- Hailo-8 (26T) vs 8L (13T): speedup is highly model-dependent (5x for yolov8n/s that become single-context, ~1.2x for yolov11n). For RPi5 the 26T AI HAT+ is worth the extra $40 mainly for s/m models or higher resolutions.
- AI HAT+ 2 (Hailo-10H) is not a vision upgrade over the Hailo-8 AI HAT+ per Raspberry Pi itself; its on-board 8 GB helps only large models (Sixfab: 2x on yolov8l).
- RK3576-based boards (cheaper, newer NPU) beat RK3588 single-core on nano models; RK3588's advantage is 3 cores + more video decode capacity.
- Coral Edge TPU and legacy Jetson Nano are end-of-life for modern detectors (frozen compiler / JetPack 4) and should be excluded from new designs.


**Legacy Jetson Nano 4GB (JetPack 4.6.x, Python 3.6, TensorRT 8.0/8.2; Ultralytics unsupported)**
- YOLOv8n TRT FP16 @416: 38.6 FPS network-only, 12.3 FPS live camera-to-display system (numpy pre/post, ctypes CUDA runner) — [jetson-nano-yolo-bench](https://github.com/PragalvaXFREZ/jetson-nano-yolo-bench)
- YOLO11n FP16 (JP 4.6.1, MAXN): 31.3 FPS @320, 11.0 FPS @640 benchmark; ~29 FPS live CSI at 320 — [jetson-object-detection PR #8](https://github.com/automaticdai/jetson-object-detection/pull/8). Inference: ~10-15 FPS nano models at 640; Nano is not viable for 1024+ inputs.


**Hailo-8 (26 TOPS; AI HAT+ 26T) model zoo, same conditions as 8L (vendor; i5-9400 host, DFC 2.20, PCIe Gen3 x4)** — [Hailo-8 object detection zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8/HAILO8_object_detection.rst)
- yolov8n 640: 1036 FPS (b1 = b8; single-context, chip-bound); yolov8s 491 FPS; yolov8m 66.9 / 149 FPS
- yolov11n 185 / 541; yolov11s 111 / 303; yolov11m 50.2 / 102; yolov10n 194 / 567; yolov10s 117 / 283; yolo26n 154 / 427; yolo26s 97.8 / 263
- 1280 entries: yolov5m6_6.1 32.7 / 50.0 FPS (49.4 HW mAP); yolov7e6 11.3 / 15.9 FPS. detr_resnet18 @800: 30.5 / 75.4 FPS.
- Hardware mAP identical to 8L (same compiled quantization). Note yolov8n/s are ~5x faster on Hailo-8 than Hailo-8L (1036 vs 201; 491 vs 110) because they fit in a single context on the bigger chip, while yolov11n is only 1.2x faster (185 vs 157) — multi-context/architecture effects dominate over TOPS ratio.
- Official NVIDIA blog confirms Orin Nano Super Dev Kit: $249 (was $499), 67 sparse TOPS / 33 dense, 102 GB/s, 25 W envelope, announced 17 Dec 2024; same hardware as original Orin Nano, unlocked via JetPack 6.1 MAXN; Orin NX 16GB rises to 157 TOPS with the update — [NVIDIA developer blog](https://developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/); [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/nvidia-launches-new-usd249-ai-development-board-that-does-67-tops)
- RK3588 community (indep.): Q-engineering YOLOv8 INT8 on RK3588: yolov8n 53.1 FPS, yolov8s 28.5, yolov8m 12.1 — [Qengineering/YoloV8-NPU](https://github.com/Qengineering/YoloV8-NPU); kaylorchen multi-threaded yolov8n demo up to ~100 FPS using all 3 cores — [rk3588-yolo-demo](https://github.com/kaylorchen/rk3588-yolo-demo); Show HN dual-stream YOLOv8n UAV detection on RK3588S at 42-46 FPS (camera ceiling) via MIPI->ISP->RGA->3 RKNN contexts (one per NPU core) — [Hacker News](https://news.ycombinator.com/item?id=48527623)
- RPi CM5 + Hailo-8, yolov8s: PCIe Gen2 28.6 FPS vs Gen3 55.7 FPS; Hailo staff confirm PCIe config is the main reason Pi numbers trail the zoo — [Hailo community](https://community.hailo.ai/t/the-performance-on-the-raspberry-pi-5-with-the-hailo-8-chip-seems-not-good-as-he-official-results/17473)


**Rockchip rknn_model_zoo v2.5.0 official benchmarks (vendor; INT8, 640x640, max NPU freq, inference only, RK3588/RK3576 = SINGLE NPU core of 3/2)** — [airockchip/rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo)
- RK3588 1-core: yolov8n 76.3 FPS, yolov8s 38.6, yolov8m 16.3; yolo11n 64.0, yolo11s 34.6, yolo11m 14.6; yolov10n 63.9; yolo26n 55.0; yolov5n 84.6; yolov6n 108.8 (ReLU models are fastest); ppyoloe_s 39.7; yolo_world_v2s 20.6
- RK3576 1-core (newer NPU, cheaper SoC): yolov8n 97.7, yolov8s 42.1; yolo11n 87.5, yolo11s 40.7 — RK3576 single-core beats RK3588 single-core for nano models.
- RK3566/3568: yolov8n 35.1; yolo11n 22.6. RV1126B: yolov8n 83.0.
- Zoo does NOT include RT-DETR, D-FINE, DEIM. Requires RKNPU2 SDK >= 2.5.0; yolo11 added in 2.3.0, yolo26 in 2.4.2.
- Note that multi-core (3 cores on RK3588) can be used either by running 3 model instances (throughput) or core_mask RKNN_NPU_CORE_0_1_2 (limited latency gain for small models).

**Raspberry Pi AI HAT+ 2 (Hailo-10H, launched Jan 2026)**
- 40 TOPS INT4 / 20 TOPS INT8, 8 GB LPDDR4X on-board, ~2.5 W typical; launched at $130 (Jan 2026), official page now $200 (Oct 2026, memory price increase); production guaranteed to Jan 2036 — [Raspberry Pi product page](https://www.raspberrypi.com/products/ai-hat-plus-2/); [The Register](https://www.theregister.com/2026/01/15/pi_5_ai_hat_2/); [Jeff Geerling](https://www.jeffgeerling.com/blog/2026/raspberry-pi-ai-hat-2/)
- Raspberry Pi itself says vision performance is "roughly on a par with the 26 TOPS AI HAT+"; Geerling: hard to recommend over the AI HAT+ for vision-only use; Tom's Hardware found "flawed results" — [Tom's Hardware review](https://www.tomshardware.com/raspberry-pi/raspberry-pi-ai-hat-plus-2-review). AI HAT+ (Hailo-8L 13T) starts at $70; Hailo-8 26T version $110 (launch pricing). Sixfab measured Hailo-10H YOLOv8l async 40 FPS vs Hailo-8 19.6 FPS (see above) - so for LARGE models Hailo-10H's on-board DRAM helps.

**Intel N100 (LattePanda Mu / N100 mini-PCs ~ $130-180, 6 W TDP)**
- LattePanda (vendor): YOLO11n detect, OpenVINO INT8, end-to-end webcam pipeline: iGPU 21 FPS, CPU 10 FPS; YOLOv8n INT8 iGPU 15-20 FPS, CPU 7-9 FPS; FP32 CPU 4-7 FPS — [LattePanda YOLO11](https://www.lattepanda.com/blog-323240.html); [LattePanda YOLOv8](https://www.lattepanda.com/blog-323173.html). Use the iGPU target; end-to-end numbers include capture/draw so benchmark_app would be higher.
- Ultralytics OpenVINO guidance: INT8 speedup is ~1.2x for n models, 2.9x for m, costing 1.2-1.7 mAP — INT8 is rarely worth it on nano models on CPU — [Ultralytics Academy OpenVINO](https://academy.ultralytics.com/courses/yolo-in-production/openvino-on-cpu)

**Price/power quick reference (list prices as found; verify at purchase)**
- Jetson Orin Nano Super Dev Kit: $249 (NVIDIA cut from $499 in Dec 2024), 7-25 W — [ChipRadar summary](https://chipradar.io/blog/jetson-orin-nano-super-benchmarks) (secondary; NVIDIA announcement is primary). Orin NX 16GB module ~ $599 class (not confirmed in this research).
- RPi 5 8GB ~$80 + AI HAT+ $70 (13T) / $110 (26T) / AI HAT+ 2 $130->$200. Pi 5 board ~5-8 W; Hailo-8L ~1.5-2.5 W; Hailo-8 ~2.5-5 W (vendor typical; not independently measured here).
- Orange Pi 5 / Rock 5B (RK3588, 6 TOPS NPU): ~$80-150 depending on RAM; ~5-10 W.


**Independent RPi5 + Hailo / DEEPX / Coral measurements**
- Sixfab head-to-head on Pi 5 (indep. vendor-of-competitor; YOLOv8l 640): NPU async throughput DEEPX DX-M1M 50.1 FPS, Hailo-8 19.6, Hailo-8L 15.0, Hailo-10H 40.0; but END-TO-END with video decode: 11.2 / 10.3 / 8.7 / 11.9 FPS - "video decode on the Pi 5 is the bottleneck, not the NPU"; Pi 5 decoder caps single-stream full pipelines to ~7-26 FPS. Efficiency: Hailo-8 AI HAT+ 1.74 FPS/W vs 1.69 for DX-M1M and Hailo-8L. Also quotes Hailo zoo: YOLOv8s Hailo-8L 110/208 FPS (b1/b8, zoo 2.19.1), Hailo-8 491 FPS, Hailo-10H 166/252 (zoo 5.4.0) — [Sixfab DEEPX vs Hailo](https://sixfab.com/blog/raspberry-pi-5-ai-hat-benchmark-deepx-vs-hailo/)
- Community: Seeed wiki claims YOLOv8s 80.7 FPS b1 on AI Kit (Hailo-8L); a user measured 54 FPS b1 — [Hailo community thread](https://community.hailo.ai/t/issue-with-yolo-fps-on-raspberry-pi-5/11706). PCIe link speed matters: YOLOv8s b8 on Hailo-8L reaches ~120 FPS at PCIe Gen3 but ~40 FPS at Gen2 (set dtparam=pciex1_gen=3) — [DataRoot Labs](https://datarootlabs.com/blog/hailo-ai-kit-raspberry-pi-5-setup-and-computer-vision-pipelines)
- Real camera pipeline comparison (front-door detection): Coral USB 5.1 FPS, Hailo-8L 30.4 FPS, Hailo-8 31.0 FPS (preprocessing-bound) — 26 TOPS board does not pull ahead of 13 TOPS in a Pi-hosted camera pipeline — [computingforgeeks](https://computingforgeeks.com/best-ai-accelerator-raspberry-pi-5/)
- Jeff Geerling's AI HAT+ post was not reachable (404 at expected URL); secondhand: ~12 ms with two cameras on Hailo-8 in a CM5 build — [computingforgeeks](https://computingforgeeks.com/best-ai-accelerator-raspberry-pi-5/). Treat as unverified.

**Coral Edge TPU (USB / M.2, 4 TOPS INT8, 8 MB on-chip SRAM)**
- Ultralytics Edge TPU export: full-INT8 mandatory; compiler "leaves the rest on the CPU, so task support does not mean every operation runs on the TPU". Commenter example YOLOv8l (VisDrone): 223 ops on TPU / 164 on CPU, later 133 TPU / 364 CPU -> Ultralytics advice: use YOLOv8n. Edge TPU Compiler still v16.0.384591198 in Oct-2024 and May-2025 logs (no newer compiler); May-2025 YOLO11 export failed ("Didn't find op for builtin opcode CONV_2D version 6") while YOLOv8 worked. No FPS tables published — [Ultralytics Edge TPU](https://docs.ultralytics.com/integrations/edge-tpu/)
- Inference: Coral is effectively frozen tooling (compiler v16, 2022-era); modern YOLO heads partly fall back to CPU; only n-sized models at <=640 are practical. Not recommended for new small-object designs.

**Qualcomm QCS6490 (Dragonwing RB3 Gen 2; 12 TOPS Hexagon NPU). Vendor AI Hub profile numbers (NPU-only latency)**
- YOLOv8-Detection (YOLOv8-N ckpt) on QCS6490 proxy: w8a8 TFLite 3.69 ms NPU; w8a8 QNN 4.85 ms; w8a16 QNN 11.9 ms; ONNX CPU fallback 43.9 ms (w8a8) / 167 ms (w8a16) — [HF qualcomm/YOLOv8-Detection README history](https://huggingface.co/qualcomm/YOLOv8-Detection/blob/1fbb611bc4910a1972dd8ae4f93cb1055b06ad51/README.md)
- YOLOv11-Segmentation QCS6490 ONNX w8a16: 19.4 ms NPU — [HF qualcomm/YOLOv11-Segmentation](https://huggingface.co/qualcomm/YOLOv11-Segmentation). YOLOv11-Detection QCS8550 TFLite FP16: 5.4 ms — [HF qualcomm/YOLOv11-Detection](https://huggingface.co/qualcomm/YOLOv11-Detection/blob/74c8b150f94d8fc078351b420509653bba8a46ab/README.md)
- Qualcomm AI Hub model zoo includes YOLOv8/YOLOv11 Detection/Segmentation, Yolo-R, and (per AI Hub) RT-DETR / DETR-ResNet50 etc.; numbers change per ai-hub-models release — check live cards.

**MemryX MX3 (4-chip M.2, ~24 TOPS total, activations BF16 / weights INT8/4)**
- BDTI independent report (x86 host): YOLOv8m reached 45 FPS (camera-limited at 24 FPS for 640x480) — [BDTI MX3 report PDF](https://www.bdti.com/sites/default/files/BDTI-Independent-Report-MemryX-MX3-M2-Module.pdf)
- On weak Arm host (i.MX8MP, PCIe Gen3 x1): YOLOv8n 640 = 61.5 FPS; MemryX says host CPU/RAM/PCIe x1, not MX3, is the bottleneck; MemryX reports better results on RK3588 boards and Pi 5 — [MemryX community](https://community.memryx.com/t/mx3-benchmark-performance-cpu-consumption/125). No Pi-5-hosted YOLOv8 FPS from MemryX found.

**Axera AX650N (18 TOPS INT8 / 72 TOPS INT4, Transformer-native NPU; Sipeed Maix4-HAT for Pi 5, M4N Dock)**
- Official HF model: yolov8s 640 w8a16 = 3.64 ms (~275 FPS) NPU-only — [AXERA-TECH/YOLOv8](https://huggingface.co/AXERA-TECH/YOLOv8); yolov8n-seg 5.1 ms (1 core)/1.85 ms (3 cores), yolov8s-seg 13.7/4.7 ms — [AXERA-TECH/YOLOv8-Seg](https://huggingface.co/AXERA-TECH/YOLOv8-Seg)
- Sipeed AXCL table (AX650N as PCIe accelerator on Pi 5): YOLOv8s 640 = 248 IPS b1 / 279 IPS b8 — [Sipeed PCIe guide](https://wiki.sipeed.com/hardware/en/maixIV/m4chat/pcie-slaveboard.html)
- AX650N natively supports Transformers (ViT/DETR-type attention) per Axera — [Axera news](https://www.axera-tech.com/en/news/2813.html); AX650N can decode up to 32 video streams (M4N Dock) — [CNX Software](https://www.cnx-software.com/2024/03/18/sipeed-maixbox-m4n-ai-box-with-43-2-tops-axera-ax650n-soc-can-decode-encode-up-to-32-videos/)

**Jetson Orin Nano Super: independent FPS + power**
- Hokwang Choi (indep., Orin Nano 8GB MAXN_SUPER, YOLOv8n 640 b1, GPU-only latency via CUDA events/trtexec): FP32 8.36 ms / 120 FPS @14.3 W; FP16 4.43 ms / 225 FPS @14.1 W; INT8 3.49 ms / 286 FPS @12.5 W. In 15 W mode: FP16 6.13 ms, INT8 4.90 ms (204 FPS). MAXN_SUPER adds ~3-4 W for 30-40% more perf — [hokwangchoi.com](https://hokwangchoi.com/blog/vision-benchmarks/)
- AgriJetsonBench (arXiv 2508.00927, external power meter, 15 W INT8): YOLO11s Orin Nano Super 145.8 FPS, 0.0767 J/inference vs AGX Orin 80.9 FPS / 0.181 J at matched 15 W — [arXiv AgriJetsonBench](https://arxiv.org/html/2608.00927v1)
- End-to-end Python pipeline numbers are far lower than engine-only: older Orin Nano (15 W) YOLOv8n TRT FP16 58 FPS / INT8 72 FPS (mAP50 37.2 vs 36.8); YOLOv8s FP16 35 FPS — [industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/resolving-yolo-model-performance-on-jetson-orin-nano-with-tensorrt-export); Turing Pi (JP 7.2.1, YOLO11n, serial replay incl. pre/post): PyTorch 20.4 FPS, TRT FP16 37.4 FPS — [Turing Pi](https://turingpi.com/yolo-jetson-orin-nano-tensorrt-benchmarks/)
- NVIDIA forum: Orin Nano Super delivers ~10 TFLOPS measured vs 17 TFLOPS FP16 spec; NVIDIA attributes to memory bandwidth (102 GB/s) — relevant to large-resolution inference — [NVIDIA forums](https://forums.developer.nvidia.com/t/performance-discrepancy-tensorrt-achieves-10-tflops-vs-17-tflops-spec-on-orin-nano-super-mode/359635)
- Power envelope: Orin Nano Super idle ~4.5 W, 8-12 W typical single-stream inference, up to ~25-28 W MAXN Super — [edgeaistack](https://edgeaistack.ai/blog/jetson-orin-nano-power-consumption/) (secondary source)


### Gaps

- No measured YOLOv8n/YOLO11n FPS at 1024/1280 found for Orin Nano Super, RPi5+Hailo, or RK3588 (only Hailo zoo yolov5m6/yolov7e6 at 1280). Must be measured in-house (trtexec / hailortcli / rknn_benchmark).
- No RT-DETR / D-FINE FPS on any NPU other than Qualcomm AI Hub cards (not fetched in detail); Jetson TensorRT RT-DETR numbers not collected here.
- Jeff Geerling's AI HAT+ article was not reachable (404); his measurements are reported only secondhand.
- Unit prices for Orin NX modules, RK3588 boards, QCS6490 kits, MemryX MX3 M.2, and Maix4-HAT were not confirmed from primary vendor pages.
- Independent power measurements exist only for Jetson (Hokwang Choi, AgriJetsonBench, NCDet-YOLO) and Sixfab FPS/W; none for RK3588/Axera/Qualcomm under YOLO load.


## Q2. Toolchains (TensorRT, ONNX Runtime, OpenVINO, TFLite/Coral, NCNN, RKNN, Hailo DFC, DeepStream) and op support for modern detectors

### Takeaway
YOLO-family CNNs (v5-v11, v26) are first-class citizens in every toolchain and model zoo (Hailo, rknn_model_zoo, Qualcomm AI Hub, DeepStream-Yolo, OpenVINO); DETR-family models with multi-scale deformable attention (RT-DETR, D-FINE, DEIM, RF-DETR) deploy cleanly only on TensorRT/OpenVINO/ONNX Runtime because grid_sample is unsupported on Hailo and RKNN NPUs (and attention-heavy YOLOv12 runs 4x slower on Hailo). DFL heads and NMS are routinely moved to the host CPU on NPUs (RKNN tail.onnx, Hailo engine=cpu NMS), and YOLO26's DFL-free, NMS-free head is explicitly designed to avoid this.

### Cited Findings

**DETR-family on NPUs: grid_sample (deformable attention) is the recurring blocker**
- RT-DETR decoder uses multi-scale deformable attention: 300 queries x 8 heads x 4 sampling points over P3/P4/P5 feature maps, implemented with F.grid_sample — [Ultralytics deformable attention glossary](https://www.ultralytics.com/glossary/deformable-attention); [RT-DETRv2 paper](https://arxiv.org/html/2407.17140v1)
- RT-DETRv2 explicitly introduced an optional `discrete_sample` operator (round offsets, drop bilinear interp) to replace grid_sample "thus removing the deployment constraints of RT-DETR"; train with grid_sample, fine-tune/deploy with discrete_sample — [RT-DETRv2 arXiv 2407.17140](https://arxiv.org/pdf/2407.17140). D-FINE inherits RT-DETRv2 strategy — [D-FINE arXiv 2410.13842](https://arxiv.org/pdf/2410.13842)
- Rockchip: GridSample listed "Not Supported" in rknn-toolkit2 op table; a GridSample network converts but fails at runtime on RK3588 — [rknn-toolkit2 issue #276](https://github.com/airockchip/rknn-toolkit2/issues/276); D-FINE users asked for a grid_sample-free variant for RK3588/Orange Pi 5 — [D-FINE issue #269](https://github.com/Peterande/D-FINE/issues/269), [#321](https://github.com/Peterande/D-FINE/issues/321)
- RF-DETR export tracking issue: Hailo HEF "Missing — grid_sample is the sticking point"; RKNN "Missing — grid_sample + mandatory INT8"; workaround pattern = rewrite GridSample as index computation + Gather (done for TFLite in PR #1054) — [rf-detr issue #1024](https://github.com/roboflow/rf-detr/issues/1024)
- Hailo-8L zoo has only a plain DETR-ResNet18 (31.5 HW mAP, 23 FPS) and no RT-DETR; yolov12 (area attention) runs 4x slower than yolo11n on Hailo-8L (38 vs 157 FPS) — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst). Axera AX650N is the one low-cost NPU advertising native Transformer support — [Axera](https://www.axera-tech.com/en/news/2813.html)

**RKNN specifics (Ultralytics RKNN integration)** — [Ultralytics RKNN](https://docs.ultralytics.com/integrations/rockchip-rknn/)
- Export must run on x86 Linux; ONNX opset <= 19; default FP16; INT8 via `quantize=8` uses rknn-toolkit2 `auto_hybrid` to keep high-error layers in FP16. For INT8 detect models the .rknn graph STOPS at the head convolutions and box decoding (DFL) runs on host CPU via a `tail.onnx` in ONNX Runtime — i.e., DFL/softmax head is deliberately kept off the NPU for accuracy. Rockchip's own airockchip/ultralytics_yolo11 fork likewise splits the head outputs (box/cls/DFL-sum) so decoding happens on CPU — [rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo)
- RV1106 user had to split detect head into separate box/score outputs because INT8 scale coupling erased confidences.

**Coral Edge TPU**: compiler frozen at v16 (2022), YOLO11 export broken as of May 2025 (CONV_2D v6 unsupported), partial CPU fallback of ops; only YOLOv8n-size practical — [Ultralytics Edge TPU](https://docs.ultralytics.com/integrations/edge-tpu/)

**TensorRT on Jetson**: TRT 10.3 (JP 6.0/6.1) INT8 bug with end2end/NMS-free exports -> use TRT 10.7+; TRT 10.7 last with DLA; export engines ON the target device (engines are not portable across GPU/TRT versions) — [Ultralytics Jetson guide](https://docs.ultralytics.com/guides/nvidia-jetson/)

**Qualcomm AI Hub**: YOLOv8/YOLOv11 Detection & Segmentation, Yolo-R in official zoo; w8a8 TFLite/QNN fastest on QCS6490 NPU; ONNX path falls back to CPU 10-40x slower — [HF qualcomm/YOLOv8-Detection](https://huggingface.co/qualcomm/YOLOv8-Detection/blob/1fbb611bc4910a1972dd8ae4f93cb1055b06ad51/README.md)


### Inferences

- Practical rule: on NPUs export the raw head tensors (box distribution + class logits) and decode on CPU; on Jetson keep the full graph (including EfficientNMS plugin) in TensorRT.
- If a DETR-family model is required on Hailo/RKNN, the only viable paths are RT-DETRv2's discrete_sample variant, a Gather-based grid_sample rewrite (RF-DETR PR #1054 pattern), or hybrid NPU-backbone / CPU-decoder execution; none have published NPU FPS yet.
- SiLU is supported on all surveyed NPUs but ReLU-ified variants are measurably faster on RKNN (yolov5s_relu 66.5 vs yolov5s 49.1 FPS on RK3588) and Hailo (yolox leaky variants); for small-object nets trained from scratch, consider ReLU/LeakyReLU backbones.
- Dynamic shapes are not supported by Hailo HEF or RKNN; batch and input size are fixed at compile time (Hailo compiles b1/b8 separately; RKNN fixed 1x3xHxW). TensorRT supports dynamic profiles but Ultralytics exports fixed shapes by default.
- Export toolchains for Hailo (DFC) and RKNN run on x86 Linux only; Edge TPU compiler likewise; plan an x86 build host in the CI loop.


### Gaps

- Hailo DFC official op-support list for GridSample/Deformable attention was not fetched directly (evidence is from RF-DETR maintainers and community).
- Qualcomm AI Hub RT-DETR/DETR entries and QCS6490 latencies were not fetched; AI Hub also lists RT-DETR but no numbers were captured.
- No measured data on dynamic-shape or non-square (e.g. 1280x720) HEF/RKNN performance.
- DeepStream-Yolo's benchmarks.md and INT8Calibration.md were not fetched (links only).


## Q3. Quantization (PTQ vs QAT) mAP loss, small-object sensitivity, mixed precision, QAT recipes

### Takeaway
INT8 PTQ costs roughly 0.5-2 mAP on COCO for YOLOv8/11 when calibrated well (Hailo zoo) but 3-7 mAP with naive TensorRT max-calibration on small models (Ultralytics Jetson tables, arXiv 2508.19600), and the loss is concentrated in small objects on aerial data (LW-DETR VisDrone: AP_S drops most; YOLO11n UAV study: FP16 lossless, INT8 'substantial' degradation). QAT recovers 2-3 mAP (LW-DETR) or lands within 1-2 pt of FP32 (Ultralytics/ModelOpt), but gains little on nano models where PTQ is already close. Speedup from INT8 over FP16 is only 1.1-1.2x for nano models on Jetson, so FP16 is the default recommendation there; INT8 is unavoidable on RKNN/Hailo/Coral.

### Cited Findings

**Measured INT8 drops in vendor benchmark tables (PTQ, TensorRT/Hailo/RKNN)**
- Ultralytics Jetson tables (YOLO26n, COCO128, TRT PTQ): Orin Nano Super FP16 0.480 -> INT8 0.449 (-3.1 pt); Orin NX 0.479 -> 0.449 (-3.0); AGX Orin 0.479 -> 0.464; Thor 0.480 -> 0.427 (-5.3) — INT8 speedup over FP16 is only 1.1-1.2x for a nano model — [Ultralytics Jetson](https://docs.ultralytics.com/guides/nvidia-jetson/)
- Hailo-8L PTQ (zoo, COCO full val): yolov8n -0.6, yolov8s -0.7, yolov11n -1.5, yolov11s -1.2, yolov10n -1.9, yolo26s -2.2, DETR -2.4 — [Hailo-8L zoo](https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst)
- RKNN (RK3588, auto_hybrid INT8, COCO128): YOLO26n 0.477 -> 0.463 (-1.4); YOLO26s 0.569 -> 0.554 — [Ultralytics RKNN](https://docs.ultralytics.com/integrations/rockchip-rknn/)
- Older Orin Nano YOLOv8n pipeline: FP16 mAP50 37.2 -> INT8 36.8 (-0.4) at 58 -> 72 FPS — [industrialmonitordirect](https://industrialmonitordirect.com/blogs/knowledgebase/resolving-yolo-model-performance-on-jetson-orin-nano-with-tensorrt-export)

**Papers 2024-2026 on quantization and small objects**
- "Quantization Robustness to Input Degradations for Object Detection" (arXiv 2508.19600, YOLO12 family, TensorRT static INT8): 1.5-3.3x speedup, baseline drop ~3-7 pt mAP50-95 absolute, "smaller models being more affected"; degradation-aware calibration gave no consistent gain; QAT left as future work — [arXiv 2508.19600](https://arxiv.org/html/2508.19600v3)
- "Enabling Fully Integer-Only Inference for Lightweight Detection Transformers" (arXiv 2607.24981, LW-DETR on VisDrone): PTQ causes "substantially larger accuracy degradation" on VisDrone than on COCO; "AP_S exhibits the largest drop" across all variants; QAT recovers 1.9-3.1 mAP without extra deployment cost; "aggressive quantization remains considerably more challenging for small-object detection" — [arXiv 2607.24981](https://arxiv.org/pdf/2607.24981)
- PTQ effect on small UAV detection (YOLO11n, TensorRT): FP16 = no measurable loss across any object-size category, -45% engine size, +13% speed; INT8 PTQ = "substantial accuracy degradation"; recommends FP16 for UAV detectors, QAT as open question — [scientia.report](https://previous.scientia.report/index.php/archive/article/view/4440/4491)
- Leiden MSc thesis (2025-26) "Efficient small-object Video Detection via QAT": INT8 disproportionately degrades small objects due to low-signal high-variance activations in shallow feature maps; on XS-VID (mean object 10.6x10.6 px) per-frame YOLO AP_small is only 6-10% — [LIACS thesis](https://theses.liacs.nl/pdf/2025-2026-JohannsenL.pdf)
- YOLO evolution overview (arXiv 2510.09653): YOLO11 improved post-quantization accuracy by reducing depthwise convs / normalising weight distributions; YOLO26 removed DFL and NMS and "INT8 exports retain nearly the same mAP as FP32" (claim by authors; Ultralytics' own Jetson table shows -3 pt on COCO128 for 26n, so treat with caution) — [arXiv 2510.09653](https://arxiv.org/html/2510.09653v1)
- QARepVGG: RepVGG-style reparam backbones (YOLOv6) collapse under PTQ: YOLOv6s-RepVGG -7.4 mAP, YOLOv6t -3.0 — [arXiv 2212.01593](https://arxiv.org/pdf/2212.01593)
- Methodology warning (uav-yolo-edge-compression, YOLO11s/VisDrone): compare INT8 to an FP32 EXPORT at the same imgsz, not the .pt — static exports force rect=False/batch 1 so .pt-vs-INT8 confounds letterboxing with quantization — [GitHub issue](https://github.com/Sri-Krishna-V/uav-yolo-edge-compression/issues/9)
- Drone-app YOLO perf analysis (arXiv 2502.15737; YOLOv8n/s on 2 Jetsons + Pi 5, FP32/FP16/INT8, aerial ground-robot dataset): Jetson YOLOv8n INT8 ~66 FPS, ~30 ms round trip — [arXiv 2502.15737](https://arxiv.org/pdf/2502.15737)
- Ultralytics OpenVINO guidance: INT8 gives 1.2x for n-models vs 2.9x for m, at 1.2-1.7 mAP cost — [Ultralytics Academy](https://academy.ultralytics.com/courses/yolo-in-production/openvino-on-cpu)


### Inferences

- Decision rule for Jetson: ship FP16; use INT8 (ideally QAT via Ultralytics quantize=8/ModelOpt, or sensitivity-guided mixed precision keeping head/P2 layers in FP16) only when latency budget fails at 1024-1280 inputs where the bandwidth-bound regime makes INT8 more valuable.
- For Hailo/RKNN, invest in calibration quality (500-1000 production-like images incl. small targets; Hailo optimization_level 2-3 with adaround; RKNN auto_hybrid) rather than QAT first; Hailo per-layer 16-bit (`quantization_param(..., precision_mode=a16_w16)`) is the mixed-precision lever for shallow/P2 layers.
- Small-object sensitivity is mechanistically explained by low-magnitude, high-variance activations in shallow feature maps being crushed by per-tensor INT8 scales; per-channel weight quant plus keeping early backbone and P2/P3 branches in higher precision is the recommended mitigation (inference from the Leiden thesis and LW-DETR findings; no direct YOLOv8 ablation found).
- Always benchmark INT8 against an FP32/FP16 export at the same imgsz with identical letterboxing, not against the .pt validator.


**QAT recipes / toolchains**
- Ultralytics now wraps NVIDIA TensorRT Model Optimizer (ModelOpt) for QAT via `quantize=8` in train; checkpoint carries ranges so INT8 export needs no calibration. Ultralytics' course states PTQ INT8 cost YOLO26s-m 4-6 mAP on COCO, QAT lands within 1-2 pt of FP32, but "QAT buys almost nothing on the smallest model". Recommended gate: FP16 first (mAP within 0.5 pt), INT8 only if latency budget missed, with 500+ production-like calibration images — [Ultralytics export docs](https://docs.ultralytics.com/modes/export); [Ultralytics Academy TensorRT](https://academy.ultralytics.com/courses/yolo-in-production/optimize-with-tensorrt)
- Community recipe with legacy NVIDIA pytorch-quantization (huangzongmou/yolov8-pytorch_quantization): PTQ max-calib YOLOv8 mAP50-95 0.446 -> 0.432 (-3.1%); scripts for PTQ, QAT and per-layer sensitivity to keep fragile layers FP16 — [deepwiki summary](https://deepwiki.com/huangzongmou/yolov8-pytorch_quantization/8-results-and-performance)
- TensorRT explicit quantization: QAT fake-quant exports as QuantizeLinear/DequantizeLinear pairs -> IQuantizeLayer/IDequantizeLayer; PyTorch GEMM per-channel axis quirk — [TensorRT docs](https://docs.nvidia.com/deeplearning/tensorrt/latest/inference-library/quantized-types-explicit-quantization.html); ModelOpt has a QAT-for-CNNs example — [TensorRT-Model-Optimizer examples](https://github.com/Yuening-wa/TensorRT-Model-Optimizer/blob/main/examples/README.md)
- Better PTQ calibration recovers a lot before QAT: SqueezeBits OwLite claims TensorRT INT8 ~3% mAP drop vs OwLite PTQ 0.3-0.6% on YOLO (vendor claim) — [SqueezeBits blog](https://blog.squeezebits.com/how-to-quantize-yolo-models-with-owlite-54076)
- Hailo DFC model-script knobs: `model_optimization_flavor(optimization_level=0-4, compression_level=0-N)`; compression_level sets share of 4-bit weight layers (faster, fewer contexts on Hailo-8L, needs higher optimization level/finetune to compensate); per-layer `quantization_param(layer, precision_mode=a16_w16)`; `auto_16bit_weights_ratio`; `post_quantization_optimization(adaround, ...)`; default optimization level is 2 without a script; level 3+ needs GPU and lots of RAM (user crash report on YOLOv8s-pose); YOLOv8 scripts set `change_output_activation(conv.., sigmoid)` and NMS on CPU (`engine=cpu`) — [RidgeRun Hailo model scripts](https://developer.ridgerun.com/wiki/index.php/Hailo/Hailo-8/AI_Software_and_Tools/Hailo_Model_Scripts); [Hailo community YOLOv8 compile](https://community.hailo.ai/t/compilation-of-yolov8-network/2028); [opt level 3 crash](https://community.hailo.ai/t/optimization-level-3-for-custom-yolov8s-pose-model-leads-to-high-ram-usage-and-crash/15258)
- Hailo DFC 5.3.0 / Hailo-10H: YOLOv8s at 4064x3040 input fails to compile at higher compiler optimization levels (only level 0 works) — very-high-res single-pass on Hailo is fragile — [Hailo community](https://community.hailo.ai/t/dfc-5-3-0-hailo-10h-yolov8s-fails-with-value-doesnt-fit-in-field-1951-119-at-4064x3040-and-with-agent-infeasible-when-on-chip-nv12-i420-input-is-combined-with-compiler-optimization-level-max/19842)


### Gaps

- No paper found reporting YOLOv8/11 INT8 PTQ vs QAT with AP_small breakdown on VisDrone/DOTA; the only size-stratified evidence is LW-DETR (transformer) and a YOLO11n UAV study with limited detail.
- No published Intel NNCF QAT results for YOLOv8/11 small objects; Ultralytics OpenVINO INT8 uses NNCF PTQ but figures are COCO-level only.
- Hailo zoo mAP deltas are COCO-wide; no Hailo AP_small or VisDrone numbers found.
- YOLO26 'near-lossless INT8' claim (arXiv 2510.09653) conflicts with Ultralytics' own Jetson tables (-3 pt on COCO128); unresolved.


## Q4. Pruning / distillation (Torch-Pruning / DepGraph on YOLO)

### Takeaway
Structured pruning with Torch-Pruning/DepGraph gives 15% (lossless, COCO YOLOv8m) to 60-73% FLOP reductions (domain datasets, with fine-tune/KD, -1 to -3 mAP50) but FLOPs do not translate to latency on edge NPUs/GPUs unless channels are rounded to multiples of 8-16 and the result is re-benchmarked (20% pruning gave zero FPS gain on Jetson Nano; ModelOpt 34% FLOPs -> 16% latency). Distillation into a YOLOv8n student yields ~1-2 pt mAP50-95; for tiny objects the teacher's P2 head and cross-scale feature pairing matter more than teacher size.

### Cited Findings

- Torch-Pruning implements DepGraph (Fang et al., CVPR 2023) to group coupled params for structural pruning — [VainF/Torch-Pruning README](https://github.com/VainF/Torch-Pruning/blob/master/README.md)
- YOLOv8m on COCO with Torch-Pruning (SPIE 2024, 13 iterations): FLOPs 39.6G -> 33.7G (-14.9%), params 25.9M -> 22.0M, AP reportedly unchanged/slightly up after fine-tune — [SPIE 2024 abstract](https://ui.adsabs.harvard.edu/abs/2024SPIE13416E..2BZ/abstract)
- YOLOv8m 50% channel pruning + distillation (arXiv 2509.12918): params 25.85M -> 6.85M (-73.5%), FLOPs 49.6G -> 13.3G, FPS 17 -> 44 (their hardware), "AP decreased only slightly", distillation recovers — [arXiv 2509.12918](https://arxiv.org/pdf/2509.12918)
- PKD-YOLOv8 (Sensors 2025, pest dataset, YOLOv8s): pruning-ratio sweep FLOPs 29.3G (0%) -> 20.7G (30%) -> 11.0G (70%) -> 6.3G (90%), mAP50 96.8 -> 96.2 -> 94.6 -> 93.7 — [MDPI Sensors](https://www.mdpi.com/1424-8220/25/16/5004)
- Practitioner caveats: Torch-Pruning's YOLOv8 example is broken and no YOLO11 example exists; `round_to=8` (channel multiples of 8) is mandatory or pruning yields zero latency gain; "report latency, never FLOPs": TensorRT issue #3884 20% structured pruning of YOLOv8s -> zero FPS gain on Jetson Nano; NVIDIA ModelOpt: 34% FLOPs reduction bought 16% latency — [uav-yolo-edge-compression issue #1](https://github.com/Sri-Krishna-V/uav-yolo-edge-compression/issues/1)
- C2f block needs a chunk-free re-implementation for channel pruning dependency tracing to work — [Zhe-g/pruning-tool](https://github.com/Zhe-g/pruning-tool)


### Inferences

**Distillation**
- CSCWD (arXiv 2609.30395; tiny objects in aerial video; YOLOv8n student): baseline YOLOv8n 45.74 mAP50 / 15.90 mAP50-95; teacher with P2 head raises teacher mAP50 52.84 -> 56.75; cross-scale P2->P3 alignment +2.09 mAP50 over same-scale CWD; zero-shot DUT-Anti-UAV +1.77 mAP50; student inference architecture unchanged — [arXiv 2609.30395](https://arxiv.org/html/2609.30395v1)
- LKD-YOLOv8 (Sensors 2025, YOLOv8s -> YOLOv8n, infrared): student 0.3756 -> 0.3874 mAP50-95 while params 3.01M -> 2.77M, 8.2 -> 7.6 GFLOPs; MGD alone contributed only +0.08 — [MDPI Sensors](https://www.mdpi.com/1424-8220/25/13/4054)
- Industrial-defect multi-level KD: detection-head distillation largest single gain (+6.6% mAP), student 6.3x faster than teacher — [IJOMAM 2025](https://ijomam.com/wp-content/uploads/2025/09/Pp.-287-303_LIGHTWEIGHT-INDUSTRIAL-DEFECT-DETECTION-ALGORITHM-FOR-EDGE-COMPUTING-YOLOV8-OPTIMIZATION-BASED-ON-KNOWLEDGE-DISTILLATION.pdf)
- UAV blurry small-object KD (YOLOv8l -> YOLOv8s, sharp teacher / blurry student, VisDrone & SOD) — [Complex & Intelligent Systems 2024](https://link.springer.com/article/10.1007/s40747-024-01676-w)
- Typical KD gain for a nano student is modest (~1-2 pt mAP50-95); teacher design (P2 head) and cross-scale feature pairing matter more than teacher size for tiny objects.


### Gaps

- No practical Torch-Pruning results on Ultralytics YOLO11/YOLO26 found; the official YOLOv8 example is reported broken.
- No pruning study reports AP_small before/after on aerial data; all gains are overall mAP.
- No measured latency on Hailo/RKNN for pruned models (NPU compilers may not benefit from irregular channel counts at all).


## Q5. Resolution vs tiling (SAHI) latency trade-offs

### Takeaway
Latency scales roughly with pixel count (3.5-4x from 640 to 1280 on bandwidth-bound Orin Nano, extrapolated; on Hailo-8L the only 1280 data point, yolov5m6, runs 21.7 FPS vs 60.2 FPS for yolov5m at 640, ~2.8x), and stock Python SAHI is 10-50x slower than single-pass inference (0.4 FPS reported), but batched-tile TensorRT SAHI on Orin Nano reaches ~15 FPS on 1080p with ByteTrack and SAHI adds +4-7 AP (up to +13 with sliced fine-tuning) on VisDrone. Native high-res or P2-head single-pass (24 FPS on Orin Nano) wins when targets are >=8-10 px after resize; tiles win when the detector must see targets at near-native pixel scale, and ROI-gated/sparse tiling is the emerging compromise.

### Cited Findings

- Batched-tile TensorRT SAHI (C++): YOLOv8 INT8 engine on Jetson Orin Nano 8GB — slicing + batched inference ~40 ms per 1080p frame (43-46 ms/img steady-state), SAHI + ByteTrack on 1080p video ~13-15 FPS end-to-end. Key: batch all tiles into one TRT call — [HouYanSong/tensorrtx-yolov8-sahi](https://github.com/HouYanSong/tensorrtx-yolov8-sahi)
- Stock Python SAHI (640 tiles, 25% overlap) on improved-YOLOv8 for UAV tree pits: 0.398 FPS (2.52 s/image) — "exponential increase in inference time" from repeated pre/post-processing and cross-slice fusion — [ScienceDirect 2025](https://www.sciencedirect.com/science/article/pii/S2772375525004125)
- ROI-Gated SAHI (arXiv 2608.23923): run cheap full-frame YOLOv8n proposer, slice only ROIs with YOLOv8s refiner — content-adaptive slicing to cut tile count — [arXiv](https://arxiv.org/pdf/2608.23923)
- SAHI accuracy gains: original paper +6.8/5.1/5.3 AP (FCOS/VFNet/TOOD) inference-only, +12.7-14.5 AP with sliced fine-tuning — [SAHI arXiv 2202.06934](https://arxiv.org/pdf/2202.06934); VisDrone YOLOv5s: 32.0 AP -> 36.2 (SAHI infer) -> 39.4 (sliced FT + SAHI), AP_small 20.7 -> 27.2 — [arXiv 2203.04799](https://arxiv.org/pdf/2203.04799)
- Native-res + P2 head alternative: LAF-YOLOv10 (P2 head) 24.3 FPS on Orin Nano (41.2 ms vs 31.2 ms for YOLOv10n); "the P2 head's 160x160 feature map dominates memory bandwidth on embedded devices" — [LAF-YOLOv10 arXiv 2602.13378](https://arxiv.org/pdf/2602.13378)
- Resi-YOLO maritime UAV: AP_small 18.4 -> 31.5 vs YOLOv8n; 12.8 FPS end-to-end (~100 ms) on Orin Nano while TRT engine-only >30 FPS at 640 — illustrates 2-3x gap between engine-only and pipeline FPS — [Drones 2026, 10(3):226](https://doi.org/10.3390/drones10030226)


### Inferences

- Rule of thumb from the data: one 1280 pass costs about the same as 4 batched 640 tiles (same pixel count) but SAHI adds overlap (25% -> ~1.6x pixels) plus merge/NMS; so at equal pixel budget a single 1280 engine is cheaper unless the model's receptive field/anchors were trained at 640 scale, in which case 640 tiles preserve the trained object-size distribution and typically give higher AP_small.
- For a 1080p stream where targets are ~10 px, SDG-Track shows YOLOv11 TRT FP16 on native 1080p <7 FPS on Orin Nano; sparse detection + tracker (35 FPS) or ROI-gated tiling is required for real time.
- On Pi 5 + Hailo, tiling multiplies host-side pre/post work that is already the bottleneck; prefer compiling a non-square HEF at camera aspect (e.g., 1280x720) over tiles.


- Hailo-8 confirmed to run yolov8n-seg at 1280x1280; Hailo staff suggest checking 1280x1280 or 1280x720 for accuracy; `hailomz optimize <model> --resize 1080 1920` supports non-square custom input; Ultralytics native Hailo export sets imgsz for the HEF — [Hailo community 1080p](https://community.hailo.ai/t/general-question-about-video-size-1080p-30-fps-and-hailo8/9308); [Ultralytics Hailo export](https://docs.ultralytics.com/integrations/hailo)
- 4K camera on Pi 5 + Hailo-8 with YOLO11m: 11 FPS at 640 model; author compares five strategies (resize / scan tiles / crop) — [Medium: YOLO with high-res cameras Part II](https://medium.com/@teig/yolo-with-high-resolution-cameras-resize-scan-or-crop-65997b1cc1e8)
- Only hard 1280 vendor numbers found are Hailo zoo yolov5m6 (Hailo-8 32.7 FPS; 8L 21.7 FPS) and yolov7e6; no official YOLOv8/11 1280 FPS for RK3588 or Hailo; Radxa forum user: "we are lacking empirical benchmarks of input size and resultant mAP and FPS" — [Radxa forum](https://forum.radxa.com/t/use-yolov8-in-rk3588-npu/15838)


### Gaps

- No single source benchmarks SAHI-640 tiles vs one 1280 pass on the same device with FPS AND AP_small; only partial data points exist.
- No measured 1024/1280/1536 YOLOv8n/11n latency on RPi5+Hailo or RK3588.


## Q6. Video pipeline engineering (HW decode, zero-copy, DeepStream/GStreamer, frame skipping + tracking, multi-stream)

### Takeaway
Deliverable FPS is governed by the video pipeline, not the detector: Pi 5 hardware decode caps single-stream NPU pipelines at ~7-26 FPS; Orin Nano 8GB handles ~4-6 1080p streams with YOLOv8 via DeepStream (Orin NX 16GB 16-18); RK3588 zero-copy MPP->RGA->RKNN reaches ~54 FPS aggregate for yolov8n at 640 across 3 cores (12 streams of yolo26n at 352x640 at ~98 ms/frame). Frame skipping with a lightweight tracker (ByteTrack/BoT-SORT, KLT, observer-follower) recovers 3-5x system throughput at ~3% precision cost; avoid DeepSORT-style ReID on edge.

### Cited Findings

- Seeed/marcoslucianops DeepStream-Yolo multistream (1080p H.264 sample, YOLOv8, deepstream-app): Orin Nano 8GB supports ~4-6 streams; Orin NX 16GB 16-18 streams "at maximum capacity"; Orin NX INT8: ~40 cameras at ~5 FPS with one YOLOv8s, ~11 cameras at ~15 FPS with per-stream models (RAM-bound). Single-stream INT8 with fakesink ~350 FPS reported — [Seeed wiki DeepStream](https://wiki.seeedstudio.com/YOLOv8-DeepStream-TRT-Jetson/)
- Real FPV 1080p60 H.264 camera, YOLOv8n, DeepStream 6.3 / JP 5.1.4 on Orin Nano: ~50 FPS end-to-end; ByteTrack did not change FPS — [DeepStream-Yolo issue #605](https://github.com/marcoslucianops/DeepStream-Yolo/issues/605)
- Ultralytics DeepStream guide: INT8 via DeepStream-Yolo calibrator "currently requires TensorRT 8.x" (does not work with TRT 10 on JetPack 6) — use FP16 there — [Ultralytics DeepStream guide](https://github.com/ultralytics/ultralytics/blob/main/docs/en/guides/deepstream-nvidia-jetson.md)
- GPU-only vs host end-to-end on Orin Nano Super (YOLOv8n 640): FP16 4.43 ms GPU vs 6.13 ms host; INT8 3.49 vs 4.90 — [hokwangchoi](https://hokwangchoi.com/blog/vision-benchmarks/); live camera TRT YOLO11n p99 39.6 ms vs 7.99 ms replay median — [Turing Pi](https://turingpi.com/yolo-jetson-orin-nano-tensorrt-benchmarks/)
- Pi 5: hardware video decode is the ceiling, capping single-stream NPU pipelines to ~7-26 FPS regardless of accelerator — [Sixfab](https://sixfab.com/blog/raspberry-pi-5-ai-hat-benchmark-deepx-vs-hailo/)
- Orin NX study: batching gave greater relative gains at 640 than at 1200 px, implying GPU saturation at large inputs — [ResearchGate Orin NX YOLOv8](https://www.researchgate.net/publication/400413845_Benchmarking_YOLOv8_Variants_for_Object_Detection_Efficiency_on_Jetson_Orin_NX_for_Edge_Computing_Applications)


### Inferences

**RK3588 zero-copy MPP -> RGA -> RKNN pipelines (independent open-source measurements)**
- rk3588s-hetero-detect-engine: DMA-BUF fd passed across MPP decode -> RGA letterbox -> RKNN; 1080p->640 RGA letterbox into rknn_create_mem dma-buf ~5.3-9.4 ms; 4x1080p30 yolov8n needs 120 FPS aggregate, achieved ~54 FPS incl. MPP+RGA+RKNN+NMS, relying on drop-old-frame to protect P99 — [Jack-GPU/rk3588s-hetero-detect-engine](https://github.com/Jack-GPU/rk3588s-hetero-detect-engine)
- PyVideoProc_RK3588 (yolo26n 352x640 FP16, H.264 1080p25, 3 NPU cores): 3 streams 35 ms/frame, 6 streams 53 ms, 9 streams 74 ms, 12 streams 98 ms; CPU 2-16% — [PyVideoProc_RK3588](https://github.com/lmk123568/PyVideoProc_RK3588)
- Camera-side V4L2 -> RGA -> NPU -> MPP encode zero-copy: ~60 FPS end-to-end, RKNN INT8 25.5 ms, MPP H.264 1080p encode 4.2-5.0 ms — [Elichenx/rk3588-yolo-release](https://github.com/Elichenx/rk3588-yolo-release-v1.0); C++ reference for RK3576/RK3588 with MPP/RGA/DMA-BUF and 2/3 NPU workers — [Hanzo-Huang/rockchip-yolo-cpp](https://github.com/Hanzo-Huang/rockchip-yolo-cpp); Radxa official YOLOv8 multi-stream doc: 9+ streams using 3 NPU cores — [Radxa docs](https://docs.radxa.com/en/som/nx/nx5/ai-dev/yolov8-multi-stream); FFmpeg with zero-copy MPP/RGA — [nyanmisaka/ffmpeg-rockchip](https://github.com/nyanmisaka/ffmpeg-rockchip)
- RK3588 VPU decode is not the bottleneck (8K-class decode, 1080p@480fps encode); practical limiter is NPU throughput + RGA conversion + scheduling — [Turing Pi RK3588 architecture](https://turingpi.com/rk3588-architecture-cpu-gpu-npu-memory/)


**Frame skipping / sparse detection + tracking**
- SDG-Track (arXiv 2512.04883): even with TensorRT FP16, YOLOv11 on native 1080p frames achieves <7 FPS on Jetson Orin Nano; a 10x10 px target becomes ~3x3 px after 640 downsampling; observer-follower sparse detection achieves 35.1 FPS system throughput retaining 97.2% of frame-by-frame detection precision — [arXiv 2512.04883](https://arxiv.org/html/2512.04883v1)
- FastMOT (GeekAlexis): YOLO detector run sparsely + KLT optical-flow tracking between detections; up to 42 FPS on Xavier NX — [FastMOT](https://github.com/GeekAlexis/FastMOT)
- DeepSORT ReID network is a common bottleneck (10 FPS with YOLOv8n TRT); ByteTrack/BoT-SORT without appearance model preferred on edge — [NVIDIA forum](https://forums.developer.nvidia.com/t/slow-fps-on-orin-nano-8-gb-yolov8/280071); GStreamer `appsink max-buffers=1 drop=True` for simple frame dropping — [Ultralytics community](https://community.ultralytics.com/t/yolov8-model-latency-on-jetson-orin-nx/1011/7)
- NCDet-YOLO anti-UAV on Orin NX Super 15 W: 31.5 FPS, 31.7 ms, 9.65 W measured — [Drones 2026 10(8):626](https://doi.org/10.3390/drones10080626)


### Gaps

- DeepStream INT8 with TensorRT 10 on JetPack 6 remains inconsistently reported (Ultralytics guide says TRT 8 required; DeepStream-Yolo README lists TRT 10.4/10.9) — verify on target.
- No end-to-end FPS found for Hailo multi-stream on Pi 5 beyond Sixfab's single-stream decode-bound numbers; Hailo TAPPAS multi-stream numbers not collected.
- NVDEC zero-copy (nvbufsurface/EGL) specifics and measured savings were not collected; GStreamer appsink drop=True is the only concrete frame-drop recipe captured.


## Q7. Open-source end-to-end reference projects (drone/aerial on Jetson/RPi)

### Takeaway
Mature building blocks exist (DeepStream-Yolo for Jetson, hailo-apps/hailo-rpi5-examples for Pi, Rockchip zero-copy demos, tensorrtx-yolov8-sahi), but there is no turnkey open-source anti-UAV/aerial small-object pipeline with rigorous published numbers; community drone-detection repos report 10-60 FPS on Jetson at unstated or 640 input sizes and should be treated as starting points, not benchmarks.

### Cited Findings

- hailo-ai/hailo-rpi5-examples (MIT): detection (YOLOv6n simple pipeline; full pipeline with tracker and multi-resolution), pose, instance seg, depth; inputs rpicam/USB; Hailo-8 and 8L; repo now flagged outdated -> use hailo-ai/hailo-apps (hailo-apps-infra pip); retraining guide in hailo-apps-infra; DFC download requires Developer Zone registration; no FPS figures published in README; Frigate has official Hailo support from v0.16 — [hailo-rpi5-examples](https://github.com/hailo-ai/hailo-rpi5-examples)
- marcoslucianops/DeepStream-Yolo: de facto YOLO->DeepStream path (custom parser lib, YOLOv5-v11/26, RT-DETR etc.); used by Seeed and Ultralytics guides; INT8 calibrator requires TRT 8.x — [Ultralytics DeepStream guide](https://github.com/ultralytics/ultralytics/blob/main/docs/en/guides/deepstream-nvidia-jetson.md); [Seeed wiki](https://wiki.seeedstudio.com/YOLOv8-DeepStream-TRT-Jetson/)
- HouYanSong/tensorrtx-yolov8-sahi: C++ TensorRT INT8 YOLOv8 + batched SAHI + ByteTrack on Orin Nano 8GB, ~15 FPS on 1080p — [GitHub](https://github.com/HouYanSong/tensorrtx-yolov8-sahi)
- samabbas19/YOLO26-Drone-Detection-Jetson-Orin-Nano: YOLO26n TensorRT + ByteTrack, "60+ FPS" recorded video / 60 FPS live global-shutter camera (self-reported; no models included; input size not stated) — [GitHub](https://github.com/samabbas19/YOLO26-Drone-Detection-Jetson-Orin-Nano)
- RishavTiwari25/aerial-weapon-detection: YOLO11n + EfficientNet-B5 two-gate cascade + ByteTrack on Orin Nano AND Pi 5 + Hailo-8L (student project) — [GitHub](https://github.com/RishavTiwari25/aerial-weapon-detection)
- rutvee-sureja/yolov8-drone-detection: YOLOv8s on legacy Jetson Nano, mAP 0.849, 10+ FPS TensorRT — [GitHub topic listing](https://github.com/topics/drone-detection); iqqy-x YOLOv5s TRT on Orin Nano 31 FPS vs 24 FPS PyTorch (video stream, from-drone detection) — [GitHub](https://github.com/iqqy-x/YOLOv5-TensorRT-Drone-Vision)
- Lalith-pochiraju yolo-v26 drone detection + LSTM-CVAE trajectory on legacy Jetson Nano, trained on DUT Anti-UAV — [GitHub](https://github.com/Lalith-pochiraju/yolo-v26-drone-detection-and-trajectory-tracking)
- Stereo drone tracker (2x IMX477, YOLOv11, triangulation, Kalman/Hungarian, Orin Nano, ~$550 build) — [jaredwatkins roundup](https://www.jaredwatkins.com/research/drone-detection/open-source/)


### Inferences

- DeepStream-Yolo (MIT) supports YOLOv4-v13, YOLO26, YOLOX, YOLO-NAS, RTMDet, DAMO-YOLO, PP-YOLOE, CO-DETR, RT-DETR (PyTorch/Paddle/Ultralytics), D-FINE, RF-DETR (not DEIM); DeepStream 5.1-8.0 incl. TRT 10.4 (DS 7.1 / JP 6.2) and TRT 10.9 (DS 8.0 / JP 7.0); INT8 PTQ calibration for Darknet and ONNX models; maintainer notes limited bandwidth for updates — [DeepStream-Yolo README](https://github.com/marcoslucianops/DeepStream-Yolo)


### Gaps

- hailo-rpi5-examples publishes no FPS; hailo-apps README not fetched.
- jetson-inference (dusty-nv) was not fetched; it does not support YOLOv8+ natively (SSD/DetectNet era) — unverified in this pass.
- SDG-Track and ROI-Gated SAHI code availability not checked.


## Q8. Licensing (Ultralytics AGPL-3.0 vs Apache-2.0 alternatives, NVIDIA TAO)

### Takeaway
Ultralytics models (v5/v8/11/26) and fine-tuned weights are AGPL-3.0 (network-use clause applies; Enterprise licence otherwise); permissive Apache-2.0 alternatives with comparable accuracy are RT-DETR (upstream Baidu), D-FINE/DEIM, RF-DETR N-L (XL/2XL restricted), YOLOX, PP-YOLOE, DAMO-YOLO, NanoDet; loading them via the ultralytics package re-imposes AGPL. NVIDIA TAO code is Apache-2.0 and most NGC pretrained weights are marked commercial-ready per model card, with fine-tuned derivatives commercialisable but some 'Critical Applications' restrictions.

### Cited Findings

- Ultralytics YOLOv5/v8/11/26 are AGPL-3.0 with paid Enterprise licence; AGPL applies to code, architectures, training pipelines AND trained/fine-tuned weights; network-served models trigger AGPL's network clause — [Lightly: Ultralytics alternatives 2026](https://www.lightly.ai/blog/best-ultralytics-alternatives-in-2026); [savant-ai licensing](https://savant-ai.io/blog/yolo-commercial-licensing/)
- Apache-2.0 detectors: YOLOX (Megvii), RT-DETR v1-v4 (Baidu/lyuwenyu), D-FINE / DEIM / DEIMv2, RF-DETR N/S/M/L (Roboflow; XL/2XL under PML 1.0 requiring Roboflow plan), PP-YOLOE, DAMO-YOLO, NanoDet; YOLOv10/12/13 are AGPL; YOLOv9 GPL-3.0; YOLO-NAS code Apache but weights restricted — [Lightly](https://www.lightly.ai/blog/best-ultralytics-alternatives-in-2026); [libreyolo](https://www.libreyolo.com/articles/best-ultralytics-alternatives)
- Loading Apache models (e.g., RT-DETR) through the `ultralytics` package re-licenses your use under AGPL — use upstream repos — [tunasakara AGPL analysis](https://tunasakara.com/en/blog/agpl-commercial-computer-vision)
- LibreYOLO (MIT) wraps RF-DETR, D-FINE, DEIM, YOLOX, RT-DETR, RTMDet etc. under one API — [libreyolo](https://www.libreyolo.com/articles/best-ultralytics-alternatives)


### Inferences

- NVIDIA TAO: toolkit code Apache-2.0 (github.com/NVIDIA-TAO); software use under NVIDIA SLA + AI Products terms allowing commercial deployment; pretrained weights licensed per NGC model card (DetectNet_v2 / classification "ready for commercial use"; some cards restrict "Critical Applications"); NVIDIA staff: you may not resell e.g. PeopleNet as-is, but a model fine-tuned from it can be commercial; since TAO 5.0 exported ONNX is unencrypted — [NVIDIA forum TAO licensing](https://forums.developer.nvidia.com/t/understanding-tao-models-commercial-licensing/281977); [TAO toolkit page](https://developer.nvidia.com/tao-toolkit); [NVIDIA-TAO GitHub](https://github.com/NVIDIA-TAO)
- NVIDIA Community Model License (2025-04-15) governs certain foundation models; restricts using outputs to train non-NVIDIA models without written approval — [license PDF](https://www.nvidia.com/content/dam/en-zz/Solutions/license-agreements/enterprise-software/NVIDIA-Models-Community-License-2025-04-15-FINAL.pdf)


### Gaps

- 'Critical Applications' restriction wording on specific NGC model cards (relevant to defence use) was not fetched verbatim; must be checked per model.
- Hailo model zoo retraining dockers wrap Ultralytics repos (AGPL) for yolov8/11 — licensing of Hailo-provided YOLO HEFs was not verified.
- Ultralytics Enterprise licence pricing not found.

