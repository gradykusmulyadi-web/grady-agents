# Computer Vision / ML Engineer

## **🧭 Job Overview**

We are looking for a **Senior Computer Vision / ML Engineer** to own the AI that turns our dashcam and video feeds into a **defensible product** — the core of TrackVision and our driver-safety roadmap.

Unlike our AI Product Engineer role, this role **IS about training real computer-vision models**.

It is about turning raw video from tens of thousands of vehicles into **accurate, real-time detection that runs cost-effectively at the edge** — and shipping it to production.

You will work closely with leadership to:

- own the video-intelligence roadmap (fatigue, distraction, ADAS-style alerts, cargo & theft detection)
- train, optimize and deploy CV models that run on-vehicle / at the edge
- build the moat: capabilities a software-only competitor cannot copy

---

## **🚀 Key Responsibilities**

### **1. Own Video Intelligence**

- Build and train CV models for:
    - driver fatigue & distraction detection
    - ADAS-style road & event detection
    - cargo, theft and in-cabin monitoring
- Turn messy, real-world video into **reliable detections**

---

### **2. Optimize for the Edge**

- Make models run **cost-effectively at scale**:
    - quantization, pruning, distillation
    - on-device / edge inference (vs streaming everything to cloud)
    - trigger-based, event-driven processing
- Treat **inference cost-per-camera** as a first-class design constraint

---

### **3. Train, Don't Just Wrap**

- Build custom models **where they create differentiation**
- Use pre-trained backbones and transfer learning to move fast
- Know when to fine-tune vs build from scratch

---

### **4. Own the Vision Data Pipeline**

- Define annotation specs and quality standards (labeling is outsourced — **you own the spec**)
- Build training and evaluation datasets from real fleet video
- Monitor model drift and retrain as conditions change

---

### **5. Ship to Production**

- Deploy models into the **product**, not notebooks
- Build inference services (edge + cloud), monitoring, and versioning
- Iterate from real field performance

---

### **6. Collaborate Across Teams**

- Work with:
    - Hardware / IoT Engineers (dashcam, edge devices)
    - Data & AI Product Engineers (shared data, benchmarking)
    - Software Engineers and Product / Leadership (integrate, refine use cases)

---

## **🧩 Requirements**

### **Must-Have**

- Strong computer-vision and deep-learning fundamentals (object detection, image/video models)
- Hands-on with PyTorch or TensorFlow — **training, not just inference**
- Track record **deploying CV models to production** (real users, real data — not just papers or Kaggle)
- Experience optimizing models for real-time / resource-constrained inference
- Solid engineering (Python; can build and ship services)
- Comfort with messy, real-world image/video data at scale

---

### **Nice-to-Have**

- Edge / embedded deployment (NVIDIA Jetson, mobile, on-device, TensorRT/ONNX)
- Driver monitoring / ADAS / dashcam / automotive vision experience
- Data-centric ML and annotation-pipeline design
- Inference cost optimization at fleet scale
- MLOps: model versioning, monitoring, automated retraining

---

## **❌ What This Role Is NOT**

- Not a pure-research / publish-papers role — **you must ship to production**
- Not a classical-ML / tabular-only role — this is **vision-first** (that's the AI Product Engineer role)
- Not an API-wrapper role — **we train custom models; that's the moat**
- Not a backend-only or dashboard-only role

---

## **🧠 What We're Looking For**

- You go **deep on models when depth creates a moat** — and stay practical about shipping
- You obsess over **inference cost and latency**, not just accuracy
- You can take a fuzzy capability ("detect drowsy drivers") and ship something that **works in the field**
- You learn from real-world performance, not just benchmark scores

---

## **🧪 Interview Process**

Candidates will be asked to:

- design a real video-detection problem end-to-end (model + data + deployment + cost)
- explain model and architecture tradeoffs clearly
- demonstrate production and edge-deployment thinking

---

## **🌏 Location**

Open to candidates based in:

- India 🇮🇳
- Vietnam 🇻🇳
- Indonesia 🇮🇩

---

## **💡 Why Join Us**

- Own the **AI moat** of a logistics platform used by real fleets
- Work with real video data from tens of thousands of vehicles
- High ownership, deep technical problems, and direct customer impact

---

## **⚡ Internal Note for TA (IMPORTANT)**

Prioritize candidates who:

- have **trained AND shipped** CV models to production
- think about **edge inference and cost** at scale
- can explain model tradeoffs simply

Avoid candidates who:

- only have research / paper / Kaggle experience with no shipped work
- ignore inference cost, latency, or deployment
- can only wrap existing APIs and can't train or optimize a model

# **TA Screening Playbook — Senior CV / ML Engineer**

👉 Goal: Filter candidates **before they reach Dave**

👉 Format: **20–30 min technical screen**

👉 Outcome: PASS or REJECT (no maybe)

# **🔴 Section 1 — Hard Filters (ALL must be YES)**

Ask / check from CV + quick confirmation:

### **1. Trained AND shipped a CV model to production?**

- Ask: "Walk me through a CV model you trained and shipped."
- ✅ YES → real model in a real product, with users / data
- ❌ NO → only papers, courses, or Kaggle → **REJECT**

---

### **2. Strong DL framework + CV fundamentals?**

- Ask: "What frameworks and architectures do you use, and why?"
- ✅ YES → PyTorch / TensorFlow + can reason about detection architectures
- ❌ NO → only high-level APIs, can't explain → **REJECT**

---

### **3. Experience with real-world image / video data?**

- Ask: "What kind of visual data have you worked with?"
- ✅ YES → production video / images, messy, at scale
- ❌ NO → only clean academic datasets → **REJECT**

---

### **4. Can explain tradeoffs clearly?**

- Ask: "Why that model / that size / that deployment?"
- ✅ YES → clear reasoning on accuracy vs cost vs latency
- ❌ NO → vague or accuracy-only → **REJECT**

---

# **🟡 Section 2 — Thinking Quality (CORE FILTER)**

👉 Ask ONLY these 2 questions

---

## **🎯 Question 1 (MAIN FILTER)**

> "We want to detect driver fatigue and distraction from dashcam video across tens of thousands of vehicles. How would you build it so it actually runs cost-effectively?"

---

### **✅ Mark YES if candidate mentions:**

- edge / on-device inference vs streaming all video to cloud
- model size / optimization (quantization, distillation, smaller backbones)
- triggered / event-based processing instead of 24/7 full inference
- annotation & data strategy, handling false positives
- accuracy vs cost vs latency tradeoffs

---

### **❌ Mark NO if candidate:**

- says "stream all video to a big cloud GPU model" with no cost thought
- ignores scale / inference cost entirely
- only talks about model accuracy
- can't sequence an end-to-end approach

---

## **🎯 Question 2 (PRODUCTION CHECK)**

> "Your model works great in training but fails in the field. What do you do?"

---

### **✅ Mark YES if:**

- talks about data drift, real-world distribution, edge cases
- collecting field data, re-labeling, retraining, monitoring
- gives a concrete example

---

### **❌ Mark NO if:**

- only suggests "train longer / bigger model"
- no concept of drift or field monitoring

---

# **🔵 Section 3 — Red Flags (ANY = REJECT)**

### **1. Research-only, never shipped**

- ❌ papers / Kaggle but no production model → **REJECT**

---

### **2. Ignores cost & latency**

- ❌ "just use the biggest model on cloud GPUs" → **REJECT**

---

### **3. Can only wrap APIs**

- ❌ can't train, fine-tune, or optimize a model → **REJECT**

---

### **4. Accuracy tunnel-vision**

- ❌ no thought for edge, cost, or deployment → **REJECT**

---

# **⚡ Final Decision Rule**

Candidate is **PASS** only if:

- Section 1 → ALL YES
- Question 1 → YES
- No red flags

👉 Then send to Dave

---

Candidate is **REJECT** if:

- ANY Section 1 = NO
- OR Question 1 = NO
- OR any red flag

---

# **🧠 TA Cheat Sheet (Very Important)**

### **Good candidate sounds like:**

> "I'd run a small optimized model on-device, trigger on motion / events, send only flagged clips to cloud, label real fleet data, and watch for drift."

---

### **Bad candidate sounds like:**

> "I'd stream all the video to the cloud and run a large model for best accuracy."

---

# **💣 Golden Rule**

> Applied scientist who **SHIPS** → PASS

> Pure researcher who can't deploy, OR engineer who only wraps APIs → **REJECT**

---

# **🎯 Final Note for TA**

Do NOT:

- be impressed by paper counts or model size
- be impressed by AI buzzwords

ONLY care about:

> can they train a model that works in the field AND runs cheaply at scale?
