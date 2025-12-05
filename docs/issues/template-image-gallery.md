# Template: Image Gallery / Reference Photos

## Category

UI — Importance: Low

## Proposal

Add a template to present reference images (photos, diagrams) with captions and optional tags, useful for assembly guidance and visual QA.

## Model

```python
class GalleryImage(BaseModel):
    src: str         # path/URL to image
    caption: str
    tags: List[str] = []
    width_mm: Optional[float]  # optional sizing override

class GalleryContext(BaseModel):
    title: str
    metadata: Metadata
    images: List[GalleryImage]
    options: PageOptions  # fonts/colors/page size
```

## Template Content

- Page layout with responsive grid of images; optional tag badges under captions.
- Supports per-image width override or auto-fit within columns.
- Optional “billboard” lead image at top, followed by grid.
- Printable-friendly (A4/A3) with consistent margins.

## Where Used

- Assembly and inspection packets requiring annotated photos.
- Reference pages in PDF bundles when sharing harness visuals without full diagrams.
