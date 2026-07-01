# Rubric: Senior Computer Vision / ML Engineer

## Must-haves (hard requirements)
Failing ANY of these caps the candidate at "Moderate fit" or below, regardless of other scores.

| # | Criterion | How to assess from a CV |
|---|-----------|------------------------|
| M1 | Trained AND shipped a CV model to production | Look for a specific CV/vision model the candidate trained (not just used) that reached real users in a real product. Phrases like "deployed", "in production", "served X users/requests", named product. Papers, courses, and Kaggle-only entries do NOT satisfy this. |
| M2 | Strong CV + deep-learning fundamentals | Evidence of object detection, image/video model work (detection, segmentation, frame classification), and reasoning about architectures (e.g. YOLO, SSD, ResNet, ViT, EfficientDet). Not generic "applied ML" or data science. |
| M3 | Hands-on training with PyTorch or TensorFlow | Explicitly lists PyTorch or TensorFlow used for training (model design, custom loss, fine-tuning), not just calling inference APIs or pre-built endpoints. |
| M4 | Optimized models for real-time / resource-constrained inference | Mentions latency targets, FPS, model-size reduction, quantization/pruning/distillation, or running on constrained hardware. Any concrete optimization work counts. |
| M5 | Solid software engineering in Python; can build and ship services | Python plus evidence of building/deploying services (APIs, inference services, pipelines, containers). Not notebook-only or research-script-only. |
| M6 | Comfort with messy, real-world image/video data at scale | Worked with production/field video or images, noisy data, large datasets. Clean academic/benchmark datasets only does NOT satisfy this. |
| M7 | Located in (or authorized to work from) India, Vietnam, or Indonesia | Check location / current base. Candidate must be in IN, VN, or ID. Mismatch caps tier. |

## Nice-to-haves (weighted positives)
Score each 0–3: 0 = absent, 1 = partial/implied, 2 = present, 3 = strong evidence.

| # | Criterion | Weight (1–3) | How to assess |
|---|-----------|-------------|---------------|
| N1 | Inference cost-per-camera / fleet-scale cost optimization | 3 | Explicit thinking about inference cost at scale, cost-per-device/stream, trigger-based / event-driven processing to avoid 24/7 inference. The strongest differentiator for this role. |
| N2 | Edge / embedded deployment (NVIDIA Jetson, mobile, on-device, TensorRT/ONNX) | 3 | Named edge hardware or runtimes: Jetson, mobile/on-device, TensorRT, ONNX Runtime, OpenVINO, Coral. On-vehicle / on-device inference experience. |
| N3 | Driver monitoring / ADAS / dashcam / automotive vision experience | 3 | Direct domain match: fatigue/distraction detection, ADAS, dashcam, in-cabin monitoring, automotive or fleet vision. |
| N4 | Data-centric ML and annotation-pipeline design | 2 | Owning annotation specs/quality standards, building training/eval datasets from real data, managing outsourced labeling. |
| N5 | MLOps: model versioning, monitoring, automated retraining, drift handling | 2 | Model registries, versioning, field/performance monitoring, drift detection, automated retraining pipelines. |
| N6 | Knows when to build custom vs fine-tune vs use pre-trained backbones | 2 | Evidence of transfer learning plus from-scratch work, with judgment about when each applies. Signals "train, don't just wrap". |
| N7 | Clear communication of model/architecture tradeoffs | 1 | Writing, talks, or CV phrasing showing ability to explain accuracy vs cost vs latency tradeoffs simply. |

## Red flags

| #   | Flag                                                       | How to detect                                                                                                  | Severity (note / concern / disqualify) |
| --- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| R1  | Research-only, never shipped                               | Strong publication/Kaggle record but no production model with real users/data                                  | disqualify                             |
| R2  | API-wrapper only — cannot train or optimize                | Only uses hosted vision APIs / pre-built endpoints; no evidence of training, fine-tuning, or optimizing models | disqualify                             |
| R3  | Accuracy tunnel-vision / ignores cost, latency, deployment | All accuracy metrics, no mention of cost, latency, edge, or deployment anywhere                                | concern                                |
| R4  | Classical-ML / tabular-only background                     | Profile centers on tabular/structured-data ML, forecasting, recommenders with little to no vision depth        | concern                                |
| R5  | Backend-only or dashboard-only profile                     | Strong software/backend or BI/dashboard history but no real CV modeling                                        | concern                                |
| R6  | Buzzword-heavy, substance-light                            | Many AI buzzwords / model names with no concrete shipped outcomes, scale, or metrics                           | concern                                |
| R7  | Location outside IN / VN / ID with no relocation signal    | Based elsewhere with no stated intent to work from the three regions                                           | concern                                |
| R8  | Job-hopping at senior level                                | Multiple sub-12-month senior stints with no clear rationale                                                    | note                                   |

## Tier thresholds

| Tier         | Rule                                                                            |
| ------------ | ------------------------------------------------------------------------------- |
| Best fit     | All must-haves met + weighted score ≥ 80% of max + zero disqualifying red flags |
| Good fit     | All must-haves met + weighted score ≥ 50% of max + no disqualifying red flags   |
| Moderate fit | 1 must-have missing OR weighted score 30–49% OR concern-level red flag          |
| Not a fit    | 2+ must-haves missing OR any disqualifying red flag                             |

## Scoring notes

- **Shipping beats research.** This is the single most important lens. An applied scientist who shipped CV models to production outranks a more decorated researcher who never deployed. Do not be impressed by paper counts, citations, or model size — treat those as neutral unless paired with shipped, in-production work. M1 is the gate; R1 (research-only) is an automatic disqualify.
- **Edge/inference-cost thinking beats pure accuracy.** Candidates who reason about inference cost-per-camera, edge vs cloud, quantization/distillation, and trigger-based processing (N1, N2) rank above candidates with marginally higher accuracy claims and no cost awareness. Accuracy-only profiles trigger R3.
- **Real-world data beats academic datasets.** Experience with messy, large-scale production video/images (M6) is required. Clean-benchmark-only experience (e.g. ImageNet/COCO and nothing else) does not satisfy M6.
- **Train, don't wrap.** Ability to train, fine-tune, and optimize custom models (M3, N6) is the moat. Anyone who can only call existing vision APIs is an automatic disqualify (R2).
- **Domain match is a strong accelerator, not a gate.** Dashcam/ADAS/driver-monitoring experience (N3) is highly valuable but not a must-have — a strong general CV engineer who ships and optimizes for the edge can succeed without prior automotive exposure.
- When a CV is ambiguous between "used" and "trained" a model, score conservatively for M1/M3 and flag the ambiguity in per-candidate notes so the recruiter can probe it in the technical screen.
