# PINNICLE Antarctica Data Product

A **mesh‑free, physics‑informed neural‑network (PINN) representation** of the Antarctic ice sheet, produced with the open‑source model **[PINNICLE][pinnicle‑repo]**.

[pinnicle‑repo]: https://github.com/ISSMteam/PINNICLE

---  

## What is in this repository?

- **`data/antarctica.pt`** – a Torch tensor that contains the trained PINN solution for the whole continent (mesh‑free).  
- **`data/param.json`** – a JSON file with all the meta‑information needed to interpret the tensor (coordinate bounds, scaling factors, model configuration, …).  
- **`client/`** – a **pure‑Python client** that lets anyone download the two files directly from the static GitHub Pages site and, optionally, load the tensor with PyTorch.  

> The repository **does not** contain any training code, examples, or the original PINNICLE source tree – it is a minimal, scriptable data‑product host only.

---  

## Data sources used  

```text
- Bed elevation: BedMachine + xOPR
- Surface velocity: NASA MEaSUREs 
- 
