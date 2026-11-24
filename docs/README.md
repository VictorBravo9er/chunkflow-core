# Chunkflow Core Documentation

Welcome to the Chunkflow Core platform documentation repository. This directory houses architectural specifications, operational plans, system designs, and visual diagrams for the workspace.

---

## 📚 Documentation Sections

| Section | Description | Key Documents |
| :--- | :--- | :--- |
| [**`systems/`**](systems/README.md) | **System Architecture & Workflows**<br>Comprehensive technical macro-dossier covering services, subsystem layers, database & storage, and deployment topology. | • [`README.md`](systems/README.md)<br>• Subsystem architecture guides |
| [**`plans/`**](plans/README.md) | **Implementation & Verification Plans**<br>Step-by-step engineering plans, checkpoints, and verification audits for completed features and platform milestones. | • Engineering plans and milestones |

---

## 🛠️ Workspace Automation & Quality Gates

The workspace includes automated scripts and quality gates to verify code quality and documentation coverage:

| Target / Command | Description |
| :--- | :--- |
| **Full Check** | Run full workspace quality gate (tests, linters, doc coverage) |
| **Doc Lint** | Audit 100% `code.md` micro-doc coverage across core directories |


---

## Documentation Layer Separation & Conversation-Time Arbitration

This workspace maintains potentially overlapping documentation types. To prevent drift, circular debates, and redundant writes during conversations, adhere to these pre-compiled arbitration gotchas:
