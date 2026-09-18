# Prompt Crafting for Cinematic Image Generation

## Prompt Template
1. **Subject & Action** – Who/what and what they're doing  
2. **Camera & Lens** – Specific gear to emulate depth-of-field  
3. **Lighting** – Time of day, quality, direction, color temperature  
4. **Film/Emulation** – Specific film stock or digital emulation  
5. **Style & Mood** – Descriptors for color grading, contrast, grain  
6. **Technical Specs** – Aspect ratio, resolution, steps, seed (if desired)

### Example Template
```
[Subject], [action], [camera model] [lens spec], [lighting description], 
[film stock emulation], [color grading descriptors], [technical specs]
```

## Cinematic Prompt Tips
- **Camera Models**: Prefix with "Sony A7IV", "Canon R5", "RED Komodo" to trigger sensor emulation  
- **Lens Specs**: Include focal length and aperture (e.g., "85mm f/1.4 GM lens")  
- **Lighting Keywords**: "golden hour rim lighting", "backlit", "soft diffused light", "sun flare"  
- **Film Emulations**: "Kodak 2383", "Kodak Portra 400", "Fujifilm Pro 400H"  
- **Grading Keywords**: "teal-orange contrast", "warm highlight rolloff", "deep cinematic shadows"  
- **Technical**: "shallow depth of field", "8K detail", "film grain texture", "85mm focal length"

## Beach Scene Prompt Formula
```
Two young women on a beach at golden hour, Sony A7IV S-Log3, 35mm f/1.4 GM lens, 
warm honey-gold sunlight wrapping around skin, candid joyful expressions, 
wind-tousled hair, sun-kissed skin with freckles, shallow depth of field, 
creamy bokeh of turquoise ocean, film grain texture, teal-orange color grade, 
high dynamic range, editorial lifestyle photography aesthetic
```

## Prompt Refinement Checklist
- [ ] Include specific camera/lens combo  
- [ ] Mention lighting quality and direction  
- [ ] Specify film stock or emulation  
- [ ] Add color grading descriptors  
- [ ] Include technical depth-of-field notes  
- [ ] Keep within 200 words for optimal model parsing  
- [ ] Avoid contradictory descriptors  

## Common Pitfalls
- Overloading adjectives → vague results  
- Mixing incompatible styles (e.g., "vintage" + "ultra modern")  
- Forgetting aspect ratio or steps constraint  
- Using >1024px on 16GB systems  
- Forgetting to validate model availability before generation