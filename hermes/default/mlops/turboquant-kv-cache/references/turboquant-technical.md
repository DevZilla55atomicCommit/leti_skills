---
title: TurboQuant Technical Reference
skill: turboquant-kv-cache
---

# TurboQuant Technical Details

## Walsh-Hadamard Transform (WHT)

TurboQuant applies a fixed 128×128 orthonormal Walsh-Hadamard matrix to K and V vectors before quantization:

```
x_rotated = H @ x  where H[i,j] = (-1)^popcount(i & j) / sqrt(128)
```

- **Why WHT?** Rotates vectors toward Gaussian distribution, making uniform quantization more efficient
- **Block size**: 128 elements (head_dim padded to next multiple of 128)
- **Inverse at dequant**: x = H^T @ x_rotated (H is orthonormal: H^T = H)

## Quantization Pipeline

```
1. Input K/V vector (f16/bf16) → head_dim elements
2. Pad to multiple of 128 with zeros
3. Split into 128-element blocks
4. WHT rotate each block: y = H @ x
5. Quantize: q = round(y / scale)  (per-block scale)
6. Store: q (int2/int3/int4) + scale (f16)
7. Dequant: y = q * scale → inverse WHT → x
```

## Asymmetric K/V Rationale

- **Keys (K)**: Used in attention score computation (Q @ K^T). Small errors amplify in softmax → keep high precision (q8_0)
- **Values (V)**: Used in weighted sum (attn @ V). Errors average out → tolerate TurboQuant compression
- **Empirical**: Asymmetric Q8_0/Turbo3 ≈ Q8_0 quality at 2.5× V cache reduction

## Layer-Adaptive Precision

`TURBO_LAYER_ADAPTIVE=7` (Boundary V):
- First/last N layers: V in q8_0 (boundary tokens critical for context boundaries)
- Middle layers: V in Turbo3 (bulk of context)
- Reduces quality degradation at context boundaries

## Flash Attention Integration

- Turbo V dequant fused into flash attention kernel
- `TURBO_SPARSE_V=1`: Skip dequant for near-zero V elements (sparsity exploit)
- Requires flash attention enabled (auto with Turbo cache types)

## MLA (Multi-Head Latent Attention)

- MLA models: V is a view of K (shared latent)
- TurboQuant skips V rotation/padding for MLA (no separate V cache)
- Only K cache quantized

## Compression Math

| Type | Bits/value | Compression vs f16 | Cache reduction (V only, 32 layers, 4K ctx) |
|------|------------|-------------------|---------------------------------------------|
| f16  | 16         | 1×                | 100% (baseline)                             |
| q8_0 | 8          | 2×                | 50%                                         |
| turbo4 | 4.25      | 3.8×              | ~26%                                        |
| **turbo3** | 3.25   | **4.9×**          | **~20%**                                    |
| turbo2 | 2.0        | 6.4×              | ~16%                                        |

For 12B model (40 layers, 32 heads, 128 head_dim):
- Full f16 KV cache @ 32K ctx: ~8.5 GB
- Q8_0 K + Turbo3 V @ 32K ctx: ~2.1 GB (4× reduction)
- Enables 131K ctx on 16GB M4 Mini